# DStream::timeSeriesEngine

## 语法

`DStream::timeSeriesEngine(windowSize, step, metrics, [timeColumn],
[useSystemTime=false], [keyColumn], [updateTime], [useWindowStartTime],
[roundTime=true], [fill='none'], [forceTriggerTime], [keyPurgeFreqInSecond=-1],
[closed='left'], [subWindow], [parallelism=1], [acceptedDelay=0])`

## 详情

创建流计算时间序列聚合引擎。参考：[createTimeSeriesEngine](../c/createTimeSeriesEngine.html)。

**返回值**：一个 DStream 对象。

## 参数

**windowSize** 正整数标量或向量，表示滑动窗口的长度。

**step** 正整数标量，表示滑动窗口移动的步长。 *windowSize* 必须是 *step*
的整数倍，否则会抛出异常。*windowSize* 和 *step* 的单位与 *useSystemTime* 有关：

* 若 *useSystemTime* 为 true，则 *windowSize* 和
  *step* 的单位为毫秒。
* 若 *useSystemTime* 为 false，则 *windowSize* 和
  *step* 的单位与 *timeColumn* 的时间精度一致。

**metrics** 以元代码的格式表示计算指标，支持输入元组。有关元代码的更多信息可参考 [元编程](../c/../../progr/objs/meta_progr.html)。

* 计算指标可以是一个或多个系统内置或用户自定义的聚合函数（使用 defg 关键字定义），如
  <[sum(volume), avg(price)]>；可以对聚合结果使用表达式，如
  <[avg(price1)-avg(price2)]>；也可对列与列的计算结果进行聚合计算，如
  <[std(price1-price2)]>。
* *metrics* 内支持调用具有多个返回值的函数，例如 <func(price) as
  `col1`col2>（可不指定列名）。
* 若 *windowSize* 为向量， *windowSize* 每个值可对应
  *metrics* 中多个计算指标。例如，*windowSize* 为[10,20]时，metrics可为
  (<[min(volume), max(volume)]>, <sum(volume)>)。
  *metrics* 也可以嵌套输入元组向量。例如：[[<[min(volume), max(volume)]>,
  <sum(volume)>], [<avg(volume)>]]

  注：
  + *metrics* 中使用的列名大小写不敏感，不需要与输入表的列名大小写保持一致。
  + *metrics* 中不可使用嵌套聚合函数。

**timeColumn** 可选参数，字符串标量或向量。当 *useSystemTime* = false
时，必须指定该参数。 该参数用于指定订阅的流数据表中时间列的名称。

注： 字符串向量必须是 date 和 time
组成的向量，date 类型为 DATE，time 类型为 TIME, SECOND 或 NANOTIME。此时，输出表第一列的时间类型必须与 [concatDateTime(date, time)](../c/concatDateTime.html)
的类型一致。

**useSystemTime** 可选参数，布尔值，表示是否使用数据注入引擎时的系统时间作为时间列进行计算。

* 当 *useSystemTime* =
  true时，时间序列引擎会按照数据注入时间序列引擎的时刻（毫秒精度的本地系统时间，与数据中的时间列无关），每隔固定时间截取固定长度窗口的流数据进行计算。只要一个数据窗口中含有数据，数据窗口结束后就会自动进行计算。结果中的第一列为计算发生的时间戳，与数据中的时间无关。
* 当 *useSystemTime* = false（缺省值）时，时间序列引擎根据流数据中的 *timeColumn*
  列来截取数据窗口。一个数据窗口结束后的第一条新数据才会触发该数据窗口的计算。请注意，触发计算的数据并不会参与该次计算。

  例如，一个数据窗口从 10:10:10 到 10:10:19。若 *useSystemTime*
  = true，则只要该窗口中至少有一条数据，该窗口的计算会在窗口结束后的 10:10:20 触发。若 *useSystemTime*
  = false，且 10:10:19 后的第一条数据为 10:10:25，则该窗口的计算会在 10:10:25 触发。

**keyColumn**
可选参数，字符串标量或向量，表示分组列名。若设置，则分组进行聚合计算，例如以每支股票为一组进行聚合计算。

**updateTime** 可选参数，非负整数，单位与 timeColumn 的时间精度一致。用于指定比
*step* 更短的计算时间间隔。*step* 必须是 *updateTime* 的整数倍。要设置
*updateTime*， *useSystemTime* 必须设为 false。

* updateTime 指定为正整数值时：

  + 从当前窗口的左边界开始，每隔 *updateTime*
    时间，若有新的数据到来，则对当前窗口内该数据之前的所有数据进行计算。
  + 如果系统经过 2 \* *updateTime* （至少2秒）后仍有未被处理的数据，则触发对当前窗口内所有数据的计算。
  + 若分组计算，则每组内进行上述操作。
* updateTime 指定为 0 时：在新的数据到来后，立即对当前窗口的最新数据计算并输出。

**useWindowStartTime** 可选参数，布尔值，表示输出表中的时间是否为数据窗口起始时间。默认值为
false，表示输出表中的时间为数据窗口起始时间 + *windowSize* 。若 *windowSize* 是向量，
*useWindowStartTime* 必须为 false。

**roundTime** 可选参数，布尔值，表示若数据时间精度为毫秒或者秒且 *step* >
一分钟，如何对窗口边界值进行规整处理。默认值为 true，表示按照既定的多分钟规则进行规整。若为 false，则按一分钟规则进行窗口规整。

**fill** 可选参数，一个标量或向量，指定某个分组的某个窗口无数据时的处理方法。可取以下值：

