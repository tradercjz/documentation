# yearBegin

## 语法

`yearBegin(X, [startingMonth=1], [offset],
[n=1])`

## 详情

返回 *X* 所在的以 *startingMonth* 为起始月份的年份的第一天。

如果指定了 *offset*，表示从 *offset* 开始，结果每隔 *n*
年更新一次。注意，只有当 *n* >1时，*offset* 才会生效。

## 参数

**X** 可以是 DATE, DATETIME, DATEHOUR, TIMESTAMP 或 NANOTIMESTAMP 类型的标量或向量。

**startingMonth** 是1到12之间的整数，表示一年的起始月份。默认值是1。

**offset** 是与 *X* 类型相同的标量，并且它必须小于等于 *X*
中的最小值。它是一个可选参数。如果没有指定，*offset* 默认为 *X* 中的最小值。

**n** 是一个正整数。它是一个可选参数，默认值为1。

## 例子

```
yearBegin(2012.06.12, 10);
// output
2011.10.01

yearBegin(2012.06.12, 4);
// output
2012.04.01

yearBegin(2012.06.12);
// output
2012.01.01

yearBegin(2012.06.12, 1, 2009.04.03, 2);
// output
2011.01.01

date=2011.04.25+(1..10)*365
time = take(09:30:00, 10);
sym = take(`MSFT,10)
price= 49.6 29.46 29.52 30.02 174.97 175.23 50.76 50.32 51.29 52.38
qty = 2200 1900 2100 3200 6800 5400 1300 2500 8800 4500
t1 = table(date, time, sym, qty, price);

t1;
```

| date | time | sym | qty | price |
| --- | --- | --- | --- | --- |
| 2012.04.24 | 09:30:00 | MSFT | 2200 | 49.6 |
| 2013.04.24 | 09:30:00 | MSFT | 1900 | 29.46 |
| 2014.04.24 | 09:30:00 | MSFT | 2100 | 29.52 |
| 2015.04.24 | 09:30:00 | MSFT | 3200 | 30.02 |
| 2016.04.23 | 09:30:00 | MSFT | 6800 | 174.97 |
| 2017.04.23 | 09:30:00 | MSFT | 5400 | 175.23 |
| 2018.04.23 | 09:30:00 | MSFT | 1300 | 50.76 |
| 2019.04.23 | 09:30:00 | MSFT | 2500 | 50.32 |
| 2020.04.22 | 09:30:00 | MSFT | 8800 | 51.29 |
| 2021.04.22 | 09:30:00 | MSFT | 4500 | 52.38 |

```
select avg(price),sum(qty) from t1 group by yearBegin(date, 10, 2010.10.01, 2);
```

| yearBegin\_date | avg\_price | sum\_qty |
| --- | --- | --- |
| 2010.10.01 | 49.6 | 2200 |
| 2012.10.01 | 29.49 | 4000 |
| 2014.10.01 | 102.495 | 10000 |
| 2016.10.01 | 112.995 | 6700 |
| 2018.10.01 | 50.805 | 11300 |
| 2020.10.01 | 52.38 | 4500 |

相关函数：[yearEnd](yearEnd.md), [businessYearBegin](../b/businessYearBegin.md),
[businessYearEnd](../b/businessYearEnd.md)

