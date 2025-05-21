# millisecond

## 语法

`millisecond(X)`

## 参数

**X** 可以是 TIME, TIMESTAMP, NANOTIME 或 NANOTIMESTAMP
类型的标量或向量。

## 详情

返回 *X* 中的毫秒数。

## 例子

```
millisecond(13:30:10.008);
// output
8

millisecond([2012.12.03 01:22:01.456120300, 2012.12.03 01:25:08.000234000]);
// output
[456,0]
```

相关函数：[dayOfYear](../d/dayOfYear.md), [dayOfMonth](../d/dayOfMonth.md), [quarterOfYear](../q/quarterOfYear.md), [monthOfYear](monthOfYear.md), [weekOfYear](../w/weekOfYear.md), [hourOfDay](../h/hourOfDay.md), [minuteOfHour](minuteOfHour.md), [secondOfMinute](../s/secondOfMinute.md), [microsecond](microsecond.md), [nanosecond](../n/nanosecond.md)

