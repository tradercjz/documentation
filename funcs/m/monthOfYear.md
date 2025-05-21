# monthOfYear

## 语法

`monthOfYear(X)`

## 参数

**X** 可以是 DATE, MONTH, DATETIME, TIMESTAMP 或 NANOTIMESTAMP 类型的标量、向量或表。

## 详情

返回 *X* 中的月份。

## 例子

```
monthOfYear(2012.07.02);
// output
7

monthOfYear([2012.06.12T12:30:00,2012.10.28T12:35:00,2013.01.06T12:36:47,2013.04.06T08:02:14]);
// output
[6,10,1,4]
```

相关函数：[dayOfYear](../d/dayOfYear.md), [dayOfMonth](../d/dayOfMonth.md), [quarterOfYear](../q/quarterOfYear.md), [weekOfYear](../w/weekOfYear.md), [hourOfDay](../h/hourOfDay.md), [minuteOfHour](minuteOfHour.md), [secondOfMinute](../s/secondOfMinute.md), [millisecond](millisecond.md), [microsecond](microsecond.md), [nanosecond](../n/nanosecond.md)

