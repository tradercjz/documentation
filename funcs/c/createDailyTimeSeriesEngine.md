# createDailyTimeSeriesEngine

## 语法

`createDailyTimeSeriesEngine(name, windowSize, step,
metrics, dummyTable, outputTable, [timeColumn], [useSystemTime=false],
[keyColumn], [garbageSize], [updateTime], [useWindowStartTime],
[roundTime=true], [snapshotDir], [snapshotIntervalInMsgCount], [fill='none'],
[sessionBegin], [sessionEnd], [mergeSessionEnd=false], [forceTriggerTime],
[raftGroup], [forceTriggerSessionEndTime], [keyPurgeFreqInSec], [closed='left'],
[outputElapsedMicroseconds=false], [subWindow],
[parallelism=1],[acceptedDelay=0], [outputHandler=NULL],
[msgAsTable=false], [keyPurgeDaily=true], [mergeLastWindow=false],
[mergeSession])`

## 详情

创建流数据日级时间序列引擎。日级时间序列引擎和时间序列引擎窗口划分和计算规则基本一致，但在此基础上做了如下拓展：

* 该引擎只能在一个自然日的指定时间段内（以下统称为 session）进行窗口的聚合计算。一个自然日内，可以指定多个 session， 如
  9:00-12:00，13:00-15:00 等。默认情况下，系统会对 session 的起始时间（*sessionBegin* 和
  *sessionEnd*）进行规整，除非特别指定（详见 *mergeLastWindow*）。
* 出现在一个 session 开始之前的数据，日级时序引擎规定将该部分数据合入该 session 的第一个窗口进行计算。
* 当日最后一个 session 后到来的数据将被丢弃，不会计入第二天的第一个窗口中。

若指定了 *keyColumn* 进行分组，则上述计算将在各分组内独立进行。

更多流数据引擎的应用场景说明可以参考 [流计算引擎](../themes/streamingEngine.html)。

## 参数

该引擎是基于时间序列引擎进行的扩展，继承了 [createTimeSeriesEngine](createTimeSeriesEngine.html) 所有的参数，请参照 `createTimeSeriesEngine`
中参数介绍。这里仅介绍与时间序列引擎不同的参数：

**sessionBegin** 为可选参数，可以是与时间列的数据类型对应的 SECOND、TIME 或 NANOTIME
类型的标量或向量，表示每个时间段的起始时刻。如果 *sessionBegin* 是一个向量，它必须是递增的。

**sessionEnd** 为可选参数，可以是与时间列的数据类型对应的 SECOND、TIME 或 NANOTIME
类型的标量或向量，表示每个时间段的结束时刻。可在 *sessionEnd* 中指定 00:00:00 表示的次日的零点（即当日的 24:00:00）。

注：

session 由 sessionBegin[i] 和 sessionEnd[i] 确定。

* 若 sessionBegin[i] > sessionEnd[i]，则 sessionEnd[i] 视为下一个自然日的时间，此后 session
  均为下一个自然日。例如 sessionBegin=[21:00:00, 23:30:00, 09:00:00, 13:00:00],
  sessionEnd=[22:00:00, 02:00:00,11:30:00, 15:00:00]，此时 session 分别为
  21:00:00-22:00:00，23:30:00-次日02:00:00, 次日09:00:00-11:30:00，
  次日13:00:00-15:00:00。 21:00:00-22:00:00为第一个session，keyPurgeDaily
  在21:00:00之前生效，15:00:00-21:00:00之间的数据都会被丢弃。

  + 若 i = 0 ，则该 session 视为该交易日的第一个 session。例如
    sessionBegin=[21:00:00，09:00:00, 13:00:00]，sessionEnd=[01:00:00,
    11:30:00, 15:00:00]，此时 session 分别为 21:00:00-次日01:00:00，次日
    09:00:00- 11:30:00， 次日13:00:00- 15:00:00。21:00:00-次日01:00:00
    为第一个 session，*keyPurgeDaily*
    在21:00:00之前生效，15:00:00-21:00:00之间的数据都会被丢弃。
  + 若 i = size(sessionBegin)-1，则该 session 视为该交易日的最后一个 session。例如
    sessionBegin=[09:00:00, 13:00:00,
    21:00:00]，sessionEnd=[11:30:00, 15:00:00, 01:00:00]，此时 session
    分别为09:00:00-11:30:00，13:00:00-15:00:00，21:00:00-次日01:00:00。09:00:00-11:30:00
    为第一个session， keyPurgeDaily
    在09:00:00之前生效，01:00:00-09:00:00之间的数据会被丢弃。
