# createStreamDispatchEngine

## 语法

`createStreamDispatchEngine(name, dummyTable, keyColumn,
outputTable, [dispatchType='hash'], [hashByBatch=false], [outputLock=true],
[queueDepth=4096], [outputElapsedTime=false], [mode='buffer'])`

## 详情

创建流数据分发引擎，返回一个表对象。该引擎将输入的数据分发到不同的输出表，以实现负载均衡。其中输出表可以是内存表，分布式表或流数据引擎。

引擎特性：

* 支持多线程输入和多线程输出。
* 只提供数据分发功能，不提供指标计算功能。

场景应用：

将快照数据分发给一个或多个计算引擎进行因子计算，以提高计算性能。

## 参数

**name** 字符串，表示流数据分发引擎的名称，可包含字母，数字和下划线，但必须以字母开头。

**dummyTable** 表对象，和订阅的流数据表的 schema 一致，可以含有数据，亦可为空表。

**keyColumn** 字符串。若设置，则会以 *dispatchType* 指定的方式，基于该列分发数据。*keyColumn*
列中的每个唯一值被视为一个 key。

**outputTable** 表对象，若 *outputElapsedTime*= false，则 *outputTable* 的表结构和
*dummyTable* 相同；否则 *outputTable* 比 *dummyTable* 在最后多了一个 LONG
类型和一个 INT 类型的列，分别表示每一个 batch 的输出耗时（单位是微秒）及其输出时的时间戳（精度为纳秒）。

可以指定1~100个输出表。引擎会为每个表创建一个线程来接收分发到该表的数据。以 tuple 或嵌套 tuple
的方式指定多张表，例如：outputTable=[table1, table2, table3,
table4]，表示将注入的数据平均分发到4张表中，每张表的数据不同；outputTable=[[table1\_1, table1\_2], [table2\_1,
table2\_2]]，则会将数据拆分并复制。两份副本分别分发到各个子元素中对应的表中。具体来说，副本1的数据分发到 table1\_1
table1\_2，副本2的数据分发到 table2\_1 和 table2\_2。此时 table1\_1 和 table2\_1
除耗时和时间列外，其它列的数据相同；table1\_2 和 table2\_2 除耗时和时间列外，其它列的数据相同。

**dispatchType** 可选参数，字符串，可选值为：

* "hash"（默认值）：对 *keyColumn*
  列进行哈希计算，并根据计算结果，将数据分发到各个输出表。由于哈希计算得到的分布不一定均匀，因此可能会出现数据分配不均的情况。
* "uniform"：按照 *keyColumn* 列，将数据均匀分发到各个输出表。
* "saltedHash"：对 *keyColumn* 列进行加盐处理，然后进行哈希计算。通过[加盐处理](https://en.wikipedia.org/wiki/Salt_%28cryptography%29)，可以确保即使输入相同，也能产生独特的哈希值，从而避免碰撞。该选项在需要进行多层哈希分发的场景（例如分发引擎嵌套分发引擎，且都采用哈希计算进行数据分发）中更为适用。

提示： 建议使用默认的分发方式，即 "hash"。如果因为哈希分配不均匀而影响性能，则可以尝试使用
"uniform" 方式。

**hashByBatch** 可选参数, 布尔类型。该参数决定了是否将一个 batch 中的所有数据输出到同一个表中。默认为 false，表示对一个 batch
中的所有 key 分组后，按照 *dispatchType* 指定的方式分发数据。 仅当 *dispatchType*='hash' 时，才可设置
*hashByBatch*=true，此时，引擎随机取 batch 中一个 key 进行哈希计算，根据计算结果，将该 batch
中的所有数据输出到某一个表。

注： 当 *hashByBatch*=false 时，可以保证相同
key 的数据被输出到同一张表，但是这种分组操作会增加一些开销。

**outputLock** 可选参数，布尔类型，默认值为
true，表示是否对输出表进行加锁以避免并发访问的冲突。若设置为
false，则不对输出表进行加锁，此时需要保证其他线程不会对输出表进行并发操作。一般情况下，建议使用默认值（true）。

当除了分发引擎以外，还有其他线程（比如其他引擎、流订阅等等）写入到输出表时，输出表需要加锁（因为内存表不允许并发写入），但加锁会增加开销。但在某些场景下，例如在输出线程数量大于等于输入线程数量，且能保证多个输入线程不会同时向一个输出线程写入数据的场景下，如果用户能保证只有一个线程写入输出表，则可以设置该参数为
false，即不对输出表加锁，以提高数据分发的性能。

**queueDepth** 可选参数，正整数，默认为4096（单位为行）。

* *mode* = “buffer” 时，表示每个输出线程的缓存表大小。
* *mode* = “queue” 时，表示每个输出线程的队列深度。

建议根据输入数据的记录数大小，适当调节该参数。如果输入数据量较小但该参数设置过大，则会导致内存空间的浪费；相反，如果输入数据量较大但该参数设置过小，可能会导致数据输出阻塞。

**outputElapsedTime** 可选参数，布尔类型，表示是否输出每个 batch 从注入引擎到分发输出的总耗时。默认为
false，不输出总耗时。若设置为 true，则会在输出表最后两列中输出耗时（单位为微秒）和数据输出的时间戳（单位为纳秒）。

**mode** 可选参数，字符串，可选值为：

* "buffer"（默认值）：引擎会为每个输出线程创建一个内存缓存表，并将待分发的数据复制到缓存表中。对于数据写入引擎过程中，可能会并发读写输入表，或频繁
  append 数据到引擎且每次 append 的数据量较小的场景，建议使用该配置。
* "queue"：引擎为每一个输出线程维护一个数据队列，只将输入表的引用加入到分发队列，不复制数据。此配置要求写入数据的过程中不能对输入表进行并发读写，适合不频繁
  append 数据到引擎且每次 append 的数据量较大的场景。

## 例子

通过分发引擎，将流数据表中的数据分发到3个状态引擎，以进行因子计算，最终将结果输出到同一个输出表中。

```
//定义状态引擎的输入和输出表
share streamTable(1:0, `sym`price, [STRING,DOUBLE]) as tickStream
share streamTable(1000:0, `sym`factor1, [STRING,DOUBLE]) as resultStream
//定义将要使用的输出表。这里定义3个状态引擎。
for(i in 0..2){
rse = createReactiveStateEngine(name="reactiveDemo"+string(i), metrics =<cumavg(price)>, dummyTable=tickStream, outputTable=resultStream, keyColumn="sym")
}
//定义分发引擎
dispatchEngine=createStreamDispatchEngine(name="dispatchDemo", dummyTable=tickStream, keyColumn=`sym, outputTable=[getStreamEngine("reactiveDemo0"),getStreamEngine("reactiveDemo1"),getStreamEngine("reactiveDemo2")])

//订阅流数据表tickStream
subscribeTable(tableName=`tickStream, actionName="sub", handler=tableInsert{dispatchEngine}, msgAsTable = true)

//订阅的数据注入引擎
n=100000
symbols=take(("A" + string(1..10)),n)
prices=100+rand(1.0,n)
t=table(symbols as sym, prices as price)
tickStream.append!(t)

select count(*) from resultStream
100,000

//查看状态引擎状态
getStreamEngineStat().ReactiveStreamEngine
```

| name | user | status | lastErrMsg | numGroups | numRows | numMetrics | metrics | snapshotDir | snapshotInterval | snapshotMsgId | snapshotTimestamp | garbageSize | memoryUsed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| dispatchDemo | admin | OK | 0 | 100,000 | 0 | 0 | -1 | 0 | 0 |  |  |  |  |

