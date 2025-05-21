# deleteReplicas

## 语法

`deleteReplicas(chunkId, nodeAlias)`

## 参数

**chunkId** 是字符串标量或向量，表示 chunk 的 ID。

**nodeAlias** 是一个字符串，表示节点的别名。

## 详情

把节点上的一个或多个 chunk 的副本删除。该命令只能由管理员在控制节点上执行。

## 例子

删除 “node1” 上所有 chunk 的副本。

```
chunkIds=exec chunkId from pnodeRun(getChunksMeta) where node="node1"
deleteReplicas(chunkIds,"node1");
```

