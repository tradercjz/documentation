# resample

## 语法

`resample(X, rule, func, [closed], [label],
[origin='start_day'])`

## 详情

依照指定时间频率（或交易日历），对给定数据使用给定函数。注意，*rule*
指定为交易日历标识时，对于非交易日的数据，将并入上一个交易日计算。

## 参数

**X** 是一个带有行标签的矩阵或序列（indexed series）。行标签要求为时间类型，不得含有空值，且必须保持递增。

**rule** 是一个字符串，可取以下值：

| rule 参数取值 | 对应 DolphinDB 函数 |
| --- | --- |
| "B" | businessDay |
| "W" | weekEnd |
| "WOM" | weekOfMonth |
| "LWOM" | lastWeekOfMonth |
| "M" | monthEnd |
| "MS" | monthBegin |
| "BM" | businessMonthEnd |
| "BMS" | businessMonthBegin |
| "SM" | semiMonthEnd |
| "SMS" | semiMonthBegin |
| "Q" | quarterEnd |
| "QS" | quarterBegin |
| "BQ" | businessQuarterEnd |
| "BQS" | businessQuarterBegin |
| "REQ" | fy5253Quarter |
| "A" | yearEnd |
| "AS" | yearBegin |
| "BA" | businessYearEnd |
| "BAS" | businessYearBegin |
| "RE" | fy5253 |
| "D" | date |
| "H" | hourOfDay |
| "U" | microsecond |
| "L" | millisecond |
| "min" | minuteOfHour |
| "N" | nanosecond |
| "S" | secondOfMinute |

上述字符串亦可配合使用数字（必须为正整数），例如 "2M" 表示频率为每两个月月末。此外，*rule*
也可以是交易日历标识（国外交易所的 ISO
Code、国内交易所简称或自定义交易日历名称），以便基于交易日历进行计算。交易日历也可以配合使用数字，表示多个交易日，此时只能指定由4个大写字母组成的交易日历标识。例如：“2XSHG”，表示上海证券交易所每两个交易日。

**func** 一个聚合函数。

**closed** 字符串，表示分组区间哪一个边界是闭合的。

* *rule* 为 'M', 'A', 'Q', 'BM', 'BA', 'BQ' 和 'W'
  时，*closed* 的默认取值为 'right' ，否则，*closed* 的默认取值为 'left'。
* *origin* 取 'end' 或者 'end\_day' 时，*closed*
  的默认值为 'right'。

**label** 字符串，表示将分组区间的哪一个边界作为 *label* 输出。

* *rule* 为 'M', 'A', 'Q', 'BM', 'BA', 'BQ' 和 'W'
  时，*label* 的默认取值为 'right' ，否则，*label* 的默认取值为 'left'。
* *origin* 取 'end' 或者 'end\_day' 时，*label*
  的默认值为 'right'。

**origin** 字符串或与 *X* 具有相同时间类型的标量，表示基于时间戳调整分组。*origin*
的取值为 'epoch', start', 'start\_day', 'end', 'end\_day' 或自定义的时间对象，默认值为 'start\_day'。

* 'epoch'：分组起始点为1970-01-01。
* 'start'：分组起始点为时间序列的第一个值。
* 'start\_day'：分组起始点是时间序列的第一个值对应日期的午夜零点。
* 'end'：分组起始点是时间序列的最后一个时间戳。
* 'end\_day'：分组起始点是时间序列的最后一个时间戳对应日期的午夜24点（即下一日的零点）。

## 例子

```
index = [2000.01.01, 2000.01.31, 2000.02.15, 2000.02.20, 2000.03.12, 2000.04.16, 2000.05.06, 2000.08.30]
s = indexedSeries(index, 1..8)
s.resample("M", sum);
```

|  | col1 |
| --- | --- |
| 2000.01.31 | 3 |
| 2000.02.29 | 7 |
| 2000.03.31 | 5 |
| 2000.04.30 | 6 |
| 2000.05.31 | 7 |
| 2000.06.30 |  |
| 2000.07.31 |  |
| 2000.08.31 | 8 |

```
s.resample("2M", last);
```

|  | col1 |
| --- | --- |
| 2000.01.31 | 2 |
| 2000.03.31 | 5 |
| 2000.05.31 | 7 |
| 2000.07.31 |  |
| 2000.09.30 | 8 |

```
index = temporalAdd(2022.01.01 00:00:00,1..8,`m)
s = indexedSeries(index, 1..8)
s.resample(rule=`3min, func=sum);
```

| label | col1 |
| --- | --- |
| 2022.01.01T00:00:00 | 3 |
| 2022.01.01T00:03:00 | 12 |
| 2022.01.01T00:06:00 | 21 |

```
s.resample(rule=`3min, func=sum, closed=`right);
```

| label | col1 |
| --- | --- |
| 2022.01.01T00:00:00 | 6 |
| 2022.01.01T00:03:00 | 15 |
| 2022.01.01T00:06:00 | 15 |

```
s.resample(rule=`3min, func=sum, closed=`left,origin=`end);
```

| label | col1 |
| --- | --- |
| 2022.01.01T00:02:00 | 1 |
| 2022.01.01T00:05:00 | 9 |
| 2022.01.01T00:08:00 | 18 |
| 2022.01.01T00:11:00 | 8 |

```
s.resample(rule=`3min, func=sum,origin=2022.10.01 00:00:10)
```

| label | col1 |
| --- | --- |
| 2022.01.01T00:00:10 | 6 |
| 2022.01.01T00:03:10 | 15 |
| 2022.01.01T00:06:10 | 15 |

```
m = matrix(1..5, 1..5)
index = temporalAdd(2000.01.01, [1, 1, 2, 2, 3], "d")
m.rename!(index, `A`B);
m.resample(rule=`D, func=sum);
```

| label | A | B |
| --- | --- | --- |
| 2000.01.02 | 3 | 3 |
| 2000.01.03 | 7 | 7 |
| 2000.01.04 | 5 | 5 |

**相关信息**

* [spline](../s/spline.html "spline")
* [neville](../n/neville.html "neville")
* [dividedDifference](../d/dividedDifference.html "dividedDifference")
* [loess](../l/loess.html "loess")

