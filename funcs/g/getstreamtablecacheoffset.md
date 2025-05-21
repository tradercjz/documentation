# getStreamTableCacheOffset

## 语法

`getStreamTableCacheOffset(streamTable)`

## 参数

**streamTable** 是一个自动清理的非持久化流表，即由 `enableTableShareAndCachePurge`
创建的流表，或由 `enableTableCachePurge` 设置后的流表。

## 详情

查看指定的流表在内存中的最旧的记录相较于流表已写入的总记录数的偏移量（offset），即总记录数减去内存中数据行的值。

## 例子

```
t = streamTable(1000:0, `time`sym`volume, [DATETIME, SYMBOL, INT])
enableTableShareAndCachePurge(table=t, tableName=`st, cachePurgeTimeColumn=`time,
 cachePurgeInterval=30m, cacheRetentionTime=20m)

time = datetime(2024.01.01T09:00:00) +1..1000*2
sym=take(`a`b`c, 1000)
volume = rand(10,1000)

insert into t values([time, sym, volume])
getStreamTableCacheOffset(t)
//0

time = datetime(2024.01.01T09:35:00) +1..1000*2
sym=take(`a`b`c, 1000)
volume = rand(10,1000)
insert into t values([time, sym, volume])
getStreamTableCacheOffset(t)
//999
```

