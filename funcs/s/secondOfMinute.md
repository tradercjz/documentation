# secondOfMinute

## 语法

`secondOfMinute(X)`

## 参数

**X** 可以是 DATE, DATEHOUR, DATETIME, TIMESTAMP 或 NANOTIMESTAMP
类型的标量或向量。

## 详情

返回 *X* 中的秒数。

## 例子

```
secondOfMinute(12:32:00);
// output
0

secondOfMinute([2012.06.12T12:30:00,2012.10.28T12:35:00,2013.01.06T12:36:47,2013.04.06T08:02:14]);
// output
[0,0,47,14]
```

相关函数：[dayOfYear](../d/dayOfYear.html), [dayOfMonth](../d/dayOfMonth.html), [quarterOfYear](../q/quarterOfYear.html), [monthOfYear](../m/monthOfYear.html), [weekOfYear](../w/weekOfYear.html), [hourOfDay](../h/hourOfDay.html), [minuteOfHour](../m/minuteOfHour.html), [millisecond](../m/millisecond.html), [microsecond](../m/microsecond.html), [nanosecond](../n/nanosecond.html)

