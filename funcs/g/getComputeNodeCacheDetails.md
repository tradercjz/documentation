# getComputeNodeCacheDetails

## 语法

`getComputeNodeCacheDetails(granularity)`

## 参数

**granularity** 字符串标量，表示查询的粒度：

* “CHUNK”： 以分区为单位查询缓存信息。
* “TABLE”：以表为单位查询信息。若存在大量分区，可选择该项以控制返回表行数。

## 详情

在存算分离架构中，在计算组中的计算节点上执行该函数，可返回该节点上的具体缓存信息。

区别于`getComputeNodeCacheStat`用于查询当前节点的缓存总使用量和缓存上限；`getComputeNodeCacheDetails`
可查询缓存的具体构成。

用户指定以表或分区为单位，查询对应数据在该节点上的缓存类型、缓存大小等。

关于存算分离架构的详细介绍与相关配置，请参见[存算分离](../../db_distr_comp/db/storage_compute_separation.md)主题页。

**返回值：**

* 当以分区为单位（*granularity*=”CHUNK”）查询时，返回一张包含以下字段的表：
  + dbName - 库名
  + tableName - 表名
  + dfsPath - 分区的 DFS 路径
  + cid - 当前缓存对应的的版本标识
  + cacheType - 缓存类型，“MEM” 表示位于内存，“DISK” 表示位于磁盘。若存在于两处，则会显示两行
  + size - 以字节为单位的缓存大小，与缓存类型对应
* 当以表为单位（*granularity*=”TABLE”）查询时，每个分区表对应一条记录，包括
  dbName、tableName、partitionCount、cacheType 和 size 字段。其中 partitionCount
  表示该表中被缓存的分区数。

## 例子

```
getComputeNodeCacheDetails("CHUNK");
```

| **dbName** | **tableName** | **dfsPath** | **cid** | **cacheType** | **size** |
| --- | --- | --- | --- | --- | --- |
| dfs://demo | pt1 | /demo/43/G6 | 509 | MEM | 222 |
| dfs://demo | pt1 | /demo/15/G6 | 509 | MEM | 184 |
| dfs://test01 | pt01 | /test01/1/8c | 515 | MEM | 280 |
| … |  |  |  |  |  |

```
getComputeNodeCacheDetails("TABLE");
```

| **dbName** | **tableName** | **partitionCount** | **cacheType** | **size** |
| --- | --- | --- | --- | --- |
| dfs://demo | pt1 | 27 | MEM | 5804 |

相关函数：[clearComputeNodeCache](../c/clearcomputenodecache.md), [clearComputeNodeDiskCache](../c/clearcomputenodediskcache.md),
[getComputeNodeCacheStat](getcomputenodecachestat.md)

