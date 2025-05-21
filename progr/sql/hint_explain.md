# [HINT\_EXPLAIN]

通过在 select / exec 关键字后添加 `[HINT_EXPLAIN]` 来显示 SQL 语句的执行过程，便于 SQL 查询中实时监测查询的速度和执行的顺序。形式如下：

```
select [HINT_EXPLAIN] * from tb where id > 20
```

注： 添加 `[HINT_EXPLAIN]` 后的查询语句仅返回一个 JSON 字符串显示了 SQL
的执行过程，不返回查询结果；对于 UPDATE 或者 DELETE 语句，目前还不支持查看执行计划。

`[HINT_EXPLAIN]` 支持分区表查询和非分区表查询，对于分区表查询，执行计划会体现 `map-reduce` 的过程。下面以一个分布式查询为例，来说明 JSON 字符串内各标签的组成和含义。

返回的 JSON 字符串的最外层包含 `measurement` 和 `explain` 两个标签。

## measurement

```
"measurement":"microsecond"
```

表示 SQL 查询执行计划的开销时间的单位为微秒。内部所有 `cost` 标签表示的耗时，均以微秒为单位。

## explain

`explain` 内包含的标签从上往下的顺序代表该 `explain` 对应的 SQL 语句的执行顺序。若 SQL
查询包含嵌套子句，`explain` 可能会嵌套在其它子标签中。

`explain` 的构成如下：

* `rows`：查询返回的记录数。
* `cost`：查询耗时。

```
{
  "measurement":"microsecond",
  "explain": {
      /* 可能包含的其他子标签模块 */
      "rows": 20000,
      "cost": 100
  }
}
```

分布式查询包含三个阶段 map → merge → reduce，通常这三个标签均包含在根标签 explain 中, 例如：

```
{
  "measurement":"microsecond",
  "explain":{
      "from":{...},
      "map":{...},
      "merge":{...},
      "reduce":{...},
      "rows":10,
      "cost":23530
  }
}
```

通常，系统会对某些查询条件进行优化。单机模式创建一个以 `date` 列为分区的分区表，查询该表的
`date` 列在单个分区的全部数据。

```
select [HINT_EXPLAIN] * from t1 where date = 2022.01.01
```

此时，该查询语句会被优化，返回如下的结果：

```
{
  "measurement":"microsecond",
  "explain":{
      "from":{ ... },
      "optimize":{ ... },
      "rows":185,
      "cost":987
  }
}
```

## from

`from` 标签说明了 SQL 语句中 `from` 子句解析后的执行过程。

根据 `from` 子句的不同， `from`
标签模块下可能包含着不同的子模块。以下列举了几种可能的场景：

1. `from` 后接一个表对象，例如 `select xref [HINT_EXPLAIN] * from pt`。

   ```
   "from": {
     "cost": 3  // from 子句的耗时
   }
   ```
2. `from` 子句嵌套 SQL 语句，例如 `select [HINT_EXPLAIN]
   * from (select max(x) as maxx from loadTable(“dfs://valuedb”,’pt’) group by month)
   where maxx <
   0.9994`。

   ```
   "from": {
     "cost": 33571,  // from 子句的耗时
     "detail": {
         "sql": "select [98304] max(x) as maxx from loadTable("dfs://valuedb", "pt") group by month",   // 嵌套的SQL语句
         "explain": { ... } // 嵌套的SQL语句的explain
     }
   }
   ```

   可以看到由于包含嵌套的子句， `explain` 标签嵌套在了
   `from` 标签中。
3. from 跟表连接相关的子句，例如 `select [HINT_EXPLAIN] * from lsj(pt1,
   pt2, “date”)`。若使用 2.00.12 之前的版本，此处的 `from` 子句为 *lsj(pt1,
   pt2, "date")*， `cost` 耗时只是获取待连接的表 pt1, pt2 数据源的耗时，两表未发生
   join。

   ```
   "from": {
     "cost": 3,  // from 子句的耗时
     "detail": "materialize for JOIN" // 表示子句中包含 join 操作
   }
   ```

   若使用 2.00.12/3.00.0 及之后的版本，“from“ 字段更改为 “materialization“ 字段，且 “detail“
   字段被替换为左表和右表数据源的 script。

   ```
   "materialization":{
       "cost": 37,                   // 准备左右表数据源的总耗时
       "left": "pt1",                // join 函数第一个参数的 script
       "right": "select * from pt2"  // join 函数第二个参数的 script
   }
   ```

## vectorindex

