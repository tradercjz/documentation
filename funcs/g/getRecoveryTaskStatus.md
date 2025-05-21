# getRecoveryTaskStatus

## 语法

`getRecoveryTaskStatus()`

## 参数

无

## 详情

返回副本恢复任务的状态。该函数只能在控制节点上执行。

返回一个表，包含以下列：

* TaskId：表示恢复副本任务的 ID。
* TaskType：恢复任务的类型，包括 LoadRebalance 和 ChunkRecovery 。
* ChunkId：分区的 ID。
* ChunkPath：分区的 DFS 路径。
* Source：恢复数据的源节点，即正常的数据节点。
* Dest：需要进行数据恢复的节点(目的节点)。
* Status：数据恢复的状态，包括 “Waiting”, “In-Progress”, “Finished”, “Aborted”。
* AttemptCount：恢复任务尝试的次数。
* DeleteSource：是否删除源节点的数据。当 TaskType 是 ChunkRecovery 时，只能返回 false；当 TaskType 是
  LoadRebalance 时，可以返回 true 或 false。
* StartTime：创建恢复任务的时间。
* LastDequeueTime：任务最后一次从任务队列出队的时间。
* LastStartTime：最后一次开始执行任务的时间。
* FinishTime：任务结束的时间。
* IsIncrementalRecovery：是否启用增量复制。
* IsAsyncRecovery：是否启用异步复制。
* ChangeFromIncrementalToFull：是否从增量恢复转为全量恢复。系统多次尝试增量恢复失败会自动转换成全量恢复。
* ChangeToSyncTime：节点在线恢复时，从异步恢复阶段转为同步恢复阶段的时刻。
* FailureReason：recovery 任务失败的原因。

## 例子

```
getRecoveryTaskStatus();
```

