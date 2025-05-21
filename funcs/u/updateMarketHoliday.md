# updateMarketHoliday

## 语法

`updateMarketHoliday(marketName, holiday)`

## 参数

**marketName** 字符串标量，表示交易日历标识，例如：国外交易所的 ISO Code、国内交易所简称或自定义交易日历名称。

**holiday** DATE 类型向量，表示日期。

* 当 *dateType*='holidayDate' 时，*holiday* 需要指定为休市日期，因为系统默认周末为休市日，所以
  *holiday* 只需指定非周末的休市日期。
* 当 *dateType*='tradingDate' 时，*holiday* 需要指定为交易日期。

## 详情

在线覆盖内存中文件名为 *marketName* 的交易市场节假日或交易日文件，并同步更新至 *marketHolidayDir*；若内存中不存在该文件，则报错。

注：

* 该函数只能由管理员调用。
* 该函数仅对当前节点有效。集群环境中，可通过 `pnodeRun`
  调用该函数，使其在其它节点生效。
* 若手动修改了 *marketHolidayDir*
  下的交易日历，想要在不关机的情况下，同步修改内容到内存，可以通过 `loadText` 将已修改的 csv
  文件加载到内存表，并转换表数据为向量（holiday），然后通过该函数将 `holiday` 更新至内存。

## 例子

```
temporalAdd(2022.01.01,1,"CCFX")
```

返回：2022.01.04

```
index = [2022.01.01, 2022.01.02, 2022.01.03, 2022.01.04]
s = indexedSeries(index, 1..4)
s.resample("CCFX", sum);
```

返回：

| label | col1 |
| --- | --- |
| 2021.12.31 | 6 |
| 2022.01.04 | 4 |

```
updateMarketHoliday("CCFX",2022.01.03 2022.01.04)
temporalAdd(2022.01.01,1,"CCFX")
```

返回：2022.01.05

**相关信息**

* [addMarketHoliday](../a/addMarketHoliday.html "addMarketHoliday")
* [getMarketCalendar](../g/getMarketCalendar.html "getMarketCalendar")
* [getTradingCalendarType](../g/gettradingcalendartype.html "getTradingCalendarType")

