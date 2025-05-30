# businessMonthBegin

## 语法

`businessMonthBegin(X, [offset], [n=1])`

## 参数

**X** 可以是 DATE, DATEHOUR, DATETIME, TIMESTAMP 或 NANOTIMESTAMP 类型的标量或向量。

**offset** 是与 *X* 类型相同的标量，并且它必须小于等于 *X*
中的最小值。它是一个可选参数。如果没有指定，*offset* 默认为 *X* 中的最小值。

**n** 是一个正整数。它是一个可选参数，默认值为1。

## 详情

返回 *X* 所在月份的第一个工作日（周一到周五）

如果指定了*offset*，表示从 *offset* 开始，结果每隔 *n* 月更新一次。注意，只有当
*n*>1时，*offset* 才会生效。

## 例子

```
businessMonthBegin(2018.09.12);
// output
2018.09.03

businessMonthBegin(2018.09.12, 2018.07.12, 3);
// output
2018.07.02

date=2016.04.12+(1..10)*30
time = take(09:30:00, 10)
sym = take(`MSFT,10)
price= 49.6 29.46 29.52 30.02 174.97 175.23 50.76 50.32 51.29 52.38
qty = 2200 1900 2100 3200 6800 5400 1300 2500 8800 4500
t1 = table(date, time, sym, qty, price);
t1;
```

| date | time | sym | qty | price |
| --- | --- | --- | --- | --- |
| 2016.05.12 | 09:30:00 | MSFT | 2200 | 49.6 |
| 2016.06.11 | 09:30:00 | MSFT | 1900 | 29.46 |
| 2016.07.11 | 09:30:00 | MSFT | 2100 | 29.52 |
| 2016.08.10 | 09:30:00 | MSFT | 3200 | 30.02 |
| 2016.09.09 | 09:30:00 | MSFT | 6800 | 174.97 |
| 2016.10.09 | 09:30:00 | MSFT | 5400 | 175.23 |
| 2016.11.08 | 09:30:00 | MSFT | 1300 | 50.76 |
| 2016.12.08 | 09:30:00 | MSFT | 2500 | 50.32 |
| 2017.01.07 | 09:30:00 | MSFT | 8800 | 51.29 |
| 2017.02.06 | 09:30:00 | MSFT | 4500 | 52.38 |

```
select avg(price),sum(qty) from t1 group by businessMonthBegin(date,2016.01.01,2);
```

| businessMonthBegin\_date | avg\_price | sum\_qty |
| --- | --- | --- |
| 2016.05.02 | 39.53 | 4100 |
| 2016.07.01 | 29.77 | 5300 |
| 2016.09.01 | 175.1 | 12200 |
| 2016.11.01 | 50.54 | 3800 |
| 2017.01.02 | 51.835 | 13300 |

相关函数：[businessMonthEnd](businessMonthEnd.md),
[monthBegin](../m/monthBegin.md), [monthEnd](../m/monthEnd.md), [semiMonthBegin](../s/semiMonthBegin.md), [semiMonthEnd](../s/semiMonthEnd.md)

