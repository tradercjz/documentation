# createCrossSectionalEngine

## 语法

`createCrossSectionalEngine(name, [metrics], dummyTable,
[outputTable], keyColumn, [triggeringPattern='perBatch'],
[triggeringInterval=1000], [useSystemTime=true], [timeColumn],
[lastBatchOnly=false], [contextByColumn], [snapshotDir],
[snapshotIntervalInMsgCount], [raftGroup], [outputElapsedMicroseconds=false],
[roundTime=true], [keyFilter], [updatedContextGroupsOnly=false])`

别名：`createCrossSectionalAggregator`

## 详情

创建横截面引擎，返回一个以 *keyColumn* 作为键值的键值表。

该表记录了每组最新记录的时间戳（可以是数据自身的时间戳或者系统时间，由参数 *timeColumn* 和
*useSystemTime* 指定）。每次新数据的到来都会更新该表。若指定了 *lastBatchOnly* =
true，此时引擎维护的键值表只会保留最新时间戳上不同组的数据。

* 如果没有指定 *metrics* 或*outputTable*，横截面引擎不会利用表中的数据进行任何运算和输出，仅更新表中记录。
* 如果指定了 *metrics* 和
  *outputTable*，横截面引擎会首先更新表中记录，然后对表中的最新记录进行运算，并把结果输出到 *outputTable*
  中。

更多流数据引擎的应用场景说明可以参考 [流计算引擎](../themes/streamingEngine.md)。

### 计算规则

可选按数据量或时间触发计算，详情请参考 *triggeringPattern* 和
*triggeringInterval* 的参数说明。

注： 若指定了
*contextByColumn*，则数据将按照指定字段分组后在组内进行计算。

### 引擎的其他功能

* 快照机制：启用快照机制之后，系统若出现异常，可及时将流数据引擎恢复到最新的快照状态。（详情请参考
  *snapshotDir* 和 *snapshotIntervalInMsgCount* 的参数说明）
* 流数据引擎高可用：若要启用引擎高可用，需在订阅端 raft 组的 leader 节点创建引擎并通过
  *raftGroup* 参数开启高可用。开启高可用后，当 leader 节点宕机时，会自动切换新 leader
  节点重新订阅流数据表。（详情请参考 *raftGroup* 的参数说明）

## 参数

**name** 字符串标量，表示横截面引擎的名称，作为其在一个数据节点/计算节点上的唯一标识。可包含字母，数字和下划线，但必须以字母开头。

**metrics** 以元代码的格式表示计算指标，支持输入元组。有关元代码的更多信息可参考[元编程](../../progr/objs/meta_progr.md)。

* 计算指标可以是系统内置或用户自定义的函数，如 <[sum(qty), avg(price)]>；可以对计算结果使用表达式，如
  <[avg(price1)-avg(price2)]>；也可以对多列进行运算，如 <[std(price1-price2)]>。
* *metrics* 内支持调用具有多个返回值的函数，例如 <func(price) as `col1`col2>（可不指定列名）。
* *metrics* 中使用的列名大小写不敏感，不要求与输入表的列名大小写保持一致。

**dummyTable** 一个表对象，和订阅的流数据表的 schema 一致，可以含有数据，亦可为空表。从 3.00.2 版本开始 *dummyTable* 支持包含
array vector 类型列。

**outputTable** 计算结果的输出表，可以是内存表或分布式表。使用
`createCrossSectionalEngine`
函数之前，需要将输出表预先设立为一个空表，并指定各列列名以及数据类型。

* 如果没有指定 *contextByColumn*， 则输出表各列的顺序如下：

  + 第一列为 TIMESTAMP 类型，用于存放发生计算的时间戳（如果指定了 *timeColumn*
    则是对应记录的时间戳）；

  + 计算结果列，可为多列。其数据类型必须与 *metrics* 返回结果的数据类型一致。
  + 耗时列，存储引擎内每个 batch 的计算耗时（单位：微秒），数据类型为 LONG。仅在指定
    *outputElapsedMicroseconds*= true 时输出。
  + 记录数列。存储引擎内每个 batch 的记录数，数据类型为 INT，仅在指定 *outputElapsedMicroseconds*=
    true 时输出。
