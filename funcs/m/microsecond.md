# microsecond

## 语法

`microsecond(X)`

## 参数

**X** 可以是 TIME, TIMESTAMP, NANOTIME 或 NANOTIMESTAMP
类型的标量或向量。

## 详情

返回 *X* 中的微秒数。

## 例子

```
microsecond(13:30:10.008);
// output
8000

microsecond([2012.12.03 01:22:01.999999000, 2012.12.03 01:22:01.000456000, 2012.12.03 01:25:08.000000234]);
// output
[999999,456,0]
```

相关函数：[dayOfYear](../d/dayOfYear.html), [dayOfMonth](../d/dayOfMonth.html), [quarterOfYear](../q/quarterOfYear.html), [monthOfYear](monthOfYear.html), [weekOfYear](../w/weekOfYear.html), [hourOfDay](../h/hourOfDay.html), [minuteOfHour](minuteOfHour.html), [secondOfMinute](../s/secondOfMinute.html), [millisecond](millisecond.html), [nanosecond](../n/nanosecond.html)

