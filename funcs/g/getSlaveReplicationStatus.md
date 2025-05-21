# getSlaveReplicationStatus

## 语法

`getSlaveReplicationStatus([limit=-1])`

## 参数

**limit** 一个整数，表示结果中最多可返回的任务数量。

## 详情

由管理员在从集群的控制节点调用，获取从集群的异步复制状态。若通过 slaveReplicationDBScope
指定了回放数据库的范围，则仅获取该范围内的异步复制情况。其中，已完成的任务排列在前面，未完成的任务排列在后面。

* 如果未指定 *limit*，则返回的任务数量不受限制。
* 如果指定 *limit*，则返回最多 *limit* 个任务列表。

其中，已完成的任务最多显示最近的1万条记录；而未完成的任务只显示从最早时间开始，直到满足指定条数的记录。

**返回值：**返回一个表，包含以下字段：

* taskId：异步复制任务 id。
* masterTid：该任务对应主集群中的事务 id。
* groupId：异步复制任务所属的组。
* executionSet：任务所属的执行集ID。
* queueId：任务所属执行队列的编号。
* operationType：任务类型，参照异步复制支持性表。
* createTime：从集群从主集群获取任务的时间，类型为 NANOTIMESTAMP。
* dbName：任务对应的数据库的路径。
* tableName：任务对应的表名。
* srcIP：存储写任务数据的数据节点 ip。
* srcPort：存储写任务数据的数据节点 port。
* finishTime：任务的完成时间，类型为 NANOTIMESTAMP。
* executionNode：执行该任务的从集群的数据节点别名。
* state：任务执行状态，包含四种类型：
  WAITING（等待执行）、EXECUTING（正在执行）、FINISHED（执行完成/任务skip）、FAILED（执行失败）。
* details：补充说明。若 state = FAILED，则该列为执行失败的原因；若 state =
  FINISHED，该列用于对该任务进行补充说明。

## 例子

```
getSlaveReplicationStatus();
```

输出返回：

| taskId | masterTid | groupId | queueId | operationType | createTime | dbName | tableName | srcIP | srcPort | finishTime | executionNode | state | details |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | CREATE\_DOMAIN | 2022.11.08T10:50:37.425056956 | db://test\_dropPartition\_value |  | localhost | 8002 | 2022.11.08T10:50:37.452792885 | NODE2 | FINISHED |  |
| 2 | 2 | 2 | 1 | CREATE\_PARTITIONED\_TABLE | 2022.11.08T10:50:37.425056988 | db://test\_dropPartition\_value | pt | localhost | 8002 | 2022.11.08T10:50:37.479906033 | NODE3 | FINISHED |  |
| 3 | 3 | 3 | 2 | APPEND | 2022.11.08T10:50:37.425057012 | db://test\_dropPartition\_value | pt | localhost | 8002 | 2022.11.08T10:50:37.638746819 | NODE1 | FINISHED |  |
| 4 | 4 | 4 | 3 | DROP\_PARTITION | 2022.11.08T10:50:37.425057037 |  | pt | localhost | 8002 | 2022.11.08T10:50:37.869783336 | NODE2 | FINISHED |  |

相关函数：[getMasterReplicationStatus](getMasterReplicationStatus.md), [getSlaveReplicationQueueStatus](getslavereplicationqueuestatus.md)

