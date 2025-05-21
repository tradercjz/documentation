# semiMonthEnd

## 语法

`semiMonthEnd(X, [dayOfMonth=15], [offset],
[n=1])`

## 参数

**X** 可以是 DATE, DATEHOUR, DATETIME, TIMESTAMP 或 NANOTIMESTAMP
类型的标量或向量。

**dayOfMonth** 是2到27之间的整数。它是一个可选参数，默认值为15。

**offset** 是与 *X* 类型相同的标量，并且它必须小于等于 *X*
中的最小值。它是一个可选参数。如果没有指定，*offset* 默认为 *X* 中的最小值。

**n** 是一个正整数。它是一个可选参数，默认值为1。

## 详情

返回 *X* 所在半月的最后一天。假设 *X* 为该月的第 d 天：

* 如果d<*dayOfMonth*，那么 *semiMonthBegin* 返回
  *X* 所在月份的上一个月的最后一天。
* 如果d>=*dayOfMonth*，那么 *semiMonthBegin*
  返回X所在月份的第 *dayOfMonth* 天。

如果指定了 *offset* ，表示从 *offset* 开始，结果每隔 *n* 个半月更新一次。注意，只有当 *n>1*
时，*offset* 才会生效。

## 例子

```
semiMonthEnd(2012.06.12);
// output
012.05.31

semiMonthEnd(2012.06.24);
// output
012.06.15

semiMonthEnd(2012.06.15);
// output
012.06.15

semiMonthEnd(2012.06.16, 16);
// output
012.06.16

date=2016.04.07+(1..10)*7
time = take(09:30:00, 10);
sym = take(`MSFT,10)
price= 49.6 29.46 29.52 30.02 174.97 175.23 50.76 50.32 51.29 52.38
qty = 2200 1900 2100 3200 6800 5400 1300 2500 8800 4500
t1 = table(date, time, sym, qty, price);
t1;
```

| date | time | sym | qty | price |
| --- | --- | --- | --- | --- |
| 2016.04.14 | 09:30:00 | MSFT | 2200 | 49.6 |
| 2016.04.21 | 09:30:00 | MSFT | 1900 | 29.46 |
| 2016.04.28 | 09:30:00 | MSFT | 2100 | 29.52 |
| 2016.05.05 | 09:30:00 | MSFT | 3200 | 30.02 |
| 2016.05.12 | 09:30:00 | MSFT | 6800 | 174.97 |
| 2016.05.19 | 09:30:00 | MSFT | 5400 | 175.23 |
| 2016.05.26 | 09:30:00 | MSFT | 1300 | 50.76 |
| 2016.06.02 | 09:30:00 | MSFT | 2500 | 50.32 |
| 2016.06.09 | 09:30:00 | MSFT | 8800 | 51.29 |
| 2016.06.16 | 09:30:00 | MSFT | 4500 | 52.38 |

```
select avg(price),sum(qty) from t1 group by semiMonthEnd(date);
```

| semiMonthEnd\_date | avg\_price | sum\_qty |
| --- | --- | --- |
| 2016.03.31 | 49.6 | 2200 |
| 2016.04.15 | 29.49 | 4000 |
| 2016.04.30 | 102.495 | 10000 |
| 2016.05.15 | 112.995 | 6700 |
| 2016.05.31 | 50.805 | 11300 |
| 2016.06.15 | 52.38 | 4500 |

相关函数：[monthBegin](../m/monthBegin.html), [monthEnd](../m/monthEnd.html), [semiMonthBegin](semiMonthBegin.html)

