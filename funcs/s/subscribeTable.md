# subscribeTable

## 语法

`subscribeTable([server],tableName,[actionName],[offset=-1],handler,[msgAsTable=false],[batchSize=0],[throttle=1],[hash=-1],[reconnect=false],[filter],[persistOffset=false],[timeTrigger=false],[handlerNeedMsgId=false],[raftGroup],[userId=""],[password=""],[udpMulticast=false])`

## 详情

从客户端节点订阅本地或远程服务器的流数据表。可在 *handler* 调用函数来处理订阅数据。

返回一个订阅主题（topic），即一个订阅的名称。它是一个字符串，由订阅表所在节点的别名、流数据表名称和订阅任务名称（如果指定了
*actionName*）组合而成，使用 "/" 分隔。如果订阅主题已经存在，函数将会抛出异常。

* 如果指定了 *batchSize*，当未处理消息数量达到 *batchSize* 或距离上次
  *handler* 被触发已过去 *throttle* 秒，*handler* 将会被触发。
* 如果订阅的表被重定义了，为了保证订阅能够正常使用，需要使用 [unsubscribeTable](../u/unsubscribeTable.html)
  命令取消订阅，然后重新创建订阅。
* 在高可用订阅流数据写入分布式表的场景下，订阅节点构成的 raft 组发生 leader
  切换或集群重启时，可能导致之前登录的用户退出。由于 guest 用户无权限写入分布式表，写入会被中断（可以通过 [getCurrentSessionAndUser](../g/getCurrentSessionAndUser.html) 函数查看当前的用户）。若配置 *userId* 和
  *password* 参数，用户退出后系统会自动尝试重新登录，以保证订阅数据成功写入分布式表。需要注意的是，从 2.00.10.10 开始，用户可以通过配置项
  *enhancedSecurityVerification* 控制在登录时是否约束密码重试的次数。若不设置
  *enhancedSecurityVerification*，则不约束；若设置
  *enhancedSecurityVerification*=true，则当用户登录时，在1分钟内连续5次使用了错误密码，会导致用户被锁定，必须等待10分钟后才可以再次登录。

如果使用 UDP 组播作为订阅发布方式，为保证组播性能，需要为发布端所在服务器的 socket 缓冲区设置合理的数值，推荐数值大于或等于 1MB。在 Linux 中的
socket 缓冲区的设置方法如下：

* 在 Linux 终端中，运行以下命令：

  ```
  sudo sysctl -w net.core.rmem_default=1048576
  sudo sysctl -w net.core.rmem_max=1048576
  sudo sysctl -w net.core.wmem_default=1048576
  sudo sysctl -w net.core.wmem_max=1048576
  ```
* 也可以编辑 */etc/sysctl.conf* 文件，添加或修改 *net.core.rmem\_default*,
  *net.core.rmem\_max*, *net.core.wmem\_default* 和
  *net.core.wmem\_max* 的值为 1048576
  后运行

  ```
  sudo sysctl -p
  ```

注： 在 TCP 和 UDP 之间切换订阅发布方式时，需要先使用
`unsubscibeTable` 取消已有订阅，再使用 `subscribeTable`
建立新的订阅任务。

注： 为流数据 join 引擎订阅数据时，*handler* 参数需要为
`appendForJoin`、[getLeftStream](../g/getLeftStream.html) 或 [getRightStream](../g/getRightStream.html) 函数。

## 参数

只有 **tableName** 和 **handler** 两个参数是必选参数。其他所有参数都是可选参数。

**server**
是一个字符串，表示服务器的别名或远程连接的句柄。如果未指定或者为空字符串，表示流数据所在的服务器是本地实例。

**tableName** 是被订阅的数据表名。该表必须为共享的流数据表。

**actionName**
是一个字符串，表示订阅任务的名称。它可以包含字母，数字和下划线，并以字母开头。如果一个节点有多个订阅任务均订阅了同一张表，则每个订阅必须指定唯一的
*actionName*。

**offset** 是一个整数，指定订阅任务的起始位置，对应流数据表中的一行记录。正整数表示从指定位置的记录开始订阅。其特殊取值含义如下：

