# where

where 子句用于在查询语句中指定选择条件。

## 详情

若 SQL 语句中包含 where 子句，则查询数据的逻辑如下：

1. 先读取 where 语句指定的列数据，然后按条件对其过滤；
2. 再读取的结果所对应的其他列数据。

因此，为提高查询效率，当 where 子句过滤出的数据占总数据的比例较大时，可以通过指定 [HINT\_PRELOAD] 预先加载所有数据到内存再进行过滤。

## 例子

在下例中，脚本创建一个包含证券交易信息的表，并显示该表的内容。

其中定义了四个变量：

sym: 代表证券代码，包括多个证券的代码。

price: 代表证券的价格，包括每个证券对应的价格。

qty: 代表证券的数量，包括每个证券对应的数量。

timestamp: 代表时间戳，包括了每个交易的时间。

接下来，脚本创建了一个名为 t1 的表，该表包含了 timestamp、sym、qty 和 price 列。最后，脚本输出了 t1 表的内容。

```
sym = `C`MS`MS`MS`IBM`IBM`C`C`C$SYMBOL
price= 49.6 29.46 29.52 30.02 174.97 175.23 50.76 50.32 51.29
qty = 2200 1900 2100 3200 6800 5400 1300 2500 8800
timestamp = [09:34:07,09:36:42,09:36:51,09:36:59,09:32:47,09:35:26,09:34:16,09:34:26,09:38:12]
t1 = table(timestamp, sym, qty, price);
t1;
```

得到：

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

### where 子句包含一个条件时

执行以下查询语句：

```
select * from t1 where sym=`IBM;
```

得到：

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:32:47 | IBM | 6800 | 174.97 |
| 09:35:26 | IBM | 5400 | 175.23 |

```
select * from t1 where timestamp.minute()>=09:36m;
```

得到：

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:36:42 | MS | 1900 | 29.46 |
| 09:36:51 | MS | 2100 | 29.52 |
| 09:36:59 | MS | 3200 | 30.02 |
| 09:38:12 | C | 8800 | 51.29 |

注： 在 where 子句中，"==" 等于
"="。例如：

```
select * from t1 where sym==`IBM;
```

得到：

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:32:47 | IBM | 6800 | 174.97 |
| 09:35:26 | IBM | 5400 | 175.23 |

### where 子句包含多个条件时

执行以下查询语句：

```
select * from t1 where sym=`IBM and qty>=2000 or timestamp>09:37:00;
```

得到：

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:32:47 | IBM | 6800 | 174.97 |
| 09:35:26 | IBM | 5400 | 175.23 |
| 09:38:12 | C | 8800 | 51.29 |

若多条件必须同时满足才能成立，则用 "and", "&&" 或 "," 连接；若只满足一个条件即可，则用
“or” 或 “||” 连接。

```
select * from t1 where qty>=2000, timestamp.minute()>=09:36m;
```

得到：

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:36:51 | MS | 2100 | 29.52 |
| 09:36:59 | MS | 3200 | 30.02 |
| 09:38:12 | C | 8800 | 51.29 |

```
select * from t1 where qty>=2000 and timestamp.minute()>=09:36m;
```

得到：

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:36:51 | MS | 2100 | 29.52 |
| 09:36:59 | MS | 3200 | 30.02 |
| 09:38:12 | C | 8800 | 51.29 |

```
select * from t1 where qty>=2000 && timestamp.minute()>=09:36m;
```

得到：

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:36:51 | MS | 2100 | 29.52 |
| 09:36:59 | MS | 3200 | 30.02 |
| 09:38:12 | C | 8800 | 51.29 |

### where 条件中包含函数时

下面的例子中，我们将价格高于平均价格的记录选择出来。这里对表中所有记录使用了函数avg。

```
select * from t1 where price>avg(price);
```

得到：

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:32:47 | IBM | 6800 | 174.97 |
| 09:35:26 | IBM | 5400 | 175.23 |

要计算每个股票的平均价格，可以使用 [c/contextby](../../funcs/ho_funcs/contextby.html)。下面的例子查询每个股票的价格大于平均价格的记录。

```
select * from t1 where price>contextby(avg, price, sym) order by sym, price;
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:34:16 | C | 1300 | 50.76 |
| 09:38:12 | C | 8800 | 51.29 |
| 09:35:26 | IBM | 5400 | 175.23 |
| 09:36:59 | MS | 3200 | 30.02 |

要随机抽取分区作为样本，只需在where子句中使用 [sample](sample.html) 函数即可。

```
n=1000000
ID=rand(50, n)
x=rand(1.0, n)
t=table(ID, x)
db=database("dfs://rangedb1", RANGE,  0 10 20 30 40 50)
pt = db.createPartitionedTable(t, `pt, `ID)
pt.append!(t)
pt=loadTable(db,`pt);
```

pt 有 5 个分区，随机抽取两个分区的数据作为样本，可以使用下面的语句：

```
x = select * from pt where sample(ID, 0.4);
x = select * from pt where sample(ID, 2);
```

### where 条件中包含 SQL 子句时

运行以下脚本：

```
t1 = table(`APPL`AMZN`IBM`IBM`AAPL`AMZN as sym, 2022.01.01 + 1..6 as date);
t2 = table(`APPL`AMZN`IBM`IBM`AAPL`AMZN as sym, 1.8 2.3 3.7 3.1 4.2 2.8 as price)
select count(*) from t1 where sym in select sym from t2 where price > 3
```

得到：3

运行以下脚本：

```
t3 = table(`APPL`AMZN`IBM`IBM`AAPL`AMZN as sym, 1.9 2.1 2.5 2.6 2.7 3.2 as price)
select * from t2 where price > select avg(price) from t3
```

得到：

| sym | price |
| --- | --- |
| IBM | 3.7 |
| IBM | 3.1 |
| AAPL | 4.2 |
| AMZN | 2.8 |

