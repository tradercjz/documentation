# restoreDB

## 语法

`restoreDB(backupDir, dbPath, [newDBPath], [keyPath])`

## 参数

**backupDir** 字符串，表示存放备份数据的目录

**dbPath** 字符串，表示已备份的分布式数据库的路径

**newDBPath** 字符串，表示新数据库的名称。如果没有指定，默认值为 *dbPath*。

**keyPath** 字符串标量，指定恢复加密表备份的密钥路径。仅 Linux
系统支持该参数。恢复数据使用的密钥必须与备份时指定的密钥版本一致。注意恢复加密表时，备份表与目标表必须指定相同的加密方式（即建表时指定相同的
*encryptMode* 参数）。

## 详情

恢复备份的数据到数据库。返回包含数据库名称和表名称的表，每一行为完成恢复的数据库及表名称。

该函数与 [migrate](../m/migrate.html)
类似，都可恢复整个数据库下的所有表，区别见表相关内容。

注：

* 该函数仅支持恢复以拷贝文件方式（即 [backup](../b/backup.html) 时指定
  *dbPath* 参数）进行的备份。
* 恢复时需要确保备份数据与待恢复数据库的引擎类型（engine）一致，且 *partitionScheme*（VALUE 除外）也保持一致。
  当采用 VALUE 分区时，须保证备份数据中的分区方案是待恢复数据库的分区方案的子集。例如：备份文件的分区方案是
  database("dfs://xxx", VALUE, 2017.08.07..2017.08.11)， 则待恢复数据库的 VALUE
  分区范围必须不小于 2017.08.07..2017.08.11。

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

backupDB(backupDir, dbName)

restoreDB(backupDir, dbName)
```

| dbName | tableName |
| --- | --- |
| dfs://compoDB2 | pt1 |
| dfs://compoDB2 | pt2 |

相关函数：[restore](restore.html), [restoreTable](restoreTable.html), [migrate](../m/migrate.html), [backup](../b/backup.html), [backupDB](../b/backupDB.html), [backupTable](../b/backupTable.html)

