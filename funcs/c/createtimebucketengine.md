# createTimeBucketEngine

## 语法

`createTimeBucketEngine(name,timeCutPoints,metrics,dummyTable,outputTable,timeColumn,[keyColumn],[useWindowStartTime],[closed='left'],[fill='none'],[keyPurgeFreqInSec=-1],[outputElapsedMicroseconds=false],[parallelism=1],[outputHandler=NULL],[msgAsTable=false])`

## 详情

创建一个自定义窗口长度（长度相同或不同）的时间序列聚合引擎。该引擎基于数据时间，按照指定的长度对输入数据进行窗口划分，并在窗口内执行增量聚合计算。通常和时序聚合引擎（createTimeSeriesEngine
）级联使用，接收其输出秒级或分钟级聚合结果（例如 K 线）进行进一步处理。

**返回值：**返回一个表对象，通过向该表对象写入，将数据注入引擎进行计算。

**窗口**

* 窗口边界：窗口的左、右边界由 *timeCutPoints* 向量的任意两个相邻元素确定。
* 边界开闭：由 *closed* 确定边界是左闭右开或者左开右闭。
* 窗口关闭时机：窗口左开右闭时，收到的第一条时间戳大于等于右边界的数据触发窗口关闭；窗口左闭右开时，收到的第一条时间戳大于等于右边界时间戳减1的数据触发窗口关闭。例如，对于窗口
  [09:00, 09:05)，当收到数据的时间戳大于等于 09:04 时，窗口关闭。
* 窗口输出时间戳：窗口输出时间戳的精度同 *timeColumn*。若 *useWindowStartTime* =
  true，显示为窗口起始时间；反之，显示时间为数据窗口终止时间。

**计算**

* 参与计算的数据时间范围：*timeCutPoints*
  向量中第一个元素和最后一个元素确定的时间范围内的数据会参与计算。该向量的时间精度决定了计算窗口的时间精度。例如，当
  *timeCutPoints =* [09:00m,
  09:05m]，且窗口左闭右开时，窗口的时间精度为分钟。此时，只有在大于等于 09:00m 且小于等于 09:04m 的数据会参与计算，而大于
  09:04m 的数据（如 09:04:00.100）则不参与计算。
* 分组计算或全局计算：若指定了 *keyColumn*，则按照分组分别进行窗口计算，否则进行全局计算。
* 计算结果填充：未指定 *fill* 或指定 *fill* = "none" 时，只输出计算结果不为空的窗口；若指定了
  *fill*，则输出所有窗口，且根据 *fill* 规则对结果为空的窗口进行填充。

## 参数

**name** 字符串标量，表示时间序列分组引擎的名称，作为其在一个数据节点/计算节点上的唯一标识。可包含字母，数字和下划线，但必须以字母开头。

**timeCutPoints** MINUTE 或 SECOND 类型向量，且不能包含空值。由
*timeCutPoints* 向量的任意两个相邻元素确定窗口的左、右边界。注意：

* *timeCutPoints* 指定的时间精度必须不高于 *timeColumn* 列的精度。
* *timeCutPoints* 指定的时间精度决定关闭窗口右边界的时间精度。如果 *timeCutPoints* 是
  MINUTE 类型，则窗口右边界的时间精度是分；如果 *timeCutPoints* 是 SECOND
  类型，则窗口右边界的时间精度是秒。

**metrics** 以元代码的格式表示计算指标，支持输入元组。有关元代码的更多信息可参考 [元编程](../../progr/objs/meta_progr.md)。

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

**dummyTable** 一个表对象，和订阅的流数据表的 schema 一致，可以含有数据，亦可为空表。

**outputTable** 计算结果的输出表，可以是内存表或者分布式表。在使用 createTimeBucketEngine
函数之前，需要将输出表预先设立为一个空表，并指定各列列名以及数据类型。引擎会将计算结果插入该表。

输出表的列顺序如下：

1. 时间列。当 *timeColumn* 为标量时，输出表中时间列的数据类型与 *timeColumn* 列
   一致。否则输出表中时间列的数据类型与 *timeColumn* 中日期和时间列应用 concatDateTime 的结果一致。
2. 分组列。如果 *keyColumn* 不为空，则其后几列和 *keyColumn* 设置的列及其顺序保持一致。
3. 耗时列。如果指定 *outputElapsedMicroseconds* = true，则指定一个 LONG
   类型的列用于存储耗时（单位：微秒）。