* 当 *offset* = -1（默认）时，订阅将从流数据表的**当前最新行**开始，接收实时新增的数据。
* 当 *offset* = 0
  时，系统将从流表的**第一条记录**开始订阅。注意：若流表开启了持久化，系统会清理超过指定保留时间的数据，此时设置*offset* =
  0 可能会导致订阅失败，建议指定 offset =
  getPersistenceMeta(StreamTable).diskOffset，从持久化流表**内存中的第一行记录**开始订阅。
* 若流表开启持久化，指定 *offset* = -2，且 *persistOffset* =
  true，系统会从**上一次流订阅结束的位置**开始订阅。
* 当 *offset* = -3
  时，从流表的**当前可获取的最早一条记录**开始订阅，包括内存中和持久化在磁盘上的数据。

注意：*offset* 是相对于流数据表创建时的第一行的定位，内存数据回收不会影响持久化数据的定位。

**handler** 是一元函数、二元函数或数据表，用于处理订阅的数据。

* 一元函数：它唯一的参数是订阅的数据。订阅的数据可以是一个表或元组，订阅数据表的每个列是元组的一个元素。
* *handlerNeedMsgId* = true 时，*handler*
  必须是二元函数，其两个参数分别是订阅的数据（msgBody）和数据偏移量（msgId）。详见 *handlerNeedMsgId*
  参数说明。
* 数据表：可以是流数据引擎、共享流数据表、共享内存表、共享键值表、共享索引表或 DFS 表。订阅数据会直接插入到该表中。

**msgAsTable** 是布尔值，表示订阅的数据是否为表。默认值是 false，表示订阅的数据是由列组成的元组。

**batchSize** 是一个整数。若为正数，表示未处理消息的数量达到 *batchSize*
时，*handler* 才会处理消息。若未指定或为非正数，每一批次的消息到达之后，*handler* 就会马上处理。

**throttle** 是一个浮点数，单位为秒，默认值为1。表示继上次 *handler* 处理消息之后，若
*batchSize* 条件一直未达到，多久后再次处理消息。如果没有指定 *batchSize*，*throttle*
即使指定，也不起作用。 若 *throttle* 需要设置小于1秒，则需要先修改配置项 *subThrottle*。

**hash**
是一个非负整数，指定某个订阅线程处理进来的消息。如果没有指定该参数，系统会自动分配一个线程。如果需要使用同一个线程来处理多个订阅任务的消息，可把这些订阅任务的 hash
设置为相同的值。

**reconnect** 是一个布尔值，表示订阅中断后，是否会自动重新订阅。默认值为 false。如果
*reconnect* = true，有以下三种情况：

* 如果发布端与订阅端处于正常状态，但是网络中断，那么订阅端会在网络正常时，自动从中断位置重新订阅。
* 如果发布端崩溃，订阅端会在发布端重启后不断尝试重新订阅。
  + 如果发布端对流数据表启用了持久化，发布端重启后会首先读取硬盘上的数据，直到发布端读取到订阅中断位置的数据，订阅端才能成功重新订阅。
  + 如果发布端没有对流数据表启用持久化，那么订阅端将自动重新订阅失败。
* 如果订阅端崩溃，订阅端重启后不会自动重新订阅，需要重新执行 subscribeTable 函数。

注： 如果订阅高可用流数据表，需要设置 *reconnect* 为 true，以保证 leader
发生切换时可以成功连接新的 leader。

**filter**用来指定过滤条件。主要分以下两种用法：

* 若配合 [setStreamTableFilterColumn](setStreamTableFilterColumn.html) 函数一起使用来指定流数据表的过滤列，则流数据表过滤列在 *filter*
  中的数据才会发布到订阅端，不在 *filter* 中的数据不会发布。*filter* 不支持过滤 BOOL
  类型数据。*filter* 参数可以使用以下三种方法指定。
  + 值过滤：一个向量。
  + 范围过滤：一个数据对。范围包含下限值，但不包括上限值。
  + 哈希过滤：一个元组。第一个元素表示 bucket 的个数；第二个元素是一个标量或数据对，其中标量表示 bucket
    的索引（从0开始），数据对表示 bucket 的索引范围（包含下限值，但不包括上限值）。