向量索引的处理过程信息将记录在此标签模块。仅当 from 后为一指定了向量索引的分布式表时，才会出现此标签。

useIndex：本次查询是否满足使用向量索引的条件，true 代表满足。当为 false 时，不会包含其他子标签。

cost：在向量索引的处理过程中花费的时间。

inputRows：通过 where 条件输入给向量索引的行数。

outputRows：经过向量索引处理完后输出的行数。

```
"vectorindex": {
	"useIndex": true,
	"cost": 457470,
	"inputRows": 200000,
	"outputRows": 3000
}，
```

## where

`TSDBIndexPrefiltering`：在 TSDB 引擎中，通过 where 条件从 Level File
文件索引筛选所需数据信息。

* blocksToBeScanned：待扫描的 TSDB 引擎 Level File 文件的 Blocks 数量。
* matchedWhereConditions：where 子句中针对 sort key
  的匹配条件数量，包括等值、非等值（不含链式比较）、in、between、like 等条件。

rows：满足 where 过滤条件的行数。

cost：where 子句的查询耗时。

```
"where": {
    "TSDBIndexPrefiltering": {
        "blocksToBeScanned": 0,
        "matchedWhereConditions": 1
    },
    "rows": 0,
    "cost": 416
}
```

## map

`map` 阶段会统计 SQL 查询涉及到的所有分区（包括本地节点 local 和远程节点 remote
的分区），然后生成相应的子查询，并把子查询分发到涉及到的所有分区，进行并行查询。

下面是一个 `map` 标签模块中可能包含的子模块：

* `generate_reshuffle_query`：是分布式 join 独有的标签，包含进行
  generate\_reshuffle\_query 过程的信息。generate\_reshuffle\_query 是进行分布式 join 前将数据按照 join
  列连续存储在内存区的一个操作。如果 join 列是分区列，则不会进行该操作。(仅 2.00 及以上版本支持分布式 join)
* `partitions` : 本次查询的分区信息，其子标签 local 和 remote
  分别表示查询的分区位于本地节点的数量和查询的分区位于远程节点的数量。
* `cost`：map 阶段完成所有过程所消耗的总时间（此时所有子查询都执行完成）。
* `partitionRoute`：集群中各个节点执行的子查询数量。
* `detail`：map 阶段查询子句的执行细节。
  + most：耗时最多的子查询的信息。
  + least：耗时最少的子查询的信息。

```
"map": {
            "generate_reshuffle_query": {
                "cost": 2
            },
            "partitions": {
                "local": 0,
                "remote": 50
            },
            "cost": 9723,
            "partitionRoute": {
                "node3": 15,
                "node1": 19,
                "node2": 16
            },
            "detail": {
                "most": {
                    "sql": "select [254215] cumsum(price) as cumsum_price from pt where sym == \"a\" map [partition = /test_explain_olap/53/b]",
                    "explain": {
                        "from": {
                            "cost": 39
                        },
                        "where": {
                            "rows": 100,
                            "cost": 246
                        },
                        "rows": 100,
                        "cost": 1222
                    }
                },
                "least": {
                    "sql": "select [254223] cumsum(price) as cumsum_price from pt where sym == \"a\" map [partition = /test_explain_olap/92/b]",
                    "explain": {
                        "where": {
                            "rows": 0,
                            "cost": 154
                        },
                        "rows": 0,
                        "cost": 245
                    }
                }
            }
        }
```

## optimize

查询优化会显示在 `optimize` 标签模块中。

`optimize`：查询优化的细节。组成如下所示：

`field`：可以是被优化的字段，如："where", "join", "group"；也可以是优化的场景说明，如 "single partition
query"。

```
"optimize": {
  "cost": 3,
  "field": ["where", "join", "group"],
  "sql": "..."  // 优化之后的SQL语句
}
```

以下列举了几种可能优化的场景：

1. 只查询单个分区数据，其 `map`
   阶段的执行过程如下：

   ```
   "map": {
     "partitions": {
         "local": 1,   // 或者0
         "remote": 0,   // 或者1
     },
     "cost": 100,
     "optimize": {
         "field": "single partition query",
         "sql": "...",
         "explain": { ... }
     }
   }
   ```

   单分区情况下，查询任务只涉及到对应分区的单个节点，因此不需要进行
   `merge`。
