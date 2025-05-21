# sortBy!

## 语法

`sortBy!(table, sortColumns, [sortDirections])`

## 参数

**table** 是 DolphinDB 中 Table 类型的表。它可以是分区或未分区的内存表。

**sortColumns** 是一个字符串标量或向量，表示某列，该表按照该列进行排序。它也可以是表达式的元代码。

**sortDirections** 是一个布尔值，表示排序方向。1表示按照升序排序，0表示按照降序排序。如果 *sortColumns* 是向量而
*sortDirections* 是标量，那么所有的排序列都根据 *sortDirections* 表示的排序方向排序。

## 详情

根据指定列和指定的排序方向对一个表进行就地排序。如果是分区表，将对每个分区进行排序，而不是对整个表进行排序。

如果 table 是分区表并且启用了并行处理功能（即配置参数 localExcutors >
0），那么该操作是并行操作。

## 例子

对未分区表进行排序：

```
n=20000000
trades=table(rand(`IBM`MSFT`GM`C`YHOO`GOOG,n) as sym, 2000.01.01+rand(365,n) as date, 10.0+rand(2.0,n) as price, rand(1000,n) as qty);
trades.sortBy!(`sym`date, [0,1]);
```

对分区表进行排序：

```
workDir = "C:/DolphinDB/Data"
if(!exists(workDir)) mkdir(workDir)
trades.saveText(workDir + "/trades.txt")
db = database(workDir + "/trade",VALUE,`IBM`MSFT`GM`C`YHOO`GOOG)
db.loadTextEx("trades","sym", workDir + "/trades.txt")
trades = db.loadTable("trades",`IBM`GM`YHOO,1)
trades.sortBy!(`date)
trades.sortBy!(`date, false)
trades.sortBy!(`date`qty, false)
trades.sortBy!(`date`qty, false true)
trades.sortBy!(<qty*price>)
trades.sortBy!(<[date, sym]>)
trades.sortBy!(<[sym, qty*price]>, true false)
```

