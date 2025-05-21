# 向量存储引擎

DolphinDB 在 3.00.1 版本中，基于 TSDB 存储引擎，开发并实现了支持向量检索的向量存储引擎（VectorDB）。VectorDB 针对 TSDB
中以数组向量（Array
Vector）形式存储的向量数据，引入了向量检索技术。它支持对向量数据创建索引，并实现了快速的近似最近邻搜索，满足现代应用场景下对海量数据高效检索和响应的需求。DolphinDB
VectorDB 具有以下特点：

* 支持向量索引的持久化存储，可以从磁盘读取预先构建好的向量索引，无需在每次查询时重复构建索引。
* 提供了高效的向量相似度检索能力，可以快速地对海量向量数据进行近似最近邻搜索。
* 支持混合搜索，可以结合关键词搜索和向量特征搜索，使得搜索更加全面和精准。

## 实现原理

VectorDB 的实现主要考虑以下三个方面：向量数据存储、向量索引构建和向量数据检索。

### 向量数据存储

在 DolphinDB 中，向量数据以数组向量的形式存储。DolphinDB 的 TSDB 引擎本身就支持数组向量的存储，因此 VectorDB
无需自行实现向量数据的存储，只需要基于 TSDB 引擎进行构建即可。关于 TSDB 数据存储原理介绍，请参考 [TSDB 存储引擎](tsdb.md)。

### **向量索引构建**

