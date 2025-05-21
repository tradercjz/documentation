# hourOfDay

## 语法

`hourOfDay(X)`

## 参数

**X** 可以是 TIME, MINUTE, SECOND, DATETIME, TIMESTAMP, NANOTIME,
NANOTIMESTAMP 类型的标量或向量。

## 详情

返回 *X* 中的小时。

## 例子

```
hourOfDay(00:46:12);
// output
0

hourOfDay([2012.06.12T12:30:00,2012.10.28T17:35:00,2013.01.06T02:36:47,2013.04.06T08:02:14]);
// output
[12,17,2,8]
```

相关函数：[dayOfYear](../d/dayOfYear.md), [dayOfMonth](../d/dayOfMonth.md), [quarterOfYear](../q/quarterOfYear.md), [monthOfYear](../m/monthOfYear.md), [weekOfYear](../w/weekOfYear.md), [minuteOfHour](../m/minuteOfHour.md), [secondOfMinute](../s/secondOfMinute.md), [millisecond](../m/millisecond.md), [microsecond](../m/microsecond.md), [nanosecond](../n/nanosecond.md)

