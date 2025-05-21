# getStreamEngineStat

## 语法

`getStreamEngineStat()`

别名：`getAggregatorStat`

## 参数

无

## 详情

返回流数据引擎的状态。返回一个字典，包含以下表：

* 表 TimeSeriesEngine 返回时间序列引擎的状态。它包含以下列：

| 列名 | 含义 |
| --- | --- |
| name | 时间序列引擎的名称 |
| user | 创建时间序列引擎的用户名 |
| status | 时间序列引擎的状态，"OK"表示可用，"FATAL"表示不可用 |
| lastErrMsg | 最后一条错误信息 |
| windowTime | 窗口的长度 |
| step | 计算的时间间隔 |
| useSystemTime | 时间序列引擎中 useSystemTime 参数值 |
| garbageSize | 触发内存清理的阈值 |
| numGroups | 时间序列引擎中的分组数 |
| numRows | 时间序列引擎中的记录行数 |
| numMetrics | 时间序列引擎使用的聚合指标的数量 |
| metrics | 时间序列引擎使用的聚合指标的元代码 |
| memoryUsed | 时间序列引擎所占用内存量，单位为字节 |
| snapshotDir | 保存引擎快照的文件目录 |
| snapshotInterval | 每隔多少条数据保存一次引擎快照 |
| snapshotMsgId | 最后一个 snapshot 的 msgId |
| snapshotTimestamp | 引擎快照的时间戳 |

* 表 CrossSectionalEngine 返回横截面聚合引擎的状态。它包含以下列：

| 列名 | 含义 |
| --- | --- |
| name | 横截面引擎的名称 |
| user | 创建横截面引擎的用户名 |
| status | 横截面引擎的状态，"OK" 表示可用，"FATAL" 表示不可用 |
| lastErrMsg | 最后一条错误信息 |
| numRows | 横截面引擎中的记录行数 |
| numMetrics | 横截面引擎使用的聚合指标的数量 |
| metrics | 横截面引擎使用的聚合指标的元代码 |
| triggeringPattern | 横截面引擎触发计算的方式 |
| triggeringInterval | 横截面引擎触发计算的时间间隔 |
| memoryUsed | 横截面引擎所占用内存量，单位为字节 |

* 表 AnomalyDetectionEngine 返回异常检测引擎的状态。它包含以下列：

| 列名 | 含义 |
| --- | --- |
| name | 异常检测引擎的名称 |
| user | 创建异常检测引擎的用户名 |
| status | 异常检测引擎的状态，"OK" 表示可用，"FATAL" 表示不可用 |
| lastErrMsg | 最后一条错误信息 |
| numGroups | 异常检测引擎中的分组数 |
| numRows | 异常检测引擎中的记录行数 |
| numMetrics | 异常指标的数量 |
| metrics | 异常指标的元代码 |
| snapshotDir | 保存引擎快照的文件目录 |
| snapshotInterval | 每隔多少条数据保存一次引擎快照 |
| snapshotMsgId | 最后一个 snapshot 的 msgId |
| snapshotTimestam | 引擎快照的时间戳 |
| garbageSize | 触发内存清理的阈值 |
| memoryUsed | 异常检测引擎所占用内存量，单位为字节 |

* 表 ReactiveStreamEngine 返回响应式状态引擎的状态。它包含以下列：

| 列名 | 含义 |
| --- | --- |
| name | 响应式状态引擎的名称 |
| user | 创建响应式状态引擎的用户名 |
| status | 响应式状态引擎的状态，"OK" 表示可用，"FATAL" 表示不可用 |
| lastErrMsg | 最后一条错误信息 |
| numGroups | 响应式状态引擎中的分组数 |
| numRows | 响应式状态引擎中的记录行数 |
| numMetrics | 指标的数量 |
| memoryInUsed | 响应式状态引擎所占用内存量，单位为字节 |
| snapshotDir | 保存引擎快照的文件目录 |
| snapshotInterval | 每隔多少条数据保存一次引擎快照 |
| snapshotMsgId | 最后一个 snapshot 的 msgId |
| snapshotTimestamp | 引擎快照的时间戳 |

* 表 SessionWindowEngine 返回会话窗口引擎的状态。它包含以下列：

