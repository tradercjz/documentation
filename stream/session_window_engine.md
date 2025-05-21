# 会话窗口引擎

会话窗口可以理解为一个活动阶段（数据产生阶段）。其前后都是非活动阶段（无数据产生阶段）。

会话窗口引擎与时间序列引擎极为相似，它们计算规则和触发计算的方式相同。不同之处在于时间序列引擎具有固定的窗口长度和滑动步长，但会话窗口引擎的窗口不是按照固定的频率产生的，其窗口长度也不是固定的。以引擎收到的第一条数据的时间戳作为第一个会话窗口的起始时间。会话窗口收到某条数据之后，若在指定的等待时间内仍未收到下一条新数据，则（该数据的时间戳
+ 等待时间）是该窗口的结束时间。窗口结束后收到的第一条新数据的时间戳是新的会话窗口的起始时间。

以物联网场景为例，根据设备在线时间段的不同，可能某些时间段有大量数据产生，而某些时间段完全没有数据。若对这类特征的数据进行滑动窗口计算，无数据的窗口会增加不必要的计算开销。因此
DolphinDB 开发了会话窗口引擎，以解决此类问题。

会话窗口引擎由 `createSessionWindowEngine` 函数创建。其语法如下：

`createSessionWindowEngine(name, sessionGap, metrics,
dummyTable, outputTable, [timeColumn], [useSystemTime=false], [keyColumn],
[updateTime], [useSessionStartTime=true], [snapshotDir],
[snapshotIntervalInMsgCount], [raftGroup], [forceTriggerTime])`

它的大多数参数与 createTimeSeriesEngine 相同，唯一不同的是 *sessionGap* 和 *useSessionStartTime*
两个参数。*sessionGap* 决定了一个会话窗口的结束时间，而 *useSessionStartTime*则决定输出表中时间列是以各个窗口的起始时刻还是结束时刻为准。

其他参数的详细含义可以参考：[createSessionWindowEngine](../funcs/c/createSessionWindowEngine.md)。

## 计算规则

若某条数据之后，经过 *sessionGap* 指定的时间长度内，没有新数据到来，就进行一次窗口截断（以截断前最后一条数据的时间戳 +
*sessionGap* 作为窗口的结束时刻）。窗口结束后新到来的一条数据将触发该窗口的计算。

注： 若指定了 *keyColumn*，则按照分组分别进行窗口计算。

## 应用示例

例1. 创建一个会话窗口引擎，在指定等待 5 毫秒内没有收到新数据时，该引擎就会结束当前窗口。

```
share streamTable(1000:0, `time`sym`volume, [TIMESTAMP, SYMBOL, INT]) as trades
output1 = table(10000:0, `time`sym`sumVolume, [TIMESTAMP, SYMBOL, INT])
engine_sw = createSessionWindowEngine(name = "engine_sw", sessionGap = 5, metrics = <sum(volume)>, dummyTable = trades, outputTable = output1, timeColumn = `time, keyColumn=`sym)
subscribeTable(tableName="trades", actionName="append_engine_sw", offset=0, handler=append!{engine_sw}, msgAsTable=true)

n = 5
timev = 2018.10.12T10:01:00.000 + (1..n)
symv=take(`A`B`C,n)
volumev = (1..n)%1000
insert into trades values(timev, symv, volumev)

n = 5
timev = 2018.10.12T10:01:00.010 + (1..n)
volumev = (1..n)%1000
symv=take(`A`B`C,n)
insert into trades values(timev, symv, volumev)

n = 6
timev = 2018.10.12T10:01:00.020 + 1 2 3 8 14 20
volumev = (1..n)%1000
symv=take(`A`B`C,n)
insert into trades values(timev, symv, volumev)

select * from output1;
```

输出返回：

| time | sym | sumVolume |
| --- | --- | --- |
| 2018.10.12T10:01:00.001 | A | 5 |
| 2018.10.12T10:01:00.002 | B | 7 |
| 2018.10.12T10:01:00.003 | C | 3 |
| 2018.10.12T10:01:00.011 | A | 5 |
| 2018.10.12T10:01:00.012 | B | 7 |
| 2018.10.12T10:01:00.013 | C | 3 |
| 2018.10.12T10:01:00.021 | A | 1 |
| 2018.10.12T10:01:00.022 | B | 2 |
| 2018.10.12T10:01:00.023 | C | 3 |

清理环境：

```
dropStreamEngine(`engine_sw)
unsubscribeTable(, tableName="trades", actionName="append_engine_sw")
```

重新创建会话引擎，此时指定 *forceTriggerTime* 为
1000ms，在引擎收到最后一条消息后，经过1000ms，将触发所有分组数据的计算和输出

```
share streamTable(1000:0, `time`sym`volume, [TIMESTAMP, SYMBOL, INT]) as trades
output1 = table(10000:0, `time`sym`sumVolume, [TIMESTAMP, SYMBOL, INT])
engine_sw = createSessionWindowEngine(name = "engine_sw", sessionGap = 5, metrics = <sum(volume)>, dummyTable = trades, outputTable = output1, timeColumn = `time, keyColumn=`sym, forceTriggerTime=1000)
subscribeTable(tableName="trades", actionName="append_engine_sw", offset=0, handler=append!{engine_sw}, msgAsTable=true)

n = 5
timev = 2018.10.12T10:01:00.000 + (1..n)
symv=take(`A`B`C,n)
volumev = (1..n)%1000
insert into trades values(timev, symv, volumev)

n = 5
timev = 2018.10.12T10:01:00.010 + (1..n)
volumev = (1..n)%1000
symv=take(`A`B`C,n)
insert into trades values(timev, symv, volumev)

n = 6
timev = 2018.10.12T10:01:00.020 + 1 2 3 8 14 20
volumev = (1..n)%1000
symv=take(`A`B`C,n)
insert into trades values(timev, symv, volumev)

sleep(1100)
select * from output1;
```

再次查询输出表，可以得到以下结果：

| time | sym | sumVolume |
| --- | --- | --- |
| 2018.10.12T10:01:00.001 | A | 5 |
| 2018.10.12T10:01:00.002 | B | 7 |
| 2018.10.12T10:01:00.003 | C | 3 |
| 2018.10.12T10:01:00.011 | A | 5 |
| 2018.10.12T10:01:00.012 | B | 7 |
| 2018.10.12T10:01:00.013 | C | 3 |
| 2018.10.12T10:01:00.021 | A | 1 |
| 2018.10.12T10:01:00.022 | B | 2 |
| 2018.10.12T10:01:00.023 | C | 3 |
| 2018.10.12T10:01:00.028 | A | 4 |
| 2018.10.12T10:01:00.034 | B | 5 |
| 2018.10.12T10:01:00.040 | C | 6 |

