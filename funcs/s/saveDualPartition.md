# saveDualPartition

## 语法

`saveDualPartition(dbHandle1, dbHandle2, table, tableName, partitionColumn1,
partitionColumn2, [compression=false])`

## 参数

**dbHandle1** 是第一级分区的数据库句柄。

**dbHandle2** 是第二级分区的数据库句柄。

**table** 是要保存的内存中的表。

**tableName** 是表示保存的分区表的名称的字符串。

**partitionColumn1** 是表示第一级分区的分区列的字符串。

**partitionColumn2** 是表示第二级分区的分区列的字符串。

**compression** 是一个布尔变量。它表示是否压缩表。当它设置为 true 时，表将被压缩保存到磁盘。默认设置为 false（不压缩）。

## 详情

在共享表前，将一张表保存为组合分区。该命令必须要用户登录后才能执行。

它通常与 [share](../../progr/statements/share.md)
一起使用。如果分区和表已经存在，该函数会把新数据追加到已有表格。

## 例子

```
n=1000000
ID=rand(10, n)
dates=2017.08.07..2017.08.11
date=rand(dates, n)
x=rand(1.0, n)
t=table(ID, date, x);

hdb = database("C:/DolphinDB/Data/dualDB", RANGE,  0 5 10)
vdb = database(, VALUE, dates)
saveDualPartition(hdb, vdb, t, `tDualPartition, `ID, `date)
```

