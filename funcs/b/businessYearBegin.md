# businessYearBegin

## 语法

`businessYearBegin(X, [startingMonth=1], [offset],
[n=1])`

## 参数

**X** 可以是 DATE, DATETIME, DATEHOUR, TIMESTAMP 或 NANOTIMESTAMP
类型的标量或向量。

**startingMonth** 是1到12之间的整数，表示一年的起始月份。默认值是1。

**offset** 是与 **X** 类型相同的标量，并且它必须小于等于 *X*
中的最小值。它是一个可选参数。如果没有指定，*offset* 默认为 *X* 中的最小值。

**n** 是一个正整数。它是一个可选参数，默认值为1。

## 详情

返回最近一个小于等于 *X* 的年度首个工作日（周一到周五）。

如果指定了*offset*，表示从 *offset* 开始，结果每隔 *n* 年更新一次。注意，只有当
*n*> 1时，*offset* 才会生效。

## 例子

```
businessYearBegin(2012.06.12);
// output
2012.01.02

businessYearBegin(2022.01.01);
// output
2021.01.01

businessYearBegin(2012.06.13 10:10:10.008,5);
// output
2012.05.01

date=2011.10.25 2012.10.25 2013.10.25 2014.10.25 2015.10.25 2016.10.25 2017.10.25 2018.10.25 2019.10.25 2020.10.25
time = [09:34:07,09:36:42,09:36:51,09:36:59,09:32:47,09:35:26,09:34:16,09:34:26,09:38:12,09:38:13]
sym = take(`MSFT,10)
price= 49.6 29.46 29.52 30.02 174.97 175.23 50.76 50.32 51.29 52.38
qty = 2200 1900 2100 3200 6800 5400 1300 2500 8800 4500
t1 = table(date, time, sym, qty, price);

select avg(price),sum(qty) from t1 group by businessYearBegin(date,1,2011.10.01,2)
```

| businessYearBegin\_date | avg\_price | sum\_qty |
| --- | --- | --- |
| 2011.01.03 | 39.53 | 4100 |
| 2013.01.01 | 29.77 | 5300 |
| 2015.01.01 | 175.1 | 12200 |
| 2017.01.02 | 50.54 | 3800 |
| 2019.01.01 | 51.835 | 13300 |

相关函数：[businessYearEnd](businessYearEnd.html), [yearBegin](../y/yearBegin.html), [yearEnd](../y/yearEnd.html)