* 若传入自定义函数进行灵活过滤，可以通过如下两种方式传入：

  + 函数：直接传入一个函数，则订阅的数据会以表的形式传入函数，并把函数返回的结果发送给订阅者。
  + 字符串：传入表示函数名称的字符串，或者是一个 lambda 表达式的字符串。

**persistOffset**
是一个布尔值，表示是否持久化保存最新一条已经处理的订阅数据的偏移量。持久化保存的偏移量用于重订阅，可通过 [getTopicProcessedOffset](../g/getTopicProcessedOffset.html)
函数获取。默认值为 false。

注：

* 若要订阅高可用流数据表，需要设置 *persistOffset* 为 true，以防止订阅端丢失数据。
* 设置 *persistOffset* 为
  true，且取消订阅（`unsubscribeTable`）时，设置 *removeOffset* =
  false，再次订阅时才会从持久化保存的偏移量开始订阅。

**timeTrigger** 是一个布尔值。若设为 true，表示即使没有新的消息进入，*handler* 也会在
*throttle* 参数所设定的时间间隔被触发。

**handlerNeedMsgId** 是一个布尔值，默认值为 false。

* 若设为 true，*handler* 必须支持两个参数：一个是 msgBody（传入的消息），一个是
  msgId（消息的偏移量）。如：以部分应用的形式固定 [appendMsg](../a/appendMsg.html)
  的 *engine* 参数后，将其作为二元应用传入 *handler*。
* 若设为 false，*handler* 仅支持一个参数：msgBody。调用 *handler* 时，只传入消息本身。

**raftGroup** 是 raft 组的 ID。设置该参数表示开启订阅端高可用，不设置则表示普通订阅。设置
*raftGroup* 参数以指定 raft 组后，在对应 raft 组内 leader 发生切换时，新的 leader 会重新订阅。

注： `subscribeTable` 函数如果指定了
*raftGroup*，则只能在 leader 上执行。若同时指定 *handlerNeedMsgId* = true，则
*handler* 只能是计算引擎，即 *handler* = engine(创建引擎时的句柄变量)或 *handler*
= getStreamEngine(engineName)。

**userId** 字符串，表示用户名。

**password** 字符串，表示用户密码。

**udpMulticast** 布尔值，默认为 false。用于设置是否开启 UDP （User Datagram
Protocol）Multicast 数据传输协议。设置为 true 后，发布端将通过 UDP 协议、以组播的方式将订阅数据发布到组播通道上。

使用 TCP 和 UDP 组播进行发布订阅的性能差异如下：

| 协议 | 优点 | 缺点 | 适用场景 |
| --- | --- | --- | --- |
| TCP | * 数据传输可靠，能够确保按序到达订阅端 * 能够检测和纠正传输中的错误 | 一对一的连接方式决定了当订阅端为多个时，需要占用发布端大量的服务器资源及网络带宽 | * 可靠性要求高 * 顺序性要求高 |
| UDP Multicast | * 可以一次性将数据发布给多个订阅端，适合实时数据传输 * 发布端服务器资源和网络带宽占用少 | 数据包可能会缺失或乱序 | 有多个订阅端、要求快速实时传输数据 |

注：

1. 启用该参数前，需要确保 *reconnect*, *persisitOffset*, *timeTrigger* 设置为
   false，以及 *raftGroup* 设置为 -1。
2. 目前仅 Linux 版本的 DolphinDB Server 支持该参数。
3. 在使用该参数前，请确保发布端和接收端所在的网络的路由器或交换机是否支持 UDP Multicast 协议栈。

## 例子

例1

下面是关于流计算的例子。在本例中，集群有两个节点：DFS\_NODE1 和 DFS\_NODE2。我们需要在
cluster.cfg 中指定 *maxPubConnections和subPort* 参数来启动发布/订阅功能。例如：

```
maxPubConnections=32
DFS_NODE1.subPort=9010
DFS_NODE1.persistenceDir=C:/DolphinDB/Data
DFS_NODE2.subPort=9011
```

在 DFS\_NODE1 上执行以下脚本：

