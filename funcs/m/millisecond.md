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

相关函数：[dayOfYear](../d/dayOfYear.html), [dayOfMonth](../d/dayOfMonth.html), [quarterOfYear](../q/quarterOfYear.html), [monthOfYear](monthOfYear.html), [weekOfYear](../w/weekOfYear.html), [hourOfDay](../h/hourOfDay.html), [minuteOfHour](minuteOfHour.html), [secondOfMinute](../s/secondOfMinute.html), [microsecond](microsecond.html), [nanosecond](../n/nanosecond.html)

