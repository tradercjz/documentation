# getCacheEngineStat

## 语法

`getCacheEngineStat()`

## 参数

无

## 详情

获取当前节点下 OLAP 引擎 Cache Engine 的状态信息。该函数只能在数据节点调用。

返回一个表对象，包含以下几列:

* chunkId: chunk 的唯一标识。
* physicalName: chunk 所属表的物理表名。
* timeSinceLastWrite: 距离最后一次写入经过的时间，单位为毫秒。
* cachedRowsOfCompletedTxn: 当前缓存的已完成事务的记录数。
* cachedRowsOfUncompletedTxn: 当前缓存的未完成事务的记录数。注意: 每个 chunk 最多只有最后一个事务是未完成的。
* cachedMemOfCompletedTxn: cachedRowsOfCompletedTxn 占用的内存，单位为字节。
* cachedMemOfUncompletedTxn: cachedRowsOfUncompletedTxn 占用的内存，单位为字节。
* cachedTids: 当前缓存的事务 id 列表。

## 例子

```
getCacheEngineStat()
```

| chunkId | physicalName | timeSinceLastWrite | cachedRowsOfCompletedTxn | cachedRowsOfUncompletedTxn | cachedMemOfCompletedTxn | cachedMemOfUncompletedTxn | cachedTids |
| --- | --- | --- | --- | --- | --- | --- | --- |
| e4558d3c-fa41-52b5-418b-94e26cb70a75 | pt\_2 | 1056 | 222,386 | 0 | 3,558,176 | 0 | 2052 |