* 若 sessionBegin[i] < sessionEnd[i-1]，则 sessionBegin[i] 视为下一个自然日的时间，此后
  session 均为下一个自然日。例如 sessionBegin=[21:00:00，09:00:00,
  13:00:00]，sessionEnd=[23:00:00, 11:30:00, 15:00:00]，此时 session 分别为
  21:00:00-23:00:00，次日09:00:00-11:30:00，
  次日13:00:00-15:00:00。21:00:00-23:00:00为第一个session， keyPurgeDaily
  在21:00:00之前生效，15:00:00-21:00:00之间的数据都会被丢弃。

其他示例：

* sessionBegin=[00:00:00, 09:00:00, 13:00:00,
  21:00:00]，sessionEnd=[01:00:00, 11:30:00, 15:00:00, 00:00:00]，此时 session
  分别为 21:00:00-次日01:00:00，09:00:00-11:30:00， 13:00:00-15:00:00。
  21:00:00-次日01:00:00为第一个session， keyPurgeDaily 在21:00:00之前生效（2.00.14.4
  前不会生效），15:00:00-21:00:00之间的数据都会被丢弃（2.00.14.4 前会并入21:00:00的第一个窗口）。
* sessionBegin=[09:00:00, 13:00:00]，sessionEnd=[11:30:00, 15:00:00]，此时
  session 分别为 09:00:00-11:30:00，13:00:00-15:00:00。keyPurgeDaily
  在15:00:00之后生效，15:00:00-24:00:00之间的数据都会被丢弃，00:00:00-09:00:00
  的数据会被并入第一个窗口。

**mergeSessionEnd** 为可选参数，是一个布尔值。当 *closed* = 'left'
时，表示每个 session 结束时刻的数据是否合入最后一个窗口。默认值为 false，此时该条数据不会合入当前 session
的最后一个窗口，但可以触发最后一个窗口的计算；如果当前 session 不是该自然日内最后一个 session，则该数据会合入下个 session
的第一个窗口。

**forceTriggerSessionEndTime** 为可选参数，正整数，单位与 *timeColumn*
的时间精度一致。若 *sessionEnd* 时刻对应的窗口数据长时间未发生计算，通过该参数可以设置系统经过多少时间后触发计算并输出。若不指定
*fill* ，未包含在该窗口内的分组不会输出结果；若指定了 *fill* ，未包含在该窗口内的分组会按照 *fill*
指定的方式输出结果。

**keyPurgeDaily** 为可选参数，是一个布尔值。默认值为
true，表示引擎在收到第一批包含新日期的数据时，先清空之前保存的所有分组，再对这批新数据进行处理。若设置为 false，则引擎不会清理前一天的分组。

**mergeLastWindow** 为可选参数，是一个布尔值，默认值为 false，可用于处理无法被等长窗口（由
*windowSize* 指定）均分的不规则 session 时段。当设置为 *true* 时，系统将最后一个不完整窗口（即小于
*windowSize* 的窗口）的数据与前一个窗口合并进行计算。该参数不支持和 *subWindow* 同时指定。

**mergeSession** 为 BOOL 类型向量，其长度为 session 的数量减
1。mergeSession[i] 为 true 表示 session[i] 和 session[i+1] 合并，false 表示不合并。若两个 session
合并，则 *mergeSessionEnd*、*forceTriggerSessionEndTime* 和
*mergeLastWindow* 在前一个 session 的 *sessionEnd* 处不生效。

## 例子

例1. 设置 *mergeSessionEnd*，将每个 session 结束时刻的数据合入最后一个窗口。

