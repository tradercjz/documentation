# 异常检测引擎

物联网设备（如机床、锅炉、电梯、水表、气表等）无时无刻不在产生海量的设备状态数据和业务消息数据。在这些数据的采集、计算和分析过程中，常常需要进行异常数据的检测。

为满足这一需求，DolphinDB
提供了基于流数据框架的异常检测引擎函数。用户只需指定异常指标，异常检测引擎就可以实时地进行异常数据检测。该引擎会根据用户指定的条件指标，自动筛查数据，并仅输出符合指标条件的数据。它常用于对实时数据进行监控的场景，因此在物联网场景下有较广泛的应用，金融领域的风控场景也可以使用该引擎。

* 物联网：对设备进行监测，例如监测设备温度、湿度；电力监控，例如电压，用电量等。
* 金融：风控场景，例如根据指定规则过滤订单，监控股票成交量，设置超量预警信号等。

## 概念介绍

异常检测引擎由 `createAnomalyDetectionEngine` 函数创建。语法如下：

`createAnomalyDetectionEngine(name, metrics, dummyTable,
outputTable, timeColumn, [keyColumn], [windowSize], [step], [garbageSize],
[roundTime=true], [snapshotDir], [snapshotIntervalInMsgCount],
[raftGroup],[anomalyDescription])`

### 异常指标

异常指标是以元代码的格式提供一组处理流数据的布尔表达式。通常是一个函数或一个表达式，其中可以包含聚合函数，以支持复杂的场景。当指标中包含聚合函数时，必须指定窗口长度和计算的时间间隔，每隔一段时间，在固定长度的移动窗口中计算指标。

异常指标一般有以下三种类型：

* 某个列与常量对比、列与列之间对比或非聚合函数中没有嵌套聚合函数，例如 qty < 4, qty > price, lt(qty,
  prev(qty)), isNull(qty) == false
  等。对于这类指标，异常检测引擎会对每一条数据进行计算，判断是否符合条件并决定输出。
* 聚合函数的结果与某个常量值对比、聚合函数结果之间的对比、非聚合函数中仅嵌套聚合函数和常量，例如 avg(qty - price) > 10,
  percentile(qty, 90) < 100, max(qty) < avg(qty) \* 2, le(sum(qty), 5)
  等。对于这类指标，异常检测引擎会在每个窗口计算时判断计算结果是否符合条件并决定输出。
* 聚合函数的结果与列对比、非聚合函数中同时嵌套聚合函数和列，例如 avg(qty) > qty, le(med(qty), price)
  等。对于这类指标，每当数据到达时，异常检测引擎会将数据与上一个计算窗口的聚合结果对比，判断计算结果是否符合条件并决定输出，直到触发下一次聚合计算。

### 数据窗口

当异常指标中包含聚合函数时，用户必须指定数据窗口。流数据聚合计算是每隔一段时间，在固定长度的移动窗口中进行。窗口长度由参数 *windowSize*
设定；计算的时间间隔由参数 *step* 设定。

在有多组数据的情况下，若每组都根据各自第一条数据进入系统的时间来构造数据窗口的边界，则一般无法将各组的计算结果在相同数据窗口中进行对比。考虑到这一点，系统按照参数
*step* 值确定一个整型的规整尺度 *alignmentSize* ，以对各组第一个数据窗口的边界值进行规整处理。

* 当数据时间类型为MONTH时，会以第一条数据对应年份的1月作为窗口的上边界。
* 当数据的时间类型为DATE时，不对第一个数据窗口的边界值进行规整。
* 若数据的时间精度为分钟，如 MINUTE(HH:mm) 类型，alignmentSize 取值如下：

  *若 roundTime = false*：

  | step | alignmentSize |
  | --- | --- |
  | 0~2 | 2 |
  | 3 | 3 |
  | 4~5 | 5 |
  | 6~10 | 10 |
  | 11~15 | 15 |
  | 16~20 | 20 |
  | 21~30 | 30 |
  | >30 | 60 (1小时) |

  *若 roundTime = true*:

  当 step <= 30 时，alignmentSize 取值同上表。当 step > 30
  时，alignmentSize 取值见下表：

  | step | alignmentSize |
  | --- | --- |
  | 31~60 | 60 (1小时) |
  | 61~120 | 120 (2小时) |
  | 121~180 | 180 (3小时) |
  | 181~300 | 300 (5小时) |
  | 301~600 | 600 (10小时) |
  | 601~900 | 900 (15小时) |
  | 901~1200 | 1200 (20小时) |
  | 1201~1800 | 1800 (30小时) |
  | >1800 | 3600 (60小时) |
