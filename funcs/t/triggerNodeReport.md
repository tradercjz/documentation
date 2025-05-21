# triggerNodeReport

## 语法

`triggerNodeReport(nodeAlias, [chunkId])`

## 参数

**nodeAlias** 字符串，表示节点的别名。

**chunkId** 可选参数，一个字符串或者字符串向量。表示需要汇报的 chunks 的 ID 值。该参数仅对集群有效。

## 详情

强制触发别名为 *nodeAlias* 的节点向控制节点汇报信息，以更新控制节点维护的元数据信息。若指定了 *chunkId* 参数，则仅上报对应
chunk 信息。

使用场景：该命令用于解决数据节点离线并再次上线后，出现不汇报某些 chunk 信息的问题。

操作步骤如下：

1. 通过命令 `getClusterPerf` 查看 state
   字段，以确定各个节点的存活情况。
2. 通过 [getClusterChunksStatus](../g/getClusterChunksStatus.md) 查看 replicas,
   replicaCount 字段，以确定 chunk 的副本信息。
3. 若节点存活，但出现副本数不一致，在 controller 的日志中，搜索对应的
   chunkId，并定位出未汇报的数据节点。在该数据节点上调用 `tirggerNodeReport` 强制触发其汇报
   chunk 信息。
4. 若此方法失效，建议重启节点。