```
share streamTable(1000:0, `date`second`sym`volume, [DATE, SECOND, SYMBOL, INT]) as trades
share keyedTable(`time`sym, 10000:0, `time`sym`sumVolume, [DATETIME, SYMBOL, INT]) as output1
engine1 = createDailyTimeSeriesEngine(name="engine1", windowSize=60, step=60, metrics=<[sum(volume)]>, dummyTable=trades, outputTable=output1, timeColumn=`date`second, useSystemTime=false, keyColumn=`sym, garbageSize=50, updateTime=2, useWindowStartTime=false, sessionBegin=09:30:00 13:00:00, sessionEnd=11:30:00 15:00:00,mergeSessionEnd=true)
subscribeTable(tableName="trades", actionName="engine1", offset=0, handler=append!{engine1}, msgAsTable=true);

insert into trades values(2018.10.08,09:25:31,`A,8)
insert into trades values(2018.10.08,09:26:01,`B,10)
insert into trades values(2018.10.08,09:30:02,`A,26)
insert into trades values(2018.10.08,09:30:10,`B,14)
insert into trades values(2018.10.08,11:29:46,`A,30)
insert into trades values(2018.10.08,11:29:50,`B,11)
insert into trades values(2018.10.08,11:30:00,`A,14)
insert into trades values(2018.10.08,11:30:00,`B,4)
insert into trades values(2018.10.08,13:00:10,`A,16)
insert into trades values(2018.10.08,13:00:12,`B,9)
insert into trades values(2018.10.08,14:59:56,`A,20)
insert into trades values(2018.10.08,14:59:58,`B,20)
insert into trades values(2018.10.08,15:00:00,`A,10)
insert into trades values(2018.10.08,15:00:00,`B,29)

sleep(1000)
select * from output1
```

| time | sym | sumVolume |
| --- | --- | --- |
| 2018.10.08T09:31:00 | A | 34 |
| 2018.10.08T09:31:00 | B | 24 |
| 2018.10.08T11:30:00 | A | 44 |
| 2018.10.08T11:30:00 | B | 15 |
| 2018.10.08T13:01:00 | A | 16 |
| 2018.10.08T13:01:00 | B | 9 |
| 2018.10.08T15:00:00 | A | 30 |
| 2018.10.08T15:00:00 | B | 49 |

例2. 设置 *forceTriggerSessionEndTime*，达到系统时间，强制触发计算。

```
share streamTable(1000:0, `date`second`sym`volume, [DATE, SECOND, SYMBOL, INT]) as trades
share keyedTable(`time`sym, 10000:0, `time`sym`sumVolume, [DATETIME, SYMBOL, INT]) as output1
engine1 = createDailyTimeSeriesEngine(name="engine1", windowSize=60, step=60, metrics=<[sum(volume)]>, dummyTable=trades, outputTable=output1, timeColumn=`date`second, useSystemTime=false, keyColumn=`sym, garbageSize=50, useWindowStartTime=false, sessionBegin=09:30:00 13:00:00, sessionEnd=11:30:00 15:00:00,mergeSessionEnd=true,forceTriggerSessionEndTime=10)
subscribeTable(tableName="trades", actionName="engine1", offset=0, handler=append!{engine1}, msgAsTable=true);

insert into trades values(date(now()),09:25:31,`A,8)
insert into trades values(date(now()),09:26:01,`B,10)
insert into trades values(date(now()),09:30:02,`A,26)
insert into trades values(date(now()),09:30:10,`B,14)
insert into trades values(date(now()),11:29:46,`A,30)
insert into trades values(date(now()),11:29:50,`B,11)
insert into trades values(date(now()),11:30:00,`B,14)
insert into trades values(date(now()),11:30:01,`A,4)

select * from output1
```

| time | sym | sumVolume |
| --- | --- | --- |
| 2022.03.24T09:31:00 | A | 34 |
| 2022.03.24T09:31:00 | B | 24 |
| 2022.03.24T11:30:00 | A | 30 |

设置 *forceTriggerSessionEndTime* = 10，则系统到达 11:30:00 后，再经过 10s
就会触发右边界为11:30:00的窗口内数据的计算。

```
sleep(10000)
select * from output1
```

| time | sym | sumVolume |
| --- | --- | --- |
| 2022.03.24T09:31:00 | A | 34 |
| 2022.03.24T09:31:00 | B | 24 |
| 2022.03.24T11:30:00 | A | 30 |
| 2022.03.24T11:30:00 | B | 25 |

例3. 如果 *sessionEnd* - *sessionBegin* 不能整除
step，则会话的最后一个窗口由于长度不足而无法输出。若希望输出该窗口的数据，需要设置 *roundTime* =
false，将窗口按一分钟规则规整后输出。

```
// 清理变量
dropStreamEngine("engine1")
unsubscribeTable(tableName="trades", actionName="engine1")
undef(`trades, SHARED)
undef(`output1,SHARED)

share streamTable(1000:0, `date`time`sym`volume, [DATE, TIME, SYMBOL, INT]) as trades
share keyedTable(`timestamp`sym, 10000:0, `timestamp`sym`sumVolume, [TIMESTAMP, SYMBOL, INT]) as output1

