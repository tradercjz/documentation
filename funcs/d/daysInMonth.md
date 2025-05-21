# daysInMonth

## 语法

`daysInMonth(X)`

## 参数

**X** 可以是 DATE, DATEHOUR, DATETIME, TIMESTAMP 或 NANOTIMESTAMP
类型的标量或向量。

## 详情

返回 *X* 所在月份的天数。

## 例子

```
daysInMonth(2012.06.12T12:30:00);
// output
30

daysInMonth([2012.02.01,2013.12.05]);
// output
[29,31]
```