4. 计算结果列，数量和 *metrics* 中指定的算子个数相同。若 *metrics*
   指定的某个算子返回多个计算结果，则它们将以数组向量的形式输出，因此，该算子对应的计算结果列必须的类型必须是数组向量。

**timeColumn** 字符串标量或长度为2的向量，用于输入表中时间列的名称。

注：若 *timeColumn* 指定为向量，则第一个元素（date）的类型为 DATE，第二个元素（time）的类型为 TIME, SECOND 或
NANOTIME。此时，输出表第一列的时间类型必须与 concatDateTime(date, time) 的类型一致。

**keyColumn**
可选参数，字符串标量或向量，表示分组列名。若设置，则分组进行聚合计算，例如以每支股票为一组进行聚合计算。

**useWindowStartTime** 可选参数。布尔值，表示输出表中的时间是否为数据窗口起始时间。默认值为
false，表示输出表中的时间为窗口结束时间。

**closed** 字符串，用于确定滑动窗口边界的开闭情况。可选值为 'left' 或 'right'，默认值为
'left'。

* closed = 'left'： 窗口左闭右开。
* closed = 'right'： 窗口左开右闭。

**fill** 可选参数，一个标量或向量，指定某个分组的某个窗口无数据时的处理方法。可取以下值：

* 'none': 不输出结果。
* 'null': 输出结果为 NULL。
* 'ffill': 输出上一个有数据的窗口的结果。
* '具体数值'：该值的数据类型需要和对应的 *metrics* 计算结果的类型保持一致。

*fill* 可以输入向量，长度与 *metrics* 元素个数保持一致，表示为每个 *metrics* 指定不同的 *fill*
方式。若为向量，向量中各项只能是 'null', 'ffill' 或一个数值，不能是 'none'。

**keyPurgeFreqInSec**
正整数，表示清理窗口数据为空的分组的时间间隔，单位为秒。指定该参数后，若当前数据注入时间与上一次清理时间的间隔大于等于
*keyPurgeFreqInSec*，则触发对当前窗口数据为空的分组信息的清理。若指定该参数，则必须指定 *keyColumn*，且不能指定
*fill。*

**outputElapsedMicroseconds**
布尔值，表示是否输出每个窗口从触发计算到计算完成输出结果的耗时（若指定了 *keyColumn* 则包含数据分组的耗时），默认为 false。指定参数
*outputElapsedMicroseconds* 后，在定义 *outputTable* 时需要在时间列和分组列后增加一个 LONG
类型的列，详见 *outputTable* 参数说明。

**parallelism** 为不超过 63 的正整数，可选参数，表示并行计算的工作线程数，默认值为
1。在计算量较大时，合理地调整该参数能够有效利用计算资源，降低计算耗时。建议小于机器核数，推荐值为 4 到 8 。

**outputHandler**
一元函数。设置此参数时，引擎计算结束后，不再将计算结果写到输出表，而是会调用此函数处理计算结果。默认值为 NULL，表示仍将结果写到输出表。

**msgAsTable** 布尔标量，表示在设置了参数 outputHandler
时，将引擎的计算结果以表的结构调用函数。默认值为 false，此时将计算结果的每一列作为元素组成元组。

## 例子

通过时序聚合引擎计算1分钟 K 线，然后通过 createTimeBucketEngine 将 1 分钟 K 线聚合为 5
分钟。在窗口左闭右开的情况下，可以提前一分钟结束窗口并计算输出，从而比使用 createTimeSeriesEngine 减少延时。

```
share streamTable(1000:0, `time`sym`price`volume, [TIMESTAMP, SYMBOL, DOUBLE, INT]) as trades
share streamTable(10000:0, `time`sym`firstPrice`maxPrice`minPrice`lastPrice`sumVolume, [TIMESTAMP, SYMBOL, DOUBLE, DOUBLE, DOUBLE, DOUBLE, INT]) as output1
timeSeries1 = createTimeSeriesEngine(name="timeSeries1", windowSize=60000, step=60000, metrics=<[first(price), max(price), min(price), last(price), sum(volume)]>, dummyTable=trades, outputTable=output1, timeColumn=`time, useSystemTime=false, keyColumn=`sym, useWindowStartTime=false)
subscribeTable(tableName="trades", actionName="timeSeries1", offset=0, handler=append!{timeSeries1}, msgAsTable=true);

