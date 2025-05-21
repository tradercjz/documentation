# getComputeNodeCacheStat

## 语法

`getComputeNodeCacheStat()`

## 参数

无

## 详情

应用于计算组中的计算节点上，返回该节点的二级缓存信息。

返回值：返回一个表，包含以下列：

* memCacheUsage：内存缓存的使用量，单位为 MB。
* memCacheSize：内存缓存的最大容量，单位为 MB。
* diskCacheUsage：磁盘缓存的使用量，单位为 MB。
* diskCacheSize：磁盘缓存的最大容量，单位为 MB。

## 例子

```
getComputeNodeCacheStat()
```

| memCacheUsage | memCacheSize | diskCacheUsage | diskCacheSize |
| --- | --- | --- | --- |
| 114.51725769042969 | 1,024 | 0 | 65,536 |

