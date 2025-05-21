# multiTableRepartitionDS

## 语法

`multiTableRepartitionDS(query, [column], [partitionType], [partitionScheme],
[local=true])`

## 参数

**query** 是一个元组，其中每个元素都是 SQL 查询的元代码，并且每个 SQL 查询表示的数据表结构（包括列名和各列的数据类型）必须完全相同。

**column** 是一个字符串，表示 *query* 中的一个列名。*repartitionDS* 函数会根据该列划分数据源。

**partitionType** 表示分区类型，它的取值可以是 RANGE 或 VALUE。

**partitionScheme** 是一个向量，表示分区方案。

**local** 是一个布尔值，表示是否将数据源获取到当前节点进行计算。默认值为 true。

## 详情

使用相同的分区类型和分区方案对多个表重新划分数据源。该函数会返回一个元组，包含一组数据源。

如果没有指定 *column*, *partitionType* 和
*partitionScheme*，该函数将根据各表原来的分区类型和分区方案划分数据源。相当于 *query* 中的每个元代码应用到 [sqlDS](../s/sqlDS.html) 函数，再将结果合并。

## 例子

```
n=100000
date=rand(2019.06.01..2019.06.05,n)
sym=rand(`AAPL`MSFT`GOOG,n)
price=rand(1000.0,n)
t1=table(date,sym,price)
db=database("dfs://value",VALUE,2019.06.01..2019.06.05)
db.createPartitionedTable(t1,`pt1,`date).append!(t1);

n=100000
date=rand(2019.06.01..2019.06.05,n)
sym=rand(`AAPL`MSFT`GOOG,n)
price=rand(1000.0,n)
qty=rand(500,n)
t2=table(date,sym,price,qty)
db1=database("",VALUE,2019.06.01..2019.06.05)
db2=database("",VALUE,`AAPL`MSFT`GOOG)
db=database("dfs://compo",COMPO,[db1,db2])
db.createPartitionedTable(t2,`pt2,`date`sym).append!(t2);

pt1=loadTable("dfs://value","pt1")
pt2=loadTable("dfs://compo","pt2");
```

例1. 根据原有的分区方案划分数据源，不指定 *column*, *partitionType*和
*partitionScheme*

```
ds=multiTableRepartitionDS([<select * from pt1>,<select date,sym,price from pt2>]);
// output
(DataSource< select [7] * from pt1 [partition = /value/20190601] >,DataSource< select [7] * from pt1 [partition = /value/20190602] >, ...... ,DataSource< select [7] date,sym,price from pt2 [partition = /compo/20190605/GOOG] >,DataSource< select [7] date,sym,price from pt2 [partition = /compo/20190605/MSFT] >)
```

例2. 根据股票代码的值划分数据源

```
ds=multiTableRepartitionDS([<select * from pt1>,<select date,sym,price from pt2>],`sym,VALUE,`AAPL`MSFT`GOOG);
// output
(DataSource< select [4] * from pt1 where sym == "AAPL" >,DataSource< select [4] * from pt1 where sym == "MSFT" >,DataSource< select [4] * from pt1 where sym == "GOOG" >,DataSource< select [4] date,sym,price from pt2 where sym == "AAPL" >,DataSource< select [4] date,sym,price from pt2 where sym == "MSFT" >,DataSource< select [4] date,sym,price from pt2 where sym == "GOOG" >)
```

例3. 根据日期范围划分数据源

```
ds=multiTableRepartitionDS([<select * from pt1>,<select date,sym,price from pt2>],`date,RANGE,2019.06.01 2019.06.03 2019.06.05);
// output
(DataSource< select [4] * from pt1 where date >= 2019.06.01,date < 2019.06.03 >,DataSource< select [4] * from pt1 where date >= 2019.06.03,date < 2019.06.05 >,DataSource< select [4] date,sym,price from pt2 where date >= 2019.06.01,date < 2019.06.03 >,DataSource< select [4] date,sym,price from pt2 where date >= 2019.06.03,date < 2019.06.05 >)
```

相关函数：[repartitionDS](../r/repartitionDS.html)

