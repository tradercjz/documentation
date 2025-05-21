# getMarketCalendar

## 语法

`getMarketCalendar(marketName, [startDate], [endDate])`

## 参数

**marketName** 字符串标量，表示交易日历标识，例如：国外交易所的 ISO Code、国内交易所简称或自定义交易日历名称。必须是
*marketHolidayDir* 下存在的文件名，否则会报错。

**startDate** DATE 类型标量。默认为空，表示起始日期为 *marketName* 同名文件中最小年份的1月1日。

**endDate** DATE 类型标量。默认为空，表示结束日期为 *marketName* 同名文件中最大年份的12月31日。

## 详情

DolphinDB 提供国内外超过50个交易所的交易日历信息（对应文件存放于 *marketHolidayDir*
中），通过该函数可以获取由 *startDate* 和 *endDate* 确定的时间范围内的交易日历。

## 例子

```
getMarketCalendar("CCFX",2022.01.01, 2022.01.10)
```

输出返回：[2022.01.04,2022.01.06,2022.01.07,2022.01.10]

**相关信息**

* [addMarketHoliday](../a/addMarketHoliday.html "addMarketHoliday")
* [updateMarketHoliday](../u/updateMarketHoliday.html "updateMarketHoliday")

