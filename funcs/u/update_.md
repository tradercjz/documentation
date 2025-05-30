# update!

## 语法

`update!(table, colNames, newValues, [filter])`

## 参数

**table** 是 DolphinDB 中 Table 类型的表。它可以是分区的内存表。

**colNames** 是一个字符串标量/向量，表示要更新的列。

**newValues** 是对指定列的操作的元代码。元代码是对象或表达式，它们包含在<>中。详情请参考元编程。

**filter** 是表示过滤条件的元代码。

## 详情

就地更新表中的列。如果 *colNames* 中的某列不存在，将会创建新列。如果指定了过滤条件，只有符合过滤条件的记录行会被更新。

如果 *table* 是分区表并且启用了并行处理功能（即配置参数 *localExcutors* >
0），那么该操作是并行操作。

## 例子

```
n=20000000
workDir = "C:/DolphinDB/Data"
if(!exists(workDir)) mkdir(workDir)
trades=table(rand(`IBM`MSFT`GM`C`YHOO`GOOG,n) as sym, 2000.01.01+rand(365,n) as date, 10.0+rand(2.0,n) as price, rand(1000,n) as qty)
trades.saveText(workDir + "/trades.txt");

trades = ploadText(workDir + "/trades.txt")
select top 10 * from trades;
```

| sym | date | price | qty |
| --- | --- | --- | --- |
| MSFT | 2000.10.09 | 10.123936 | 569 |
| IBM | 2000.09.22 | 10.825785 | 834 |
| MSFT | 2000.09.13 | 10.467937 | 418 |
| IBM | 2000.08.06 | 10.159152 | 252 |
| IBM | 2000.09.01 | 10.614444 | 400 |
| MSFT | 2000.05.03 | 10.40847 | 253 |
| MSFT | 2000.02.20 | 11.470027 | 431 |
| YHOO | 2000.11.09 | 11.570013 | 518 |
| GOOG | 2000.03.02 | 10.206973 | 630 |
| C | 2000.07.09 | 10.477621 | 287 |

```
trades.update!(`qty, <qty+10>)
select top 10 * from trades;
```

| sym | date | price | qty |
| --- | --- | --- | --- |
| MSFT | 2000.10.09 | 10.123936 | 579 |
| IBM | 2000.09.22 | 10.825785 | 844 |
| MSFT | 2000.09.13 | 10.467937 | 428 |
| IBM | 2000.08.06 | 10.159152 | 262 |
| IBM | 2000.09.01 | 10.614444 | 410 |
| MSFT | 2000.05.03 | 10.40847 | 263 |
| MSFT | 2000.02.20 | 11.470027 | 441 |
| YHOO | 2000.11.09 | 11.570013 | 528 |
| GOOG | 2000.03.02 | 10.206973 | 640 |
| C | 2000.07.09 | 10.477621 | 297 |

```
trades.update!(`qty`price, <[qty*2, price/2]>)
select top 10 * from trades;
```

| sym | date | price | qty |
| --- | --- | --- | --- |
| MSFT | 2000.10.09 | 5.061968 | 1158 |
| IBM | 2000.09.22 | 5.412893 | 1688 |
| MSFT | 2000.09.13 | 5.233969 | 856 |
| IBM | 2000.08.06 | 5.079576 | 524 |
| IBM | 2000.09.01 | 5.307222 | 820 |
| MSFT | 2000.05.03 | 5.204235 | 526 |
| MSFT | 2000.02.20 | 5.735014 | 882 |
| YHOO | 2000.11.09 | 5.785007 | 1056 |
| GOOG | 2000.03.02 | 5.103487 | 1280 |
| C | 2000.07.09 | 5.238811 | 594 |

```
trades.update!(`qty`price, <[qty*2, price/2]>, <(sym in `IBM`MSFT`GM`GOOG) and date>=2000.07.01>)
select top 10 * from trades;
```

| sym | date | price | qty |
| --- | --- | --- | --- |
| MSFT | 2000.10.09 | 2.530984 | 2316 |
| IBM | 2000.09.22 | 2.706446 | 3376 |
| MSFT | 2000.09.13 | 2.616984 | 1712 |
| IBM | 2000.08.06 | 2.539788 | 1048 |
| IBM | 2000.09.01 | 2.653611 | 1640 |
| MSFT | 2000.05.03 | 5.204235 | 526 |
| MSFT | 2000.02.20 | 5.735014 | 882 |
| YHOO | 2000.11.09 | 5.785007 | 1056 |
| GOOG | 2000.03.02 | 5.103487 | 1280 |
| C | 2000.07.09 | 5.238811 | 594 |

