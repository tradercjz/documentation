# replay

## 语法

`replay(inputTables, outputTables, [dateColumn], [timeColumn], [replayRate],
[absoluteRate=true], [parallelLevel=1], [sortColumns],
[preciseRate=false])`

## 详情

根据指定的回放模式，按时间顺序将一个或多个数据表或数据源列表（由 [replayDS](replayDS.html) 函数的返回值）的数据回放到数据表，以模拟实时数据写入，通常用于高频策略回测场景。

### 回放形式

根据输入表到输出表的映射（mapping），`replay` 支持 1 对 1，N 对 N，N
对 1 三种回放形式。

相比于N对N回放，N个1对1的各个回放相互独立。当 *inputTables* 指定为数据源列表时，N对N
回放形式可以确保所有回放的第一个数据源回放完，再开始回放第二个数据源。

相比于N对N回放无法保证所有表的数据在全局上的时间顺序，N对1回放形式可以确保不同表的数据写入目标表的顺序与时间字段的先后顺序严格一致。

### 回放模式

根据回放速度的不同设定，`replay` 提供以下四种回放模式：

* 指定每秒回放记录数：如果 *replayRate* 为正整数，且
  *absoluteRate* 为 true，则回放的速率基于记录数计算，系统按照每秒 *replayRate*
  条记录进行回放。
* 指定时间跨度回放加速倍数：如果 *replayRate* 为正整数，并且
  *absoluteRate* 为 false，则根据输入表数据的时间跨度加速 *replayRate*
  倍回放。注意，每秒回放的记录数是相同的。
* 全速回放：如果 *replayRate* 未指定或者为负，无论
  *absoluteRate* 为 false 还是 true，系统都将以最快的速率进行回放。
* 精确速度回放：如果 *replayRate* 为正整数，且 *preciseRate* 为
  true，则数据完全按照事件时间进行倍速回放。系统根据两条相邻数据的时间间隔加速 *replayRate*
  倍依次回放每条数据。例如，*replayRate* 为 2 时，原本时间戳相差 t 毫秒 的相邻两条数据，会尽量以 t/2
  毫秒的时间间隔依次回放。

### 回放过程

1. 数据加载（仅当输入表是数据源列表时）。

   从磁盘加载数据源到内存时，用户可以指定 *parallelLevel*
   参数并行加载数据，以提升性能。数据加载和数据回放异步进行。
2. 分批回放。

   每批回放的记录数和回放耗时受回放模式和系统性能影响。

   | 回放模式 | 每批数据包含的记录数 | 取数据的方式 | 回放耗时 |
   | --- | --- | --- | --- |
   | 按指定记录数回放（数据总数为 s） | *replayRate* 条数据请注意：此模式下每秒回放一批数据。若输入表是数据源列表（即从磁盘加载）时，回放速度亦受磁盘IO性能制约。若一秒内加载的数据量小于 *replayRate*，则将已加载的数据作为一个批次进行回放。 | 1 对 1：从单表取一批数据。N 对 1 / N 对 N：根据数据的时间戳顺序，从 N 张表中取一批数据。 | 约为 s/replayRate 秒 |
   | 按时间跨度加速回放(数据时间跨度为 n 秒，数据总数为 s) | replayRate\*s/n 条数据（若不足 1 条，则取 1 条）请注意：此模式下每秒回放一批数据。若输入表是数据源列表（即从磁盘加载）时，回放速度亦受磁盘IO性能制约。若一秒内加载的数据量小于 replayRate\*s/n，则将已加载的数据作为一个批次进行回放。 | 1 对 1：从单表取一批数据。N 对 1 / N 对 N：根据数据的时间戳顺序，从 N 张表中取一批数据。 | 约为 n/replayRate 秒 |
   | 全速回放 | 每次回放时系统已加载的所有数据 | 1 对 1：同上。N 对 1：同上。N 对 N：逐一回放各输入表，每次从单表取一批数据。 | 取决于系统性能 |

   注： 上表的回放耗时计算方法适用于评估同构回放的耗时，异构回放的耗时会略高于同构回放。

   回放过程中，系统会先从内存按批取出数据并回放。`replay`
   只保证同一批次数据的回放结果是有序的。因此，在调用 `replay` 函数前，请将输入表按照指定的时间列（由参数
   *dateColumn* 和 *timeColumn* 决定）排序。