* 如果指定 *contextByColumn*， 则输出表各列的顺序如下：
  + 第一列为 TIMESTAMP 类型，用于存放发生计算的时间戳（如果指定了 *timeColumn* 则是对应记录的时间戳）；
  + 第二列为 *contextByColumn* 指定的列；
  + 计算结果列，可为多列。其数据类型必须与 *metrics* 返回结果的数据类型一致。
  + 耗时列，存储引擎内每个 batch 的计算耗时（单位：微秒），数据类型为 LONG。仅在指定
    *outputElapsedMicroseconds*= true 时输出。
  + 记录数列。存储引擎内每个 batch 的记录数，数据类型为 INT，仅在指定 *outputElapsedMicroseconds*=
    true 时输出。

**keyColumn**
字符串标量或向量，指定流数据表中某列的值为横截面引擎的键值。横截面引擎的计算时，仅使用每个键值对应的最新一行记录。

**triggeringPattern**
字符串标量，表示触发计算的方式，每触发一次计算，输出一条结果到输出表。该字符串可选值如下：

* 'perBatch'：*triggeringPattern* 的默认值。每插入一次数据触发一次计算。
* 'perRow'：插入的每一行数据都会触发一次计算。
* 'interval'：基于系统时间间隔触发计算。
* 'keyCount'：若相同时间戳的数据分批次到达，则只有在当前时间戳的记录数达到
  *triggeringInterval*，或有更新时间戳的数据到达时，才会触发计算。使用该参数值时，必须指定
  *timeColumn*，且 *useSystemTime* = false。若设置
  *triggeringPattern* = 'keyCount'，收到的数据中出现的乱序数据会被丢弃，不参与计算。
* 'dataInterval'：基于数据时间间隔触发计算。使用该参数值时，必须指定 *timeColumn*，且指定
  *useSystemTime* = false。

**triggeringInterval** 整数或元组，触发计算规则如下：

* *triggeringPattern* 取值为 'interval' 时，*triggeringInterval*
  是一个正整数，表示触发计算的时间间隔，单位为毫秒，默认值为 1000。每经过 *triggeringInterval*
  指定的时间间隔，检查引擎中的数据是否被计算。若存在未被计算的数据，则触发一次计算。
* *triggeringPattern* 取值为 'keyCount' 时：
  + *triggeringInterval* 可以是一个整数。设置后，在更新的时间戳的数据到来前，当前时间戳的记录数需要累积到
    *triggeringInterval* 才会触发计算。
  + *triggeringInterval* 也可以是一个长度为 2 的
    元组。元组的第一个元素是整数，表示触发计算的最新时间戳的记录数量。元组的第二个值可以是整数或者 duration 类型数据。假设设置
    *triggeringInterval* = (c1, c2):
    - 当 c2 为整数时，若收到的最新时间戳 t1 的数据数量小于 c1，这批数据不会触发计算，系统可以继续缓存更新时间戳
      t2(t2>t1) 的数据，当 t2 的数据量达到 c2 或者收到更新的时间戳 t3(t3>t2)
      的数据时，会触发时间戳 t1 对应数据的计算。注意必须满足 c2 < c1。
    - 当 c2 为 duration 时，若收到的最新时间戳 t1 的数据数量小于
      c1，这批数据不会触发计算，系统收到更新的时间戳 t2(t2>t1) 的数据后，会等待 duration
      指定的时间，若在此期间继续收到了 t1 的数据且满足 t1 时间戳的数据总量达到 c1，或者在此期间又收到了更新的时间戳
      t3(t3>t2) 的数据，则直接触发 t1 对应数据的计算，等待时间结束后不再触发计算。否则，等待
      duration 设置的时间后才会触发 t1 数据的计算。
