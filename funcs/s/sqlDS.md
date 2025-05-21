# sqlDS

## 语法

`sqlDS(sqlObj, [forcePartition=false])`

## 参数

**sqlObj** 是 SQL 元代码。元代码的详情请参考 [Metaprogramming](../../progr/objs/meta_progr.html)。

**forcePartition** 是一个布尔值。默认值为 false。如果
*forcePartition*=false，系统会检查该查询能够拆分为多个子查询。如果不能拆分为多个子查询，系统不会在分区上拆分查询，并且会抛出异常。如果
*forcePartition*=true，系统会在分区上拆分查询，并且在选中的分区中执行查询。下面两种情况的查询不能拆分为多个子查询：(1)
group by 关键字不是分区列；(2) 指定了 order by 子句。

## 详情

根据输入的 SQL 元代码创建数据源列表。如果 SQL 查询中的数据表有 n 个分区，`sqlDS`
生成 n 个数据源。如果 SQL 查询没有包含任何分区表，`sqlDS` 返回包含一个数据源的元组。

## 例子

```
n=1000000
date=take(2019.01.01..2019.01.03,n)
sym = take(`C`MS`MS`MS`IBM`IBM`IBM`C`C$SYMBOL,n)
price= take(49.6 29.46 29.52 30.02 174.97 175.23 50.76 50.32 51.29,n)
qty = take(2200 1900 2100 3200 6800 5400 1300 2500 8800,n)
t=table(date, sym, price, qty)

db1=database("",VALUE,2019.01.01..2019.01.03)
db2=database("",VALUE,`C`MS`IBM)
db=database("dfs://stock",COMPO,[db1,db2])
trades=db.createPartitionedTable(t,`trades,`date`sym).append!(t)

ds=sqlDS(<select * from trades where date=2019.01.02>);

typestr ds;
// output
ANY VECTOR

size ds;
// output
3

ds[0];
// output
DataSource< select [7] * from trades [partition = /stock/20190102/C] >

ds[1];
// output
DataSource< select [7] * from trades [partition = /stock/20190102/IBM] >

ds[2];
// output
DataSource< select [7] * from trades [partition = /stock/20190102/MS] >
```