3. 数据写入。

   注： 目前系统仅支持单线程写入输出表。
4. 终止回放：可使用 [cancelJob](../c/cancelJob.html) 和 [cancelConsoleJob](../c/cancelConsoleJob.html) 命令。

   注：
   * 2.00.5 版本前，N 对 1 回放要求输入表结构必须相同，称为同构回放。自
     2.00.5 版本起，N 对 1
     回放开始支持输入结构不同的表，称为异构回放。由于异构回放到输出表的记录均被序列化存储，无法直接读取，需要通过 [streamFilter](../s/streamFilter.html)
     进行数据过滤和分发，详情请参考 [streamFilter](../s/streamFilter.html)。
   * 2.00.9 版本后，若 N 对 1
     回放的输入表为多个数据源列表，会自动按照时间戳排序后回放。在该版本前，系统每次仅加载多个列表相同索引位置的数据源排序后回放，不保证全局的有序性。

## 参数

根据回放形式的不同， **inputTables** 的数据形式也有所不同：

* 1 对 1 回放时，*inputTables* 是一个未分区的表或数据源列表。
* N 对 1 同构回放或 N 对 N 回放时，*inputTables*
  是多个未分区的表或数据源列表构成的元组。
* N 对 1 异构回放时，*inputTables* 是一个字典。字典的 key
  可以是任意数据类型，表示输入表或数据源列表的唯一标识，value 是一个表对象或数据源列表。

根据回放形式的不同， **outputTables** 的数据形式也有所不同：

* 1 对 1 回放或 N 对 1
  同构回放时，*outputTables*\_是一个表对象（未分区的内存表/流数据表）或表示共享表名的字符串，必须与输入表的 schema
  相同。
* N 对 N 回放，*outputTables*
  是多个表对象（未分区的内存表/流数据表）或表示共享表名的字符串构成的元组，且它的长度必须与 *inputTables*
  相同。输出表和输入表一一对应，且 schema 必须相同。
* N 对 1 异构回放时 *outputTables* 是
  一个表对象（未分区的内存表/流数据表），至少包含三列：

其中：

* 第一列为 *dateColumn* 和 *timeColumn* 指定的回放时间的时间戳；
* 第二列为 SYMBOL 或 STRING 类型，对应 *inputTables* 字典的 key；
* 第三列为 BLOB 类型，用于存储被回放的每条记录序列化后的结果。

此外，可输出各输入表的公共列（列名和类型一致的列）。

**dateColumn** 和 **timeColumn**
为时间列的列名，至少指定其中一个参数。根据回放形式的不同，*dateColumn* 和 *timeColumn* 的取值有所区别：

* 1 对 1 回放或 N 对 1 同构回放: 输入表与输出表的时间列列名必须相同，指定为字符串标量；
* N 对 N 回放：输入表时间列的列名相同，指定为字符串标量；输入表时间列的列名不同，指定为字符串向量；
* N 对 1 异构回放：输入表时间列的列名相同，指定为字符串标量；输入表时间列的列名不同，指定为字典，其中 key 为输入表的唯一标识符，value
  是对应表时间列的列名。

只指定 *dateColumn* 或 *timeColumn* 中的一个参数，或者 *dateColumn* 和
*timeColumn* 指定为同一列时，对指定的时间列的类型没有限制。

若指定 *dateColumn* 和 *timeColumn* 为不同列，*dateColumn* 必须是 DATE
类型，*timeColumn* 只能是 SECOND, TIME 或 NANOTIME 类型。

**replayRate** 整数，和参数 *absoluteRate* 共同决定了回放的速率。

**absoluteRate** 布尔值。默认值为 true，表示系统每秒按 *replayRate*
指定的记录数回放。若为 false，表示依照数据的时间跨度加速 *replayRate* 倍回放。

**parallelLevel** 正整数，表示从数据源加载数据到内存的工作线程数量，默认值为 1。如果
*inputTables* 不是数据源，无需指定该参数。

