# getTSDBDataStat

## 语法

`getTSDBDataStat([dbName="*"],[tableName="*"],[chunkId])`

## 参数

**dbName** 字符串，表示数据库的名称。可以包含通配符(“\*“, “%”和”?”)。

**tableName** 字符串，表示数据表名。可以包含通配符(“\*“, “%”和”?”)。

通配符 ”\*” 表示匹配所有，”?”表示单个字符，”%”表示0，1或多个字符。

**chunkId** 字符串标量或向量，表示 chunk 的 ID。若指定该参数，则 *dbName* 和 *tableName*
必须为空或者 \*。

## 详情

获取当前节点上 TSDB 引擎存储的表的所有或指定 chunk 下的 Level File 和 sortKeyEntry 的数量。

结合 pnodeRun 函数，可以查看一个集群内（某个）表的 Level File 和 sortKeyEntry 的数量。

返回一个表，包含以下列：

**levelFileCount**: 每个分区内表的 Level File 的数量。

**sortKeyEntryCount**：每个分区内所有 Level File 文件里未去重的 sortKeyEntry 数量。

## 例子

```
t = table(1 2 1 1 2 2 3 as month, `Rome`Paris`London`Paris`Rome`London`Rome as city, 200 500 100 300 300 400 400 as sold)
db_name = "dfs://window_function"
if (existsDatabase(db_name)) {
    dropDatabase(db_name)
}
db = database(db_name, HASH, [INT, 4], , 'TSDB')

pt = db.createPartitionedTable(t, "pt", "month", ,"sold")
pt.append!(t)

pt1 = db.createPartitionedTable(t, "pt1", "month", ,"sold")
pt1.append!(t)

flushTSDBCache()
```

获取以 `dfs://window` 开头的数据库下所有表的 Level File 和 sortKeyEntry 的数量

```
getTSDBDataStat("dfs://window%")
```

| dbName | chunkId | tableName | levelFileCount | sortKeyEntryCount |
| --- | --- | --- | --- | --- |
| dfs://window\_function | d334ffab-741a-dcbd-174e-42b412058877 | pt1 | 1 | 1 |
| dfs://window\_function | c3de728c-4efb-7e8e-024c-cfafd46c506c | pt1 | 1 | 3 |
| dfs://window\_function | 572b1660-790e-e3a0-3944-9b81e50f4eb4 | pt1 | 1 | 3 |
| dfs://window\_function | e9ea31f6-4e12-2881-b04a-c540dc3947c8 | pt | 1 | 1 |
| dfs://window\_function | 673a7c12-c0d4-72bf-6a42-9c374589e2d6 | pt | 1 | 3 |
| dfs://window\_function | 57ceedc9-4aaf-2aad-aa43-37924da3d32e | pt | 1 | 3 |

获取以 `dfs://window` 开头的数据库下表 pt 的 Level File 和 sortKeyEntry
的数量

```
getTSDBDataStat("dfs://window%","pt")
```

| dbName | chunkId | tableName | levelFileCount | sortKeyEntryCount |
| --- | --- | --- | --- | --- |
| dfs://window\_function | e9ea31f6-4e12-2881-b04a-c540dc3947c8 | pt | 1 | 1 |
| dfs://window\_function | 673a7c12-c0d4-72bf-6a42-9c374589e2d6 | pt | 1 | 3 |
| dfs://window\_function | 57ceedc9-4aaf-2aad-aa43-37924da3d32e | pt | 1 | 3 |

获取指定 chunkId 的分区下的 Level File 和 sortKeyEntry 的数量。

```
getTSDBDataStat(chunkId=["e9ea31f6-4e12-2881-b04a-c540dc3947c8", "673a7c12-c0d4-72bf-6a42-9c374589e2d6"])
```

| dbName | chunkId | tableName | levelFileCount | sortKeyEntryCount |
| --- | --- | --- | --- | --- |
| dfs://window\_function | 673a7c12-c0d4-72bf-6a42-9c374589e2d6 | pt | 1 | 3 |
| dfs://window\_function | 57ceedc9-4aaf-2aad-aa43-37924da3d32e | pt | 1 | 3 |