* 若数据的时间精度为秒，如 DATETIME(yyyy-MM-dd HH:mm:ss) 与
  SECOND(HH:mm:ss) 类型，alignmentSize 的 取值如下：

  *若
  roundTime = false*：

  | step | alignmentSize |
  | --- | --- |
  | 0~2 | 2 |
  | 3 | 3 |
  | 4~5 | 5 |
  | 6~10 | 10 |
  | 11~15 | 15 |
  | 16~20 | 20 |
  | 21~30 | 30 |
  | >30 | 60 (1分钟) |

  *若 roundTime = true*：

  当 step <= 30
  时，alignmentSize 取值同上表。当 step > 30 时，alignmentSize 取值见下表：

  | step | alignmentSize |
  | --- | --- |
  | 31~60 | 60 (1分钟) |
  | 61~120 | 120 (2分钟) |
  | 121~180 | 180 (3分钟) |
  | 181~300 | 300 (5分钟) |
  | 301~600 | 600 (10分钟) |
  | 601~900 | 900 (15分钟) |
  | 901~1200 | 1200 (20分钟) |
  | 1201~1800 | 1800 (30分钟) |
  | >1800 | 3600 (1小时) |
* 若数据的时间精度为毫秒，如 TIMESTAMP(yyyy-MM-dd HH:mm:ss.mmm) 与
  TIME(HH:mm:ss.mmm) 类型，alignmentSize 的取值如下：

  *若 roundTime = false*:

  | step | alignmentSize |
  | --- | --- |
  | 0~2 | 2 |
  | 3~5 | 5 |
  | 6~10 | 10 |
  | 11~20 | 20 |
  | 21~25 | 25 |
  | 26~50 | 50 |
  | 51~100 | 100 |
  | 101~200 | 200 |
  | 201~250 | 250 |
  | 251~500 | 500 |
  | 501~1000 | 1000（1秒） |
  | 1001~2000 | 2000（2秒） |
  | 2001~3000 | 3000（3秒） |
  | 3001~5000 | 5000（5秒） |
  | 5001~10000 | 10000（10秒） |
  | 10001~15000 | 15000（15秒） |
  | 15001~20000 | 20000（20秒） |
  | 20001~30000 | 30000（30秒） |
  | >30000 | 60000（1分钟） |

  *若 roundTime = true*:

  若 *step* <= 30000，alignmentSize 取值同上表；若
  *step* > 30000，alignmentSize 取值见下表：

  | step | alignmentSize |
  | --- | --- |
  | 30001~60000 | 60000（1分钟） |
  | 60001~120000 | 120000（2分钟） |
  | 120001~300000 | 300000（5分钟） |
  | 300001~600000 | 600000（10分钟） |
  | 600001~900000 | 900000（15分钟） |
  | 900001~1200000 | 1200000（20分钟） |
  | 1200001~1800000 | 1800000（30分钟） |
  | >1800000 | 3600000（1小时） |
* 若数据的时间精度为纳秒，如 NANOTIMESTAMP(yyyy-MM-dd
  HH:mm:ss.nnnnnnnnn) 与 NANOTIME(HH:mm:ss.nnnnnnnnn) 类型，alignmentSize
  的取值如下：

  *若 roundTime = false*:

  | step | alignmentSize |
  | --- | --- |
  | 0~2ns | 2ns |
  | 3ns~5ns | 5ns |
  | 6ns~10ns | 10ns |
  | 11ns~20ns | 20ns |
  | 21ns~25ns | 25ns |
  | 26ns~50ns | 50ns |
  | 51ns~100ns | 100ns |
  | 101ns~200ns | 200ns |
  | 201ns~250ns | 250ns |
  | 251ns~500ns | 500ns |
  | >500ns | 1000ns |

  *若 roundTime = true*:

  | step | alignmentSize |
  | --- | --- |
  | 1000ns~1ms | 1ms |
  | 1ms~10ms | 10ms |
  | 10ms~100ms | 100ms |
  | 100ms~1s | 1s |
  | 1s~2s | 2s |
  | 2s~3s | 3s |
  | 3s~5s | 5s |
  | 5s~10s | 10s |
  | 10s~15s | 15s |
  | 15s~20s | 20s |
  | 20s~30s | 30s |
  | >30s | 1min |

