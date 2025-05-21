# enableTableShareAndCachePurge

## 语法

`enableTableShareAndCachePurge(table, tableName,
[cacheSize],[cachePurgeTimeColumn],[cachePurgeInterval],[cacheRetentionTime])`

### 参数

**table** 是一个空的流数据表。

**tableName** 是一个字符串，表示 table 共享后的名称。

**cacheSize** 是一个正整数，可选参数，表示流数据表在内存中最多保留的记录数。

**cachePurgeTimeColumn** 字符串标量，可选参数。需要指定为持久化流表中的时间列名称。

**cachePurgeInterval** DURATION 类型标量，表示触发清理内存中数据的时间间隔。

**cacheRetentionTime** DURATION 类型标量，表示内存中数据的最长保留期限。

## 详情

将非持久化的流数据表共享，并设置定时清理。

通过以下两种方式之一来清理内存中的数据：

* 配置 *cacheSize* 参数时，如果插入的数据使内存中流数据表的行数达到阈值，系统将清理内存中较旧的已发布记录。阈值确定方法如下：

  + 每次 append 的数据都不超过 *cacheSize* 时，阈值为 *cacheSize* 的 2.5
    倍。
  + 当 append 的数据超过 *cacheSize* 时，阈值为追加行数和 cacheSize 之和的 1.2 倍。
* 同时配置 *cachePurgeTimeColumn*, *cachePurgeInterval* 和
  *cacheRetentionTime*，系统将根据时间列清理数据。每次插入新数据时，系统会计算新数据与内存中第一条数据的时间戳差值，当差值大于等于
  *cachePurgeInterval* 时，系统仅保留时间戳与新数据时间戳差值小于等于 *cacheRetentionTime*的数据，清理其它数据。

## 例子

例1. 配置 cacheSize 参数，根据内存中的数据量进行清理。

```
t = streamTable(1000:0, `time`sym`volume, [DATETIME, SYMBOL, INT])
enableTableShareAndCachePurge(table=t, tableName=`st, cacheSize=1000)
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
//500
```

例2. 配置 *cachePurgeTimeColumn*, *cachePurgeInterval* 和
*cacheRetentionTime，*根据时间列清理数据。

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