| 列名 | 含义 |
| --- | --- |
| name | 会话窗口引擎的名称 |
| user | 创建会话窗口引擎的用户名 |
| status | 会话窗口引擎的状态，"OK" 表示可用，"FATAL" 表示不可用 |
| lastErrMsg | 最后一条错误信息 |
| sessionGap | 每个会话窗口之间的时间间隔 |
| useSystemTime | 会话窗口聚合引擎计算的触发方式 |
| numGroups | 会话窗口引擎中的分组数 |
| numRows | 会话窗口引擎中的记录行数 |
| numMetrics | 指标的数量 |
| Metrics | 会话窗口聚合引擎使用的聚合指标的元代码 |
| memoryUsed | 会话窗口引擎所占用内存量，单位为字节 |
| snapshotDir | 会话窗口引擎快照保存的文件目录 |
| snapshotInterval | 每隔多少条数据保存一次引擎快照 |
| snapshotMsgId | 最后一个 snapshot 的 msgId |
| snapshotTimestamp | 触发保存快照的时间戳 |

* 表 DailyTimeSeriesEngine 返回日级时间序列引擎的状态。它包含以下列：

| 列名 | 含义 |
| --- | --- |
| name | 日级时间序列引擎的名称 |
| user | 创建日级时间序列引擎的用户名 |
| status | 日级时间序列引擎的状态，"OK" 表示可用，"FATAL" 表示不可用 |
| lastErrMsg | 最后一条错误信息 |
| windowTime | 数据窗口的长度 |
| step | 计算的时间间隔 |
| useSystemTime | 日级时间序列引擎中 useSystemTime 参数值 |
| garbageSize | 触发内存清理的阈值 |
| numGroups | 日级时间序列引擎中的分组数 |
| numRows | 日级时间序列引擎中的记录行数 |
| numMetrics | 日级时间序列引擎使用的聚合指标的数量 |
| metrics | 日级时间序列引擎使用的聚合指标的元代码 |
| memoryUsed | 日级时间序列引擎所占用内存量，单位为字节 |
| snapshotDir | 日级时间序列聚合引擎快照保存的文件目录 |
| snapshotInterval | 每隔多少条数据保存一次引擎快照 |
| snapshotMsgId | 最后一个 snapshot 的 msgId |
| snapshotTimestamp | 触发保存快照的时间戳 |

* 表 TimeBucketEngine 返回时间序列分组引擎的状态。它包含以下列：

| 列名 | 含义 |
| --- | --- |
| name | 时间序列分组引擎的名称 |
| user | 创建时间序列分组引擎的用户名 |
| status | 时间序列分组引擎的状态，"OK"表示可用，"FATAL"表示不可用 |
| lastErrMsg | 最后一条错误信息 |
| numGroups | 时间序列分组引擎中的分组数 |
| numRows | 时间序列分组引擎中的记录行数 |
| numMetrics | 时间序列分组引擎使用的聚合指标的数量 |
| metrics | 时间序列分组引擎使用的聚合指标的元代码 |
| memoryUsed | 时间序列分组引擎所占用内存量，单位为字节 |

* 表 AsofJoinEngine 返回 asof join 引擎的状态。它包含以下列：

| 列名 | 含义 |
| --- | --- |
| name | asof join 引擎的名称 |
| user | 创建 asof join 引擎的用户名 |
| status | asof join 引擎的状态，"OK" 表示可用，"FATAL" 表示不可用 |
| lastErrMsg | 最后一条错误信息 |
| useSystemTime | asof join 引擎中 useSystemTime 参数值 |
| delayedTime | asof join 引擎中 delayedTime 参数值 |
| garbageSize | 触发内存清理的阈值 |
| leftTableNumRows | asof join 引擎左表中的记录行数 |
| rightTableNumRows | asof join 引擎右表中的记录行数 |
| numMetrics | asof join 引擎使用的指标的数量 |
| metrics | asof join 引擎使用的指标的元代码 |
| memoryUsed | asof join 引擎所占用内存量，单位为字节 |

* 表 EqualJoinEngine 返回等值连接引擎的状态。它包含以下列：

| 列名 | 含义 |
| --- | --- |
| name | 等值连接引擎的名称 |
| user | 创建等值连接引擎的用户名 |
| status | 等值连接引擎的状态，"OK" 表示可用，"FATAL" 表示不可用 |
| lastErrMsg | 最后一条错误信息 |
| garbageSize | 触发内存清理的阈值 |
| leftTableNumRows | 等值连接引擎左表中的记录行数 |
| rightTableNumRows | 等值连接引擎右表中的记录行数 |
| numMetrics | 等值连接引擎使用的指标的数量 |
| metrics | 等值连接引擎使用的指标的元代码 |
| memoryUsed | 等值连接引擎所占用内存量，单位为字节 |

* 表 WindowJoinEngine 返回 window join 引擎的状态。它包含以下列：