//创建引擎，指定窗口长度为 10 分钟。最后一个 sessionEnd 是 14:57:00
engine1 = createDailyTimeSeriesEngine(name="engine1", windowSize=600000, step=600000,
  metrics=<[sum(volume)]>, dummyTable=trades, outputTable=output1, timeColumn=`date`time, garbageSize=50, updateTime=2,
  useSystemTime=false, keyColumn=`sym,  useWindowStartTime=false, mergeSessionEnd=true,
  sessionBegin=09:30:00.000 13:00:00.000,  sessionEnd=11:30:00.000 14:57:00.000, roundTime=false)

subscribeTable(tableName="trades", actionName="engine1", offset=0,
  handler=append!{engine1}, msgAsTable=true);

// 模拟数据插入流表。
// 最后一条数据时间是 14:56:00，按照一分钟规则进行规整，则该条数据将输出到 14:57:00 的窗口中
insert into trades values(2024.09.10,14:00:10.988,`A,16)
insert into trades values(2024.09.10,14:00:12.458,`B,9)
insert into trades values(2024.09.10,14:21:10.772,`A,13)
insert into trades values(2024.09.10,14:22:12.090,`B,15)
insert into trades values(2024.09.10,14:29:56.953,`A,20)
insert into trades values(2024.09.10,14:29:58.537,`B,20)
insert into trades values(2024.09.10,14:31:00.612,`A,10)
insert into trades values(2024.09.10,14:56:00.000,`B,29)

sleep(1000)
select * from output1
```

| timestamp | sym | sumVolume |
| --- | --- | --- |
| 2024.09.10T14:10:00.000 | A | 16 |
| 2024.09.10T14:10:00.000 | B | 9 |
| 2024.09.10T14:30:00.000 | A | 33 |
| 2024.09.10T14:30:00.000 | B | 35 |
| 2024.09.10T14:40:00.000 | A | 10 |
| 2024.09.10T14:57:00.000 | B | 29 |

例4.

设置 *keyPurgeDaily*=false, 则在收到第一批日期是 2024.09.11 的数据时，引擎不会清空日期是 2024.09.10
的分组数据。

```
share streamTable(1000:0, `date`second`sym`volume, [DATE, SECOND, SYMBOL, INT]) as trades
share table(10000:0, `time`sym`sumVolume, [DATETIME, SYMBOL, INT]) as output1
engine1 = createDailyTimeSeriesEngine(name="engine1", windowSize=30*60, step=30*60, metrics=<[sum(volume)]>, dummyTable=trades, outputTable=output1, timeColumn=`date`second, useSystemTime=false, keyColumn=`sym, garbageSize=50, useWindowStartTime=false, sessionBegin=09:30:00 13:00:00, sessionEnd=11:30:00 15:00:00,mergeSessionEnd=true, keyPurgeDaily=false, fill="null", forceTriggerTime=60)

insert into engine1 values(2024.09.10,13:00:10,`A,16)
insert into engine1 values(2024.09.10,13:00:12,`B,9)
insert into engine1 values(2024.09.10,13:00:12,`C,9)
insert into engine1 values(2024.09.10,14:59:56,`A,20)
insert into engine1 values(2024.09.10,14:59:58,`B,20)
insert into engine1 values(2024.09.10,15:00:00,`A,10)
insert into engine1 values(2024.09.10,15:00:00,`B,29)
insert into engine1 values(2024.09.11,09:30:02,`A,26)
insert into engine1 values(2024.09.11,09:30:10,`B,14)
insert into engine1 values(2024.09.11,10:30:46,`A,30)
insert into engine1 values(2024.09.11,10:30:50,`B,11)