1. 创建一个共享的流数据表 trades\_stream，并以同步模式保存。此时，表 trades\_stream
   有0行记录。

   ```
   n=20000000
   colNames = `time`sym`qty`price
   colTypes = [TIME,SYMBOL,INT,DOUBLE]
   enableTableShareAndPersistence(table=streamTable(n:0, colNames, colTypes), tableName="trades_stream", asynWrite=false, cacheSize=n)
   go
   ```
2. 创建一个分布式表 trades。此时，表 trades
   有0行记录。

   ```
   if(existsDatabase("dfs://STREAM_TEST")){
        dropDatabase("dfs://STREAM_TEST")
   }
   dbDate = database(directory="", partitionType=VALUE, partitionScheme=temporalAdd(date(today()),0..30,'d'))
   dbSym= database(directory="", partitionType=RANGE, partitionScheme=string('A'..'Z') join "ZZZZ")
   db = database(directory="dfs://STREAM_TEST", partitionType=COMPO, partitionScheme=[dbDate, dbSym])
   colNames = `date`time`sym`qty`price
   colTypes = [DATE,TIME,SYMBOL,INT,DOUBLE]
   trades = db.createPartitionedTable(table=table(1:0, colNames, colTypes), tableName="trades", partitionColumns=`date`sym)
   ```
3. 创建表 trades\_stream 的本地订阅。使用 saveTradesToDFS 函数把表 trades\_stream 的流数据和今天的日期保存至表
   trades。

   ```
   def saveTradesToDFS(mutable dfsTrades, msg): dfsTrades.append!(select today() as date,* from msg)
   subscribeTable(tableName="trades_stream", actionName="trades", offset=0, handler=saveTradesToDFS{trades}, msgAsTable=true, batchSize=100000, throttle=60)
   ```
4. 创建表 trades\_stream 的另一个本地订阅。使用每分钟的流数据计算成交量加权平均价格（vwap），并以异步模式把结果保存至共享的流数据表
   vwap\_stream
   中。

   ```
   n=1000000
   tmpTrades = table(n:0, colNames, colTypes)
   lastMinute = [00:00:00.000]
   colNames = `time`sym`vwap
   colTypes = [MINUTE,SYMBOL,DOUBLE]
   enableTableShareAndPersistence(table=streamTable(n:0, colNames, colTypes), tableName="vwap_stream")
   go

   def calcVwap(mutable vwap, mutable tmpTrades, mutable lastMinute, msg){
       tmpTrades.append!(msg)
       curMinute = time(msg.time.last().minute()*60000l)
       t = select wavg(price, qty) as vwap from tmpTrades where time < curMinute, time >= lastMinute[0] group by time.minute(), sym
       if(t.size() == 0) return
       vwap.append!(t)
       t = select * from tmpTrades where time >= curMinute
       tmpTrades.clear!()
       lastMinute[0] = curMinute
       if(t.size() > 0) tmpTrades.append!(t)
   }
   subscribeTable(tableName="trades_stream", actionName="vwap", offset=0, handler=calcVwap{vwap_stream, tmpTrades, lastMinute}, msgAsTable=true, batchSize=100000, throttle=60)
   ```

在 DFS\_NODE2 上执行以下脚本，创建表 trades\_stream 的远程订阅，并以异步模式把流数据保存至表
trades\_stream\_slave 中。

```
n=20000000
colNames = `time`sym`qty`price
colTypes = [TIME,SYMBOL,INT,DOUBLE]
enableTableShareAndPersistence(table=streamTable(n:0, colNames, colTypes), tableName="trades_stream_slave", cacheSize=n)
go
subscribeTable(server="DFS_NODE1", tableName="trades_stream", actionName="slave", offset=0, handler=trades_stream_slave)
```

在 DFS\_NODE1
上执行以下脚本，模拟3支股票在10分钟内的流数据。每支股票每分钟生成2,000,000条记录。每分钟的数据被插入到流数据表 trades\_stream
的600个数据块中。每两个数据块有100毫秒的时间间隔。

