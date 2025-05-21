# 时序聚合引擎

时间聚合引擎将数据基于时间进行窗口划分，并在窗口内进行聚合计算。DolphinDB 提供了三种时间序列引擎，分别为：

* 时间序列引擎（createTimeSeriesEngine），按照指定频率对时序数据进行滑动聚合计算，如计算 K
  线等。适用于物联网、数字货币、外汇等无固定交易时段的场景。
* 日级时间序列引擎（createDailyTimeSeriesEngine），是在时间序列引擎的基础上的进一步扩展。除了可以实现时序引擎的全部功能外，它还可以指定交易时间段，将一个自然日之内各个交易时段开始之前的所有未参与计算的数据，并入该交易时段的第一个窗口进行计算。适用于在股票、期货市场等有固定交易时段的场景。
* 会话窗口引擎（createSessionWindowEngine）。与时间序列引擎极为相似，它们计算规则和触发计算的方式相同。不同之处在于时间序列引擎具有固定的窗口长度和滑动步长，但会话窗口引擎的窗口不是按照固定的频率产生的，其窗口长度也不是固定的。适用于需要根据事件活跃度划分窗口的场景。

本节以时间序列引擎为例，介绍时序引擎在流计算中的应用。

## **应用示例**

### 示例1. 窗口边界规整

下例说明数据窗口如何规整以及流数据时序引擎如何进行计算。以下代码建立流数据表 *trades*，包含 time 和 volume 两列。创建时序引擎
streamAggr1，每 3 毫秒对过去 6 毫秒的数据计算 sum(volume)。time
列的精度为毫秒，模拟插入的数据流频率也设为每毫秒一条数据。

```
share streamTable(1000:0, `time`volume, [TIMESTAMP, INT]) as trades
outputTable = table(10000:0, `time`sumVolume, [TIMESTAMP, INT])
tradesAggregator = createTimeSeriesEngine(name="streamAggr1", windowSize=6, step=3, metrics=<[sum(volume)]>, dummyTable=trades, outputTable=outputTable, timeColumn=`time)
subscribeTable(tableName="trades", actionName="append_tradesAggregator", offset=0, handler=append!{tradesAggregator}, msgAsTable=true)
```

向流数据表 *trades* 中写入 10 条数据，并查看流数据表 *trades* 内容：

```
def writeData(t, n){
    timev = 2018.10.08T01:01:01.001 + timestamp(1..n)
    volumev = take(1, n)
    insert into t values(timev, volumev)
}
writeData(trades, 10)

