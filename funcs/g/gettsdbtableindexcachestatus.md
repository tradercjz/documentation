# getTSDBTableIndexCacheStatus

## 语法

`getTSDBTableIndexCacheStatus()`

## 参数

无。

## 详情

TSDB 引擎在查询 Level File 时，会将其尾部的索引信息（包括 zonemap 等）加载 Level File
时加载到内存中。该函数用于获取已加载的数据库中表的 Level File 索引所占用的内存（单位为字节）。结合 getTSDBDataStat
函数，可以评估内存中的 Level File 对应的表的 sort key 设置是否合理。

输出一个表，包含以下字段：

* dbName：数据库名称。
* chunkId：chunk 的唯一标识。
* tableName：chunk 所属的表名称。
* memUsage：Level File 索引占用的内存，单位为字节。

## 例子

```
t = table(1 2 1 1 2 2 3 as month, `Rome`Paris`London`Paris`Rome`London`Rome as city, 200 500 100 300 300 400 400 as sold)
db_name = "dfs://tsdb_01"
if (existsDatabase(db_name)) {
    dropDatabase(db_name)
}
db = database(db_name, HASH, [INT, 4], , 'TSDB')

pt = db.createPartitionedTable(t, "pt", "month", ,"sold")
pt.append!(t)

pt1 = db.createPartitionedTable(t, "pt1", "month", ,"sold")
pt1.append!(t)

flushTSDBCache()

getTSDBTableIndexCacheStatus()
```

| dbName | chunkId | tableName | memUsage |
| --- | --- | --- | --- |
| dfs://tsdb\_01 | 01e891fa-f66d-7599-7544-4e0449f4e608 | pt1\_3 | 680 |
| dfs://tsdb\_01 | 81c0f8f7-e195-b298-da4a-d007492f4733 | pt1\_3 | 680 |
| dfs://tsdb\_01 | 17f8bc0b-946e-f688-374c-955c586faccf | pt\_2 | 296 |
| dfs://tsdb\_01 | 1df88c41-bccf-449b-504c-5978df9cc03f | pt\_2 | 680 |
| dfs://tsdb\_01 | 10371e0c-685a-51b1-3042-1ba289514bb9 | pt1\_3 | 296 |
| dfs://tsdb\_01 | 0be81d1e-1962-108b-274e-3dc2632921bc | pt\_2 | 680 |

