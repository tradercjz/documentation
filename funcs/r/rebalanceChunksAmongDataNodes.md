# rebalanceChunksAmongDataNodes

## 语法

`rebalanceChunksAmongDataNodes([exec = false], [updatedBeforeDays =
7.0])`

## 参数

**exec** 布尔值，表示是否进行数据平衡。默认值为 false，表示输出数据平衡的执行计划，并不执行数据迁移。若设置为
true，则系统会执行数据迁移。

**updatedBeforeDays**
非负浮点数，用于确定可以进行平衡的数据的时间范围，默认值是7，单位是天。表示数据块（chunk）的最后一次写入或更新（修改）时间发生在7天前时，才会进行平衡。

## 详情

在集群中的所有磁盘间平衡数据，以保证集群达到最佳性能。在集群中增加节点、磁盘后，或者在磁盘负载过高时，通常需要执行此操作。只能由管理员在控制节点上执行。

返回一个表，包含以下列：

| 列名 | 含义 |
| --- | --- |
| srcNode | 源节点的别名 |
| chunkId | chunk 的唯一标识 |
| destNode | 目标节点的别名 |
| destVolume | 目标磁盘卷的路径 |

调用该函数后，可以在控制节点上执行 [getRecoveryTaskStatus](../g/getRecoveryTaskStatus.md) 查看任务执行的状态。

调用该函数后，系统会打印 INFO
级别的日志，输出每个磁盘的原始使用率以及平衡后的使用率。日志内容的格式如下：

```
[rebalance] Expected change of disk usage rate is 原本占有率->搬运后占有率
[rebalance] Change of disk usage rate in 磁盘所在IP@磁盘fsid(1/磁盘数) is 原本占有率->搬运后占有率
[rebalance] Change of disk usage rate in 磁盘所在IP@磁盘fsid(2/磁盘数) is 原本占有率->搬运后占有率
...
```

## 例子

```
rebalanceChunksAmongDataNodes()
```

| srcNode | chunkId | destNode | destVolume |
| --- | --- | --- | --- |
| node1 | 99279094-ca12-3b87-48b6-520cbb986f39 | node2 | /home/xxx/node2/storage |
| node1 | 45f612b8-42f5-aebd-4cef-e522b6ae1fc8 | node2 | /home/xxx/node2/storage |

