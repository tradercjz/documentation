# businessYearEnd

## 语法

`businessYearEnd(X, [endingMonth=12], [offset],
[n=1])`

## 参数

**X** 可以是 DATE, DATETIME, DATEHOUR, TIMESTAMP 或 NANOTIMESTAMP
类型的标量或向量。

**endingMonth** 是1到12之间的整数，表示一年的结束月份。默认值是12。

**offset** 是与 **X** 类型相同的标量，并且它必须小于等于 *X*
中的最小值。它是一个可选参数。如果没有指定，*offset* 默认为 *X* 中的最小值。

**n** 是一个正整数。它是一个可选参数，默认值为1。

## 详情

返回 *X* 所在年份的最后一个工作日（周一到周五）。

如果指定了*offset*，表示从 *offset* 开始，结果每隔 *n* 年更新一次。注意，只有当
*n*>1 时，*offset* 才会生效。

## 例子

```
businessYearEnd(2012.06.12, 3);
// output
2013.03.29

businessYearEnd(2012.06.12, 9);
// output
2012.09.28

businessYearEnd(2012.06.12);
// output
2012.12.31

businessYearEnd(2012.06.12, 12, 2009.04.03, 2);
// output
2013.12.31

date=2011.04.25+(1..10)*365
time = take(09:30:00, 10)
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
select avg(price),sum(qty) from t1 group by businessYearEnd(date, 4, 2010.04.01, 2);
```

| businessYearEnd\_date | avg\_price | sum\_qty |
| --- | --- | --- |
| 2012.04.30 | 49.6 | 2200 |
| 2014.04.30 | 29.49 | 4000 |
| 2016.04.29 | 102.495 | 10000 |
| 2018.04.30 | 112.995 | 6700 |
| 2020.04.30 | 50.805 | 11300 |
| 2022.04.29 | 52.38 | 4500 |

相关函数：[businessYearBegin](businessYearBegin.md),
[yearBegin](../y/yearBegin.md), [yearEnd](../y/yearEnd.md)