**sortColumns**
字符串标量或者长度为2的向量。相同回放时间戳的数据将根据该参数指定的字段进行排序。仅异构回放支持该参数。

注： 该参数可以指定 *inputTables*
的非公共列。若某个输入表不存在指定的非公共列，则填充空值且将其前置。

**preciseRate** 布尔值。默认值为 false，表示不开启精确速度回放。若指定为 true，则系统根据相邻记录的时间戳，以
*replayRate* 指定的倍数精确回放。

## 例子

### 一对一回放

以下为按不同回放模式进行一对一回放的例子

```
n=1000
sym = take(`IBM,n)
timestamp= take(temporalAdd(2012.12.06T09:30:12.000,1..500,'s'),n)
volume = rand(100,n)
trades=table(sym,timestamp,volume)
trades.sortBy!(`timestamp)
share streamTable(100:0,`sym`timestamp`volume,[SYMBOL,TIMESTAMP,INT]) as st
```

* 每秒回放100条数据：

  ```
  timer replay(inputTables=trades, outputTables=st, dateColumn=`timestamp,
      timeColumn=`timestamp,replayRate=100, absoluteRate=true);
   Time elapsed: 10001.195 ms
  ```

  表 trades 中一共有1000条数据，每秒回放100条耗时大约10秒。
* 加速100倍时间回放：

  ```
  timer replay(inputTables=trades,outputTables=st,dateColumn=`timestamp,
      timeColumn=`timestamp,replayRate=100,absoluteRate=false);
    Time elapsed: 5001.909 ms
  ```

  表 trades 中的最大时间与最小时间相差500秒，加速 100 倍时间回放耗时大约5秒。
* 以最快的速率回放：

  ```
  timer replay(inputTables=trades,outputTables=st,dateColumn=`timestamp,
      timeColumn=`timestamp);
    Time elapsed: 0.974 ms
  ```
* 精确速度回放：

  ```
  timer replay(inputTables=trades,outputTables=st,dateColumn=`timestamp,
      timeColumn=`timestamp,replayRate=100,absoluteRate=false, preciseRate=true);
    Time elapsed: 4991.177 ms
  ```

  表 trades 中，以相邻两条记录时间戳的 100 倍速度回放，回放时间大约 4.99 秒。

### N 对 N 回放

以下为将多个数据源列表回放到多个输出表中的例子。

以下脚本将两个数据源回放到连接引擎，进行 asof join 计算。

```
n=50000
sym = rand(symbol(`IBM`APPL`MSFT`GOOG`GS),n)
date=take(2012.06.12..2012.06.16,n)
time=rand(13:00:00.000..16:59:59.999,n)
volume = rand(100,n)
t1=table(sym,date,time,volume).sortBy!([`date, `time])

sym = rand(symbol(`IBM`APPL`MSFT`GOOG`GS),n)
date=take(2012.06.12..2012.06.16,n)
time=rand(13:00:00.000..16:59:59.999,n)
price = 100 + rand(10.0,n)
t2=table(sym,date,time,price).sortBy!([`date, `time])

if(existsDatabase("dfs://test_stock")){
dropDatabase("dfs://test_stock")
}
db=database("dfs://test_stock",VALUE,2012.06.12..2012.06.16)
pt1=db.createPartitionedTable(t1,`pt1,`date).append!(t1)
pt2=db.createPartitionedTable(t2,`pt2,`date).append!(t2)

left = table(100:0,`sym`dt`volume,[SYMBOL,TIMESTAMP,INT])
right = table(100:0,`sym`dt`price,[SYMBOL,TIMESTAMP,DOUBLE])

opt=table(100:0, `dt`sym`volume`price`total, [TIMESTAMP, SYMBOL, INT, DOUBLE, DOUBLE])
ajEngine=createAsofJoinEngine(name="ajEngine", leftTable=left, rightTable=right,
    outputTable=opt, metrics=<[volume, price, volume*price]>,
    matchingColumn=`sym, timeColumn=`dt, useSystemTime=false, delayedTime=1)

ds1=replayDS(sqlObj=<select sym, concatDateTime(date, time) as dt, volume from pt1>,
    dateColumn=`date, timeColumn=`time,
    timeRepartitionSchema=[13:00:00.000, 14:00:00.000, 15:00:00.000, 16:00:00.000, 17:00:00.000])
ds2=replayDS(sqlObj=<select sym, concatDateTime(date, time) as dt, price from pt2>,
    dateColumn=`date, timeColumn=`time,
    timeRepartitionSchema=[13:00:00.000, 14:00:00.000, 15:00:00.000, 16:00:00.000, 17:00:00.000])

replay(inputTables=[ds1,ds2], outputTables=[getLeftStream(ajEngine),
    getRightStream(ajEngine)], dateColumn=`dt);

