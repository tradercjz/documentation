# startClusterReplication

## 语法

`startClusterReplication()`

## 参数

无

## 详情

重启由多次任务失败而停止或调用 [stopClusterReplication](stopClusterReplication.html) 主动停止的异步复制。该命令只能由管理员在主/从集群的控制节点调用。调用该命令前，必须先配置
*replicationMode* 参数。

## 例子

```
startClusterReplication();
```

相关函数： [stopClusterReplication](stopClusterReplication.html), [skipClusterReplicationTask](skipClusterReplicationTask.html)