select * from trades;
```

| time | volume |
| --- | --- |
| 2018.10.08T01:01:01.002 | 1 |
| 2018.10.08T01:01:01.003 | 1 |
| 2018.10.08T01:01:01.004 | 1 |
| 2018.10.08T01:01:01.005 | 1 |
| 2018.10.08T01:01:01.006 | 1 |
| 2018.10.08T01:01:01.007 | 1 |
| 2018.10.08T01:01:01.008 | 1 |
| 2018.10.08T01:01:01.009 | 1 |
| 2018.10.08T01:01:01.010 | 1 |
| 2018.10.08T01:01:01.011 | 1 |

再查看结果表 *outputTable*:

```
select * from outputTable;
```

| time | sumVolume |
| --- | --- |
| 2018.10.08T01:01:01.003 | 1 |
| 2018.10.08T01:01:01.006 | 4 |
| 2018.10.08T01:01:01.009 | 6 |

时序引擎根据收到的第一条数据时刻规整第一个窗口的起始时间后，窗口以 *step*
为步长移动。下面详细解释时序引擎的计算过程。为简便起见，以下提到时间时，省略相同的 2018.10.08T01:01:01
部分，只列出毫秒部分。基于第一行数据的时间 002，第一个窗口的起始时间规整为 000，到 002 结束，只包含 002 一条记录，计算被 003
记录触发，sum(volume) 的结果是 1；第二个窗口从 000 到 005，包含了 4 条数据，计算被 006 记录触发，计算结果为 4；第三个窗口从
003 到 008，包含 6 条数据，计算被 009 记录触发，计算结果为 6。虽然第四个窗口从 006 到 011 且含有 6
条数据，但是由于该窗口结束之后没有数据，所以该窗口的计算没有被触发。

若需要重复执行以上程序，应首先解除订阅，并将流数据表 *trades* 与时序引擎 streamAggr1 二者删除：

```
unsubscribeTable(tableName="trades", actionName="append_tradesAggregator")
undef(`trades, SHARED)
dropStreamEngine("streamAggr1")
```

### 示例2. 设置多个窗口

DolphinDB 时序聚合引擎支持多个窗口，可以为每个窗口设置相同或不同的算子。

下例说如何对相同的 *metrics* 按不同的 *windowSize* 聚合。以下代码建立流数据表 *trades*，包含
time 和 volume 两列。创建时序引擎 streamAggr1，每 3 毫秒对过去 6 毫秒和过去 12 毫秒的数据计算
`sum(volume)`。

```
share streamTable(1000:0, `time`volume, [TIMESTAMP, INT]) as trades
outputTable = table(10000:0, `time`sumVolume1`sumVolume2, [TIMESTAMP, INT,INT])
tradesAggregator = createTimeSeriesEngine(name="streamAggr1", windowSize=[6,12], step=3, metrics=[<sum(volume)>,<sum(volume)>], dummyTable=trades, outputTable=outputTable, timeColumn=`time)
subscribeTable(tableName="trades", actionName="append_tradesAggregator", offset=0, handler=append!{tradesAggregator}, msgAsTable=true)
```

```
def writeData(t, n){
    timev = 2018.10.08T01:01:01.001 + timestamp(1..n)
    volumev = take(1, n)
    insert into t values(timev, volumev)
}
writeData(trades, 20)

select * from trades;
```

再查看结果表 *outputTable*:

```
select * from outputTable;
```

| time | sumVolume1 | sumVolume2 |
| --- | --- | --- |
| 2018.10.08T01:01:01.003 | 1 | 1 |
| 2018.10.08T01:01:01.006 | 4 | 4 |
| 2018.10.08T01:01:01.009 | 6 | 7 |
| 2018.10.08T01:01:01.012 | 6 | 10 |
| 2018.10.08T01:01:01.015 | 6 | 12 |
| 2018.10.08T01:01:01.018 | 6 | 12 |
| 2018.10.08T01:01:01.021 | 6 | 12 |

### 示例3. *metrics* 指定多种表达式

DolphinDB 时序聚合引擎支持使用多种表达式进行实时计算。

* 一个或多个聚合函数

  ```
  tsAggregator = createTimeSeriesEngine(name="streamAggr1", windowSize=6, step=3, metrics=<sum(ask)>, dummyTable=quotes, outputTable=outputTable, timeColumn=`time)
  ```
* 使用聚合结果进行计算

  ```
  tsAggregator = createTimeSeriesEngine(name="streamAggr1", windowSize=6, step=3, metrics=<max(ask)-min(ask)>, dummyTable=quotes, outputTable=outputTable, timeColumn=`time)
  ```
* 对列与列的操作结果进行聚合计算

  ```
  tsAggregator = createTimeSeriesEngine(name="streamAggr1", windowSize=6, step=3, metrics=<max(ask-bid)>, dummyTable=quotes, outputTable=outputTable, timeColumn=`time)
  ```
* 输出多个聚合结果

  ```
  tsAggregator = createTimeSeriesEngine(name="streamAggr1", windowSize=6, step=3, metrics=<[max((ask-bid)/(ask+bid)*2), min((ask-bid)/(ask+bid)*2)]>, dummyTable=quotes, outputTable=outputTable, timeColumn=`time)
  ```
* 使用多参数聚合函数

  ```
  tsAggregator = createTimeSeriesEngine(name="streamAggr1", windowSize=6, step=3, metrics=<corr(ask,bid)>, dummyTable=quotes, outputTable=outputTable, timeColumn=`time)

  tsAggregator = createTimeSeriesEngine(name="streamAggr1", windowSize=6, step=3, metrics=<percentile(ask-bid,99)/sum(ask)>, dummyTable=quotes, outputTable=outputTable, timeColumn=`time)
  ```
* 使用自定义函数

  ```
  defg diff(x,y){
  	return sum(x)-sum(y)
  }
  tsAggregator = createTimeSeriesEngine(name="streamAggr1", windowSize=6, step=3, metrics=<diff(ask, bid)>, dummyTable=quotes, outputTable=outputTable, timeColumn=`time)
  ```
* 使用多个返回结果的函数

  ```
  defg sums(x){
  	return [sum(x),sum2(x)]
  }
  tsAggregator = createTimeSeriesEngine(name="streamAggr1", windowSize=6, step=3, metrics=<sums(ask) as `sumAsk`sum2Ask>, dummyTable=quotes, outputTable=outputTable, timeColumn=`time)
  ```

注： 不支持聚合函数嵌套调用，例如
`sum(spread(ask,bid))`。

### 示例4. 指定输出表的类型

计算结果可以输出到内存表或流数据表。输出到流数据表的数据无法更新或删除，但是可以通过流数据表将结果作为另一个引擎的数据源再次发布。

下例中，时序引擎 electricityAggregator1 订阅流数据表 *electricity*，进行移动均值计算，并将结果输出到流数据表
*outputTable1*。时序引擎 electricityAggregator2 订阅 *outputTable1*
表，并对移动均值计算结果求移动峰值。

```
share streamTable(1000:0,`time`voltage`current,[TIMESTAMP,DOUBLE,DOUBLE]) as electricity

