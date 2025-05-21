# clearAllCache

## 语法

`clearAllCache()`

## 参数

无

## 详情

清除以下缓存数据：

* 维度表在内存中的缓存
* OLAP 引擎分区表中已经载入内存的数据
* TSDB 引擎的 Level File 索引的缓存
* TSDB 引擎中 SYMBOL 类型的字典编码的缓存
* 分布式计算中 map-reduce 任务的中间结果

## 例子

```
clearAllCache();
```

