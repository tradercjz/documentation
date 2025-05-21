# setChunkLastUpdateTime

## 语法

`setChunkLastUpdateTime(chunkId, lastUpdateTime)`

## 参数

**chunkId** 字符串向量，用于指定分区 ID。

**lastUpdateTime** TIMESTAMP 类型，指定分区的更新时间。

## 详情

手动设置指定分区的上次更新时间（可通过函数 `getClusterChunksStatus` 返回的 lastUpdated
字段查看）。

该函数仅支持管理员用户在单节点、或集群模式中的控制节点上调用。

## 例子

```
setChunkLastUpdateTime(["32953d51-980c-59a1-5f43-c90bfddd5a63","d957b444-be92-9296-ba4a-9d8a41682168"], timestamp(2016.05.12T19:32:49))
```