| 列名 | 含义 |
| --- | --- |
| name | window join 引擎的名称 |
| user | 创建 window join 引擎的用户名 |
| status | window join 引擎的状态，"OK" 表示可用，"FATAL" 表示不可用 |
| lastErrMsg | 最后一条错误信息 |
| garbageSize | 触发内存清理的阈值 |
| leftTableNumRows | window join 引擎左表中的记录行数 |
| rightTableNumRows | window join 引擎右表中的记录行数 |
| numMetrics | window join 引擎使用的指标的数量 |
| metrics | window join 引擎使用的指标的元代码 |
| memoryUsed | window join 引擎所占用内存量，单位为字节 |

* 表 LookupJoinEngine 返回 lookup join 引擎的状态。它包含以下列：

| 列名 | 含义 |
| --- | --- |
| name | lookup join 引擎的名称 |
| user | 创建 lookup join 引擎的用户名 |
| status | lookup join 引擎的状态，"OK" 表示可用，"FATAL" 表示不可用 |
| lastErrMsg | 最后一条错误信息 |
| leftTableNumRows | lookup join 引擎左表中的记录行数 |
| rightTableNumRows | lookup join 引擎右表中的记录行数 |
| numMetrics | lookup join 引擎使用的指标的数量 |
| metrics | lookup join 引擎使用的指标的元代码 |
| memoryUsed | lookup join 引擎所占用内存量，单位为字节 |

* 表 LeftSemiJoinEngine 返回左半等值连接引擎的状态。它包含以下列：

| 列名 | 含义 |
| --- | --- |
| name | 左半等值连接引擎的名称 |
| user | 创建左半等值连接引擎的用户名 |
| status | 左半等值连接引擎的状态，"OK" 表示可用，"FATAL" 表示不可用 |
| lastErrMsg | 最后一条错误信息 |
| garbageSize | 触发内存清理的阈值 |
| leftTableNumRows | 左半等值连接引擎左表中的记录行数 |
| rightTableNumRows | 左半等值连接引擎右表中的记录行数 |
| numMetrics | 左半等值连接引擎使用的指标的数量 |
| metrics | 左半等值连接引擎使用的指标的元代码 |
| memoryUsed | 左半等值连接引擎所占用内存量，单位为字节 |

* 表 StreamFilter 返回流数据过滤引擎的状态。它包含以下列：

| 列名 | 含义 |
| --- | --- |
| name | 流数据过滤引擎的名称 |
| user | 创建流数据过滤引擎的用户名 |
| status | 流数据过滤引擎的状态，"OK" 表示可用，"FATAL" 表示不可用 |
| lastErrMsg | 最后一条错误信息 |
| numRows | 流数据过滤引擎中的记录行数 |
| filters | 流数据过滤引擎的过滤条件 |

* 表 StreamDispatchEngine 返回流数据分发引擎的状态。它包含以下列：

| 列名 | 含义 |
| --- | --- |
| name | 分发引擎的名称 |
| user | 创建分发引擎的用户名 |
| status | 分发引擎的状态，”OK”表示可用，”FATAL”表示不可用 |
| lastErrMsg | 最后一条错误信息 |
| numRows | 分发引擎中的记录行数 |
| memoryUsed | 分发引擎所占用内存量，单位为字节 |

* 表 ReactiveStateEngine 返回响应式状态引擎的状态。它包含以下列：

| 列名 | 含义 |
| --- | --- |
| name | 响应式状态引擎的名称 |
| metrics | 响应式状态引擎使用的计算公式的元代码 |
| dummyTable | 表对象，可以含有数据，亦可为空表 |
| outputTable | 计算结果的输出表，可以是内存表或分布式表 |
| keyColumn | 分组列名 |
| filter | 过滤条件的元代码 |
| snapshotDir | 保存引擎快照的文件目录 |
| snapshotIntervalInMsgCount | 每隔多少条数据保存一次流数据引擎快照 |
| keepOrder | 输出表数据是否按照输入时的顺序排序 |
| keyPurgeFilter | 清理条件的元代码 |
| keyPurgeFreqInSecond | 触发数据清理需要满足的时间间隔（以秒为单位） |
| raftGroup | 流数据高可用订阅端 raft 组的 ID |
| outputElapsedMicroseconds | 是否输出每个 batch 中数据从注入引擎到计算输出的总耗时，以及每个 batch 包含的总记录数 |
| keyCapacity | 建表时系统为该表预分配的 key 分组数量 |
| parallelism | 并行计算的工作线程数 |

* 表 DualOwnershipReactiveStateEngine 返回 Dual Ownership Reactive State Engine
  的状态。它包含以下列：

