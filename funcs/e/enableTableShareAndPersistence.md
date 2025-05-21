# enableTableShareAndPersistence

## 语法

`enableTableShareAndPersistence(table, tableName, [asynWrite=true],
[compress=true], [cacheSize], [retentionMinutes=1440], [flushMode=0],
[preCache],[cachePurgeTimeColumn],[cachePurgeInterval],[cacheRetentionTime])`

## 参数

**table** 是一个空的流数据表。

**tableName** 是一个字符串，表示 table 共享后的名称。

**asynWrite** 可选参数，是一个布尔值，表示是否异步持久化数据到磁盘。默认值为
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

注： 自 3.00.2 版本起，该函数要求参数 *cacheRetentionTime* 必须小于
*cachePurgeInterval*。

## 详情

该命令将流数据表共享，并把它持久化到磁盘上。

为了保证该命令能够正常执行，需要在配置文件中（单节点：dolphindb.cfg，集群：cluster.cfg）指定配置参数
*persistenceDir*，配置参考：[功能配置](../../db_distr_comp/cfg/function_configuration.md)。流数据表在磁盘上的存储目录是
<PERSISTENCE\_DIR>/<TABLE\_NAME>。目录包含两种类型的文件：数据文件（名称类型
*data0.log, data1.log...*）和索引文件
*index.log*。把这些数据保存到磁盘后，如果重启系统，再次执行该命令会把磁盘中的数据加载到内存中，加载的记录条数由参数 *preCache*
指定，但是实际加载的记录条数有可能会超过 *preCache*。

参数 *asynWrite*
会告知系统是否以异步模式保存表。在异步模式中，追加的数据会被放进队列，之后用于保存的工作线程把数据写入磁盘。在同步模式中，表的追加数据操作直到追加数据被保存到磁盘中才完成。该参数的默认值是
true，即为异步模式。通常情况下，异步模式实现更高的吞吐量，但是如果服务器崩溃，可能会丢失最后追加的行。在异步模式中，保存表的工作是由单个工作线程完成，并且一个工作线程可能处理多个表。如果只保存一个表，增加工作线程的数量并不会提升性能。

默认情况下，流数据表将所有数据保存在内存中。如果流数据表太大，系统可能会出现内存不足的情况。为了避免内存不足的问题，可以通过以下两种方式之一来清理内存中的数据：

* 配置 *cacheSize*
  参数时，如果插入的数据使内存中流数据表的行数达到阈值，系统将清理内存中较旧的已发布记录。阈值确定规则如下：

  + 每次 append 的数据都不超过 *cacheSize* 时，内存中的记录数不会大于 *cacheSize* 的
    2.5 倍。
  + 否则，当 append 的数据超过 *cacheSize* 时，内存中的记录数不会超过追加行数和
    *cacheSize* 之和的 1.2 倍。
* 同时配置 *cachePurgeTimeColumn*, *cachePurgeInterval* 和
  *cacheRetentionTime*，系统将根据时间列清理数据。每次插入新数据时，系统会计算新数据与内存中第一条数据的时间戳差值，当差值大于等于
  *cachePurgeInterval* 时，系统仅保留时间戳与新数据时间戳差值小于等于
  *cacheRetentionTime*的数据，清理其它数据。

注：

* 如果手动重启 server，建议调用 [fflush](../f/fflush.md) 函数先把缓存区的数据写入磁盘使用 `kill -15` 命令 进程。
* 如果设置 asynWrite=true，此时流数据写入速度最快，若 server 发生 crash
  可能导致部分数据丢失。
* 如果设置 asynWrite=false，flushmode=0，此时流数据写入速度中等，server 发生
  crash 不会丢失数据，但操作系统崩溃可能导致部分数据丢失。
* 如果设置 asynWrite=false，flushmode=1，此时流数据写入速度最慢，server 发生
  crash 或操作系统崩溃都不会导致数据丢失。
* 不可以将同一个流数据表通过修改共享变量名称的方式共享 2 次及以上。

## 例子

例1.

```
colName=["time","x"]
colType=["timestamp","int"]
t = streamTable(100:0, colName, colType);
enableTableShareAndPersistence(table=t, tableName=`st, cacheSize=1200000)
go;
```

```
for(s in 0:200){
  n=10000
  time=2019.01.01T00:00:00.000+s*n+1..n
  x=rand(10.0, n)
  insert into st values(time, x)
}
```

```
getPersistenceMeta(st);

/* output:
sizeInMemory->800000
asynWrite->true
totalSize->2000000
compress->true
memoryOffset->1200000
retentionMinutes->1440
sizeOnDisk->2000000
persistenceDir->/home/llin/hzy/server1/pst/st
hashValue->0
diskOffset->0
*/
```

例2. 本例将说明 *cachePurgeTimeColumn*, *cachePurgeInterval* 和
*cacheRetentionTime* 的使用方法。

```
colName=["time","x"]
colType=["timestamp","int"]
t1 = streamTable(100:0, colName, colType);

enableTableShareAndPersistence(table=t1,tableName=`st1, cachePurgeTimeColumn=`time, cachePurgeInterval=duration("7H"),cacheRetentionTime=duration("2H"))

go;

time=2019.01.01T00:00:00.000
for(s in 0:6000){
  time = temporalAdd(time,1,"m");
  x=rand(10.0, 1)
  insert into st1 values(time, x)
}

getPersistenceMeta(st1);

/* output:
lastLogSeqNum->-1
sizeInMemory->300
totalSize->12000
asynWrite->true
compress->true
raftGroup->-1
memoryOffset->11700
retentionMinutes->1440
sizeOnDisk->11879
persistenceDir->/home/ffliu/jjxu/DolphinDB_Linux64_V3.0/server/persistence/st1
hashValue->0
diskOffset->0
*/
```

**相关信息**

* [disableTablePersistence](../d/disableTablePersistence.html "disableTablePersistence")
* [clearTablePersistence](../c/clearTablePersistence.html "clearTablePersistence")
* [getPersistenceMeta](../g/getPersistenceMeta.html "getPersistenceMeta")