2. context by + csort + limit。对于 context by 和 csort 以及 limit 配合使用的 SQL
   查询，系统内部进行了查询优化：

   ```
   select * from pt where device in ["a", "b"] context by device csort time limit n
   ```

   其中
   pt 可以是单分区表或者组合分区的分区表。优化需满足以下几个条件：
   1. context by 指定的列在 where 子句中进行了条件过滤。 比如上例中的 device, where 子句中筛选了
      `device in ["a", "b"]` 的数据。
   2. csort 指定的列（如例中的 time）是分区列, 且分区方式是 VALUE 或 RANGE。
   3. csort, context by 只能指定单列。
   4. context by 指定的列也需要一起输出（通过 select 语句指定该列）。此时返回的结果中， `map`
   标签模块的组成如下所示：

   ```
   "map":{
     "optimize":{
         "cost":4,  // 完成优化耗费的时间
         "field":"optimize for CONTEXT BY + CSORT + LIMIT: partial parallel execution."
     },
     "cost":1082  // 完成 map 阶段耗费的时间
   }
   ```

   如果进行了查询优化，返回结果可能不包含 `merge` 和 `reduce` 阶段。

## merge

`merge` 阶段会将 `map` 阶段分配到各个节点的子查询的结果进行合并。

下面是一个 `merge` 标签模块中可能包含的子模块：

* `row`： `merge` 后的结果的总行数。
* `cost`： `merge` 阶段消耗的时间。
* `detail`： `merge` 阶段查询子句的执行细节。
  + most：返回行数最多的子查询的信息。
  + least：返回行数最少的子查询的信息。

```
"merge": {
  "row": 10000,
  "cost": 50,
  "detail": {
      "most": {  // 返回行数最多的SubQuery
      "sql": "select time,id,value from pt [partition = /iot/6]",
      "explain": { ...}
      },
      "least": {
      "sql": "select time,id,value from pt [partition = /iot/9]",
      "explain": { ...}
      }
  }

}
```

## reduce

reduce 阶段通常是对子查询返回的结果做收尾处理，通常是对 merge 的结果表做最后一次查询。执行计划是否包含 reduce 阶段视具体情况而定。

下面介绍一个 `reduce` 标签模块中可能包含的子模块：

```
"reduce": {
  "sql": "...",  // Final Query
  "explain": { ... }
}
```

除了上述在分布式查询各个阶段说明的标签模块以外，实际运行的结果中还可能包含一部分其他 SQL 相关的子标签模块。显示如下：

**join, csort, sort以及pivotBy标签模块，只包含 cost 指标：**

```
"join": {
"cost": 10
}
```

## groupBy

* `sortKey`：是否利用了表的 *sortColumn* 来进行 groupBy。如果该值为true, 则没有 `algo`
  标签。
* `algo`：分组算法, 可以为: "hash", "vectorize", "sort"。当分组算法为
  “sort” 时，将显示以下两个字段：
  + `inplaceOptimization` 是否进行了 inplace
    Optimization，即预先分配所需的内存来存储所有分组的查询结果，而不是每计算一组结果就进行小规模的内存分配，避免了频繁的小内存分配带来的开销，且节省了中间内存的使用。
  + `optimizedColumns` 若
    `inplaceOptimization` 为 true，则该字段将显示进行了 inplace Optimization
    的列名。
* `fill`： [interval](interval.html)
  插值填充过程的标签。

```

"groupBy":{
 "sortKey":false,
 "algo":"hash",
 "cost":8
}
// group by 搭配 interval 使用
"groupBy": {
 "sortKey": false,
 "algo": "hash",
 "fill": {
 "cost": 23
 },
 "cost": 248
}
// 进行 inplace Optimization
"groupBy": {
 "sortKey": false,
 "algo": "sort",
 "inplaceOptimization": true,
 "optimizedColumns": [
 "std_price0"
 ],
 "cost": 16422
},
```

## contextBy

`sortKey`：是否利用了表的 *sortColumn* 来做 contextBy。

```
"contextBy":{
  "sortKey":false,
  "cost":1994
}
```

## 表连接

自 2.00.12/3.00.0 版本起，`HINT_EXPLAIN` 支持显示如下表连接操作：

* cross join
* inner join
* left join
* left semi join
* right join
* full join

注： 如果表连接操作中存在分区内存表，则不遵循本节说明。

### 标准 SQL 写法的表连接查询

SQL 示例如下：

```
select [HINT_EXPLAIN] * from pt1 left join t2 on pt1.p1=t2.p2 where p1+p2>4 and p2 < 6
```

使用标准 SQL 写法的表连接查询的显示输出由如下模块依情况进行组合，且一个模块的输出中也可能包含其他模块的输出：

