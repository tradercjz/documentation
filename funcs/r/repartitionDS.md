# repartitionDS

## 语法

`repartitionDS(query, [column], [partitionType], [partitionScheme],
[local=true])`

## 参数

**query** 是一个 SQL 查询的元代码，或一个元组，其中每个元素都是 SQL 查询的元代码。

**column** 是一个字符串，表示 *query* 中的一个列名。`repartitionDS`
函数会根据该列划分数据源。

**partitionType** 表示分区类型，它的取值可以是 RANGE, VALUE 或 HASH。

**partitionScheme** 是一个向量，表示分区方案。

**local** 可选参数，布尔值，表示是否将数据源获取到当前节点进行计算。默认值为 true。

## 详情

使用新的分区类型和分区方案重新划分数据源。该函数会返回一个元组，包含一组数据源。

* 如果 *query* 是一个 SQL 查询的元代码，必须指定 *column* 参数。对于
  COMPO 分区类型的表，可以不指定 *partitionType* 和 *partitionScheme*
  参数，`repartitionDS` 函数会根据 *column*
  列原始的分区类型和分区方案划分数据源。
* 如果 *query* 是包含多个 SQL 查询元代码的元组，无需指定
  *column*、*partitionType* 和 *partitionScheme*
  参数，`repartitionDS` 函数会返回一个和 *query* 长度相同的元组，每个元素都是
  *query* 中的元代码对应的数据源。
* 当 *local* 设置为 true 时：将数据源获取到执行该函数的节点上。
* 当 *local* 设置为 false
  时：如果在指定了计算组的计算节点上执行该函数时，仅将数据源获取到同组内的所有计算节点上；否则将数据源获取到集群中所有数据节点、未指定计算组的计算节点上。

## 例子

创建分布式数据库和表：

```
n=1000000
ID=rand(100, n)
dates=2017.08.07..2017.08.11
date=rand(dates, n)
x=rand(10.0, n)
t=table(ID, date, x)

dbDate = database(, VALUE, 2017.08.07..2017.08.11)
dbID = database(, RANGE, 0 50 100)
db = database("dfs://compoDB", COMPO, [dbDate, dbID])
pt = db.createPartitionedTable(t, `pt, `date`ID)
pt.append!(t);
```

例1：*query*是一个 SQL 查询的元代码，指定了 *partitionType* 和
*partitionScheme*。

```
repartitionDS(<select * from pt>,`date,RANGE,2017.08.07 2017.08.09 2017.08.11);

// output
[DataSource< select [4] * from pt where date >= 2017.08.07,date < 2017.08.09 >,DataSource< select [4] * from pt where date >= 2017.08.09,date < 2017.08.11 >]
```

例2：*query*是一个 SQL 查询的元代码，没有指定 *partitionType*和
*partitionScheme*。

```
repartitionDS(<select * from pt>,`ID)

// output
[DataSource< select [4] * from pt [partition = */0_50] >,DataSource< select [4] * from pt [partition = */50_100] >]
```

例3：*query* 是包含多个 SQL 查询元代码的元组。

```
repartitionDS([<select * from pt where id between 0:50>,<select * from pt where id between 51:100>]);

// output
[DataSource< select [4] * from pt where id between 0 : 50 >,DataSource< select [4] * from pt where id between 51 : 100 >]
```

