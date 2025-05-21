# update

update 语句用于更新数据表中的记录。

## 详情

update 语句不仅支持更新内存表，也支持更新没有正在写入数据的 DFS
表（分布式表与维度表）。当更新分布式表时，系统把要更新记录所在的分区整体更新；更新维度表时，系统将该表整体更新。因此更新分布式表仅适用于低频更新任务，例如分钟级更新任务；不适用于高频更新任务，例如毫秒级更新任务。自
2.00.10 版本开始，支持对 OLAP 和 TSDB 引擎（设置 keepDuplicates=ALL
时）下分布式表的分区列进行更新。

更新采取了多版本的方式，并且支持事务。系统会创建一个新的版本以存储新的数据。提交事务之前，其他 SQL
语句仍然访问旧版本的数据。若更新涉及多个分区，只要其中某一个分区更新失败，系统会回滚所有分区的修改。

通过查看[分布式表数据更新原理和性能](../../tutorials/dolphindb_update.html#4-%E6%95%B0%E6%8D%AE%E6%9B%B4%E6%96%B0%E5%8E%9F%E7%90%86)中“数据更新原理”章节的内容来了解分布式表的更新原理。

通过 update 语句，可以使用向量或数组向量更新数组向量列，详情参考例4，例5。

注：

* 暂不支持更新内存分区表的数组向量列。
* 暂不支持通过表连接更新内存表的数组向量列。

注： 自 3.00.0 版本起，支持 catalog 结构。

自 2.00.12 版本起，update 语句支持在 context by 子句中使用 csort 指定顺序；支持使用 having
指定只对满足聚合函数条件的分组进行更新；支持通过 having 使用非聚合函数、或者混用非聚合函数与聚合函数对满足条件的分组进行更新。可参考例3。

注：

* update 语句无法改变列的数据类型。
* 根据分布式表的更新原理，update 操作首先获取数据所在的分区，然后在每个分区内进行数据更新，最后将更新后的分区写回磁盘。因此，DolphinDB
  限制了对跨分区数据进行更新操作。当 update 语句的 set 部分使用聚合函数、序列函数或自定义函数，这些操作不能跨分区执行。然而，当 update
  与 context by 结合使用，且 context by 指定了所有分区列时，set 部分可以使用聚合函数、序列函数或自定义函数。这里
  context by 指定分区列两种情况：一是直接使用原始分区列，二是对分区列使用时间转换函数，此时，分区类型必须是 VALUE 或
  RANGE，且转换后的时间精度必须和分区方案中指定的时间列类型相同。可参考下面例2。

## 语法

```
update
   table_name
   set col1=X1, [col2=X2,...]
   [from table_joiner(table_names)]
   [where condition(s)]
   [context by col_name(s)]
```

## 例子

*例 1：更新内存表*

```
sym = `C`MS`MS`MS`IBM`IBM`C`C`C$SYMBOL
price= 49.6 29.46 29.52 30.02 174.97 175.23 50.76 50.32 51.29
qty = 2200 1900 2100 3200 6800 5400 1300 2500 8800
timestamp = [09:34:07,09:36:42,09:36:51,09:36:59,09:32:47,09:35:26,09:34:16,09:34:26,09:38:12]
t1 = table(timestamp, sym, qty, price);

t1;
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:34:07 | C | 2200 | 49.6 |
| 09:36:42 | MS | 1900 | 29.46 |
| 09:36:51 | MS | 2100 | 29.52 |
| 09:36:59 | MS | 3200 | 30.02 |
| 09:32:47 | IBM | 6800 | 174.97 |
| 09:35:26 | IBM | 5400 | 175.23 |
| 09:34:16 | C | 1300 | 50.76 |
| 09:34:26 | C | 2500 | 50.32 |
| 09:38:12 | C | 8800 | 51.29 |

使用 update 语句创建新的列，该列的值为空。

```
update t1 set vol=long();
t1;
```

| timestamp | sym | qty | price | vol |
| --- | --- | --- | --- | --- |
| 09:34:07 | C | 2200 | 49.6 |  |
| 09:36:42 | MS | 1900 | 29.46 |  |
| 09:36:51 | MS | 2100 | 29.52 |  |
| 09:36:59 | MS | 3200 | 30.02 |  |
| 09:32:47 | IBM | 6800 | 174.97 |  |
| 09:35:26 | IBM | 5400 | 175.23 |  |
| 09:34:16 | C | 1300 | 50.76 |  |
| 09:34:26 | C | 2500 | 50.32 |  |
| 09:38:12 | C | 8800 | 51.29 |  |

```
t1.drop!(`vol);
// 将 t1 还原到初始状态
```

更新 trades 表，将股票符号为 C 的记录的 price 列加 $0.5 以及 qty 列减 50。

```
update t1 set price=price+0.5, qty=qty-50 where sym=`C;
t1;
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:34:07 | C | 2150 | 50.1 |
| 09:36:42 | MS | 1900 | 29.46 |
| 09:36:51 | MS | 2100 | 29.52 |
| 09:36:59 | MS | 3200 | 30.02 |
| 09:32:47 | IBM | 6800 | 174.97 |
| 09:35:26 | IBM | 5400 | 175.23 |
| 09:34:16 | C | 1250 | 51.26 |
| 09:34:26 | C | 2450 | 50.82 |
| 09:38:12 | C | 8750 | 51.79 |

```
update t1 set price=price-0.5, qty=qty+50 where sym=`C;
// 将 t1 还原到初始状态
```

