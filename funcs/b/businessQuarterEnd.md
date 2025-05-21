# businessQuarterEnd

## 语法

`businessQuarterEnd(X, [endingMonth=12], [offset],
[n=1])`

## 参数

**X** 可以是 DATE, DATETIME, DATEHOUR, TIMESTAMP 或 NANOTIMESTAMP
类型的标量或向量。

**startingMonth** 是1到12之间的整数，表示一年的结束月份。默认值是12。

**offset** 是与 **X** 类型相同的标量，并且它必须小于等于 *X*
中的最小值。它是一个可选参数。如果没有指定，*offset* 默认为 *X* 中的最小值。

**n** 是一个正整数。它是一个可选参数，默认值为1。

## 详情

返回 *X* 所在季度的最后一个工作日（周一到周五）。

如果指定了*offset*，表示从 *offset* 开始，结果每隔 *n*
个季度更新一次。注意，只有当 *n*>1 时，offset 才会生效。

## 例子

```
businessQuarterEnd(2012.04.12);
// output
2012.06.30

businessQuarterEnd(2012.04.12, 2);
// output
2012.05.31

businessQuarterEnd(2012.04.12, 8, 2011.08.01, 3);
// output
2012.05.31

date=2011.04.25+(1..10)*90
time = take(09:30:00, 10)
sym = take(`MSFT,10)
price= 49.6 29.46 29.52 30.02 174.97 175.23 50.76 50.32 51.29 52.38
qty = 2200 1900 2100 3200 6800 5400 1300 2500 8800 4500
t1 = table(date, time, sym, qty, price);

t1;
```

| date | time | sym | qty | price |
| --- | --- | --- | --- | --- |
| 2011.07.24 | 09:30:00 | MSFT | 2200 | 49.6 |
| 2011.10.22 | 09:30:00 | MSFT | 1900 | 29.46 |
| 2012.01.20 | 09:30:00 | MSFT | 2100 | 29.52 |
| 2012.04.19 | 09:30:00 | MSFT | 3200 | 30.02 |
| 2012.07.18 | 09:30:00 | MSFT | 6800 | 174.97 |
| 2012.10.16 | 09:30:00 | MSFT | 5400 | 175.23 |
| 2013.01.14 | 09:30:00 | MSFT | 1300 | 50.76 |
| 2013.04.14 | 09:30:00 | MSFT | 2500 | 50.32 |
| 2013.07.13 | 09:30:00 | MSFT | 8800 | 51.29 |
| 2013.10.11 | 09:30:00 | MSFT | 4500 | 52.38 |

```
select avg(price),sum(qty) from t1 group by businessQuarterEnd(date, , 2010.06.01, 2)
```

| businessQuarterEnd\_date | avg\_price | sum\_qty |
| --- | --- | --- |
| 2011.12.30 | 39.53 | 4100 |
| 2012.06.29 | 29.77 | 5300 |
| 2012.12.31 | 175.1 | 12200 |
| 2013.06.28 | 50.54 | 3800 |
| 2013.12.31 | 51.835 | 13300 |

相关函数：[businessQuarterBegin](businessQuarterBegin.html), [quarterBegin](../q/quarterBegin.html), [quarterEnd](../q/quarterEnd.html)

