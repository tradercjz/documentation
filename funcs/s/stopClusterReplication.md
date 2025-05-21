# stopClusterReplication

## 语法

`stopClusterReplication()`

## 参数

无

## 详情

停止集群间的异步复制。该命令只能由管理员在主/从集群的控制节点调用。

* 主集群：调用后，停止将任务放入发送队列。
* 从集群：调用后，停止从主集群读取新任务，但执行中的任务不会停止。

调用该命令前，必须先配置 *replicationMode* 参数。

## 例子

```
stopClusterReplication();
```

相关函数： [startClusterReplication](startClusterReplication.md), [skipClusterReplicationTask](skipClusterReplicationTask.md)