| 列名 | 含义 |
| --- | --- |
| name | Dual Ownership Reactive State Engine 的名称 |
| metrics | Dual Ownership Reactive State Engine 使用的计算公式的元代码 |
| dummyTable | 表对象，可以含有数据，亦可为空表 |
| outputTable | 计算结果的输出表，可以是内存表或分布式表 |
| keyColumn | 分组列名 |
| filter | 过滤条件的元代码 |
| snapshotDir | 保存引擎快照的文件目录 |
| snapshotIntervalInMsgCount | 每隔多少条数据保存一次流数据引擎快照 |
| keepOrder | 输出表数据是否按照输入时的顺序排序 |
| keyPurgeFilter | 清理条件的元代码 |
| keyPurgeFreqInSecond | 触发数据清理需要满足的时间间隔（以秒为单位） |
| raftGroup | 流数据高可用订阅端 raft 组的 ID |
| outputElapsedMicroseconds | 是否输出每个 batch 中数据从注入引擎到计算输出的总耗时，以及每个 batch 包含的总记录数 |
| keyCapacity | 建表时系统为该表预分配的 key 分组数量 |
| parallelism | 并行计算的工作线程数 |

* 表 NarrowReactiveStateEngine 返回生成窄表的响应式状态引擎的状态。它包含以下列：

| 列名 | 含义 |
| --- | --- |
| name | 生成窄表的响应式状态引擎的名称 |
| metrics | 需要输出到 *outputTable* 中的除 *keyColumn* 外的输入表中的列或计算指标，用元代码表示 |
| metricNames | 输出到 *outputTable* 中的指标的名称 |
| dummyTable | 表对象，可以含有数据，亦可为空表 |
| outputTable | 计算结果的输出表，可以是内存表或分布式表 |
| keyColumn | 分组列名 |
| filter | 过滤条件的元代码 |
| keepOrder | 输出表数据是否按照输入时的顺序排序 |
| keyPurgeFilter | 清理条件的元代码 |
| keyPurgeFreqInSecond | 触发数据清理需要满足的时间间隔（以秒为单位） |
| outputElapsedMicroseconds | 是否输出每个 batch 中数据从注入引擎到计算输出的总耗时，以及每个 batch 包含的总记录数 |
| keyCapacity | 建表时系统为该表预分配的 key 分组数量 |
| parallelism | 并行计算的工作线程数 |

* 表 SnapshotJoinEngine 返回快照连接引擎的状态。它包含以下列：

| 列名 | 含义 |
| --- | --- |
| name | 快照连接引擎的名称 |
| user | 创建快照连接引擎的用户名 |
| status | 快照连接引擎的状态，"OK" 表示可用，"FATAL" 表示不可用 |
| lastErrMsg | 最后一条错误信息 |
| leftTableNumRows | 快照连接引擎左表中的记录行数 |
| rightTableNumRows | 快照连接引擎右表中的记录行数 |
| numMetrics | 快照连接引擎使用的指标的数量 |
| metrics | 快照连接引擎使用的指标的元代码 |
| memoryUsed | 快照连接引擎所占用内存量，单位为字节 |

## 例子

```
share streamTable(10:0,`time`sym`price`qty,[TIMESTAMP,SYMBOL,DOUBLE,INT]) as trades
outputTable1 = table(10000:0, `time`sym`sumQty, [TIMESTAMP, SYMBOL, INT])
outputTable2 = table(1:0, `time`avgPrice`sumqty`Total, [TIMESTAMP,DOUBLE,INT,DOUBLE])
tradesTsAggregator = createTimeSeriesEngine(name="TimeSeriesDemo", windowSize=3, step=3, metrics=<[sum(qty)]>, dummyTable=trades, outputTable=outputTable1, timeColumn=`time, keyColumn=`sym, garbageSize=50)
tradesCsAggregator=createCrossSectionalEngine(name="CrossSectionalDemo", metrics=<[avg(price), sum(qty), sum(price*qty)]>, dummyTable=trades, outputTable=outputTable2, keyColumn=`sym, triggeringPattern=`perRow)
subscribeTable(tableName="trades", actionName="tradesTsAggregator", offset=0, handler=append!{tradesTsAggregator}, msgAsTable=true)
subscribeTable(tableName="trades", actionName="tradesCsAggregator", offset=0, handler=append!{tradesCsAggregator}, msgAsTable=true)

def writeData(n){
   timev = 2000.10.08T01:01:01.001 + timestamp(1..n)
   symv =take(`A`B, n)
   pricev=take(102.1 33.4 73.6 223,n)
   qtyv = take(60 74 82 59, n)
   insert into trades values(timev, symv, pricev,qtyv)
}

writeData(4);

getStreamEngineStat().TimeSeriesEngine;
getStreamEngineStat().CrossSectionalEngine;
```

