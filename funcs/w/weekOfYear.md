# weekOfYear

## 语法

`weekOfYear(X)`

## 参数

**X** 可以是 DATE, DATETIME, TIMESTAMP 或 NANOTIMESTAMP
类型的标量或向量。

## 详情

计算 *X* 的周数（1~53），返回的结果是整型。

注：

* 该函数假设一周的第一天是周日，且每年的第一周至少有4天。
* 如果12月31日是星期一、星期二或星期三，则该周为下一年的第 01
  周。如果是星期四，则该周为刚刚结束的一年的第53周；如果是星期五，则该周为第52周（如果刚刚结束的年份是闰年，则该周为第53周）；如果是周六或周日，则该周为刚刚结束的一年的第52周。

## 例子

```
weekOfYear(2012.01.07);
```

输出返回：1

```
weekOfYear(2013.01.07);
```

输出返回：2

```
weekOfYear(2012.07.02);
```

输出返回：27

```
weekOfYear([2012.06.12T12:30:00,2012.10.28T12:35:00,2013.01.06T12:36:47,2013.04.06T08:02:14]);
```

输出返回：[24,43,1,14]

相关函数：[dayOfYear](../d/dayOfYear.md), [dayOfMonth](../d/dayOfMonth.md), [quarterOfYear](../q/quarterOfYear.md), [monthOfYear](../m/monthOfYear.md), [hourOfDay](../h/hourOfDay.md), [minuteOfHour](../m/minuteOfHour.md), [secondOfMinute](../s/secondOfMinute.md), [millisecond](../m/millisecond.md), [microsecond](../m/microsecond.md), [nanosecond](../n/nanosecond.md)