* 'none': 不输出结果。
* 'null': 输出结果为 NULL。
* 'ffill': 输出上一个有数据的窗口的结果。
* '具体数值'：该值的数据类型需要和对应的 *metrics* 计算结果的类型保持一致。

*fill* 可以输入向量，长度与 *metrics* 元素个数保持一致，表示为每个 *metrics* 指定不同的 *fill*
方式。若为向量，向量中各项只能是 'null', 'ffill' 或一个数值，不能是 'none'。

**forceTriggerTime** 可选参数，是非负整数，单位与 *timeColumn*
的时间精度一致。用于强制触发各个分组未计算的窗口进行计算。要设置 *forceTriggerTime*， *useSystemTime* 必须设置为
false，且不能指定 *updateTime*。强制触发计算及输出规则如下：

1. 未被触发计算的窗口结束后（窗口结束时刻为 t），若收到了其他分组的数据（时间戳为 t1），且满足 t1-t
   ≥ *forceTriggerTime*，则该窗口将被触发计算。
2. 如果某个分组在最后一个窗口被强制触发计算后，没有再收到新的数据，但其他分组仍然收到了新的数据，那么通过 *fill*
   来填充该分组的所有缺失窗口，可以确保在最新时间截面上仍然输出该分组的窗口。如果不指定
   *fill*，则最后一个窗口被触发计算后，该分组不会产生新的窗口。

设置 *forceTriggerTime* 或 *updateTime* 时需注意以下几点：

* 设置 *updateTime*，计算发生后仍有属于当前窗口的数据到达时，当前窗口计算结果会再次更新；
* 设置 *forceTriggerTime*，则触发计算之后收到的数据会被丢弃，建议不要设置太小的
  *forceTriggerTime*。

**keyPurgeFreqInSec**
正整数，表示清理窗口数据为空的分组的时间间隔，单位为秒。指定该参数后，若当前数据注入时间与上一次清理时间的间隔大于等于
*keyPurgeFreqInSec*，则触发对当前窗口数据为空的分组信息的清理。

注：

* 若需指定该参数，必须指定 *forceTriggerTime*，且不能指定 *fill*。
* 可以通过调用 [getStreamEngineStat](../c/../g/getStreamEngineStat.html) 函数查看 TimeSeriesEngine 引擎状态的
  numGroups 列，来对比响应式状态引擎清理前后分组数的变化。

**closed** 字符串，用于确定滑动窗口边界的开闭情况。可选值为 'left' 或 'right'，默认值为
'left'。

* closed = 'left'： 窗口左闭右开。
* closed = 'right'： 窗口左开右闭。

**subWindow** 整型或者 DURATION
数据对。在滑动窗口内指定子窗口，仅计算子窗口内的数据。子窗口边界的开闭情况由参数 *closed*
决定。子窗口结束后收到第一条数据触发对子窗口内数据的计算（参考例4）。当 *subWindow* 为整型数据对时，其单位与 *timeColumn*
的时间精度一致。若指定 *subWindow*，则：

* *windowSize* 和 *step* 必须相等。
* 不可设置 *updateTime*>0和 *useSystemTime*=true。

**parallelism** 为不超过 63 的正整数，可选参数，表示并行计算的工作线程数，默认值为
1。在计算量较大时，合理地调整该参数能够有效利用计算资源，降低计算耗时。建议小于机器核数，推荐值为 4 到 8 。

**acceptedDelay** 正整数，可选参数。指定每个窗口接收数据的最大延迟，默认值为 0。若设置该参数，则不能设置
*forceTriggerTime* 或 *updateTime*。

* 当 useSystemTime= true 时，*acceptedDelay* 必须小于等于
  *windowSize*。在窗口结束后的 *acceptedDelay*
  时间内接收到的数据，仍然属于此窗口并参与计算，而不会参与下一个窗口的计算。
* 当 useSystemTime= false 时，该参数用于处理乱序数据。假设当前窗口结束的时间戳为 t ，若收到一条时间戳大于等于
  t+*acceptedDelay*的数据，则触发在此之前收到的所有属于当前窗口的数据进行计算输出，并关闭该窗口。

## 例子

```
if (!existsCatalog("orca")) {
	createCatalog("orca")
}
go
use catalog orca

// 如已存在流图，则先销毁该流图
// dropStreamGraph('engine')
g = createStreamGraph('engine')

g.source("trades", 1000:0, ["time","sym","volume"], [TIMESTAMP, SYMBOL, INT])
.timeSeriesEngine(windowSize=60000, step=60000, metrics=<[sum(volume)]>, timeColumn="time", useSystemTime=false, keyColumn="sym", useWindowStartTime=false)
.sink("output")
g.submit()
go

times = [2018.10.08T01:01:01.785, 2018.10.08T01:01:02.125, 2018.10.08T01:01:10.263, 2018.10.08T01:01:12.457, 2018.10.08T01:02:10.789, 2018.10.08T01:02:12.005, 2018.10.08T01:02:30.021, 2018.10.08T01:04:02.236, 2018.10.08T01:04:04.412, 2018.10.08T01:04:05.152]
syms = [`A, `B, `B, `A, `A, `B, `A, `A, `B, `B]
volumes = [10, 26, 14, 28, 15, 9, 10, 29, 32, 23]

tmp = table(times as time, syms as sym, volumes as volume)
appendOrcaStreamTable("trades", tmp)

select * from orca_table.output
```

| time | sym | sum\_volume |
| --- | --- | --- |
| 2018.10.08 01:02:00.000 | A | 38 |
| 2018.10.08 01:02:00.000 | B | 40 |
| 2018.10.08 01:03:00.000 | A | 25 |
| 2018.10.08 01:03:00.000 | B | 9 |

