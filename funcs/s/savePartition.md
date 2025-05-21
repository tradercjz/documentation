# savePartition

## 语法

`savePartition(dbHandle, table, tableName,
[compression=true])`

## 参数

**dbHandle** 是一个 DolphinDB 数据库句柄。

**table** 是将要保存的内存中的表。

**tableName** 是表示保存的分区表名称的字符串。

**compression** 是否压缩数据。默认的设置是 true。

## 详情

把一张表保存为分布式数据库中的分区表。该命令必须要用户登录后才能执行。

在用 *savePartition* 保存之前，要用 [createPartitionedTable](../c/createPartitionedTable.html) 先创建空的分区表。

## 例子

```
n=1000000
ID=rand(10, n)
value=rand(1.0, n)
t=table(ID, value);

db=database("dfs://rangedb_Trades", RANGE,  0 5 10)
Trades = db.createPartitionedTable(t, "Trades", "ID");
savePartition(db, t, `Trades)

Trades=loadTable(db, `Trades)
select count(value) from Trades;
// output
1,000,000
```

在上述例子中，数据库 db 有两个分区：[0,5)和[5,10)。表t被保存为一个分区表 Trades，它包含数据库 db
中的分区列。

我们可以在表 Trades 中追加另一个表：

```
n=500000
ID=rand(10, n)
value=rand(1.0, n)
t1=table(ID, value);
savePartition(db, t1, `Trades)
Trades=loadTable(db, `Trades)
select count(value) from Trades;
// output
1,500,000
```