//将第一个时序引擎的输出表定义为流数据表，可以再次订阅
share streamTable(10000:0,`time`avgVoltage`avgCurrent,[TIMESTAMP,DOUBLE,DOUBLE]) as outputTable1

electricityAggregator1 = createTimeSeriesEngine(name="electricityAggregator1", windowSize=10, step=10, metrics=<[avg(voltage), avg(current)]>, dummyTable=electricity, outputTable=outputTable1, timeColumn=`time, garbageSize=2000)
subscribeTable(tableName="electricity", actionName="avgElectricity", offset=0, handler=append!{electricityAggregator1}, msgAsTable=true)

//订阅计算结果，再次进行聚合计算
outputTable2 =table(10000:0, `time`maxVoltage`maxCurrent, [TIMESTAMP,DOUBLE,DOUBLE])
electricityAggregator2 = createTimeSeriesEngine(name="electricityAggregator2", windowSize=100, step=100, metrics=<[max(avgVoltage), max(avgCurrent)]>, dummyTable=outputTable1, outputTable=outputTable2, timeColumn=`time, garbageSize=2000)
subscribeTable(tableName="outputTable1", actionName="maxElectricity", offset=0, handler=append!{electricityAggregator2}, msgAsTable=true);

//向electricity表中插入500条数据
def writeData(t, n){
        timev = 2018.10.08T01:01:01.000 + timestamp(1..n)
        voltage = 1..n * 0.1
        current = 1..n * 0.05
        insert into t values(timev, voltage, current)
}
writeData(electricity, 500);
```

聚合计算结果:

```
select * from outputTable2;
```

| time | maxVoltage | maxCurrent |
| --- | --- | --- |
| 2018.10.08T01:01:01.100 | 8.45 | 4.225 |
| 2018.10.08T01:01:01.200 | 18.45 | 9.225 |
| 2018.10.08T01:01:01.300 | 28.45 | 14.225 |
| 2018.10.08T01:01:01.400 | 38.45 | 19.225 |
| 2018.10.08T01:01:01.500 | 48.45 | 24.225 |

若要对上述脚本进行重复使用，需先执行以下脚本以清除共享表、订阅以及流数据引擎：

```
unsubscribeTable(tableName="electricity", actionName="avgElectricity")
undef(`electricity, SHARED)
unsubscribeTable(tableName="outputTable1", actionName="maxElectricity")
undef(`outputTable1, SHARED)
dropStreamEngine("electricityAggregator1")
dropStreamEngine("electricityAggregator2")
```

### 示例5. 分组计算

下例中设定 *keyColumn* 参数为 sym，时序引擎将基于 sym 列对数据进行分组，然后在分组内进行窗口计算。

```
share streamTable(1000:0, `time`sym`volume, [TIMESTAMP, SYMBOL, INT]) as trades
outputTable = table(10000:0, `time`sym`sumVolume, [TIMESTAMP, SYMBOL, INT])
tradesAggregator = createTimeSeriesEngine(name="streamAggr1", windowSize=3, step=3, metrics=<[sum(volume)]>, dummyTable=trades, outputTable=outputTable, timeColumn=`time, useSystemTime=false, keyColumn=`sym, garbageSize=50)
subscribeTable(tableName="trades", actionName="append_tradesAggregator", offset=0, handler=append!{tradesAggregator}, msgAsTable=true)

