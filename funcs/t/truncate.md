# truncate

## 语法

`truncate(dbUrl, tableName)`

## 参数

**dbUrl** 字符串，表示数据库的路径。

**tableName** 字符串，表示数据表的表名。

## 详情

删除分布式表的所有数据，但保留数据表结构。其性能较 [delete](../../progr/sql/delete.html) 语句以及 [dropPartition](../d/dropPartition.html) 命令均有数倍提升。

若仅需要删除表中所有的数据，但保留表结构，建议调用 `truncate`
实现。若无需保留表结构，建议调用 [dropTable](../d/dropTable.html) 命令。

## 例子

```
n=1000000
ID=rand(150, n)
dates=2017.08.07..2017.08.11
date=rand(dates, n)
x=rand(10.0, n)
t=table(ID, date, x)
dbDate = database(, VALUE, 2017.08.07..2017.08.11)
dbID = database(, RANGE, 0 50 100 150)

dbName="dfs://compoDB"
if(existsDatabase(dbName)){

      dropDatabase(dbName)
}
db = database(dbName, COMPO, [dbDate, dbID])
pt = db.createPartitionedTable(t, `pt, `date`ID)
pt.append!(t);

truncate(dbName, `pt)
```

