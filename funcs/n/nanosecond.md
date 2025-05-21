# nanosecond

## 语法

`nanosecond(X)`

## 参数

**X** 可以是 TIME, TIMESTAMP, NANOTIME 或 NANOTIMESTAMP
类型的标量或向量。

## 详情

返回 *X* 中的纳秒数。

## 例子

```
nanosecond(13:30:10.008);
// output
8000000

nanosecond([2012.12.03 01:22:01.999999999, 2012.12.03 01:25:08.000000234]);
// output
[999999999,234]
```

相关函数：[dayOfYear](../d/dayOfYear.html), [dayOfMonth](../d/dayOfMonth.html), [quarterOfYear](../q/quarterOfYear.html), [monthOfYear](../m/monthOfYear.html), [weekOfYear](../w/weekOfYear.html), [hourOfDay](../h/hourOfDay.html), [minuteOfHour](../m/minuteOfHour.html), [secondOfMinute](../s/secondOfMinute.html), [millisecond](../m/millisecond.html), [microsecond](../m/microsecond.html)

