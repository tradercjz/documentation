# monthBegin

## 语法

`monthBegin(X, [offset], [n=1])`

别名：`monthStart`

## 参数

**X** 可以是 DATE, DATEHOUR, DATETIME, TIMESTAMP 或 NANOTIMESTAMP 类型的标量、向量或表。

**offset** 是与 *X* 类型相同的标量，并且它必须小于等于 *X*
中的最小值。它是一个可选参数。如果没有指定，*offset* 默认为 *X* 中的最小值。

**n** 是一个正整数。它是一个可选参数，默认值为1。

## 详情

返回 *X* 所在月份的第一天。

如果指定了 *offset*，表示从 *offset* 开始，结果每隔 *n* 月更新一次。注意，只有当 *n* > 1
时，*offset* 才会生效。

## 例子

```
monthBegin(2016.12.06);
// output
2016.12.01

date=2016.04.12 2016.04.25 2016.05.12 2016.06.28 2016.07.10 2016.07.18 2016.08.02 2016.08.16 2016.09.26 2016.09.30
time = [09:34:07,09:36:42,09:36:51,09:36:59,09:32:47,09:35:26,09:34:16,09:34:26,09:38:12,09:38:13]
sym = take(`MSFT,10)
price= 49.6 29.46 29.52 30.02 174.97 175.23 50.76 50.32 51.29 52.38
qty = 2200 1900 2100 3200 6800 5400 1300 2500 8800 4500
t1 = table(date, time, sym, qty, price);

select avg(price),sum(qty) from t1 group by monthBegin(date,2016.01.01,2);
```

| monthBegin\_date | avg\_price | sum\_qty |
| --- | --- | --- |
| 2016.03.01 | 39.53 | 4100 |
| 2016.05.01 | 29.77 | 5300 |
| 2016.07.01 | 112.82 | 16000 |
| 2016.09.01 | 51.835 | 13300 |

相关函数：[monthEnd](monthEnd.md), [businessMonthBegin](../b/businessMonthBegin.md),
[businessMonthEnd](../b/businessMonthEnd.md),
[semiMonthBegin](../s/semiMonthBegin.md),
[semiMonthEnd](../s/semiMonthEnd.md)