* *triggeringPattern* 取值为 'dataInterval' 时，*triggeringInterval*
  是一个正整数，单位和数据时间的单位一致，默认值为 1000。从第一条数据的时间戳开始一个窗口，窗口长度为
  *triggeringInterval*。一个窗口结束后到达的第一条数据会触发当前窗口内数据的计算输出。输出表的时间为窗口结束的时间戳。

注：

* 在 2.00.11.2 及之前版本，每个窗口都会输出。
* 从版本 2.00.11.3 起，仅当窗口内有数据插入时才会触发输出。

**useSystemTime** 可选参数，布尔值，表示是否使用数据注入引擎时的系统时间作为计算参照的时间列。

* 若 *useSystemTime* = true，*outputTable* 中第一列（时间列）为系统时间；
* 若 *useSystemTime* = false，必须指定 *timeColumn*，*outputTable*
  中第一列（时间列）为数据的时间戳。

**timeColumn** 是一个字符串。当 *useSystemTime* = false
时，指定订阅的流数据表中时间列的名称。仅支持 TIMESTAMP 类型。

**lastBatchOnly** 可选参数。横截面引擎是否只保留最新时间戳上的数据。当
*lastBatchOnly* = true 时，只能指定 *triggeringPattern* =
'keyCount'，此时横截面引擎维护的键值表只保存最新时间戳的键值数据；否则，更新并保留所有时间戳上的键值数据。

**contextByColumn**
可选参数，字符串标量或向量。设置后，将对横截面引擎中数据按照指定的字段或字段组合分组，并在组内进行指定计算。

* 设置该参数，必须指定 *metrics* 和 *outputTable*.
* 如果 *metrics* 全为聚合函数，则分组计算结果和 groupby 分组计算结果一致，否则和 contextby
  分组计算结果一致。

若要开启快照机制 (snapshot)，必须指定 **snapshotDir** 与
**snapshotIntervalInMsgCount**。

**snapshotDir** 可选参数，字符串，表示保存引擎快照的文件目录。

* 指定的目录必须存在，否则系统会提示异常。
* 创建流数据引擎时，如果指定了 *snapshotDir*，会检查该目录下是否存在快照。如果存在，会加载该快照，恢复引擎的状态。
* 多个引擎可以指定同一个目录存储快照，用引擎的名称来区分快照文件。
* 一个引擎的快照可能会使用三个文件名：
  + 临时存储快照信息：文件名为 <engineName>.tmp；
  + 快照生成并刷到磁盘：文件保存为 <engineName>.snapshot；
  + 存在同名快照：旧快照自动重命名为 <engineName>.old。

**snapshotIntervalInMsgCount** 可选参数，为整数类型，表示每隔多少条数据保存一次流数据引擎快照。

**raftGroup** 是流数据高可用订阅端 raft 组的 ID (大于 1 的整数，由流数据高可用相关的配置项
*streamingRaftGroups* 指定)。设置该参数表示开启计算引擎高可用。在 leader 节点创建流数据引擎后，会同步在
follower 节点创建该引擎。每次保存的 snapshot 也会同步到 follower。当 raft 组的 leader 节点宕机时，会自动切换新 leader
节点重新订阅流数据表。注意，若要指定 *raftGroup*，必须同时指定 *snapshotDir*。

**outputElapsedMicroseconds** 布尔值，表示是否输出每个 batch 中数据从注入引擎到计算输出的总耗时，以及每个 batch
包含的总记录数，默认为 false，不输出。

注： *outputElapsedMicroseconds*= true 时，若同时指定
*useSystemTime*=true，则 *metrics* 中不可使用聚合函数。

**roundTime** 可选参数，布尔值。用于对第一个数据窗口的起始时间进行规整，仅在
*triggeringPattern*=dataInterval 时有效。系统将根据该参数、triggeringInterval
和时间精度来确定规整尺度（alignmentSize）。窗口规整规则同[时序引擎](createTimeSeriesEngine.md)。

**keyFilter** 可选参数，以元代码形式表示的过滤条件。过滤条件是一个表达式或者函数调用，应用于截面数据中的列（列值为
key），返回一个布尔向量。引擎会从截面数据中过滤出 key 满足条件的数据进行计算。

