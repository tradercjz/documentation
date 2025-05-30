# asof join

## 语法

```
aj(leftTable, rightTable, matchingCols, [rightMatchingCols])
```

## 参数

* **leftTable** 和 **rightTable** 是连接的表。
* **matchingCols** 是表示连接列的字符串标量或向量。
* **rightMatchingCols** 是表示右表连接列的字符串标量或向量。当 *leftTable和rightTable*
  至少有一个连接列不同时，必须指定 *rightMatchingCols*。返回结果中的连接列与左表的连接列名称相同。

## 详情

asof join 和左连接函数十分相似，但有以下区别：

* 假设最后一个连接列为 time，对于左表中某 time=t 的行：
  + 如果右表中其它连接列都匹配的记录中有 time=t 的记录，则取之（若有多行，则取其中最后一行）；
  + 若没有 time=t 的记录，则取这些记录中在 t 之前的最近时间对应的行（若有多行，则取其中最后一行）。
* 如果只有 1 个连接列，则 aj 函数假定右表已按照连接列排过序。如果有多个连接列，则 aj
  函数假定右表根据除最后一个连接列外的其他连接列定义分组，每个分组根据最后一个连接列排序。右表的其他连接列不需要排序。如果这些条件不符合，处理将与期望值不符。左表不需要排序。

asof join 的最后一个连接列通常为时间类型，也可为整数类型，以及UUID或IPADDR类型。

注：

* 若 *leftTable* 不是分布式表，则其 *rightTable* 也不能是分布式表。
* 若 *leftTable* 和 *rightTable*
  为分区表时，用于分组的连接列（即除了最后一个连接列之外的所有连接列）必须包含全部分区字段。

## 例子

```
t1 = table(2015.01.01+(0 31 59 90 120) as date, 1.2 7.8 4.6 5.1 9.5 as value)
t2 = table(2015.02.01+(0 15 89 89) as date, 1..4 as qty);
t1;
```

返回：

| date | value |
| --- | --- |
| 2015.01.01 | 1.2 |
| 2015.02.01 | 7.8 |
| 2015.03.01 | 4.6 |
| 2015.04.01 | 5.1 |
| 2015.05.01 | 9.5 |

```
t2;
```

返回：

| date | qty |
| --- | --- |
| 2015.02.01 | 1 |
| 2015.02.16 | 2 |
| 2015.05.01 | 3 |
| 2015.05.01 | 4 |

```
select * from lsj(t1, t2, `date);
```

返回：

| date | value | qty |
| --- | --- | --- |
| 2015.01.01 | 1.2 |  |
| 2015.02.01 | 7.8 | 1 |
| 2015.03.01 | 4.6 |  |
| 2015.04.01 | 5.1 |  |
| 2015.05.01 | 9.5 | 3 |

```
select * from aj(t1, t2, `date);
```

返回：

| date | value | t2\_date | qty |
| --- | --- | --- | --- |
| 2015.01.01 | 1.2 |  |  |
| 2015.02.01 | 7.8 | 2015.02.01 | 1 |
| 2015.03.01 | 4.6 | 2015.02.16 | 2 |
| 2015.04.01 | 5.1 | 2015.02.16 | 2 |
| 2015.05.01 | 9.5 | 2015.05.01 | 4 |

```
select * from aj(t1, t2, `date) where t1.date>=2015.03.01;
```

返回：

| date | value | t2\_date | qty |
| --- | --- | --- | --- |
| 2015.03.01 | 4.6 | 2015.02.16 | 2 |
| 2015.04.01 | 5.1 | 2015.02.16 | 2 |
| 2015.05.01 | 9.5 | 2015.05.01 | 4 |

asof 连接的常用场景是在时间字段上作连接，用来获取最新信息。

假设有三张表，全部按照 minute 字段排过序。

```
minute = 09:30m 09:32m 09:33m 09:35m
price = 174.1 175.2 174.8 175.2
t1 = table(minute, price)

minute = 09:30m 09:31m 09:33m 09:34m
price = 29.2 28.9 29.3 30.1
t2 = table(minute, price)

minute =09:30m 09:31m 09:34m 09:36m
price = 51.2 52.4 51.9 52.8
t3 = table(minute, price);

