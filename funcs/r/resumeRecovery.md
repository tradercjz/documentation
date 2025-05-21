# resumeRecovery

## 语法

`resumeRecovery()`

## 参数

无

## 详情

用于重启节点恢复的进程。调用该命令后，会继续恢复 "Waiting" 状态的数据。该函数只能由管理员在控制节点上调用。

注：

启用高可用集群时，需要在 raft 组内每个节点执行该命令。

相关命令： [suspendRecovery](../s/suspendRecovery.md)

