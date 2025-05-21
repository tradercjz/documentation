# getPerf

## 语法

`getPerf()`

## 参数

无

## 详情

以字典的形式返回本地节点上的多个性能监控度量值。包含以下 key：

* runningJobs：正在执行中的 Job 个数。
* jobLoad：作业负载。
* avgLoad：CPU 平均负载。
* queuedJobs：队列中的 Job 个数。
* lastMinuteNetworkSend：前一分钟网络发送字节数（单位：字节）。
* lastMinuteNetworkRecv：前一分钟网络接收字节数 （单位：字节）。
* lastMinuteReadVolume：前一分钟读磁盘容量（单位：字节）。
* lastMinuteWriteVolume：前一分钟写磁盘容量（单位：字节）。
* lastMsgLatency：前一批消息的延时（单位：纳秒）。
* cumMsgLatency：所有消息的平均延时（单位：纳秒）。
* maxLast10QueryTime：前 10 个完成的查询执行所耗费时间的最大值（单位：纳秒）。
* maxLast100QueryTime：前100个完成的查询执行所耗费时间的最大值（单位：纳秒）。
* medLast10QueryTime：前 10 个完成的查询执行所耗费时间的中间值（单位：纳秒）。
* medLast100QueryTime：前 100 个完成的查询执行所耗费时间的中间值（单位：纳秒）。
* maxRunningQueryTime：当前正在执行的查询的耗费时间的最大值（单位：纳秒）。
* diskFreeSpaceRatio：磁盘可用空间占比。
* diskReadRate：磁盘读速率（单位：字节/秒）。
* diskWriteRate：磁盘写速率（单位：字节/秒）。
* diskFreeSpace：磁盘剩余空间（单位：字节）。
* diskCapacity：磁盘容量（单位：字节）。
* cpuUsage：CPU 使用率。
* memoryAlloc：系统已分配给当前节点的内存（单位：字节）。
* memoryUsed：节点的内存占用量（单位：字节）。
* networkSendRate：网络发送速率（单位：字节/秒）。
* networkRecvRate：网络接收速率（单位：字节/秒）。
* connectionNum：连接到本地节点的连接数。

## 例子

```
getPerf();

// output
cumMsgLatency->-9.223372036854776E18
lastMsgLatency->-9.223372036854776E18
lastMinuteNetworkRecv->2184101
maxLast10QueryTime->224829
lastMinuteNetworkSend->378283
diskWriteRate->144
networkSendRate->3924
medLast100QueryTime->131965
avgLoad->1.0228125
runningJobs->0
connectionNum->2
medLast10QueryTime->131965
cpuUsage->0
diskFreeSpaceRatio->0.041250206237365
jobLoad->0
memoryUsed->7970304
memoryAlloc->19513344
maxLast100QueryTime->224829
networkRecvRate->32238
maxRunningQueryTime->0
diskCapacity->1.859747577856E12
queuedJobs->0
diskFreeSpace->7.6714971136E10
diskReadRate->6538
lastMinuteWriteVolume->1515
lastMinuteReadVolume->392408
```