DolphinDB 采用 Facebook 开源的向量检索库 [Faiss](https://github.com/facebookresearch/faiss)，为 VectorDB 的向量索引构建提供支持。

在创建分区表时，如果为表中的某列指定了索引信息，系统会为该列构建并存储向量索引。VectorDB 以 Level File
为单位进行向量索引的构建和存储。也就是说，VectorDB 不会在全局仅保存一个向量索引，而是在每个 Level File
文件存储一个独立的向量索引。每次生成新的 Level File 文件时，VectorDB 会根据指定的索引类型，为该 Level File
中的向量数据建立向量索引。

### 向量数据检索

相似度计算和检索方法是向量数据检索中的关键技术。VectorDB 利用欧式距离（L2, Euclidean distance）计算向量数据之间的相似度。L2
是最常用的距离度量，计算所得的值越小，越与搜索值相似。L2 在低维空间中表现良好，但是在高维空间中，由于维度灾难的影响，L2 的效果会逐渐变差。

如下代码展示了在 VectorDB 进行向量检索的查询语句。在查询时，VectorDB 会根据所使用的向量索引的类型来搜索并获取与查询向量最相似的 K
个向量。

```
SELECT {col1,...,colx}
FROM table [where]
ORDER BY rowEuclidean(<vectorCol>, queryVector)
LIMIT <TOPK>
```

**普通向量检索**

普通向量检索即在查询语句中没有指定 where 语句进行条件过滤。由于只有存储在磁盘 Level File 中的数据拥有向量索引，而 Cache Engine
中的数据并没有建立向量索引，因此普通向量检索的流程如下：

1. 首先，遍历磁盘上所有 Level File，读取每个 Level File 中存储的向量索引。通过索引搜索得到 N \* K
   个初步查询结果。
2. 其次，对 Cache Engine 中的数据（若有）进行穷举搜索，得到共（N + 1）\* K 个查询结果。
3. 最后，将这*（N + 1）\* K* 个查询结果根据与查询向量的 L2 距离从小到大进行归并排序，取出并返回与查询向量最相近的
   K条数据。

**混合检索**

VectorDB 支持在查询语句中使用 where
条件过滤数据，以充分利用向量数据库的优势，提高检索的准确性和灵活性。这种检索方式适用于综合多个属性进行查询的场景。此时的向量检索流程为：

1. 根据 where 条件对数据进行初步过滤。
2. 将过滤后的数据按照 Level File 进行划分，确保同一 Level File 中的数据被划分在一起。
3. 对每个 Level File 中的数据使用其对应的索引进行相似性搜索。
4. 合并各 Level File 的搜索结果，并从中选出与查询向量最相近的 K 条数据作为最终返回结果。

## 索引类型

向量索引（Vector
Index）是一种针对向量数据构建的高效数据结构。它帮助在时间和空间上提供更高效的向量相似性查询能力。通过向量索引，可以快速地查询出与目标向量最相似的若干个向量。
当前 VectorDB 支持以下索引类型：Flat, PQ, IVF, IVFPQ, HNSW。

| **索引类型** | **索引说明** | **索引构建复杂度** |
| --- | --- | --- |
| Flat | Flat 索引提供精确的向量最近邻检索。它在构建索引时无需进行训练，而是直接对系统中存储的所有向量进行穷举搜索。在查询时，Flat 索引会计算查询向量与所有存储向量的相似度，从而找出与查询向量最相似的向量。 | 无需复杂的索引构建过程。 |
| PQ | PQ（Product Quantization）索引通过对向量数据进行训练来构建向量索引。在训练过程中，PQ 会将每个向量划分为多个子向量，并对每个子向量进行乘积量化（Product Quantization）处理。这样可以大幅压缩每个向量的存储空间。 | 构建 PQ 索引时需要训练乘积量化器。与除 Flat 索引之外的其他索引相比，PQ 索引在内存占用方面更小。 |
| IVF | * IVF（Inverted File Index）索引在构建时需要对向量数据进行训练。训练过程中，IVF 会采用   k-means   聚类算法将向量数据划分为多个簇（cluster）。然后为每个簇建立一个倒排索引，记录该簇中包含的所有向量数据。 * 在查询时，IVF   会先计算查询向量与各个簇的距离，找出与查询向量距离较近的几个簇。然后仅对这些相关簇中的向量进行相似度计算，而不需要计算全部向量，从而大幅降低了计算量,提高了搜索效率。 | 构建 IVF 索引需要对向量数据进行聚类训练，并为每个聚类簇建立倒排索引。相比其他索引方式，IVF 索引的构建过程较为复杂。 |
| IVFPQ | IVFPQ（Inverted File Index with Product Quantization）是 IVF 和 PQ 两种索引技术的结合。在构建 IVFPQ 索引时，需要对向量数据进行训练。训练过程中，IVFPQ 会将向量数据划分为多个簇，并对每个簇的向量数据采用 PQ 的乘积量化方式进行压缩处理。 | 构建 IVFPQ 索引需要同时进行向量数据聚类训练和乘积量化器训练。因此，与单独使用 IVF 或 PQ 相比,IVFPQ 索引的构建和维护过程更为复杂。 |
| HNSW | HNSW（Hierarchical Navigable Small World）基于图算法为向量数据构建多层次的导航图结构，实现高精度和高速度的近似最近领搜索。在查询过程中HNSW会根据查询向量从导航图的顶层开始查找最近的向量，然后在更低的层次中进一步搜索，逐渐逼近目标向量。每一层的搜索都是局部的，从而大幅提高了搜索效率。 | 构建索引时不需要进行训练，但是需要在构建索引时动态地构建和维护多层次导航图，构建多层次的图结构复杂度高耗时长。且相比其他索引，HNSW对内存的占用最高。 |

## 选择索引类型

| **索引类型** | **使用场景** | **适用向量规模** | **检索速度** | **检索精度** |
| --- | --- | --- | --- | --- |
| Flat | 需要最高精度的场景 | 10万以内 | 慢 | 高 |
| PQ | 对搜索精度要求不高的场景。例如：大型数据库、视频库等。 | 数十万至数千万级别 | 较 Flat 快 | 最低 |
| IVF | 图片检索、文本检索等。 | 数万至数百万级别 | 较 PQ 快 | 较 Flat 低 |
| IVFPQ | 在检索速度和精度之间找到最佳平衡的场景。例如：大型推荐系统、社交网络中的用户匹配等。 | 数百万至数千万级别 | 比单独使用 IVF 或 PQ 更快 | 比单独使用 PQ 高，但比单独使用 IVF 低 |
| HNSW | 对检索速度，精度和动态更新有高要求的场景，例如：实时推荐系统、在线搜索、RAG 等。 | 数亿至数十亿级别 | 最快 | 与 IVF 相近 |

## 创建 VectorDB 中的数据表

在 DolphinDB 中，创建分布式分区表有两种方式：一种是使用 [createPartitionedTable](../../funcs/c/createPartitionedTable.md) 函数，另一种是使用 [create](../../progr/sql/create.md) 语句。这两个函数中的
*indexes* 参数用于指定需要建立向量索引的列、向量索引的类型以及向量数据的维度。在创建数据表时，必须指定该参数，才能创建
VectorDB 中分布式分区表。

关于数据表的创建方法，请参考函数页面。本文仅说明 VectorDB 的使用限制。

**建库限制：**

只能创建 TSDB 引擎下的数据库，因此在使用 `database` 函数创建数据库时，必须设置
*engine*="TSDB"。

**建表限制:**

* 仅支持为分布式分区表设置向量索引，且建表时必须指定 *keepDuplicate*s=ALL。
* 最多只能为一个 FLOAT[] 类型的列建立向量索引。该列中的每一行代表一个向量，且所有向量必须具有相同的维度。维度表示每个向量中的元素数量，由
  *indexes* 参数中的 dim 指定。
* 插入向量索引列的数据维度必须与维度（dim）一致。

**搜索限制:**

只有在满足如下条件时，才会使用向量索引加速检索：

* 不能使用表连接查询。
* 查询语句中 `order by` 必须按升序排序，且仅支持使用
  `rowEuclidean`计算距离。
* 传入 `rowEuclidean` 的第一个参数必须是已指定了向量索引的列，即
  `rowEuclidean(<vectorCol>, queryVec)` 。
* 必须指定 `limit` 子句。
* 若指定了 `where`，则 `where` 条件中不能包含
  *sortColumns* 中的任意列。
* 查询语句中不能指定 `group by`, `having` 等其他子句。

**其它说明：**

* 内存 Cache Engine 中的向量数据没有索引，无法对其通过向量索引加速检索。若需要检索这部分数据，可以通过
  `flushTSDBCache` 强制将缓存中的数据写入磁盘后，再进行查询。

## 简单示例

```
// 创建 TSDB 引擎中的数据库
db = database(directory="dfs://indexesTest", partitionType=VALUE, partitionScheme=1..10, engine="TSDB")
// 创建表结构，其中 col3 列的类型是 FLOAT[]
schematb = table(1:0,`col0`col1`col2`col3,[INT,INT,TIMESTAMP,FLOAT[]])
// 通过 indexes 参数，为 col3 指定向量索引
pt = createPartitionedTable(dbHandle=db, table=schematb, tableName=`pt, partitionColumns=`col0, sortColumns=`col1`col2, indexes={"col3":"vectorindex(type=flat, dim=5)"})

tmp = cj(table(1..10 as col0),cj(table(1..10 as col1),table(now()+1..10 as col2))) join table(arrayVector(1..1000*5,1..5000) as col3)

//分区表中写入数据后，强制将数据写入磁盘
pt.tableInsert(tmp)
flushTSDBCache()

select * from pt where col2<now() order by rowEuclidean(col3,[1339,252,105,105,829]) limit 10
```

## 应用场景

向量检索技术在检索增强生成（RAG）系统中扮演着至关重要的角色，其能够有效地从知识库中找到与查询相关的信息，为生成模型提供丰富的上下文支持。将 VectorDB 与
RAG 结合，可以进一步扩展系统知识库，并利用向量检索提供的上下文信息提高生成结果的质量和准确性。VectorDB 还可以改进推荐系统、实现高效图像和视频搜索、提升
AI 生成模型的准确性以及多样性等。