```
n=10
ticks = 2000000
rows = ticks*3
startMinute = 09:30:00.000
blocks=600
for(x in 0:n){
    time = startMinute + x*60000 + rand(60000, rows)
    indices = isort(time)
    time = time[indices]
    sym = array(SYMBOL,0,rows).append!(take(`IBM,ticks)).append!(take(`MSFT,ticks)).append!(take(`GOOG,ticks))[indices]
    price = array(DOUBLE,0,rows).append!(norm(153,1,ticks)).append!(norm(91,1,ticks)).append!(norm(1106,20,ticks))[indices]
    indices = NULL
    blockSize = rows / blocks
    for(y in 0:blocks){
        range =pair(y * blockSize, (y+1)* blockSize)
        insert into trades_stream values(subarray(time,range), subarray(sym,range), 10+ rand(100, blockSize), subarray(price,range))
        sleep(100)
    }

    blockSize = rows % blocks
    if(blockSize > 0){
        range =pair(rows - blockSize, rows)
        insert into trades_stream values(subarray(time,range), subarray(sym,range), 10+ rand(100, blockSize), subarray(price,range))
    }
}
```

在 DFS\_NODE1 上执行以下脚本来检查结果：

```
trades=loadTable("dfs://STREAM_TEST", `trades)
select count(*) from trades
```

预期结果有 60,000,000 条记录。

```
select * from vwap_stream
```

表 vwap\_stream 预期有 27 条记录。

在 DFS\_NODE2 上执行以下脚本：

```
select count(*) from trades_stream_slave
```

我们看到的结果小于 60,000,000 行，因为部分表的记录已经保存到磁盘中。

例2

在集群的 dnode1
上执行以下脚本创建流数据表
publisher：

```
share streamTable(10:0,`time`id`value,[TIMESTAMP,INT,DOUBLE])
              as publisher
```

在 dnode2 节点执行以下脚本，采用 UDP 组播订阅 dnode1 上的
publisher，将其写入本地流表
sub1：

```
sub1 = streamTable(10:0,`time`id`value,[TIMESTAMP,INT,DOUBLE])
            subscribeTable(server="dnode1",tableName="publisher",actionName="sub1",offset=-1,handler=append!{sub1},msgAsTable=true,
            udpMulticast=true)
```

在 dnode1
节点模拟数据写入：

```
publisher.tableInsert(table(now()+1..10*1000 as time,1..10 as
              id, rand(100,10) as value))
```

此时在 dnode1 可以查看 UDP
组播发布状态：

`getStreamingStat().udpPubTables`

| tableName | channel | msgOffset | actions | subNum |
| --- | --- | --- | --- | --- |
| publisher | 224.1.1.1:1235 | 10 | sub1 | 1 |

在 dnode2
可以查看订阅工作线程状态

`getStreamingStat().subWorkers`

| workerId | topic | type | queueDepthLimit | queueDepth | processedMsgCount | lastMsgId | failedMsgCount | lastFailedMsgId | lastFailedTimestamp | lastErrMsg | msgAsTable | batchSize | throttle | hash | filter | persistOffset | timeTrigger | handlerNeedMsgId | raftGroup |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 2 | localhost:8702:dnode1/publisher/sub1 | udp | 10,000,000 | 0 | 10 | 9 | 0 | -1 |  |  | true | 0 | 0 | 1 |  | false | false | false |

例3

传入自定义函数 `filterFn`
对订阅数据进行过滤。

```
st = streamTable(100:0, `sym`val, `SYMBOL`DOUBLE)
enableTableShareAndPersistence(st, `st1, cacheSize=1000)

outTable = table(100:0, `sym`val, `SYMBOL`DOUBLE)

filterFn = def (msg) {
	return (select * from msg where val > 50.0)
}

subscribeTable(tableName=`st1, actionName=`testFilter, handler=tableInsert{outTable}, filter="filterFn", offset=0)

for (i in 1..100) {
	n = 100
	t = table(rand(`A`B`C, n) as sym, rand(100.0, n) as val)
	st.append!(t)
}
select * from outTable
```

`subscribeTable` 中关于参数 *filter*的另一种表述方式：

```
filterFn = "def (msg) { return (select * from msg where val > 50.0) }"
subscribeTable(tableName=`st1, actionName=`testFilter, handler=tableInsert{outTable}, filter=filterFn, offset=0)
```

