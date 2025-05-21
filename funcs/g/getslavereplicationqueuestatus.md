# getSlaveReplicationQueueStatus

## 语法

`getSlaveReplicationQueueStatus()`

## 参数

无

## 详情

获取从集群每个执行队列的任务执行状态。该函数只能由管理员在从集群的控制节点调用。

返回一个表，包含以下字段：

* executionSet：任务所属的执行集ID。
* queueId：任务所属队列的编号。
* unifinishedTasks：队列中未执行的任务数量。
* executionGroupId：正在执行任务所属的组号。
* executionNode：执行该 group 的数据节点别名。
* executionTime：当前 group 已经执行的时间。
* status：任务执行状态，包含四种类型：
  EXECUTING（正在执行）、FAILED（执行失败）、STOPPED（停止执行）、FINISHED（执行完成）

## 例子

```
getSlaveReplicationQueueStatus()
```

输出返回：

| executionSet | queueId | unfinishedTasks | executionGroupId | executionNode | executionTime | status |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | -1 | dnode1 | 00:00:00.000 | FINISHED |
| 0 | 1 | 0 | -1 | dnode2 | 00:00:00.000 | FINISHED |
| 0 | 2 | 0 | -1 | dnode3 | 00:00:00.000 | FINISHED |
| 1 | 3 | 0 | -1 | dnode1 | 00:00:00.000 | FINISHED |
| 1 | 4 | 0 | -1 | dnode2 | 00:00:00.000 | FINISHED |
| 1 | 5 | 0 | -1 | dnode3 | 00:00:00.000 | FINISHED |

