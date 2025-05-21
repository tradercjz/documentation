# getBackupMeta

## 语法

`getBackupMeta(backupDir, dbPath, partition,
tableName)`

## 参数

**backupDir** 是字符串，表示存放备份数据的目录。

**dbPath** 是字符串，表示分布式数据库的名称，例如
"dfs://demo"。

**partition** 是字符串，表示分区在数据库内的路径，例如
"/20190101/GOOG"。

请注意：若使用 2.00.4 到 2.00.6 版本
server，对表级分区数据进行备份和恢复时，该参数必须指定路径到物理索引（可通过函数 [listTables](../l/listTables.html) 获取），例如分区 "/compoDB/20170807/0\_50"
下表的物理索引为8，则 partition 需指定为 "/compoDB/20170807/0\_50/8"。

**tableName** 是字符串，表示数据库中表的名称。

## 详情

返回指定某分布式数据表中某个分区的备份信息。返回的结果是一个字典，包含以下 key：

* schema：该数据表的结构。
* dfsPath：该分区的完整路径。
* rows：分区数据包含的行数。
* chunkID：该分区的 ID。
* cid：版本号。

## 例子

查看数据库 dfs://valuedb 中数据表 "pt" 在
"/200001M" 分区的备份信息。

```
getBackupMeta("/home/DolphinDB/backup","dfs://valuedb", "/200001M","pt")
// output
schema->
name  typeString typeInt extra comment
----- ---------- ------- ----- -------
month MONTH      7
x     INT        4

dfsPath->dfs://valuedb/200001M/b39
rows->750000
chunkID->0061427c-4b24-e3b6-425c-c0e1553d3c35
cid->13349
```