**updatedContextGroupsOnly** 可选参数，布尔标量，默认值为 false。决定是否仅计算相较上次输出存在更新的分组数据。

## 例子

例1. 横截面引擎 csEngineDemo1 触发计算的方式为 "perRow"。6 行数据写入流数据表 trades1，结果亦为
6 行。

```
share streamTable(10:0,`time`sym`price`volume,[TIMESTAMP,SYMBOL,DOUBLE,INT]) as trades1
share table(1:0, `time`avgPrice`volume`dollarVolume`count, [TIMESTAMP,DOUBLE,INT,DOUBLE,INT]) as outputTable
csEngine1=createCrossSectionalEngine(name="csEngineDemo1", metrics=<[avg(price), sum(volume), sum(price*volume), count(price)]>, dummyTable=trades1, outputTable=outputTable, keyColumn=`sym, triggeringPattern="perRow", useSystemTime=false, timeColumn=`time)
subscribeTable(tableName="trades1", actionName="tradesStats", offset=-1, handler=append!{csEngine1}, msgAsTable=true)
insert into trades1 values(2020.08.12T09:30:00.000 + 123 234 456 678 890 901, `A`B`A`B`B`A, 10 20 10.1 20.1 20.2 10.2, 20 10 20 30 40 20);

select * from trades1;
```

| time | sym | price | volume |
| --- | --- | --- | --- |
| 2020.08.12T09:30:00.123 | A | 10 | 20 |
| 2020.08.12T09:30:00.234 | B | 20 | 10 |
| 2020.08.12T09:30:00.456 | A | 10.1 | 20 |
| 2020.08.12T09:30:00.678 | B | 20.1 | 30 |
| 2020.08.12T09:30:00.890 | B | 20.2 | 40 |
| 2020.08.12T09:30:00.901 | A | 10.2 | 20 |

```
select * from outputTable;
```

| time | avgPrice | volume | dollarVolume | count |
| --- | --- | --- | --- | --- |
| 2020.08.12T09:30:00.123 | 10 | 20 | 200 | 1 |
| 2020.08.12T09:30:00.234 | 15 | 30 | 400 | 2 |
| 2020.08.12T09:30:00.456 | 15.05 | 30 | 402 | 2 |
| 2020.08.12T09:30:00.678 | 15.1 | 50 | 805 | 2 |
| 2020.08.12T09:30:00.890 | 15.15 | 60 | 1010 | 2 |
| 2020.08.12T09:30:00.901 | 15.2 | 60 | 1012 | 2 |

例2. 横截面引擎 csEngineDemo2 触发计算的方式为 "perBatch"。数据分为 2 个批次写入流数据表
trades2，结果为 2 行。

```
share streamTable(10:0,`time`sym`price`volume,[TIMESTAMP,SYMBOL,DOUBLE,INT]) as trades2
share table(1:0, `time`avgPrice`volume`dollarVolume`count, [TIMESTAMP,DOUBLE,INT,DOUBLE,INT]) as outputTable
csEngine2=createCrossSectionalEngine(name="csEngineDemo2", metrics=<[avg(price), sum(volume), sum(price*volume), count(price)]>, dummyTable=trades2, outputTable=outputTable, keyColumn=`sym, triggeringPattern="perBatch", useSystemTime=false, timeColumn=`time)
subscribeTable(tableName="trades2", actionName="tradesStats", offset=-1, handler=append!{csEngine2}, msgAsTable=true)
insert into trades2 values(2020.08.12T09:30:00.000 + 123 234 456, `A`B`A, 10 20 10.1, 20 10 20);
sleep(1)
insert into trades2 values(2020.08.12T09:30:00.000 + 678 890 901, `B`B`A, 20.1 20.2 10.2, 30 40 20);

select * from outputTable;
```

| time | avgPrice | volume | dollarVolume | count |
| --- | --- | --- | --- | --- |
| 2020.08.12T09:30:00.456 | 15.05 | 30 | 402 | 2 |
| 2020.08.12T09:30:00.901 | 15.2 | 60 | 1012 | 2 |

例3. 横截面引擎 csEngineDemo4 触发计算的方式为 "keyCount"。设置
*lastBatchOnly* = true，只有最新时间戳上的数据会参与计算。因为 *metrics*
里聚合函数和非聚合函数混合使用，所以，输出记录行数等于输入记录行数，聚合结果重复输出多行。

```
share streamTable(10:0,`time`sym`price`volume,[TIMESTAMP,SYMBOL,DOUBLE,INT]) as trades1
share table(1:0, `time`factor1`factor2, [TIMESTAMP, DOUBLE,INT]) as outputTable
agg=createCrossSectionalAggregator(name="csEngineDemo4", metrics=<[price+ 0.1, sum(volume)]>, dummyTable=trades1, outputTable=outputTable, keyColumn=`sym, triggeringPattern="keyCount", triggeringInterval=5, useSystemTime=false, timeColumn=`time,lastBatchOnly=true)
subscribeTable(tableName=`trades1, actionName="csEngineDemo4", msgAsTable=true, handler=append!{agg})
num=10
time=array(TIMESTAMP)
time=take(2018.01.01T09:30:00.000,num)
sym=take("A"+string(1..10),num)
price=1..num
volume=1..num
tmp=table(time, sym, price, volume)
trades1.append!(tmp)

// 第二次输入 5 条数据，lastBatchOnly=true，所以只有最新的 5 条数据参与计算。
num=5
time = array(TIMESTAMP)
time=take(2018.01.01T09:30:01.000,num)
sym=take("A"+string(1..10),num)
price=6..10
volume=6..10
tmp=table(time, sym, price, volume)
trades1.append!(tmp)
```

| time | factor1 | factor2 |
| --- | --- | --- |
| 2018.01.01T09:30:00.000 | 1.1 | 55 |
| 2018.01.01T09:30:00.000 | 2.1 | 55 |
| 2018.01.01T09:30:00.000 | 3.1 | 55 |
| 2018.01.01T09:30:00.000 | 4.1 | 55 |
| 2018.01.01T09:30:00.000 | 5.1 | 55 |
| 2018.01.01T09:30:00.000 | 6.1 | 55 |
| 2018.01.01T09:30:00.000 | 7.1 | 55 |
| 2018.01.01T09:30:00.000 | 8.1 | 55 |
| 2018.01.01T09:30:00.000 | 9.1 | 55 |
| 2018.01.01T09:30:00.000 | 10.1 | 55 |
| 2018.01.01T09:30:01.000 | 6.1 | 40 |
| 2018.01.01T09:30:01.000 | 7.1 | 40 |
| 2018.01.01T09:30:01.000 | 8.1 | 40 |
| 2018.01.01T09:30:01.000 | 9.1 | 40 |
| 2018.01.01T09:30:01.000 | 10.1 | 40 |

例4. 横截面引擎 csEngineDemo3 触发计算的方式为 "interval"，每 500
毫秒触发一次计算。向流数据表中写入6行数据，第一次批量写入，间隔 500 毫秒后再次写入。请注意，这里没有指定 *useSystemTime* 参数为
false，会返回计算发生的时刻。

```
share streamTable(10:0,`time`sym`price`volume,[TIMESTAMP,SYMBOL,DOUBLE,INT]) as trades3
share table(1:0, `time`avgPrice`volume`dollarVolume`count, [TIMESTAMP,DOUBLE,INT,DOUBLE,INT]) as outputTable
csEngine3=createCrossSectionalEngine(name="csEngineDemo3", metrics=<[avg(price), sum(volume), sum(price*volume), count(price)]>, dummyTable=trades3, outputTable=outputTable, keyColumn=`sym, triggeringPattern="interval", triggeringInterval=500)
subscribeTable(tableName="trades3", actionName="tradesStats", offset=-1, handler=append!{csEngine3}, msgAsTable=true);

insert into trades3 values(2020.08.12T09:30:00.000, `A, 10, 20)
insert into trades3 values(2020.08.12T09:30:00.000 + 500, `B, 20, 10)
insert into trades3 values(2020.08.12T09:30:00.000 + 1000, `A, 10.1, 20)
insert into trades3 values(2020.08.12T09:30:00.000 + 2000, `B, 20.1, 30)
sleep(500)
insert into trades3 values(2020.08.12T09:30:00.000 + 2500, `B, 20.2, 40)
insert into trades3 values(2020.08.12T09:30:00.000 + 3000, `A, 10.2, 20);
sleep(500)

select * from outputTable;
```

| time | avgPrice | volume | dollarVolume | count |
| --- | --- | --- | --- | --- |
| 2022.03.02T11:17:02.341 | 15.1 | 50 | 805 | 2 |
| 2022.03.02T11:17:02.850 | 15.2 | 60 | 1,012 | 2 |

*triggeringPattern* = "interval" 时，系统每隔 500ms 触发一次计算，输出一条结果。在计算被触发时，即使同一个 key
有多条记录未被计算，系统也只取最新时间戳上的数据进行计算。

例5. 在股票数据中，有些股票在某一时刻之后就不再更新数据了，此时可通过 *keyFilter*
参数指定过滤条件。当之后收到其它股票数据并触发截面计算时不会计算该股票的数据。以在截面引擎中过滤出1小时内未更新的数据为例：

```
// 定义休市和过滤数据的逻辑
def checkTime(time){
    maxTime = max(time)
    if(between(maxTime, 2024.05.22T13:00:00.000:2024.05.22T13:30:00.000)){
        return time > maxTime - 120*60*1000
    } else{
        return time > maxTime - 30*60*1000
    }
}
// 定义截面引擎
share streamTable(10:0,`time`sym`price`volume,[TIMESTAMP,SYMBOL,DOUBLE,INT]) as trades1
t=keyedTable(`sym,10:0,`time`sym`price`volume,[TIMESTAMP,SYMBOL,DOUBLE,INT])
share table(1:0, `time`factor1`factor2, [TIMESTAMP, DOUBLE, DOUBLE]) as outputTable
// 指定 keyFilter 为一个函数，过滤出1小时内未更新的数据。
csEngine5=createCrossSectionalEngine(name="csEngineDemo5", metrics=<[avg(price), sum(volume)]>, dummyTable=trades1, outputTable=outputTable, keyColumn=`sym, keyFilter=<checkTime(time)>)
// 模拟数据，A1 从 2024.05.22T09:32:00.000 之后未收到新的数据
time = 2024.05.22T09:30:00.000 join 2024.05.22T09:31:00.000 join 2024.05.22T09:32:00.000 join 2024.05.22T13:30:00.000 join 2024.05.22T13:31:00.000
sym=`A1`A2`A1`A2`A2
price=100.0 100.5 100.3 100.8 100.6
volume=100 110 112 200 120
tmp=table(time, sym, price, volume)
csEngine5.append!(tmp)
// 查看截面引擎中的数据
select * from csEngine5
```