假设第一条数据的时间为 x,
那么根据其类型，第一个数据窗口的左边界的计算规则为：`timeType_cast(x/alignmentSize*alignmentSize+step-windowSize)`。其中，timeType\_cast
表示依据时间精度，需要强制转换的时间类型；'/' 表示整除。例如，第一条数据的时间为 2018.10.08T01:01:01.365，windowSize 为
120000，step 为 60000，那么 alignmentSize 为 60000，第一个数据窗口的左边界为
`timestamp(2018.10.08T01:01:01.365/60000*60000+60000-120000)`，即
2018.10.08T01:00:00.000。

## 应用示例1

现模拟传感器设备采集温度。假设窗口长度为 4ms，每隔 2ms 移动一次窗口，每隔 1ms 采集一次温度，规定以下异常指标：

1. 单次采集的温度超过 65；
2. 单次采集的温度超过上一个窗口中 75% 的值；

采集的数据存放到流数据表中，异常检测引擎通过订阅流数据表来获取实时数据，并进行异常检测，符合异常指标的数据输出到另外一个表中。

实现步骤如下：

（1） 定义流数据表 *sensor* 来存放采集的数据：

```
share streamTable(1000:0, `time`temp, [TIMESTAMP, DOUBLE]) as sensor
```

（2） 定义异常检测引擎和输出表 *outputTable*，输出表也是流数据表：

