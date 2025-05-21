# quarterBegin

## 语法

`quarterBegin(X, [startingMonth=1], [offset],
[n=1])`

## 参数

**X** 可以是 DATE, DATETIME, DATEHOUR, TIMESTAMP 或 NANOTIMESTAMP
类型的标量或向量。

**startingMonth** 是1到12之间的整数，表示一年的起始月份。默认值是1。

**offset** 是与 *X* 类型相同的标量，并且它必须小于等于 *X*
中的最小值。它是一个可选参数。如果没有指定，*offset* 默认为 *X* 中的最小值。

**n** 是一个正整数。它是一个可选参数，默认值为1。

## 详情

返回 *X* 所在季度的第一天。每季度包含的月份由参数 *startingMonth* 决定。

如果指定了 *offset*，表示从 *offset*开始，结果每隔n个季度更新一次。注意，只有当 *n*
>1时，*offset* 才会生效。

## 例子

```
quarterBegin(2012.06.12);
// output
2012.04.01

quarterBegin(2012.06.13 10:10:10.008,5);
// output
2012.05.01

date=2016.01.12 2016.02.25 2016.05.12 2016.06.28 2016.07.10 2016.08.18 2016.09.02 2016.10.16 2016.11.26 2016.12.30
time = [09:34:07,09:36:42,09:36:51,09:36:59,09:32:47,09:35:26,09:34:16,09:34:26,09:38:12,09:38:13]
sym = take(`MSFT,10)
price= 49.6 29.46 29.52 30.02 174.97 175.23 50.76 50.32 51.29 52.38
qty = 2200 1900 2100 3200 6800 5400 1300 2500 8800 4500
t1 = table(date, time, sym, qty, price);

select avg(price),sum(qty) from t1 group by quarterBegin(date,1,2016.01.01,2)
```

| quarterBegin\_date | avg\_price | sum\_qty |
| --- | --- | --- |
| 2016.01.01 | 34.65 | 9400 |
| 2016.07.01 | 92.491667 | 29300 |

相关函数：[quarterEnd](quarterEnd.md), [businessQuarterBegin](../b/businessQuarterBegin.md), [businessQuarterEnd](../b/businessQuarterEnd.md)