| time | sym | price | volume |
| --- | --- | --- | --- |
| 2024.05.22T09:32:00.000 | A1 | 100.3 | 112 |
| 2024.05.22T13:31:00.000 | A2 | 100.6 | 120 |

上面代码通过 *keyFilter* 找到截面引擎中仅 A2 的数据满足要求，因此结果表中仅 A2
的数据参与了计算。

```
select * from outputTable
```

| time | factor1 | factor2 |
| --- | --- | --- |
| 2024.05.22T05:11:12.259 | 100.6 | 120 |

在以上的例子中， `createCrossSectionalEngine`
的返回结果（以下成为横截面表）是为计算提供的一个中间结果，但横截面表亦可为最终结果。例如若需要定时刷新某只股票的最新交易价格，
按照常规思路是从实时交易表中按代码筛选股票并取出最后一条记录，而交易表的数据量是随着时间快速增长的，如果频繁做这样的查询，无论从系统的资源消耗还是从查询的效能来看都不是最优的做法。
而横截面表永远只保存所有股票的最近一次交易数据，数据量是稳定的，对于这种定时轮询的场景非常合适。

要将横截面表作为最终结果，需要在对 `createCrossSectionalEngine` 中的 *metrics* 与
*outputTable* 这两个参数置空。

```
tradesCrossEngine=createCrossSectionalEngine(name="CrossSectionalDemo", dummyTable=trades, keyColumn=`sym, triggeringPattern=`perRow)
```

