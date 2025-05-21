# getComputeGroupChunksStatus

## 语法

`getComputeGroupChunksStatus([computeGroup])`

## 参数

**computeGroup** 可选参数，字符串标量，表示计算组名称。

## 详情

应用于控制节点，获取指定或所有计算组中缓存的所有 chunk （包括 file chunk 和 tablet chunk）的元数据信息。

**返回值：**返回一个表，包含以下列：

* chunkId：chunk 的唯一标识
* file：分区路径
* routedTo：计算节点别名，控制节点会将对该分区的查询调度到此计算节点。
* cachedOn：缓存分区的计算节点别名，形式为 alias:[version]，例如：orca2:[29] 表示名为 orca2
  的计算节点缓存了分区版本号为 29 的数据。
* computeGroup：缓存分区的计算组名字。一个分区可能被多个计算组缓存。
* size：file chunk 占用磁盘空间，单位为 byte。对于 tablet chunk，返回 0，需要使用 getTabletsMeta
  来查看它们实际占用的磁盘空间。
* version：版本号。
* vcLength：版本链长度。
* versionChain：版本链。
* state：chunk 状态。CONSTRUCTING：正在事务中； RECOVERING：正在 recovery
  中；COMPLETE：已经处于事务终止状态。
* dataNodeReplicas：数据节点上副本的分布信息。
* dataNodeReplicaCount：数据节点上副本的数量。
* lastUpdated：上一次更新的时间戳。
* permission：CHUNK 的权限。CHUNK 的权限分为 READ\_ONLY 以及
  READ\_WRITE（默认权限）两类。正在进行迁移的分区，或存储在 s3 的分区权限均为 READ\_ONLY。

## 例子

```
getComputeGroupChunksStatus()
```

| chunkId | path | routedTo | cachedOn | computeGroup | size | version | vcLength | versionChain | state | dataNodeReplicas | dataNodeReplicaCount | lastUpdated | permission |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| abec288a-49f7-61b9-464e-56bf134c8340 | /Storage\_compute\_separation\_tsdb/20120110/Key19/2 | orca3 | [NOT CACHED] | orca | 0 | 1 | 1 | 1466:0:1:1466 -> | COMPLETE | dnode2:1:0:false:0 | 1 | 2024.10.12 17:26:51.757 | READ\_WRITE |
| fdb95a8e-72f0-21a7-0443-2cbe02feeca2 | /Storage\_compute\_separation\_tsdb/20120229/Key1/2 | orca1 | [NOT CACHED] | orca | 0 | 1 | 1 | 1463:0:1:1463 -> | COMPLETE | dnode3:1:0:false:0 | 1 | 2024.10.12 17:26:51.708 | READ\_WRITE |
| 55020019-8b2c-75a1-3b40-7ad2469abe48 | /Storage\_compute\_separation\_tsdb/20120110/Key13/2 | orca3 | [NOT CACHED] | orca | 0 | 1 | 1 | 1458:0:1:1458 -> | COMPLETE | dnode3:1:0:false:0 | 1 | 2024.10.12 17:26:51.618 | READ\_WRITE |
| 96678f5f-6ae5-2b98-9944-5d4370473dee | /Storage\_compute\_separation\_tsdb/20120110/Key7/2 | orca2 | [NOT CACHED] | orca | 0 | 1 | 1 | 1456:0:1:1456 -> | COMPLETE | dnode1:1:0:false:0 | 1 | 2024.10.12 17:26:51.583 | READ\_WRITE |