t1;
```

返回：

| minute | price |
| --- | --- |
| 09:30m | 174.1 |
| 09:32m | 175.2 |
| 09:33m | 174.8 |
| 09:35m | 175.2 |

```

t2;
```

返回：

| minute | price |
| --- | --- |
| 09:30m | 29.2 |
| 09:31m | 28.9 |
| 09:33m | 29.3 |
| 09:34m | 30.1 |

```
t3;
```

返回：

| minute | price |
| --- | --- |
| 09:30m | 51.2 |
| 09:31m | 52.4 |
| 09:34m | 51.9 |
| 09:36m | 52.8 |

```
t2 = aj(t2, t3, `minute);
t2;
```

返回：

| minute | price | t3\_minute | t3\_price |
| --- | --- | --- | --- |
| 09:30m | 29.2 | 09:30m | 51.2 |
| 09:31m | 28.9 | 09:31m | 52.4 |
| 09:33m | 29.3 | 09:31m | 52.4 |
| 09:34m | 30.1 | 09:34m | 51.9 |

```
aj(t1, t2, `minute);
```

返回：

| minute | price | t2\_minute | t2\_price | t3\_minute | t3\_price |
| --- | --- | --- | --- | --- | --- |
| 09:30m | 174.1 | 09:30m | 29.2 | 09:30m | 51.2 |
| 09:32m | 175.2 | 09:31m | 28.9 | 09:31m | 52.4 |
| 09:33m | 174.8 | 09:33m | 29.3 | 09:31m | 52.4 |
| 09:35m | 175.2 | 09:34m | 30.1 | 09:34m | 51.9 |

注意，t2 和 t3 在 09:32m 时没有匹配记录，所以最近的 09:31m 时的价格被选中。而 t3 的 09:33m
时的价格，以及 t2 和 t3 在 09:35m
处的价格也使用了最近的前一条记录用来替代缺失的记录。这个功能在需要生成特定时间点的数据时特别有用。比如说，一些信息于每周或者每月更新一次。在设计一个日交易策略时，可以使用那些更新不是很频繁的数据，通过
asof 连接来生成每日数据集。

asof 最后一个连接列为 uuid 类型：

```
t1 = table(2015.01.01 2015.02.01 2015.03.01 2015.04.01 2015.05.01 as date,  uuid(["5d212a78-cc48-e3b1-4235-b4d91473ee81", "5d212a78-cc48-e3b1-4235-b4d91473ee83", "5d212a78-cc48-e3b1-4235-b4d91473ee85", "5d212a78-cc48-e3b1-4235-b4d91473ee87", "5d212a78-cc48-e3b1-4235-b4d91473ee89"]) as uid)
t2 = table(2015.01.15 2015.01.20 2015.01.25 2015.03.01 as date,uuid(["5d212a78-cc48-e3b1-4235-b4d91473ee81", "5d212a78-cc48-e3b1-4235-b4d91473ee83", "5d212a78-cc48-e3b1-4235-b4d91473ee85", "5d212a78-cc48-e3b1-4235-b4d91473ee87"]) as uid)
select * from aj(t1, t2, `uid);
```

返回：

| date | uid | t2\_date | t2\_uid |
| --- | --- | --- | --- |
| 2015.01.01 | 5d212a78-cc48-e3b1-4235-b4d91473ee81 | 2015.01.15 | 5d212a78-cc48-e3b1-4235-b4d91473ee81 |
| 2015.02.01 | 5d212a78-cc48-e3b1-4235-b4d91473ee83 | 2015.01.20 | 5d212a78-cc48-e3b1-4235-b4d91473ee83 |
| 2015.03.01 | 5d212a78-cc48-e3b1-4235-b4d91473ee85 | 2015.01.25 | 5d212a78-cc48-e3b1-4235-b4d91473ee85 |
| 2015.04.01 | 5d212a78-cc48-e3b1-4235-b4d91473ee87 | 2015.03.01 | 5d212a78-cc48-e3b1-4235-b4d91473ee87 |
| 2015.05.01 | 5d212a78-cc48-e3b1-4235-b4d91473ee89 | 2015.03.01 | 5d212a78-cc48-e3b1-4235-b4d91473ee87 |

