# suspendRecovery

## 语法

`suspendRecovery()`

## 参数

无

## 详情

用于暂停在线恢复节点的进程。恢复进程中，处于 "In-Progress" 状态的数据会继续恢复，"Waiting"
状态的数据会暂停恢复。暂停后，恢复进程的源节点可以继续写入数据。该函数只能由管理员在控制节点上调用。

注：

启用高可用集群时，需要在 raft 组内每个节点执行该命令。

相关命令： [resumeRecovery](../r/resumeRecovery.md)