def writeData(t, n){
    timev = 2018.10.08T01:01:01.001 + timestamp(1..n)
    symv =take(`A`B, n)
    volumev = take(1, n)
    insert into t values(timev, symv, volumev)
}

writeData(trades, 6)
```

为了方便观察，对 *trades* 表的 sym 列排序输出：

```
select * from trades order by sym
```

| time | sym | volume |
| --- | --- | --- |
| 2018.10.08T01:01:01.002 | A | 1 |
| 2018.10.08T01:01:01.004 | A | 1 |
| 2018.10.08T01:01:01.006 | A | 1 |
| 2018.10.08T01:01:01.003 | B | 1 |
| 2018.10.08T01:01:01.005 | B | 1 |
| 2018.10.08T01:01:01.007 | B | 1 |

分组计算结果：

```
select * from outputTable
```

| time | sym | sumVolume |
| --- | --- | --- |
| 2018.10.08T01:01:01.003 | A | 1 |
| 2018.10.08T01:01:01.006 | A | 1 |
| 2018.10.08T01:01:01.006 | B | 2 |

各组窗口规整后统一从 000 时间点开始，根据 *windowSize*=3 以及 *step*=3，每个组的窗口会按照
000-003-006 划分。

* (1) 在 003，B组有一条数据，但是由于B组在第一个窗口没有任何数据，不会进行计算，所以B组第一个窗口没有结果输出。
* (2) 004 的A组数据触发A组第一个窗口的计算。
* (3) 006 的A组数据触发A组第二个窗口的计算。
* (4) 007 的B组数据触发B组第二个窗口的计算。

如果进行分组聚合计算，流数据源中的每个分组中的 'timeColumn' 必须是递增的，但是整个数据源的 'timeColumn'
可以不是递增的；如果没有进行分组聚合，那么整个数据源的 'timeColumn' 必须是递增的，否则时序引擎的输出结果会与预期不符。

### 示例6. 设置 *updateTime* 参数，在窗口未结束前强制触发计算

时序聚合引擎如果没有指定 *updateTime*，一个数据窗口结束前，不会发生对该数据窗口数据的计算。若一个窗口长时间未触发计算，可以指定
*updateTime*，分多次触发当前窗口数据的计算。以下通过两个例子，帮助用户理解 *updateTime* 的作用。

首先创建流数据表并写入数据：

```
share streamTable(1000:0, `time`sym`volume, [TIMESTAMP, SYMBOL, INT]) as trades
insert into trades values(2018.10.08T01:01:01.785,`A,10)
insert into trades values(2018.10.08T01:01:02.125,`B,26)
insert into trades values(2018.10.08T01:01:10.263,`B,14)
insert into trades values(2018.10.08T01:01:12.457,`A,28)
insert into trades values(2018.10.08T01:02:10.789,`A,15)
insert into trades values(2018.10.08T01:02:12.005,`B,9)
insert into trades values(2018.10.08T01:02:30.021,`A,10)
insert into trades values(2018.10.08T01:04:02.236,`A,29)
insert into trades values(2018.10.08T01:04:04.412,`B,32)
insert into trades values(2018.10.08T01:04:05.152,`B,23);
```

* 不指定 *updateTime*：

  ```
  output1 = table(10000:0, `time`sym`sumVolume, [TIMESTAMP, SYMBOL, INT])
  agg1 = createTimeSeriesEngine(name="agg1", windowSize=60000, step=60000, metrics=<[sum(volume)]>, dummyTable=trades, outputTable=output1, timeColumn=`time, useSystemTime=false, keyColumn=`sym, garbageSize=50, useWindowStartTime=false)
  subscribeTable(tableName="trades", actionName="agg1", offset=0, handler=append!{agg1}, msgAsTable=true)

  sleep(10)

  select * from output1;
  ```

  | time | sym | sumVolume |
  | --- | --- | --- |
  | 2018.10.08T01:02:00.000 | A | 38 |
  | 2018.10.08T01:03:00.000 | A | 25 |
  | 2018.10.08T01:02:00.000 | B | 40 |
  | 2018.10.08T01:03:00.000 | B | 9 |
* 将 *updateTime* 设为 1000：

  ```
  output2 = keyedTable(`time`sym,10000:0, `time`sym`sumVolume, [TIMESTAMP, SYMBOL, INT])
  agg2 = createTimeSeriesEngine(name="agg2", windowSize=60000, step=60000, metrics=<[sum(volume)]>, dummyTable=trades, outputTable=output2, timeColumn=`time, useSystemTime=false, keyColumn=`sym, garbageSize=50, updateTime=1000, useWindowStartTime=false)
  subscribeTable(tableName="trades", actionName="agg2", offset=0, handler=append!{agg2}, msgAsTable=true)

  sleep(2010)

  select * from output2;
  ```

  | time | sym | sumVolume |
  | --- | --- | --- |
  | 2018.10.08T01:02:00.000 | A | 38 |
  | 2018.10.08T01:03:00.000 | A | 25 |
  | 2018.10.08T01:02:00.000 | B | 40 |
  | 2018.10.08T01:03:00.000 | B | 9 |
  | 2018.10.08T01:05:00.000 | B | 55 |
  | 2018.10.08T01:05:00.000 | A | 29 |

下面我们介绍以上两个例子在处理最后一个数据窗口（01:04:00.000 到
01:05:00.000）的区别。为简便起见，我们省略日期部分，只列出（小时:分钟:秒.毫秒）部分。假设 time 列时间亦为数据进入时序引擎的时刻。

(1) 在 01:04:04.236 时，A 分组的第一条记录到达后已经过 2000 毫秒，触发一次 A 组计算，输出表增加一条记录(01:05:00.000,
`A, 29)。

(2) 在 01:04:05.152 时的 B 组记录为 01:04:04.412 所在小窗口 [01:04:04.000, 01:04:05.000)
之后第一条记录，触发一次 B 组计算，输出表增加一条记录 (01:05:00.000,"B",32)。

(3) 2000 毫秒后，在 01:04:07.152 时，由于 01:04:05.152 时的 B 组记录仍未参与计算，触发一次 B 组计算，输出一条记录
(01:05:00.000,"B",55)。由于输出表的主键为 time 和 sym，并且输出表中已有 (01:05:00.000,"B",32)
这条记录，因此将该记录更新为 (01:05:00.000,"B",55)。

### 示例7. 为引擎开启快照

为引擎开启快照机制后，若引擎出现异常，可及时将它的状态恢复到最新的快照状态。以下例子，将帮助用户理解 *snapshotDir* 和
*snapshotIntervalInMsgCount* 的作用。如果启用
*snapshot*，引擎订阅流表时（subscribeTable），*handler* 必须是 appendMsg
函数，且必须指定 *handlerNeedMsgId*=true，用来记录快照的消息位置。

```
share streamTable(10000:0,`time`sym`price`id, [TIMESTAMP,SYMBOL,INT,INT]) as trades
output1 =table(10000:0, `time`sumprice, [TIMESTAMP,INT]);
Agg1 = createTimeSeriesEngine(name=`Agg1, windowSize=100, step=50, metrics=<sum(price)>, dummyTable=trades, outputTable=output1, timeColumn=`time, snapshotDir="/home/server1/snapshotDir", snapshotIntervalInMsgCount=100)
subscribeTable(server="", tableName="trades", actionName="Agg1",offset= 0, handler=appendMsg{Agg1}, msgAsTable=true, handlerNeedMsgId=true)

n=500
timev=timestamp(1..n) + 2021.03.12T15:00:00.000
symv = take(`abc`def, n)
pricev = int(1..n)
id = take(-1, n)
insert into trades values(timev, symv, pricev, id)

select * from output1
```

| time | sumprice |
| --- | --- |
| 2021.03.12T15:00:00.050 | 1225 |
| 2021.03.12T15:00:00.100 | 4950 |
| 2021.03.12T15:00:00.150 | 9950 |
| 2021.03.12T15:00:00.200 | 14950 |
| 2021.03.12T15:00:00.250 | 19950 |
| 2021.03.12T15:00:00.300 | 24950 |
| 2021.03.12T15:00:00.350 | 29950 |
| 2021.03.12T15:00:00.400 | 34950 |
| 2021.03.12T15:00:00.450 | 39950 |
| 2021.03.12T15:00:00.500 | 44950 |

```
getSnapshotMsgId(Agg1)
 >499
```

取消订阅并删除引擎来模拟系统异常

```
unsubscribeTable(, "trades", "Agg1")
dropStreamEngine("Agg1")
Agg1=NULL
```

此时发布端仍在写入数据

```
n=500
timev=timestamp(501..1000) + 2021.03.12T15:00:00.000
symv = take(`abc`def, n)
pricev = int(1..n)
id = take(-1, n)
insert into trades values(timev, symv, pricev, id)
```

再次创建 Agg1, 加载 snapshot，从上次处理最后一条消息开始重新订阅

```
Agg1 = createTimeSeriesEngine(name=`Agg1, windowSize=100, step=50, metrics=<sum(price)>, dummyTable=trades, outputTable=output1, timeColumn=`time, snapshotDir="/home/server1/snapshotDir", snapshotIntervalInMsgCount=100)

ofst=getSnapshotMsgId(Agg1)
print(ofst)
>499

subscribeTable(server="", tableName="trades", actionName="Agg1",offset=ofst+1, handler=appendMsg{Agg1}, msgAsTable=true, handlerNeedMsgId=true)

select * from output1
```

| time | sumprice |
| --- | --- |
| 2021.03.12T15:00:00.050 | 1225 |
| 2021.03.12T15:00:00.100 | 4950 |
| 2021.03.12T15:00:00.150 | 9950 |
| 2021.03.12T15:00:00.200 | 14950 |
| 2021.03.12T15:00:00.250 | 19950 |
| 2021.03.12T15:00:00.300 | 24950 |
| 2021.03.12T15:00:00.350 | 29950 |
| 2021.03.12T15:00:00.400 | 34950 |
| 2021.03.12T15:00:00.450 | 39950 |
| 2021.03.12T15:00:00.500 | 44950 |
| **2021.03.12T15:00:00.550** | **25450** |
| **2021.03.12T15:00:00.600** | **5450** |
| 2021.03.12T15:00:00.650 | 9950 |
| 2021.03.12T15:00:00.700 | 14950 |
| 2021.03.12T15:00:00.750 | 19950 |
| 2021.03.12T15:00:00.800 | 24950 |
| 2021.03.12T15:00:00.850 | 29950 |
| 2021.03.12T15:00:00.900 | 34950 |
| 2021.03.12T15:00:00.950 | 39950 |
| 2021.03.12T15:00:01.000 | 44950 |

结果和订阅不中断一样。

```
share streamTable(10000:0,`time`sym`price`id, [TIMESTAMP,SYMBOL,INT,INT]) as trades
output1 =table(10000:0, `time`sumprice, [TIMESTAMP,INT]);
Agg1 = createTimeSeriesEngine(name=`Agg1, windowSize=100, step=50, metrics=<sum(price)>, dummyTable=trades, outputTable=output1, timeColumn=`time)
subscribeTable(server="", tableName="trades", actionName="Agg1",offset= 0, handler=append!{Agg1}, msgAsTable=true)

n=500
timev=timestamp(1..n) + 2021.03.12T15:00:00.000
symv = take(`abc`def, n)
pricev = int(1..n)
id = take(-1, n)
insert into trades values(timev, symv, pricev, id)

n=500
timev=timestamp(501..1000) + 2021.03.12T15:00:00.000
symv = take(`abc`def, n)
pricev = int(1..n)
id = take(-1, n)
insert into trades values(timev, symv, pricev, id)

select * from output1
```

| time | sumprice |
| --- | --- |
| 2021.03.12T15:00:00.050 | 1225 |
| 2021.03.12T15:00:00.100 | 4950 |
| 2021.03.12T15:00:00.150 | 9950 |
| 2021.03.12T15:00:00.200 | 14950 |
| 2021.03.12T15:00:00.250 | 19950 |
| 2021.03.12T15:00:00.300 | 24950 |
| 2021.03.12T15:00:00.350 | 29950 |
| 2021.03.12T15:00:00.400 | 34950 |
| 2021.03.12T15:00:00.450 | 39950 |
| 2021.03.12T15:00:00.500 | 44950 |
| **2021.03.12T15:00:00.550** | **25450** |
| **2021.03.12T15:00:00.600** | **5450** |
| 2021.03.12T15:00:00.650 | 9950 |
| 2021.03.12T15:00:00.700 | 14950 |
| 2021.03.12T15:00:00.750 | 19950 |
| 2021.03.12T15:00:00.800 | 24950 |
| 2021.03.12T15:00:00.850 | 29950 |
| 2021.03.12T15:00:00.900 | 34950 |
| 2021.03.12T15:00:00.950 | 39950 |
| 2021.03.12T15:00:01.000 | 44950 |

如果不开启 snapshot，即使从上次中断的地方开始订阅，得到的结果也与订阅不中断不一样。

```
share streamTable(10000:0,`time`sym`price`id, [TIMESTAMP,SYMBOL,INT,INT]) as trades
output1 =table(10000:0, `time`sumprice, [TIMESTAMP,INT]);
Agg1 = createTimeSeriesEngine(name=`Agg1, windowSize=100, step=50, metrics=<sum(price)>, dummyTable=trades, outputTable=output1, timeColumn=`time)
subscribeTable(server="", tableName="trades", actionName="Agg1",offset= 0, handler=append!{Agg1}, msgAsTable=true)

n=500
timev=timestamp(1..n) + 2021.03.12T15:00:00.000
symv = take(`abc`def, n)
pricev = int(1..n)
id = take(-1, n)
insert into trades values(timev, symv, pricev, id)

unsubscribeTable(, "trades", "Agg1")
dropStreamEngine("Agg1")
Agg1=NULL

n=500
timev=timestamp(501..1000) + 2021.03.12T15:00:00.000
symv = take(`abc`def, n)
pricev = int(1..n)
id = take(-1, n)
insert into trades values(timev, symv, pricev, id)

Agg1 = createTimeSeriesEngine(name=`Agg1, windowSize=100, step=50, metrics=<sum(price)>, dummyTable=trades, outputTable=output1, timeColumn=`time)
subscribeTable(server="", tableName="trades", actionName="Agg1",offset= 500, handler=append!{Agg1}, msgAsTable=true)

select * from output1
```

| time | sumprice |
| --- | --- |
| 2021.03.12T15:00:00.050 | 1225 |
| 2021.03.12T15:00:00.100 | 4950 |
| 2021.03.12T15:00:00.150 | 9950 |
| 2021.03.12T15:00:00.200 | 14950 |
| 2021.03.12T15:00:00.250 | 19950 |
| 2021.03.12T15:00:00.300 | 24950 |
| 2021.03.12T15:00:00.350 | 29950 |
| 2021.03.12T15:00:00.400 | 34950 |
| 2021.03.12T15:00:00.450 | 39950 |
| 2021.03.12T15:00:00.500 | 44950 |
| **2021.03.12T15:00:00.550** | **1225** |
| **2021.03.12T15:00:00.600** | **4950** |
| 2021.03.12T15:00:00.650 | 9950 |
| 2021.03.12T15:00:00.700 | 14950 |
| 2021.03.12T15:00:00.750 | 19950 |
| 2021.03.12T15:00:00.800 | 24950 |
| 2021.03.12T15:00:00.850 | 29950 |
| 2021.03.12T15:00:00.900 | 34950 |
| 2021.03.12T15:00:00.950 | 39950 |
| 2021.03.12T15:00:01.000 | 44950 |

### 示例8. 过滤订阅数据

使用 `subscribeTable` 函数时，可利用 *handler* 参数过滤订阅的流数据。

在下例中，传感器采集电压和电流数据并实时上传作为流数据源，其中电压 voltage<=122 或电流 current=NULL
的数据需要在进入时序引擎之前过滤掉。

```
share streamTable(1000:0, `time`voltage`current, [TIMESTAMP, DOUBLE, DOUBLE]) as electricity
outputTable = table(10000:0, `time`avgVoltage`avgCurrent, [TIMESTAMP, DOUBLE, DOUBLE])

//自定义数据处理过程，过滤 voltage<=122 或 current=NULL的无效数据。
def append_after_filtering(inputTable, msg){
	t = select * from msg where voltage>122, isValid(current)
	if(size(t)>0){
		insert into inputTable values(t.time,t.voltage,t.current)
	}
}
electricityAggregator = createTimeSeriesEngine(name="electricityAggregator", windowSize=6, step=3, metrics=<[avg(voltage), avg(current)]>, dummyTable=electricity, outputTable=outputTable, timeColumn=`time, garbageSize=2000)
subscribeTable(tableName="electricity", actionName="avgElectricity", offset=0, handler=append_after_filtering{electricityAggregator}, msgAsTable=true)

//模拟产生数据
def writeData(t, n){
        timev = 2018.10.08T01:01:01.001 + timestamp(1..n)
        voltage = 120+1..n * 1.0
        current = take([1,NULL,2]*0.1, n)
        insert into t values(timev, voltage, current);
}
writeData(electricity, 10)
```

流数据表：

```
select * from electricity
```

| time | voltage | current |
| --- | --- | --- |
| 2018.10.08T01:01:01.002 | 121 | 0.1 |
| 2018.10.08T01:01:01.003 | 122 |  |
| 2018.10.08T01:01:01.004 | 123 | 0.2 |
| 2018.10.08T01:01:01.005 | 124 | 0.1 |
| 2018.10.08T01:01:01.006 | 125 |  |
| 2018.10.08T01:01:01.007 | 126 | 0.2 |
| 2018.10.08T01:01:01.008 | 127 | 0.1 |
| 2018.10.08T01:01:01.009 | 128 |  |
| 2018.10.08T01:01:01.010 | 129 | 0.2 |
| 2018.10.08T01:01:01.011 | 130 | 0.1 |

聚合计算结果：

```
select * from outputTable
```

| time | avgVoltage | avgCurrent |
| --- | --- | --- |
| 2018.10.08T01:01:01.006 | 123.5 | 0.15 |
| 2018.10.08T01:01:01.009 | 125 | 0.15 |

由于 voltage<=122 或 current=NULL 的数据已经在进入时序引擎时被过滤了，所以第一个窗口 [000,003)
里没有数据，也就没有发生计算。

