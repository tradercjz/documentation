# rebalanceChunksWithinDataNode

## 语法

`rebalanceChunksWithinDataNode(nodeAlias, [exec=false], [updatedBeforeDays =
7.0])`

## 参数

**nodeAlias** 字符串，表示数据节点的别名。

**exec** 布尔值，表示是否在节点内进行数据平衡。默认值为 false，输出数据平衡的执行计划，并不执行数据迁移。若设置为
true，则系统会执行数据迁移。

**updatedBeforeDays**
非负浮点数，用于确定可以进行平衡的数据的时间范围，默认值是7，单位是天。表示数据块（chunk）的最后一次写入或更新（修改）时间发生在7天前时，才会进行平衡。

## 详情

一个节点内部增加磁盘卷后，需要调整现有磁盘卷上的数据量，使各个磁盘卷上的数据量达到平衡。该函数用于平衡一个数据节点内各磁盘卷间的数据，返回一个表，显示各磁盘卷间数据平衡计划。
若 *exec* 为 true，则进行数据平衡；若 *exec* 为
false，则不进行数据平衡。它只能在集群环境下由管理员在控制节点上执行。

返回结果包含以下列：

| 列名 | 含义 |
| --- | --- |
| chunkId | chunk 的唯一标识 |
| srcVolume | 源磁盘卷 |
| destVolume | 目标磁盘卷 |

调用该函数进行数据平衡后，可以在控制节点上执行 [getRecoveryTaskStatus](../g/getRecoveryTaskStatus.md) 查看任务执行的状态。

注： 自 2.00.12 版本起，rebalanceChunksWithinDataNode 支持单节点模式。

调用该函数后，系统会打印 INFO
级别的日志，输出每个磁盘的原始使用率以及平衡后的使用率。日志内容的格式如下：

```
[rebalance] Change of disk usage rate () expect: 原本占有率 -> 搬运后占有率
[rebalance] Change of disk usage rate (1 / 磁盘数) 磁盘所在IP@磁盘fsid: 原本占有率 -> 搬运后占有率
[rebalance] Change of disk usage rate (2 / 磁盘数) 磁盘所在IP@磁盘fsid: 原本占有率 -> 搬运后占有率
...
```

## 例子

```
rebalanceChunksWithinDataNode("node1")
```

| ChunkId | srcVolume | destVolume |
| --- | --- | --- |
| 82c6eb6c-36ee-b1b6-4a86-ca24d9faaa25 | /hdd/hdd1/volumes | /hdd/hdd2/volumes |