```
share streamTable(1000:0, `time`anomalyType`anomalyString, [TIMESTAMP, INT, SYMBOL]) as outputTable
engine = createAnomalyDetectionEngine(name="engine1", metrics=<[temp > 65, temp > percentile(temp, 75)]>, dummyTable=sensor, outputTable=outputTable, timeColumn=`time, windowSize=6, step=3)
```

（3） 异常检测引擎 engine 订阅流数据表 *sensor*：

```
subscribeTable(, "sensor", "sensorAnomalyDetection", 0, append!{engine}, true)
```

（4） 向流数据表 *sensor* 中写入 10 次数据模拟采集温度：

```
timev = 2018.10.08T01:01:01.001 + 1..10
tempv = 59 66 57 60 63 51 53 52 56 55
insert into sensor values(timev, tempv)
```

查看流数据表 *sensor* 的内容：

| time | temp |
| --- | --- |
| 2018.10.08T01:01:01.002 | 59 |
| 2018.10.08T01:01:01.003 | 66 |
| 2018.10.08T01:01:01.004 | 57 |
| 2018.10.08T01:01:01.005 | 60 |
| 2018.10.08T01:01:01.006 | 63 |
| 2018.10.08T01:01:01.007 | 51 |
| 2018.10.08T01:01:01.008 | 53 |
| 2018.10.08T01:01:01.009 | 52 |
| 2018.10.08T01:01:01.010 | 56 |
| 2018.10.08T01:01:01.011 | 55 |

再查看结果表 *outputTable* ：

| time | anomalyType | anomalyString |
| --- | --- | --- |
| 2018.10.08T01:01:01.003 | 0 | temp > 65 |
| 2018.10.08T01:01:01.003 | 1 | temp > percentile(temp, 75) |
| 2018.10.08T01:01:01.005 | 1 | temp > percentile(temp, 75) |
| 2018.10.08T01:01:01.006 | 1 | temp > percentile(temp, 75) |

下面详细解释异常检测引擎的计算过程。为方便阅读，对时间的描述中省略相同的 2018.10.08T01:01:01 部分，只列出毫秒部分。

（1）指标`temp > 65`只包含不作为函数参数的列 temp，因此会在每条数据到达时计算。模拟数据中只有 003
时的温度满足检测异常的指标。

（2）指标`temp > percentile(temp, 75)`中，temp
列既作为聚合函数`percentile`的参数，又单独出现，因此会在每条数据到达时，将其中的`temp`与上一个窗口计算得到的`percentile(temp,
75)`比较。第一个窗口基于第一行数据的时间 002 进行对齐，对齐后窗口起始边界为 000，第一个窗口是从 000 到 002，只包含
002 一条记录，计算`percentile(temp, 75)`的结果是 59，数据 003 到 005
与这个值比较，满足条件的有 003 和 005。第二个窗口是从 002 到 005，计算`percentile(temp,
75)`的结果是 60，数据 006 到 008 与这个值比较，满足条件的有 006。第三个窗口是从 003 到
008，计算`percentile(temp, 75)`的结果是 63，数据 009 到 011
与这个值比较，其中没有满足条件的行。最后一条数据 011 到达后，尚未触发新的窗口计算。

监控异常检测引擎的状态

```
getStreamEngineStat().AnomalyDetectionEngine
```

| name | user | status | lastErrMsg | numGroups | numRows | numMetrics | metrics | snapshotDir | snapshotInterval | snapshotMsgId | snapshotTimestamp | garbageSize | memoryUsed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| engine1 | admin | OK |  | 1 | 10 | 2 | temp > 65, temp > percentile(temp, 75) |  |  | -1 |  | 2,000 | 8,524 |

## 应用例子 2

快照机制可以用于系统出现异常之后，对引擎进行恢复。通过以下这个例子，可以理解 *snapshotDir* 和
*snapshotIntervalInMsgCount* 的作用。如果启用snapshot，引擎订阅流表时，*handler* 需是
`appendMsg` 函数，需指定 *handlerNeedMsgId* =
true，用来记录快照的消息位置。

```
WORK_DIR="/home/root/WORK_DIR"
mkdir(WORK_DIR+"/snapshotDir")
enableTableShareAndPersistence(table = streamTable(10000:0,`time`sym`price`qty, [TIMESTAMP,SYMBOL,DOUBLE,INT]) , tableName="trades", cacheSize=1000000)
enableTableShareAndPersistence(table = streamTable(10000:0, `time`sym`type`metric, [TIMESTAMP,STRING,INT,STRING]), tableName = "output", cacheSize=1000000)
go

adengine = createAnomalyDetectionEngine(name="test", metrics=<[avg(qty)>1]>, dummyTable=trades, outputTable=output, timeColumn=`time, keyColumn=`sym, windowSize=10, step=10, snapshotDir=WORK_DIR+"/snapshotDir", snapshotIntervalInMsgCount=100)
subscribeTable(server="", tableName="trades", actionName="adengine",offset= 0, handler=appendMsg{adengine}, msgAsTable=true, handlerNeedMsgId=true)

def writeData(mutable t){
do{
batch = 10
tmp = table(batch:batch, `time`sym`price`qty, [TIMESTAMP, SYMBOL, DOUBLE, DOUBLE])
tmp[`time] = take(now(), batch)
tmp[`sym] = "A"+string(1..batch)
tmp[`price] = round(rand(100.0, batch), 2)
tmp[`qty] = rand(10, batch)
t.append!(tmp)
sleep(1000)
}while(true)
}

job1=submitJob("write", "", writeData, trades)
//执行一段时间后重启server

enableTableShareAndPersistence(table = streamTable(10000:0,`time`sym`price`qty, [TIMESTAMP,SYMBOL,DOUBLE,INT]) , tableName="trades", cacheSize=1000000)
enableTableShareAndPersistence(table = streamTable(10000:0, `time`sym`type`metric, [TIMESTAMP,STRING,INT,STRING]), tableName = "output", cacheSize=1000000)

select last(time) from output
>2021.03.16T11:59:10.920

select last(time) from trades
>2021.03.16T11:59:13.916

WORK_DIR="/home/root/WORK_DIR"
adengine = createAnomalyDetectionEngine(name="test", metrics=<[avg(qty)>qty]>, dummyTable=trades, outputTable=output, timeColumn=`time, keyColumn=`sym, windowSize=10, step=10, snapshotDir=WORK_DIR+"/snapshotDir", snapshotIntervalInMsgCount=100)

ofst = getSnapshotMsgId(adengine)
print(ofst)
>299

select count(*) from trades
>390

//从第300条数据开始订阅
subscribeTable(server="", tableName="trades", actionName="adengine",offset=ofst+1, handler=appendMsg{adengine}, msgAsTable=true, handlerNeedMsgId=true)
```