select count(*) from opt
```

返回：50000

### 异构回放

异构回放中，回放的输出表通常注入 streamFilter 引擎，进一步过滤分发处理。

```
n=1000
sym = take(`IBM`GS,n)
myDate=take(2021.01.02..2021.01.06, n).sort!()
myTime=take(09:30:00..15:59:59,n)
vol =  array(INT[], 0, 10)
for(i in 0:n){vol.append!([rand(100,3)])}
t=table(sym,myDate,myTime,vol)

sym = take(`IBM`GS,n)
date=take(2021.01.02..2021.01.06, n).sort!()
time=take(09:30:00..15:59:59,n)
vol =  array(INT[], 0, 10)
for(i in 0:n){vol.append!([rand(100,3)])}
price =  array(DOUBLE[], 0, 10)
for(i in 0:n){price.append!([rand(10.0,3)])}
t1=table(sym, date,time,vol,price)

if(existsDatabase("dfs://test_stock1")){
  dropDatabase("dfs://test_stock1")
}
db1=database("",RANGE, 2021.01.02..2021.01.07)
db2=database("",VALUE,`IBM`GS)
db=database("dfs://test_stock1",COMPO,[db1, db2], engine="TSDB")
orders=db.createPartitionedTable(t,`orders,`myDate`sym, sortColumns=`sym`myDate`myTime)
orders.append!(t);
trades=db.createPartitionedTable(t1,`trades,`date`sym, sortColumns=`sym`date`time)
trades.append!(t1);
// 获取数据源
ds = replayDS(sqlObj=<select * from loadTable(db, `orders)>, dateColumn=`myDate, timeColumn=`myTime)
ds.size();
ds1 = replayDS(sqlObj=<select * from loadTable(db, `trades)>, dateColumn=`date, timeColumn=`time)
ds1.size();

input_dict  = dict(["msg1", "msg2"], [ds, ds1])
date_dict = dict(["msg1", "msg2"], [`myDate, `date])
time_dict = dict(["msg1", "msg2"], [`myTime, `time])
// replay 的输出表，被订阅输入 streamFilter
share streamTable(100:0,`timestamp`sym`blob`vol, [DATETIME,SYMBOL, BLOB, INT[]]) as opt

filterOrder=table(100:0, `sym`date`time`volume, [SYMBOL, DATE, SECOND, INT[]])
filterTrades=table(100:0, `sym`date`time`volume`price, [SYMBOL, DATE, SECOND, INT[], DOUBLE[]])
// 定义 streamFilter 输入表
share streamTable(100:0,`timestamp`sym`blob`vol, [DATETIME,SYMBOL, BLOB, INT[]]) as streamFilter_input
// streamFilter 对接收的数据进行处理，分别分发到表 filterOrder 和 filterTrades
filter1=dict(STRING,ANY)
filter1['condition']=`msg1
filter1['handler']=filterOrder

filter2=dict(STRING,ANY)
filter2['condition']=`msg2
filter2['handler']=filterTrades
schema=dict(["msg1","msg2"], [filterOrder, filterTrades])
stEngine=streamFilter(name=`streamFilter, dummyTable=streamFilter_input,
    filter=[filter1,filter2], msgSchema=schema)
subscribeTable(tableName="opt", actionName="sub1", offset=0, handler=stEngine, msgAsTable=true)

replay(inputTables=input_dict, outputTables=opt, dateColumn = date_dict,
    timeColumn=time_dict,  replayRate=100, absoluteRate=false);

select count(*) from filterOrder
```

返回：1000

```
select count(*) from filterTrades
```

返回：1000

**相关信息**

* [replayDS](replayDS.html "replayDS")