* SQL 引擎
* 多表 Join 框架
* Pipelined Join 执行过程
* 串行 Join 执行过程
* 取数据过程

**SQL 引擎**

与其他模块的数据构成相同。

```
{
    "measurement": "microsecond",
    "explain": {
        // <UniversalTableJoinImp explain 结果>
        "rows": 10,                             //查询返回的记录数
        "cost": 237                             //查询耗时
    },
}
```

**多表 Join 框架**

* `numPipelinedStages`：能用 pipeline 的 join 数量。
* `numSerialStages`：不能用 pipeline 的 join 数量。
* `pipelinedStages`：包含 Pipelined Join 执行过程的 explain 结果。下节将详细介绍。
* `serialStages`：包含串行 Join 执行过程的 explain 结果。后文将详细介绍。

```
"numPipelinedStages": 2,
"numSerialStages": 3,
"pipelinedStages": {
    // <Pipelined Join 执行过程的 explain 结果>
},
"serialStages": {
    // <串行 Join 执行过程的 explain 结果>
}
```

**Pipelined Join 执行过程如下：**

* `rows`：pipeline 阶段产生结果的行数。
* `cost`：pipeline 阶段总耗时。
* `numTasks`：pipeline 任务数。
* `most`：耗时最长的任务。
  + `cost`：此 pipeline 运行耗时。
  + `segments`：此 pipeline 每张表的分区 path，如果是内存表则为""，如果是分区表但被剪枝则为"<Empty
    Segment>"。
  + `explain`：
    - `left`：取数据过程的 explain 结果，如果是分区表但被剪枝则为 "sql":"<Empty
      Segment>"。
    - `right`：取数据过程的 explain 结果。
    - `join`：
      * `script`：join 操作的脚本。
      * `predicates`：下推到此次 join 的谓词。
      * `rows`：此次 join 的结果行数。
      * `cost`：join 运行耗时。
  + `least`：耗时最短的任务，格式与`most`相同。
  + `resultPartitionInfo`：join 结果的分区信息。
    - `isPartitioned`：join 结果是否分区，如果为 true 则有下面的字段。
    - `estimatedRows`：估计的总行数。
    - `domainType`：结果复用的 database 的分区方式，如果没有复用，值为 NULL。
    - `domainScheme`：如果 "domainType" 不为 NULL，其分区 scheme。
    - `partitionColumns`：结果分区列。
    - `useSeqPartition`：结果是否用 SEQ 方式分区。
  + `totalExecutionCost`：执行 pipeline 任务的总耗时（不包含生成分区表的耗时）。
  + `totalAppendCost`：结果生成分区表的总耗时。
  + `final`：最终查询结果。如果 pipeline 覆盖所有 join，会有一次最终查询，下面是对应的 explain 结果、
    - `sql`：最终查询 SQL。
    - `rows`：最终查询的结果行数 。
    - `cost`：最终查询耗时。
    - `explain`：最终查询的 explain 结果。

```
"pipelinedStages": {
    "rows": 10,
    "cost": 35,
    "numTasks": 10,
    "most": {
        "cost": 20,
        "segments": [
            "20210101/Key1",
            ""
        ],
        "explain": {
            "stage1": {
                "left": {
                    // <取数据过程的 explain 结果>
                },
                "right": {
                    // <取数据过程的 explain 结果>
                },
                "join": {
                    "script": "ej(t1, t2, `id, `id)",
                    "predicates": [
                        "t1.id > 3",
                        "t2.id < 5"
                    ],
                    "rows": 10,
                    "cost": 152
                }
            },
            "stage2": {
                "right": {
                    // <取数据过程的 explain 结果>
                },
                "join": {
                    // 与上面 "join" 格式相同
                }
            },
            ...
        }
    },
    "least": {
        // 与 "most" 格式相同
    },
    "resultPartitionInfo": {
        "isPartitioned": true,
        "estimatedRows": 50000,
        "domainType": "NULL/VALUE/HASH/...",
        "domainScheme": [1, 2, 3],
        "partitionColumns": ["col1", "col2"],
        "useSeqPartition": false
    "totalExecutionCost": 20,
    "totalAppendCost": 30,
    "final": {
        "sql": "...",
        "rows": 10,
        "cost": 237,
        "explain": {
            // <最终查询的 explain 结果>
        }
    }
},
```

**串行 Join 执行过程**