// 定义 createTimeBucketEngine 的输出表和窗口区间
share streamTable(10000:0, `time`sym`firstPrice`maxPrice`minPrice`lastPrice`sumVolume, [TIMESTAMP, SYMBOL, DOUBLE, DOUBLE, DOUBLE, DOUBLE, INT]) as output2
timeCutPoints=[10:00m, 10:05m, 10:10m, 10:15m]

timeBucket1 = createTimeBucketEngine(name="timeBucket1", timeCutPoints=timeCutPoints, metrics=<[first(firstPrice), max(maxPrice), min(minPrice), last(lastPrice), sum(sumVolume)]>, dummyTable=output1, outputTable=output2, timeColumn=`time,  keyColumn=`sym)
subscribeTable(tableName="output1", actionName="timeBucket1", offset=0, handler=append!{timeBucket1}, msgAsTable=true);

insert into trades values(2024.10.08T10:01:01.785,`A, 10.83, 2110)
insert into trades values(2024.10.08T10:01:02.125,`B,21.73, 1600)
insert into trades values(2024.10.08T10:01:12.457,`A,10.79, 2850)
insert into trades values(2024.10.08T10:03:10.789,`A,11.81, 2250)
insert into trades values(2024.10.08T10:03:12.005,`B, 22.96, 1980)
insert into trades values(2024.10.08T10:08:02.236,`A, 11.25, 2400)
insert into trades values(2024.10.08T10:08:04.412,`B, 23.03, 2130)
insert into trades values(2024.10.08T10:08:05.152,`B, 23.18, 1900)
insert into trades values(2024.10.08T10:08:30.021,`A, 11.04, 2300)
insert into trades values(2024.10.08T10:10:20.123,`A, 11.85, 2200)
insert into trades values(2024.10.08T10:11:02.236,`A, 11.06, 2200)
insert into trades values(2024.10.08T10:13:04.412,`B, 23.15, 1880)
insert into trades values(2024.10.08T10:15:12.005,`B, 22.06, 2100)

sleep(10)

// 查看时序引擎输出的 1 分钟 K 线结果
select * from output1;

```

| time | sym | firstPrice | maxPrice | minPrice | lastPrice | sumVolume |
| --- | --- | --- | --- | --- | --- | --- |
| 2024.10.08T10:02:00.000 | A | 10.83 | 10.83 | 10.79 | 10.79 | 4,960 |
| 2024.10.08T10:02:00.000 | B | 21.73 | 21.73 | 21.73 | 21.73 | 1,600 |
| 2024.10.08T10:04:00.000 | A | 11.81 | 11.81 | 11.81 | 11.81 | 2,250 |
| 2024.10.08T10:04:00.000 | B | 22.96 | 22.96 | 22.96 | 22.96 | 1,980 |
| 2024.10.08T10:09:00.000 | A | 11.25 | 11.25 | 11.04 | 11.04 | 4,700 |
| 2024.10.08T10:09:00.000 | B | 23.03 | 23.18 | 23.03 | 23.18 | 4,030 |
| 2024.10.08T10:11:00.000 | A | 11.85 | 11.85 | 11.85 | 11.85 | 2,200 |
| 2024.10.08T10:14:00.000 | B | 23.15 | 23.15 | 23.15 | 23.15 | 1,880 |

查看 5 分钟 K 线结果：

```
select * from output2;
```

| time | sym | firstPrice | maxPrice | minPrice | lastPrice | sumVolume |
| --- | --- | --- | --- | --- | --- | --- |
| 2024.10.08T10:05:00.000 | A | 10.83 | 11.81 | 10.79 | 11.81 | 7,210 |
| 2024.10.08T10:05:00.000 | B | 21.73 | 22.96 | 21.73 | 22.96 | 3,580 |
| 2024.10.08T10:10:00.000 | A | 11.25 | 11.25 | 11.04 | 11.04 | 4,700 |
| 2024.10.08T10:10:00.000 | B | 23.03 | 23.18 | 23.03 | 23.18 | 4,030 |
| 2024.10.08T10:15:00.000 | B | 23.15 | 23.15 | 23.15 | 23.15 | 1,880 |

