# migrate

## 语法

`migrate(backupDir, [backupDBPath], [backupTableName],
[newDBPath=backupDBPath], [newTableName=backupTableName],
[keyPath])`

## 参数

**backupDir** 字符串，表示存放已备份数据的目录。

**backupDBPath** 字符串，表示已备份的数据库的名称。

**backupTableName** 字符串，表示已备份的表的名称。

**newDBPath** 字符串，表示新数据库的名称。如果没有指定，默认值为 *backupDBPath*。
若指定该参数，则需要确保备份数据与 *newDBPath* 的引擎类型（engine）一致，且 partitionScheme（VALUE 除外）也保持一致。
当采用 VALUE 分区时，须保证备份数据中的分区方案是待恢复数据库的分区方案的子集。

**newTableName** 字符串，表示新表的名称。如果没有指定，默认值为 *backupTableName*。

**keyPath** 字符串标量，指定恢复加密表备份的密钥路径。仅 Linux
系统支持该参数。恢复数据使用的密钥必须与备份时指定的密钥版本一致。注意恢复加密表时，备份表与目标表必须指定相同的加密方式（即建表时指定相同的
*encryptMode* 参数）。

## 详情

恢复数据库中已备份的数据。返回的结果是一个表，包含了每个表恢复数据的结果。该函数必须要用户登录后才能执行。

**migrate 函数有以下三种用法**：

* migrate(backupDir): 恢复该目录下所有数据库的备份数据。恢复后的数据库名称、表名称与原数据库、原表一致。
* migrate(backupDir, backupDBPath):
  恢复该目录下指定数据库的备份数据。恢复后的数据库名称、表名称与原数据库、原表一致。
* migrate(backupDir, backupDBPath, backupTableName, [newDBPath],
  [newTableName]): 恢复该目录下指定数据库指定表的备份数据。如果没有指定 *newDBPath* 和
  *newTableName*，恢复后的数据库名称、表名称与原数据库、原表一致。如果指定了 *newDBPath* 和
  *newTableName*，恢复后的数据库名称为 *newDBPath*，表名为
  *newTableName*。

## 例子

创建两个示例数据库，并将它们备份到相同的目录中：

```
backupDir="/home/DolphinDB/backup"

n = 1000000
t1 = table(rand(2012.12.01..2012.12.10, n) as date, rand(`AAPL`IBM`GOOG`MSFT, n) as sym, rand(1000.0,n) as price)
t2 = table(rand(2012.12.01..2012.12.10, n) as date, rand(`AAPL`IBM`GOOG`MSFT, n) as sym, rand(1000,n) as qty)
db1 = database("dfs://db1", VALUE, 2012.12.01..2012.12.10)
trades1 = db1.createPartitionedTable(t1, `trades1, `date).append!(t1)
trades2 = db1.createPartitionedTable(t2, `trades2, `date).append!(t2)

n = 1000000
t1 = table(rand(2012.12.01..2012.12.10, n) as date, rand(`AAPL`IBM`GOOG`MSFT, n) as sym, rand(1000.0,n) as price)
t2 = table(rand(2012.12.01..2012.12.10, n) as date, rand(`AAPL`IBM`GOOG`MSFT, n) as sym, rand(1000,n) as qty)
db1 = database("dfs://db2", VALUE, `AAPL`IBM`GOOG`MSFT)
quotes1 = db1.createPartitionedTable(t1, `quotes1, `sym).append!(t1)
quotes2 = db1.createPartitionedTable(t2, `quotes2, `sym).append!(t2)

backup(backupDir, <select * from trades1>, true)
backup(backupDir, <select * from trades2>, true)
backup(backupDir, <select * from quotes1>, true)
backup(backupDir, <select * from quotes2>, true)
```

删除原来的数据库：

```
dropDatabase("dfs://db1")
dropDatabase("dfs://db2")
```

例1. 恢复所有数据库的数据

```
migrate(backupDir);
```

| dbName | tableName | success | errorMsg |
| --- | --- | --- | --- |
| dfs://db1 | trades1 | 1 |  |
| dfs://db1 | trades2 | 1 |  |
| dfs://db2 | quotes2 | 1 |  |
| dfs://db2 | quotes1 | 1 |  |

例2. 恢复数据库 dfs://db1中所有表的数据

```
migrate(backupDir, "dfs://db1");
```

| dbName | tableName | success | errorMsg |
| --- | --- | --- | --- |
| dfs://db1 | trades1 | 1 |  |
| dfs://db1 | trades2 | 1 |  |

例3. 恢复数据库 dfs://db1 中表 trades1 的数据

例3.1 不指定新数据库名称和表名称

```
migrate(backupDir, "dfs://db1", "trades1");
```

| dbName | tableName | success | errorMsg |
| --- | --- | --- | --- |
| dfs://db1 | trades1 | 1 |  |

例3.2 指定新数据库名称和表名称

```
migrate(backupDir, "dfs://db1", "trades1", "dfs://db3", "trades");
```

| dbName | tableName | success | errorMsg |
| --- | --- | --- | --- |
| dfs://db1 | trades1 | 1 |  |

```
exec count(*) from loadTable("dfs://db3", "trades")
// output
1000000
```

相关函数：[backup](../b/backup.html), [backupDB](../b/backupDB.html), [backupTable](../b/backupTable.html), [restore](../r/restore.html), [restoreDB](../r/restoreDB.html), [restoreTable](../r/restoreTable.html)

