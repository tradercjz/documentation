# existsPartition

## 语法

`existsPartition(partitionUrl, [tableName])`

## 参数

**partitionUrl** 字符串，表示分区文件夹的路径。

**tableName** 字符串，表示表名。

* 若分区粒度为数据库级（ [database](../d/database.html) :
  *chunkGranularity* = 'DATABASE'），可以不指定该参数。
* 若分区粒度为表级（ [database](../d/database.html) :
  *chunkGranularity* = 'TABLE'）

  + 若 *path* 指定的路径包含了物理索引（通过函数 [listTables](../l/listTables.html) 获取），可以不指定该参数。
  + 否则，必须指定该参数。

## 详情

检查指定分区是否存在。

## 例子

检查分区是否在分布式文件系统中（以下脚本需要在集群的数据节点/计算节点中执行）：

```
n=1000000
ID=rand(10, n)
dates=2017.08.07..2017.08.11
date=rand(dates, n)
x=rand(10.0, n)
t=table(ID, date, x)

db = database("dfs://valueDB", VALUE, 2017.08.07..2017.08.11)
pt = db.createPartitionedTable(t, `pt, `date);
pt.append!(t);

listTables("dfs://valueDB")
```

| tableName | physicalIndex |
| --- | --- |
| pt | s |

```
existsPartition("dfs://valueDB/20170807/s");
// output
true

//表级分区时，path 不包含物理索引，检查分区时需指定表名，否则查找不到分区信息
existsPartition("dfs://valueDB/20170807", `pt)
// output
true

existsPartition("dfs://valueDB/20170807");
// output
false

existsPartition("dfs://valueDB");
// output
false

existsPartition("dfs://valueDB/20170807/s/pt");
// output
false
```

