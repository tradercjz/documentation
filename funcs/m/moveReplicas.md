# moveReplicas

## 语法

`moveReplicas(srcNode, destNode, chunkId,
[destVolumes])`

## 参数

**srcNode** 字符串，表示源节点的别名。

**destNode** 字符串，表示目标节点的别名。

**chunkId** 字符串/UUID 标量或向量，表示 chunk 的 ID。

**destVolumes** 字符串标量或向量，表示移动到目的节点的具体目录，此目录必须来自配置文件中 volumes
指定的目录。如果为向量，则优先移动到向量中位次靠前的目录下。

## 详情

通过该函数将源节点上的一个或多个 chunk 的副本移动到目标节点。如果目标节点上已经存在该 chunk，那么系统将放弃本次操作。

该命令只能由管理员在控制节点上执行。

通过 [getRecoveryTaskStatus](../g/getRecoveryTaskStatus.md) 函数可以查看任务状态。

## 例子

把 "node1" 上所有 chunk 的副本移动到 "node2"的指定目录。

```
chunkIds=exec chunkId from pnodeRun(getChunksMeta) where node="node1"
moveReplicas("node1","node2",chunkIds,"/ddb/server/clusterDemo/data/node2/storage");
```