select * from output1
```

| time | sym | sumVolume |
| --- | --- | --- |
| 2024.09.10T13:30:00 | A | 16 |
| 2024.09.10T13:30:00 | B | 9 |
| 2024.09.10T13:30:00 | C | 9 |
| 2024.09.10T14:00:00 | A | 11 |
| 2024.09.10T14:00:00 | B | 30 |
| 2024.09.10T14:00:00 | C | 13 |
| 2024.09.10T14:30:00 | A | 20 |
| 2024.09.10T14:30:00 | B | 20 |
| 2024.09.10T14:30:00 | C | 10 |
| 2024.09.10T15:00:00 | A | 30 |
| 2024.09.10T15:00:00 | B | 49 |
| 2024.09.10T15:00:00 | C |  |
| 2024.09.11T10:00:00 | A | 26 |
| 2024.09.11T10:00:00 | B | 14 |
| 2024.09.11T10:00:00 | C |  |
| 2024.09.11T10:30:00 | A |  |

从上表的结果可以看出，2024.09.11 的数据中未包含 C 分组，但由于引擎未删除 2024.09.10 中的 C 分组，因此填充结果中仍然出现了 C 分组。

例5. 将第二个 session 的时间调整为 13:00:00~15:00:30，并设置 *mergeLastWindow* 为 true。session
的起止时间将不进行规整，最后一个不完整的窗口 [15:00:00, 15:00:30) 的数据与前一个窗口 [14:59:00, 15:00:00)一同计算，合并为一个
[14:59:00,15:00:30)
窗口输出。

```
dropStreamEngine("engine1")
unsubscribeTable(tableName="trades", actionName="engine1")
undef(`trades, SHARED)
undef(`output1,SHARED)

share streamTable(1000:0, `date`second`sym`volume, [DATE, SECOND, SYMBOL, INT]) as trades
share keyedTable(`time`sym, 10000:0, `time`sym`sumVolume, [DATETIME, SYMBOL, INT]) as output1
engine1 = createDailyTimeSeriesEngine(name="engine1", windowSize=60, step=60, timeColumn=`date`second,
  metrics=<[sum(volume)]>, dummyTable=trades, outputTable=output1,
  useSystemTime=false, keyColumn=`sym, garbageSize=50,
  useWindowStartTime=false, sessionBegin=09:00:00 13:00:00,
  sessionEnd=11:30:00 15:00:30, roundTime=false, mergeLastWindow=true)
subscribeTable(tableName="trades", actionName="engine1", offset=0,
  handler=append!{engine1}, msgAsTable=true);

insert into trades values(2018.10.08,13:00:10,`A,16)
insert into trades values(2018.10.08,13:00:12,`B,9)
insert into trades values(2018.10.08,14:29:56,`A,20)
insert into trades values(2018.10.08,14:29:58,`B,20)
insert into trades values(2018.10.08,14:31:00,`A,10)
insert into trades values(2018.10.08,14:55:00,`B,29)
insert into trades values(2018.10.08,14:56:00,`B,29)
insert into trades values(2018.10.08,14:57:01,`A,29)
insert into trades values(2018.10.08,14:57:01,`B,29)
insert into trades values(2018.10.08,14:59:01,`B,29)
insert into trades values(2018.10.08,14:59:01,`A,29)
insert into trades values(2018.10.08,15:00:01,`B,29)
insert into trades values(2018.10.08,15:00:01,`A,29)
insert into trades values(2018.10.08,15:00:31,`B,29)
insert into trades values(2018.10.08,15:00:31,`A,29)
sleep(2000)
select * from output1
```

|  |  |  |
| --- | --- | --- |
| **Time** | **Symbol** | **Sum Volume** |
| 2018.10.08T13:01:00 | A | 16 |
| 2018.10.08T13:01:00 | B | 9 |
| 2018.10.08T14:30:00 | A | 20 |
| 2018.10.08T14:30:00 | B | 20 |
| 2018.10.08T14:56:00 | B | 29 |
| 2018.10.08T14:32:00 | A | 10 |
| 2018.10.08T14:57:00 | B | 29 |
| 2018.10.08T14:58:00 | A | 29 |
| 2018.10.08T14:58:00 | B | 29 |
| 2018.10.08T15:00:30 | A | 58 |
| 2018.10.08T15:00:30 | B | 58 |

**相关信息**

* [createTimeSeriesEngine](createTimeSeriesEngine.html "createTimeSeriesEngine")