使用 [contextBy](contextBy.html) 更新一张表。context by
可以用来做分组调整，而 contextby 不可。下例首先使用 context by 计算每只股票的平均价格，然后将每个记录的原始价格减去平均价格。

```
update t1 set price=price-avg(price) context by sym;
t1;
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:34:07 | C | 2150 | -0.8925 |
| 09:36:42 | MS | 1900 | -0.206667 |
| 09:36:51 | MS | 2100 | -0.146667 |
| 09:36:59 | MS | 3200 | 0.353333 |
| 09:32:47 | IBM | 6800 | -0.13 |
| 09:35:26 | IBM | 5400 | 0.13 |
| 09:34:16 | C | 1250 | 0.2675 |
| 09:34:26 | C | 2450 | -0.1725 |
| 09:38:12 | C | 8750 | 0.7975 |

使用表连接来更新表。

```
item = table(1..10 as id, 10+rand(100,10) as qty, 1.0+rand(10.0,10) as price)
promotion = table(1..10 as id, rand(0b 1b, 10) as flag, 0.5+rand(0.4,10) as discount);
item;
```

| id | qty | price |
| --- | --- | --- |
| 1 | 23 | 7.839664 |
| 2 | 44 | 7.635988 |
| 3 | 76 | 5.378054 |
| 4 | 91 | 8.078173 |
| 5 | 11 | 10.316152 |
| 6 | 58 | 9.510634 |
| 7 | 90 | 1.643082 |
| 8 | 68 | 5.787797 |
| 9 | 52 | 7.53352 |
| 10 | 62 | 6.222249 |

```
promotion;
```

| id | flag | discount |
| --- | --- | --- |
| 1 | 0 | 0.650346 |
| 2 | 0 | 0.697081 |
| 3 | 0 | 0.774207 |
| 4 | 1 | 0.819562 |
| 5 | 0 | 0.710393 |
| 6 | 0 | 0.728223 |
| 7 | 1 | 0.602512 |
| 8 | 0 | 0.71226 |
| 9 | 1 | 0.606631 |
| 10 | 0 | 0.765697 |

```
update item set price = price*discount from ej(item, promotion, `id) where flag=1;
item;
```

| id | qty | price |
| --- | --- | --- |
| 1 | 23 | 7.839664 |
| 2 | 44 | 7.635988 |
| 3 | 76 | 5.378054 |
| 4 | 91 | 6.620566 |
| 5 | 11 | 10.316152 |
| 6 | 58 | 9.510634 |
| 7 | 90 | 0.989976 |
| 8 | 68 | 5.787797 |
| 9 | 52 | 4.570069 |
| 10 | 62 | 6.222249 |

*例 2. 更新分布式表*

```
login(`admin, `123456)
n=1000000
ID=rand(10, n)
x=rand(1.0, n)
t=table(ID, x)
db=database("dfs://rangedb123", RANGE,  0 5 10)
pt=db.createPartitionedTable(t, `pt, `ID)
pt.append!(t)
```

```
pt=loadTable("dfs://rangedb123", `pt)
select avg(x) from pt;

0.4999

update pt set x=x+1;

pt=loadTable("dfs://rangedb123", `pt)
select avg(x) from pt;

//output: 1.4999
```

```
//不允许使用序列函数对跨分区数据进行更新，因此会报错。
update pt set x=prev(x)

// update pt set x = prev(x) => Aggregate or order-sensitive functions are not allowed without context by clause when updating a partitioned table.

update pt set x=prev(x) context by ID
//搭配 context by 将数据更新限制在分区内时，可以正确执行。
select TOP 10* from pt order by ID

/*
ID	x
0
0	1.4483
0	1.6277
0	1.7735
0	1.4349
*/
```

*例3 在 context by 子句中使用 csort, having 进行更新*

```
login("admin", "123456")
dbName = "dfs://time_comparison"
if(existsDatabase(dbName))
	dropDatabase(dbName)

db = database(dbName, VALUE, [2019.12M,2020.01M,2020.02M,2020.03M,2021.01M,2021.02M,2021.03M,2021.12M,2022.01M],engine="TSDB")
n = 100
t = table(n:n,[`time,`id,`value],[MONTH,INT,DOUBLE])
t[`time] = take([2019.12M,2020.01M,2020.02M,2020.03M,2021.01M,2021.02M,2021.03M,2021.12M,2022.01M],n)
t[`id] = take(1..10,n)
t[`value] = rand(100.0,n)
pt = db.createPartitionedTable(t, `pt, `time, sortColumns=`time).append!(t)
pnodeRun(flushIotCache)

