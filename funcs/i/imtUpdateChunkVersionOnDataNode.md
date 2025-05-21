# imtUpdateChunkVersionOnDataNode

## 语法

`imtUpdateChunkVersionOnDataNode(chunkId, version)`

## 参数

**chunkId** 字符串标量或向量，表示 chunk 的 ID。

**version** 整型数字，表示版本号。

## 详情

修改数据节点上对应 *chunkId*
的版本号，以维护集群中多副本数据之间，或数据节点与控制节点之间的版本一致性。

该函数只能在数据节点执行。

## 相关函数

控制节点可调用函数 [getClusterChunksStatus](../g/getClusterChunksStatus.html) 查询所有节点上 chunk 对应的版本号。

数据节点可调用函数 [getChunksMeta](../g/getChunksMeta.html) 查询当前数据节点上 chunk 对应的版本号。

