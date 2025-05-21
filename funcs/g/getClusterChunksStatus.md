# getClusterChunksStatus

## 语法

`getClusterChunksStatus()`

## 详情

应用在控制节点上，返回集群中所有 chunk（包括 file chunk 和 tablet chunk）的元数据信息。可以查看 chunk
在集群中数据节点上的分布。

返回一个表，包含以下列

* chunkId：chunk 的唯一标识
* file：分区路径
* size：file chunk 占用磁盘空间，单位为 byte。对于 tablet chunk，返回 0，需要使用
  getTabletsMeta 来查看它们实际占用的磁盘空间
* version：版本号
* vcLength：版本链长度
* versionChain：版本链
* state：chunk 状态。CONSTRUCTING：正在事务中； RECOVERING：正在 recovery
  中；COMPLETE：已经处于事务终止状态
* replicas：副本的分布信息
* replicaCount：副本数
* lastUpdated：上一次更新的时间戳。请注意，server 从 2.00.1
  版本才开始支持该字段，因此获取已经存在的由 2.00.1 之前的 server 创建的 chunk 元数据信息时，该字段将返回空值。
* permission：CHUNK 的权限。CHUNK 的权限分为 READ\_ONLY 以及
  READ\_WRITE（默认权限）两类。正在进行迁移的分区，或存储在 s3 的分区权限均为 READ\_ONLY

对于 READ\_ONLY 权限的分区：

(1) 不能追加或更新数据，并只能通过调用 `drop`
类函数进行删除，且遵从事务的原则。（注意：存储在 s3 的分区不支持事务）。

(2) 不能对其进行 recovery, rebalance 以及 TSDB 引擎的
level file 合并操作。

## 例子

```
rpc(getControllerAlias(), getClusterChunksStatus);
```

| chunkId | file | size | version | vcLength | versionChain | state | replicas | replicaCount | lastUpdated | permission |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 092d5e12-e595-6f... | /testDB/pt2.tbl | 49 | 1 | 1 | 2052:49:1 -> | COMPLETE | P1-node1:1:0,P2-... | 2 | 2022.03.31T18:09:41.138 | READ\_WRITE |
| 42936e31-8be0-fa... | /testDB/9/i | 0 | 2 | 2 | 2053:0:2 -> 2051... | COMPLETE | P3-node1:2:0,P1-... | 2 | 2022.03.31T18:09:41.138 | READ\_WRITE |
| d31e6b47-18f0-37... | /testDB/7/i | 0 | 2 | 2 | 2053:0:2 -> 2051... | COMPLETE | P1-node1:2:0,P2-... | 2 | 2022.03.31T18:09:41.138 | READ\_WRITE |
| 647a5fd6-cd85-3b... | /testDB/6/i | 0 | 2 | 2 | 2053:0:2 -> 2051... | COMPLETE | P1-node1:2:0,P3-... | 2 | 2022.03.31T18:09:41.138 | READ\_WRITE |
| 8bec6445-bc6d-36... | /testDB/5/i | 0 | 2 | 2 | 2053:0:2 -> 2051... | COMPLETE | P2-node1:2:0,P3-... | 2 | 2022.03.31T18:09:41.138 | READ\_WRITE |
| ca690ba5-be73-a6... | /testDB/4/i | 0 | 2 | 2 | 2053:0:2 -> 2051... | COMPLETE | P3-node1:2:0,P1-... | 2 | 2022.03.31T18:09:41.138 | READ\_WRITE |

