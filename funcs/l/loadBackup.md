# loadBackup

## 语法

`loadBackup(backupDir, dbPath, partition, tableName)`

## 参数

**backupDir** 是字符串，表示存放备份数据的目录。

**dbPath** 是字符串，表示 DFS 数据库的路径，例如 "dfs://demo"。

**partition** 是字符串，表示分区在数据库内的路径，例如 "/20190101/GOOG"。

注： 若使用 2.00.4 到 2.00.6 版本
server，对表级分区数据进行备份和恢复时，该参数必须指定路径到物理索引（可通过函数 [listTables](listTables.md) 获取），例如分区 "/compoDB/20170807/0\_50"
下表的物理索引为8，则 *partition* 需指定为
"/compoDB/20170807/0\_50/8"。

**tableName** 是字符串，表示分布式表的名称。

## 详情

加载指定分布式表中某个分区的备份数据。该函数必须要用户登录后才能执行。

请注意，目前该函数只支持加载 SQL 元代码（即 [backup](../b/backup.md)
时指定 *sqlObj* 参数）备份的数据。

## 例子

```
loadBackup("/home/DolphinDB/backup","dfs://valuedb", "/200001M","pt");
```

输出返回：

| month | x |
| --- | --- |
| 2000.01M | 1 |
| 2000.01M | 205 |
| 2000.01M | 409 |
| 2000.01M | 613 |
| 2000.01M | 817 |

