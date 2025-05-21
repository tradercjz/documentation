# renameTable

## 语法

`renameTable(dbHandle, tableName, newTableName)`

## 参数

**dbHandle** 是一个DFS数据库句柄。

**tableName** 是一个字符串，表示要改名的数据表名称。该表既可为分布式表，亦可为维度表。

**newTableName** 是一个字符串，表示要改名后的数据表名称。

## 详情

将给定分布式数据库内数据表改名。

## 例子

```
n=1000000
ID=rand(10, n)
x=rand(1.0, n)
t=table(ID, x)
db=database("dfs://hashdb101", HASH,  [INT, 2]);
pt = db.createPartitionedTable(t, `pt, `ID)
pt.append!(t)
renameTable(db, `pt, `pt1)
select count(x) from loadTable(db, `pt1);
```

输出返回： 1000000