例6. 按照 volume 分组，引擎每插入一行数据，就触发一次计算。

```
try {
    dropAggregator(`csEngineDemo)
} catch(ex) {}
try {
    dropStreamTable(`trades1)
} catch(ex) {}
share streamTable(10:0, `time`sym`price`volume, [SECOND, SYMBOL, DOUBLE, INT]) as trades1
outputTable = table(1:0, `time`volume`factor1`factor2, [SECOND, INT, DOUBLE, DOUBLE])
agg1 = createCrossSectionalEngine(
    name="csEngineDemo",
    metrics=<[avg(price), sum(volume)]>,
    dummyTable=trades1,
    outputTable=outputTable,
    keyColumn=`sym,
    triggeringPattern="perRow",
    useSystemTime=false,
    timeColumn=`time,
    outputElapsedMicroseconds=false,
    contextByColumn=`volume,
    updatedContextGroupsOnly=false
)

num = 4
time = take(09:30:00, num)
sym = take(`A1`B1`C1`D1, num)
price = rand(100.0, num)
volume = take(1 1 2 2, num)
tmp = table(time, sym, price, volume)
agg1.append!(tmp)
outputTable
```

以上创建的引擎根据 volume 分组后得到 1 和 2 两个分组。由于设置了 *updatedContextGroupsOnly* =
false，引擎不会检查各个分组的数据是否有更新。每当插入一行数据时，都会触发所有分组的计算和输出，因此， outputTable 中将输出 6 行数据。

| time | volume | factor1 | factor2 |
| --- | --- | --- | --- |
| 09:30:00 | 1 | 82.3447 | 1 |
| 09:30:00 | 1 | 69.9793 | 2 |
| 09:30:00 | 1 | 69.9793 | 2 |
| 09:30:00 | 2 | 95.262 | 2 |
| 09:30:00 | 1 | 69.9793 | 2 |
| 09:30:00 | 2 | 80.5988 | 4 |

```
try{dropAggregator(`csEngineDemo)}catch(ex){}
try{dropStreamTable(`trades1)}catch(ex){}

share streamTable(10:0,`time`sym`price`volume,[SECOND,SYMBOL,DOUBLE,INT]) as trades1
outputTable = table(1:0, `time`volume`factor1`factor2, [SECOND, INT, DOUBLE, DOUBLE])
agg1=createCrossSectionalEngine(name="csEngineDemo", metrics=<[avg(price), sum(volume)]>, dummyTable=trades1, outputTable=outputTable, keyColumn=`sym, triggeringPattern="perRow",useSystemTime=false, timeColumn=`time, outputElapsedMicroseconds=false, contextByColumn=`volume, updatedContextGroupsOnly=false)
num=4
time = take(09:30:00, num)
sym= take(`A1`B1`C1`D1, num)
price=rand(100.0, num)
volume=take(1 1 2 2, num)
tmp=table(time, sym, price, volume)
agg1.append!(tmp)
outputTable

```

设置 *updatedContextGroupsOnly* = true 后，引擎将仅计算本次插入的分组数据，因此，outputTable 中将输出 4
行数据。

| time | volume | factor1 | factor2 |
| --- | --- | --- | --- |
| 09:30:00 | 1 | 54.6926 | 1 |
| 09:30:00 | 1 | 40.5904 | 2 |
| 09:30:00 | 2 | 73.1741 | 2 |
| 09:30:00 | 2 | 46.0153 | 4 |

