# getClusterStatus

## 语法

`getClusterStatus(clusterName)`

## 参数

**clusterName** 字符串标量或向量，表示集群名称。

## 详情

查询指定集群当前的状态。只能由管理员在 MoM（Master of Master，管理集群）上执行该函数。

**返回值：**一个表，除 clusterName 和 computeGroup 字段外，其它字段与 [getClusterPerf](getClusterPerf.md) 函数的结果一致：

* clusterName：集群名称。
* computeGroup：计算组名称。若集群中无计算组，则该字段为空。

## 例子

```
getClusterStatus("ShangHai_cluster2")
```

| clusterName | computeGroup | host | port | site | mode | state | agentSite | maxConnections | maxMemSize | workerNum | executorNum | connectionNum | name | memoryUsed | memoryAlloc | cpuUsage | avgLoad | medLast10QueryTime | maxLast10QueryTime | medLast100QueryTime | maxLast100QueryTime | maxRunningQueryTime | runningJobs | queuedJobs | runningTasks | queuedTasks | jobLoad | diskCapacity | diskFreeSpace | diskFreeSpaceRatio | diskWriteRate | diskReadRate | lastMinuteWriteVolume | lastMinuteReadVolume | networkSendRate | networkRecvRate | lastMinuteNetworkSend | lastMinuteNetworkRecv | publicName | lastMsgLatency | cumMsgLatency | isLeader |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ShangHai\_cluster2 |  | localhost | 8,921 | localhost:8921:agent1 | 1 | 1 | localhost:8921:agent1 | 32 | 4 | 4 | 0 | 0 | agent1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | 0 | 0 |  |
| ShangHai\_cluster2 |  | localhost | 8,923 | localhost:8923:cnode1 | 4 | 0 | localhost:8921:agent1 | 0 | 0 | 0 | 0 | 0 | cnode1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | 0 | 0 |  |
| ShangHai\_cluster2 |  | localhost | 8,922 | localhost:8922:dnode1 | 0 | 0 | localhost:8921:agent1 | 0 | 0 | 0 | 0 | 0 | dnode1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | 0 | 0 |  |
| ShangHai\_cluster2 |  | localhost | 8,920 | localhost:8920:controller8920 | 2 | 1 |  | 512 | 8 | 4 | 0 | 2 | controller8920 | 123,862,496 | 127,377,408 | 16.049382716049383 | 0.16049382716049382 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 148 | 0 | 21,028 | 0 | 0 | 0 | 0 | 0 |  | 0 | 0 |  |

