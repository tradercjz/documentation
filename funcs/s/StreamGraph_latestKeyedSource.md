# StreamGraph::latestKeyedSource

## 语法

`StreamGraph::latestKeyedSource(name, keyColumn, timeColumn, capacity:size,
colNames, colTypes, [asyncWrite=true], [compress=true], [cacheSize],
[retentionMinutes=1440], [flushMode=0], [preCache], [cachePurgeTimeColumn],
[cachePurgeInterval], [cacheRetentionTime])`

## 详情

创建一个最新值键值流数据表，并将它持久化到磁盘上。参考 [latestKeyedStreamTable](../l/latestkeyedstreamtable.md) 和 [enableTableShareAndPersistence](../e/enableTableShareAndPersistence.md)。

**返回值**：一个 DStream 对象。

## 参数

**name** 表示持久化共享流表的名称。字符串标量，可以传入完整的流表全限定名（如
trading.orca\_graph.trades）；也可以仅提供流表名（如 trades），系统会根据当前的 catalog 设置自动补全为对应的全限定名。

**timeColumn** 字符串标量或长度为 2 的向量，分别用于指定 1 个或 2 个时间列。当仅指定 1 个时间列时，该列可以为整型或时间类型；当指定 2
个时间列时，第 1 列必须是 DATE 类型，第 2 列则是 TIME, SECOND 或 NANOTIME 类型。通过这两列，可以共同确定唯一的时间值。

**capacity** 是正整数，表示建表时系统为该表分配的内存（以记录数为单位）。当记录数超过
*capacity* 时，系统首先会分配 *capacity*
1.2~2倍的新的内存空间，然后复制数据到新的内存空间，最后释放原来的内存。对于规模较大的表，此类操作的内存占用会很高。因此，建议建表时预先分配一个合理的
*capacity*。

**size** 是整数，表示该表新建时的行数。若 *size* =0，创建一个空表。 若
*size*>0，则建立一个只包含 size 条记录的表，记录初始值如下：

* BOOL 类型默认值为 false；
* 数值类型、时间类型、IPADDR、COMPLEX、POINT 的默认值为 0；
* Literal, INT128 类型的默认值为 NULL。

注： 如果
*colTypes* 指定为数组向量， *size* 必须为0。

**colNames** 是一个向量，表示列名。

**colTypes**
是一个向量，表示每列的数据类型，支持数组向量类型和元组（ANY）类型。可使用表示数据类型的系统保留字或相应的字符串。

**asyncWrite** 可选参数，是一个布尔值，表示是否异步持久化数据到磁盘。默认值为
true，流数据写入内存即为写入成功，持久化到磁盘的操作将会由另一个线程执行。

注：

持久化数据到磁盘包含两个步骤：

* 写内存数据到操作系统缓存
* 写缓存数据到磁盘（是否开启同步刷盘由参数 *flushMode* 决定）

**compress** 可选参数，是一个布尔值，表示是否以压缩模式模式保存至磁盘。默认值为 true。

**cacheSize** 可选参数，整数，表示流数据表在内存中最多保留多少行。如果未指定该参数，则所有记录行都会保存在内存中。如果
*cacheSize* 小于 1000，它会被自动调整为 1000。

**retentionMinutes** 可选参数，是一个整数，表示文件大小超过 1GB的 log
文件的保留时间(从文件的最后修改时间开始计算)，单位是分钟。默认值是 1440，即一天。如果 log 文件未达 1GB，则会一直保留至大小达到 1GB。

**flushMode** 可选参数，是一个整数，表示是否开启同步刷盘，取值只能为 0 或 1。默认值是
0，表示异步刷盘，内存中的流数据写入操作系统缓存即为写入成功，并进行下一批数据的写入。 若为
1，则表示同步刷盘，当前批次的流数据必须落盘完成，才会进行下一批数据的写入。

**preCache** 可选参数，是一个整数，表示从磁盘加载到内存的记录条数。如果没有指定该参数，默认会把所有记录加载到内存中。

**cachePurgeTimeColumn** 可选参数，字符串标量，需要指定为持久化流表中的时间列名称。

**cachePurgeInterval** 可选参数，DURATION 类型标量，表示触发清理内存中数据的时间间隔。

**cacheRetentionTime** 可选参数，DURATION
类型标量，表示内存中数据的最长保留期限。

## 例子

```
if (!existsCatalog("orca")) {
	createCatalog("orca")
}
go
use catalog orca

g = createStreamGraph("indicators")
g.latestKeyedSource("trade", `symbol, `time, 1:0, `time`symbol`price`volume, [DATETIME,SYMBOL,DOUBLE,LONG])
```