update pt set value = 1
select * from pt where time = 2019.12M order by time, id
```

此时返回初始 pt：

| time | id | value |
| --- | --- | --- |
| 2019.12M | 1 | 1 |
| 2019.12M | 1 | 1 |
| 2019.12M | 2 | 1 |
| 2019.12M | 3 | 1 |
| 2019.12M | 4 | 1 |
| 2019.12M | 5 | 1 |
| 2019.12M | 6 | 1 |
| 2019.12M | 7 | 1 |
| 2019.12M | 8 | 1 |
| 2019.12M | 9 | 1 |
| 2019.12M | 10 | 1 |
| 2019.12M | 10 | 1 |

不使用 csort 进行更新：

```
update pt set value = cumsum(value) context by time;
select * from pt where time = 2019.12M order by time, id
```

返回：

| time | id | value |
| --- | --- | --- |
| 2019.12M | 1 | 1 |
| 2019.12M | 1 | 11 |
| 2019.12M | 2 | 10 |
| 2019.12M | 3 | 9 |
| 2019.12M | 4 | 8 |
| 2019.12M | 5 | 7 |
| 2019.12M | 6 | 6 |
| 2019.12M | 7 | 5 |
| 2019.12M | 8 | 4 |
| 2019.12M | 9 | 3 |
| 2019.12M | 10 | 2 |
| 2019.12M | 10 | 12 |

将 pt 恢复至初始，使用 csort 进行更新：

```
update pt set value = 1
update pt set value = cumsum(value) context by time csort id;
select * from pt where time = 2019.12M order by time, id
```

返回：

| time | id | value |
| --- | --- | --- |
| 2019.12M | 1 | 1 |
| 2019.12M | 1 | 2 |
| 2019.12M | 2 | 3 |
| 2019.12M | 3 | 4 |
| 2019.12M | 4 | 5 |
| 2019.12M | 5 | 6 |
| 2019.12M | 6 | 7 |
| 2019.12M | 7 | 8 |
| 2019.12M | 8 | 9 |
| 2019.12M | 9 | 10 |
| 2019.12M | 10 | 11 |
| 2019.12M | 10 | 12 |

csort 支持升序（asc）或降序（desc）语法。以下将 pt 恢复至初始进行示例：

```
update pt set value = 1
update pt set value = cumsum(value) context by time csort id desc, value asc;
select * from pt where time = 2019.12M order by time, id
```

返回：

| time | id | value |
| --- | --- | --- |
| 2019.12M | 1 | 11 |
| 2019.12M | 1 | 12 |
| 2019.12M | 2 | 10 |
| 2019.12M | 3 | 9 |
| 2019.12M | 4 | 8 |
| 2019.12M | 5 | 7 |
| 2019.12M | 6 | 6 |
| 2019.12M | 7 | 5 |
| 2019.12M | 8 | 4 |
| 2019.12M | 9 | 3 |
| 2019.12M | 10 | 1 |
| 2019.12M | 10 | 2 |

将 pt 恢复至初始，使用 having 指定部分更新，若满足 having 条件则进行更新：

```
update pt set value = 1
update pt set value = cumsum(value) context by time having sum(id) > 60
select * from pt where time = 2019.12M order by time, id
```

返回：

| time | id | value |
| --- | --- | --- |
| 2019.12M | 1 | 1 |
| 2019.12M | 1 | 11 |
| 2019.12M | 2 | 10 |
| 2019.12M | 3 | 9 |
| 2019.12M | 4 | 8 |
| 2019.12M | 5 | 7 |
| 2019.12M | 6 | 6 |
| 2019.12M | 7 | 5 |
| 2019.12M | 8 | 4 |
| 2019.12M | 9 | 3 |
| 2019.12M | 10 | 2 |
| 2019.12M | 10 | 12 |

将 pt 恢复至初始，同时使用 csort 和 having 进行更新：

```
update pt set value = 1
update pt set value = cumsum(value) context by time csort id having sum(id) > 60;
select * from pt where time = 2019.12M order by time, id
```

返回：

| time | id | value |
| --- | --- | --- |
| 2019.12M | 1 | 1 |
| 2019.12M | 1 | 2 |
| 2019.12M | 2 | 3 |
| 2019.12M | 3 | 4 |
| 2019.12M | 4 | 5 |
| 2019.12M | 5 | 6 |
| 2019.12M | 6 | 7 |
| 2019.12M | 7 | 8 |
| 2019.12M | 8 | 9 |
| 2019.12M | 9 | 10 |
| 2019.12M | 10 | 11 |
| 2019.12M | 10 | 12 |

having 支持使用非聚合函数，也支持混用非聚合函数与聚合函数。

以下将 pt 恢复至初始，having 使用非聚合函数：

```
update pt set value = 1
update pt set value = cumsum(value) context by time csort id having denseRank(id) > 3
select * from pt where time = 2019.12M order by time, id
```

返回：

| time | id | value |
| --- | --- | --- |
| 2019.12M | 1 | 1 |
| 2019.12M | 1 | 1 |
| 2019.12M | 2 | 1 |
| 2019.12M | 3 | 1 |
| 2019.12M | 4 | 1 |
| 2019.12M | 5 | 6 |
| 2019.12M | 6 | 7 |
| 2019.12M | 7 | 8 |
| 2019.12M | 8 | 9 |
| 2019.12M | 9 | 10 |
| 2019.12M | 10 | 11 |
| 2019.12M | 10 | 12 |

以下将 pt 恢复至初始，having 混用非聚合函数与聚合函数：

```
update pt set value = 1
update pt set value = cumsum(value) context by time csort id having denseRank(id) > 3 and sum(id) > 10000
select * from pt where time = 2019.12M order by time, id
```

返回：

| time | id | value |
| --- | --- | --- |
| 2019.12M | 1 | 1 |
| 2019.12M | 1 | 1 |
| 2019.12M | 2 | 1 |
| 2019.12M | 3 | 1 |
| 2019.12M | 4 | 1 |
| 2019.12M | 5 | 1 |
| 2019.12M | 6 | 1 |
| 2019.12M | 7 | 1 |
| 2019.12M | 8 | 1 |
| 2019.12M | 9 | 1 |
| 2019.12M | 10 | 1 |
| 2019.12M | 10 | 1 |

*例 4. 使用向量更新 DFS 表的数组向量列*

通过以下脚本创建一个某一列为数组向量的分布式分区表

```
dbName = "dfs://updateArrayVector"
db = database(dbName,VALUE,2024.01.01..2024.01.03, engine='TSDB')
a = arrayVector(2 4 6 8 10 12, [1, 1, 1, 2, 1, 3, 1, 1, 1, 2, 1, 3])
date = take(2024.01.03 2024.01.02 2024.01.01, 6)
sym = take(`a`b`c, 6)
t = table(a as a, sym as sym, date as date)
pt=createPartitionedTable(db,t,`pt,partitionColumns=`date, sortColumns=`date)
pt.append!(t)
select * from pt
```

| a | sym | date |
| --- | --- | --- |
| [1, 3] | c | 2024.01.01 |
| [1, 3] | c | 2024.01.01 |
| [1, 2] | b | 2024.01.02 |
| [1, 2] | b | 2024.01.02 |
| [1, 1] | a | 2024.01.03 |
| [1, 1] | a | 2024.01.03 |

更新数据

```
update pt set a = [2,2,3] where date = 2024.01.01
select * from pt where date = 2024.01.01
```

| a | sym | date |
| --- | --- | --- |
| [2, 2, 3] | c | 2024.01.01 |
| [2, 2, 3] | c | 2024.01.01 |

*例 5. 使用数组向量更新 DFS 表的数组向量列*

更新 例4 的分布式表，此时应确保数组向量的长度与满足条件的行数相等：

```
update pt set a=array(INT[], 0).append!([1 2 3, 4 5]) where date = 2024.01.02
select * from pt where date = 2024.01.02
```

| a | sym | date |
| --- | --- | --- |
| [1, 2, 3] | b | 2024.01.02 |
| [4, 5] | b | 2024.01.02 |

例 6. 自 2.00.15 版本起，支持通过 update 语句向内存表中添加 ANY 类型的列。本例向例 1 中的表 t1 添加一个 ANY 类型的列
info。

```
update t1 set info = [1, 2 2, 2 2, 2 2, 3 3, 3 3, 1, 1, 1]
select * from t1
```

| timestamp | sym | qty | price | info |
| --- | --- | --- | --- | --- |
| 09:34:07 | C | 2,200 | 49.6 | 1 |
| 09:36:42 | MS | 1,900 | 29.46 | [2,2] |
| 09:36:51 | MS | 2,100 | 29.52 | [2,2] |
| 09:36:59 | MS | 3,200 | 30.02 | [2,2] |
| 09:32:47 | IBM | 6,800 | 174.97 | [3,3] |
| 09:35:26 | IBM | 5,400 | 175.23 | [4,4] |
| 09:34:16 | C | 1,300 | 50.76 | 1 |
| 09:34:26 | C | 2,500 | 50.32 | 1 |
| 09:38:12 | C | 8,800 | 51.29 | 1 |

