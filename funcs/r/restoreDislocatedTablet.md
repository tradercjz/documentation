# restoreDislocatedTablet

## 语法

`restoreDislocatedTablet()`

## 参数

无

## 详情

当配置分区粒度为表级分区时（详见 [StandaloneMode](../../db_distr_comp/cfg/standalone.html)
*enableChunkGranularityConfig* 参数），同一个分区的所有表将分布在相同的节点下。当调用函数 [rebalanceChunksAmongDataNodes](rebalanceChunksAmongDataNodes.html)
进行数据平衡时，若出现节点宕机或离线，可能出现同一个分区里部分表的数据转移成功，部分表的数据转移失败的情况，即同一个分区下的不同表会分布在不同的节点。该函数可以修复此问题，将同一个分区里的表转移到同一个节点下。

返回一个表，包含以下列：

| 列名 | 含义 |
| --- | --- |
| chunkId | chunk 的唯一标识 |
| srcNode | 源节点的别名 |
| destNode | 目标节点的别名 |

注： 该函数必须在控制节点下运行。

调用该函数后，可以在进行数据平衡的数据节点上执行 [getRecoveryTaskStatus](../g/getRecoveryTaskStatus.html) 查看任务执行的状态。

## 例子

```
restoreDislocatedTablet()
```

| ChunkId | srcNode | destNode |
| --- | --- | --- |
| 99279094-ca12-3b87-48b6-520cbb986f39 | node1 | node2 |
| 45f612b8-42f5-aebd-4cef-e522b6ae1fc8 | node1 | node2 |

