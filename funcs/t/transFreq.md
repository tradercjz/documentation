# transFreq

## 语法

`transFreq(X, rule, [closed], [label],
[origin='start_day'])`

## 详情

将给定日期或时间变量转换为给定的时间格式（或对应的交易日）。结果长度与 *X* 相同。

## 参数

**X** 是表示日期或时间类型的标量或向量。

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
| "A" | yearEnd |
| "AS" | yearBegin |
| "BA" | businessYearEnd |
| "BAS" | businessYearBegin |
| "D" | date |
| "H" | hourOfDay |
| "min" | minuteOfHour |
| "S" | secondOfMinute |
| "L" | millisecond |
| "U" | microsecond |
| "N" | nanosecond |

上述字符串亦可配合使用数字（必须为正整数），例如 "2M" 表示频率为每两个月月末。此外，*rule*
也可以是交易日历标识（国外交易所的 ISO
Code、国内交易所简称或自定义交易日历名称），以便基于交易日历进行计算。交易日历也可以配合使用数字，表示多个交易日，此时只能指定由4个大写字母组成的交易日历标识。例如：“2XSHG”，表示上海证券交易所每两个交易日。

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

**origin** 字符串或和 *X* 具有相同时间类型的标量，表示基于时间戳调整分组。取值为 'epoch',
start', 'start\_day', 'end', 'end\_day' 或自定义的时间对象，默认值为 'start\_day'。

* 'epoch'：分组起始点为1970-01-01。
* 'start'：分组起始点为时间序列的第一个值。
* 'start\_day'：分组起始点是时间序列的第一个值对应日期的午夜零点。
* 'end'：分组起始点是时间序列的最后一个时间戳。
* 'end\_day'：分组起始点是时间序列的最后一个时间戳对应日期的午夜24点（即下一日的零点）。

## 例子

```
transFreq(2020.11.08 2020.11.09 2020.11.18, "SM");
// output
[2020.10.31,2020.10.31,2020.11.15]

transFreq(2020.08.08 2020.11.18, "Q");
// output
[2020.09.30,2020.12.31]

transFreq(2020.08.08 2020.11.18, "2Q");
// output
[2020.09.30,2021.03.31]
```

```
s = temporalAdd(2022.01.01 00:00:00,1..8,`m);

s.transFreq(rule="3min");
// output
[2022.01.01T00:00:00,2022.01.01T00:00:00,2022.01.01T00:03:00,2022.01.01T00:03:00,2022.01.01T00:03:00,2022.01.01T00:06:00,2022.01.01T00:06:00,2022.01.01T00:06:00]

s.transFreq(rule=`3min,closed=`right);
// output
[2022.01.01T00:00:00,2022.01.01T00:00:00,2022.01.01T00:00:00,2022.01.01T00:03:00,2022.01.01T00:03:00,2022.01.01T00:03:00,2022.01.01T00:06:00,2022.01.01T00:06:00]

s.transFreq(rule=`3min,closed=`right,origin=`end);
// output
[2021.12.31T23:59:00,2021.12.31T23:59:00,2022.01.01T00:02:00,2022.01.01T00:02:00,2022.01.01T00:02:00,2022.01.01T00:05:00,2022.01.01T00:05:00,2022.01.01T00:05:00]
```

