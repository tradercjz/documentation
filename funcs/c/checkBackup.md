# checkBackup

## 语法

`checkBackup(backupDir, dbPath, [tableName],
[partition])`

## 参数

**backupDir** 字符串，表示存放备份数据的目录。

**dbPath** 字符串，表示数据库路径。

**tableName** 字符串标量或向量，表示表名。若不指定，表示指定数据库下的所有表。

**partition**
表示分区。是字符串，表示备份分区的相对路径。分区路径可以包含通配符("%"和"?")，"?"表示单个字符，"%"表示0，1或多个字符。

* 若仅检查某个分区，输入分区的相对路径或者"%/"+”分区名称”。举例：要检查 "dfs://compoDB"
  下的分区”20170810/50\_100”，输入 "/compoDB/20170807/0\_50" 或者 "%/20170807/0\_50"。
* 若需要检查所有分区，直接输入"%"。

## 详情

检查备份文件的的完整性和准确性。若所有备份文件均完整且准确，则返回一个空表；否则返回异常的备份文件信息，此时可通过在
`backup` 函数设置 *force* = true 开启强制备份以恢复受损的备份分区数据。

## 例子

```
dbName = "dfs://compoDB2"
n=1000
ID=rand("a"+string(1..10), n)
dates=2017.08.07..2017.08.11
date=rand(dates, n)
x=rand(10, n)
t=table(ID, date, x)
db1 = database(, VALUE, 2017.08.07..2017.08.11)
db2 = database(, HASH,[INT, 20])
if(existsDatabase(dbName)){
   dropDatabase(dbName)
}
db = database(dbName, COMPO,[ db1,db2])

// 创建2个表
pt1 = db.createPartitionedTable(t, `pt1, `date`x).append!(t)
pt2 = db.createPartitionedTable(t, `pt2, `date`x).append!(t)

// SQL 元代码方式备份 pt1
backup(backupDir=backupDir1, sqlObj=<select * from pt1>, parallel=true)
// 拷贝文件方式备份 pt2
backup(backupDir=backupDir2, dbName, parallel=true, tableName=`pt2)

// pt2 备份文件都正常，pt1 中一个 chunk 文件出现问题
checkBackup(backupDir=backupDir2, dbPath=dbName, tableName="pt2")  // 返回一个空表
checkBackup(backupDir=backupDir1, dbPath=dbName, tableName="pt1")  // 返回出错的 chunk 信息
```

| dbName | tableName | chunkPath | chunkID | partitionPath |
| --- | --- | --- | --- | --- |
| dfs://compoDB2 pt1 | /compoDB2/20170807/Key2/9 | 4ae71414-8bfe-4283-b04c-b2e48e90be08 | /20170807/Key2 |  |

上例中，通过调用 *checkBackup* 函数，可以发现在 pt1 中存在损坏的 chunk 文件。此时，设置 *force* = true
再次强制备份，以恢复受损文件。

```
backup(backupDir1, <select * from pt1>,force=true, parallel=true)
checkBackup(backupDir=backupDir1, dbPath=dbName, tableName="pt1")  // 返回一个空表
```

