# getBackupList

## 语法

`getBackupList(backupDir, dbPath, tableName)`

## 参数

**backupDir** 是字符串，表示存放备份数据的目录。

**dbPath** 是字符串，表示分布式数据库的名称。

**tableName** 是字符串，表示数据库中表的名称。

## 详情

返回一个表，包含指定分布式表的备份信息，每个分区对应表中的一行。其中表中各字段的含义如下：

* chunkID：分区的 ID。
* chunkPath：分区的完整路径。
* cid：版本号。
* rows：分区数据包含的行数。
* updateTime：chunk 最后一次更新的时间戳。

## 例子

```
if(existsDatabase("dfs://valuedb")){
   dropDatabase("dfs://valuedb")
}
n=3000000
month=take(2000.01M..2000.04M, n);
x=1..n
t=table(month,x);

db=database("dfs://valuedb", VALUE, 2000.01M..2000.04M)
pt = db.createPartitionedTable(t, `pt, `month);
pt.append!(t);
backup("/home/DolphinDB/backup","dfs://valuedb",tableName="pt");
getBackupList("/home/DolphinDB/backup","dfs://valuedb","pt");
```

| chunkID | chunkPath | cid | rows | updateTime |
| --- | --- | --- | --- | --- |
| 0061427c-4b24-e3b6-425c-c0e1553d3c35 | dfs://valuedb/200001M/b39 | 13,348 | 750,000 | 2022.09.21T15:45:50.931 |
| dabbd90d-6001-f8a9-4d3e-8000d96eba68 | dfs://valuedb/200002M/b39 | 13,348 | 750,000 | 2022.09.21T15:45:50.931 |
| f5c259b4-4be3-f385-46d4-1a1a2d224e9d | dfs://valuedb/200003M/b39 | 13,348 | 750,000 | 2022.09.21T15:45:50.931 |
| 6ed58eb9-a2ae-6197-4f81-3186ca1e8b20 | dfs://valuedb/200004M/b39 | 13,348 | 750,000 | 2022.09.21T15:45:50.931 |