* `rows`：串行阶段产生结果的行数。
* `cost`：串行阶段总耗时。
* `stage`：编号从 pipeline 后一个编号开始。如果完全没有 pipeline 阶段，第一次 join 会有
  "left"，即取左表数据的 explain 结果。
* `left`：取数据过程的 explain 结果。
* `right`：取数据过程的 explain 结果。
* `resultPartitionInfo`：join 结果的分区信息。
  + `partitionParamsSet`：此次 join
    结果是否尝试分区。对除了最后一次以外的join，"partitionParamsSet" 为 true，且有其他字段。
  + `forcePartition`：是否强制生成分区结果。
  + `domainType`：结果复用的 database 的分区方式，如果没有复用，值为 NULL。
  + `domainScheme`：如果 "domainType" 不为 NULL，其分区 scheme。
  + `partitionColumns`：结果分区列。
  + `useSeqPartition`：结果是否用 SEQ 方式分区。
  + `numForcedPartitions`：在 "domainType" 为 NULL 且 "useSeqPartition" 为
    false 时默认 HASH 分区的强制分区数量，-1 为未设置。

```
"serialStages": {
    "rows": 10,
    "cost": 30,
    "stage3": {
        "left": {
            // <取数据过程的 explain 结果>
        },
        "right": {
            // <取数据过程的 explain 结果>
        },
        "join": {
            "sql": "...",
            "rows": 10,
            "cost": 237,
            "resultPartitionInfo": {
                "partitionParamsSet": true,

                "forcePartition": true,
                "domainType": "NULL/VALUE/HASH/...",
                "domainScheme": [1, 2, 3],
                "partitionColumns": ["col1", "col2"],
                "useSeqPartition": false
                "numForcedPartitions": -1,
            },
            "explain": {
                // <本次 join 查询的 explain 结果>
            }
        }
    },
    "stage4": {
        "right": {
            // <取数据过程的 explain 结果>
        },
        "join": {
            // 与上面的 "join" 格式相同
        }
    },
    ...
},
```

**取数据过程**

* `sql`：取数据的 SQL。
* `rows`：取到的数据条数。
* `cost`：取数据 SQL 运行耗时。
* `resultPartitionInfo`：join 结果的分区信息。
  + `partitionParamsSet`：取数据结果是否尝试分区；若为 true，且有其他字段。
  + `forcePartition`：是否强制生成分区结果。
  + `domainType`：结果复用的 database 的分区方式，如果没有复用，值为 NULL。
  + `domainScheme`：如果 "domainType" 不为 NULL，其分区 scheme。
  + `partitionColumns`：结果分区列
  + `useSeqPartition`：结果是否用 SEQ 方式分区。
  + `numForcedPartitions`：在 "domainType" 为 NULL 且 "useSeqPartition" 为
    false 时默认 HASH 分区的强制分区数量，-1 为未设置。

```
"sql": "...",
"rows": 10,
"cost": 237,
"resultPartitionInfo": {
    "partitionParamsSet": true,
    "forcePartition": true,
    "domainType": "NULL/VALUE/HASH/...",
    "domainScheme": [1, 2, 3],
    "partitionColumns": ["col1", "col2"],
    "useSeqPartition": false
    "numForcedPartitions": -1,
},
"explain": {
    // <取当前表数据的查询的 explain 结果>
}
```

### 使用函数写法的 Join 查询

由于分区全部覆盖，使用函数写法的 Join 查询的 explain 的结果维持原先格式。SQL 语句示例：

```
select [HINT_EXPLAIN] * from ej(pt1,pt2,`p1,`p2)
```

**使用 cj 的特殊情况说明：**

在满足以下所有条件时，连续 `cj` 的输出结果遵循前文所述的标准 SQL 输出结构：

* 查询的 from 是不涉及分区内存表的连续多表 `cj`，不涉及其他 join 类型。
* 嵌套的任何一次 `cj` 只能出现在外层 `cj` 的左表。
  + 这是一个符合条件的例子：`cj(cj(cj(t1, t2), t3), t4)`
  + 这是一个不符合条件的例子：`cj(t1, cj(t2, t3))`
* cj 以及 表 的外面可以嵌套任意个子查询，但不能是 pivot by
  查询。例子：

  ```
  select * from cj(select * from cj(select * from cj(t1, t2), t3), select * from
                  t4)
  ```

通过打印 SQL 执行过程，分析 SQL 语句执行中每一部分的耗时，可以帮助我们优化 SQL 语句，提升执行效率。具体的优化场景可以参考 [DolphinDB SQL执行计划教程](../../tutorials/DolphinDB_Explain.html)

