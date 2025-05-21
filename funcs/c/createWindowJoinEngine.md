# createWindowJoinEngine

## 语法

`createWindowJoinEngine(name, leftTable, rightTable,
outputTable, window, metrics, matchingColumn, [timeColumn],
[useSystemTime=false], [garbageSize = 5000], [maxDelayedTime], [nullFill],
[outputElapsedMicroseconds=false], [sortByTime], [closed], [snapshotDir], [snapshotIntervalInMsgCount],
[cachedTableCapacity=1024], [keyPurgeFreqInSec])`

## 详情

创建流数据 window join 引擎。返回一个左、右两表实时 [window join](../../progr/sql/windowjoin.html) 后的表对象。

该引擎与 window join 存在以下区别：

* window join 仅支持聚合计算，window join 引擎支持聚合计算，也支持非聚合计算。
* 计算指标中的列未指定表名时，window join 默认取右表列，而 window join 引擎默认取左表列。

注入 window join 引擎左、右两表的数据，根据 *matchingColumn*
分组。在各分组内，左表的每条记录，都会同右表中一个时间区间（即窗口）内的数据进行连接，并根据指定的 *metrics* 计算窗口内的数据并输出。

* 普通窗口（*window* 不为 0:0）：

  右表的计算窗口将由左表当前数据的时间戳和 *window* 确定。假设左表当前记录的时间戳为 t，*window* 为
  a:b，则右表时间戳属于 [t+a, t+b] 的数据将与左表当前记录连接并计算输出。

  触发计算的规则：
  + *useSystemTime*=false：
    - **同组数据触发：**各分组当前窗口数据的计算将由该窗口结束后的第一条属于该分组的数据触发。触发计算的数据不参与该窗口的计算。
    - **其它分组数据触发：**对于某个分组中未发生计算的窗口，若其窗口右边界 +
      *maxDelayedTime* <
      右表最新收到的任意一个分组数据的时间戳，则该窗口的计算将被新收到的这条数据触发。
  + *useSystemTime*=true：当系统时间到达各分组未发生计算的窗口的右边界时，触发该窗口的计算。
* 特殊窗口（*window* 为 0:0）：

  右表的计算窗口将由左表当前数据和其上一条数据的时间戳决定。默认情况下，该窗口左闭右开，假设左表当前记录的时间戳为 t，上一条记录的时间戳为 t0，则右表计算窗口为 [t0, t)。可以通过指定参数 *closed* = “right”，设置窗口为左开右闭。
  触发计算的规则：

  + *useSystemTime*=false：各分组当前窗口数据的计算将由窗口结束后的第一条属于该分组的右表数据触发。
  + *useSystemTime*=true：各个分组收到的左表数据将触发对应分组窗口的数据计算输出。

注：

*window*=0:0 时，若 *metrics* 中指定了非聚合的指标，其输出列必须为对应类型的
array vector。

更多流数据引擎的应用场景说明可以参考 [流计算引擎](../themes/streamingEngine.html)。

## 参数

**name** 必选参数，表示 window join
引擎的名称，作为其在一个数据节点/计算节点上的唯一标识。可包含字母，数字和下划线，但必须以字母开头。

**leftTable** 表对象。可以不包含数据，但结构必须与订阅的流数据表相同。2.00.9.3 版本开始支持
array vector 类型。

**rightTable** 表对象。可以不包含数据，但结构必须与订阅的流数据表相同。

**outputTable** 必选参数，为计算结果的输出表。window join 引擎会将计算结果插入该表。

* 输出表各列的顺序如下：
  1. 时间列。其中：
     + 若 *useSystemTime* = true，为 TIMESTAMP 类型；
     + 若 *useSystemTime* = false，数据类型与 *timeColumn* 列一致。
  2. 连接列。与 *matchingColumn* 中的列以及其顺序一致，可为多列。
  3. 计算结果列。可为多列。
  4. 耗时列。若指定 *outputElapsedMicroseconds* =
     true，则需要增加一个 LONG 类型和一个 INT 类型的列，分别用于存储引擎内部每个 batch
     的数据耗时（单位：微秒）和记录数。

**window** 必选参数，表示滑动窗口区间的整型或 DURATION 数据对，其中左右边界都包含在内。

**metrics** 以元代码的格式表示计算指标，支持输入元组。有关元代码的更多信息可参考 [元编程](../../progr/objs/meta_progr.html)。

* 计算指标可以是一个或多个表达式、系统内置或用户自定义函数。
* *metrics* 内支持调用具有多个返回值的函数，且必须指定列名，例如 <func(price) as
  `col1`col2>。

  若在 *metrics* 指定了 *leftTable* 和
  *rightTable* 中具有相同名称的列，默认取左表的列，可以通过 "tableName.colName"
  指定该列来自哪个表。

  注：
  + *metrics* 中使用的列名大小写不敏感，不要求与输入表的列名大小写保持一致。
  + 当以下函数只计算 *rightTable* 中的数据列时，window join 引擎对它们进行了优化：sum,
    sum2, avg, std, var, corr, covar, wavg, wsum, beta, max, min,
    last, first, med, percentile。

**matchingColumn** 表示连接列的字符串标量/向量/tuple，支持 Integral, Temporal 或
Literal（UUID 除外）类型。*matchingColumn* 指定规则为：

1. 只有一个连接列：当左表和右表的连接列名相同时，*matchingColumn* 是一个字符串标量，否则是一个长度为 2 的
   tuple，例如：左表连接列名为 sym，右表连接列名为 sym1，则 *matchingColumn* =
   [[`sym],[`sym1]]。
2. 有多个连接列：当左表和右表的连接列名相同时，*matchingColumn* 是一个字符串向量，否则是一个长度为 2 的
   tuple，例如：左表连接列名为 timestamp, sym，右表连接列名为 timestamp, sym1，则
   *matchingColumn* = [[`timestamp, `sym], [`timestamp,`sym1]]。

**timeColumn** 可选参数，当 *useSystemTime* =
false时，指定要连接的两个表中时间列的名称。*leftTable* 和 *rightTable*
时间列名称可以不同，但数据类型需保持一致。当 *leftTable* 和 *rightTable*
时间列名称不同时，*timeColumn* 为一个长度为2的字符串向量。

**useSystemTime**
可选参数，表示 *outputTable* 中第一列（时间列）为系统当前时间（*useSystemTime* =
true）或左表的时间列（*useSystemTime* = false）。

**garbageSize** 可选参数，是正整数，默认值是5,000（单位为行）。随着订阅的流数据不断积累进入 window
join 引擎，存放在内存中的数据会越来越多，这时需要清理不再需要的历史数据。当左/右两表各个分组内的数据行数超过 *garbageSize*
值时，系统会清理本次计算不需要的历史数据。

**maxDelayedTime** 可选参数，是正整数，用于触发引擎中长时间未输出的分组数据进行计算。
具体来说，若`(某个分组中未发生计算的窗口右边界) + (maxDelayedTime) <
(右表最新收到的任意一个分组数据的时间戳)`，则这条数据会触发该窗口计算输出。

指定该参数时，必须同时指定 timeColumn，且两者的单位需一致。默认值为3秒，根据 *`timeColumn`*
的精度换算。例如，若 *timeColumn* 的精度是毫秒，则默认值为3000毫秒。

**nullFill**
和输出表列字段等长且类型一一对应的元组，用于填充以下列中的空值：输出表中包含的左表列、右表列、右表列被聚合计算后的计算结果列。

若同时有一批数据注入引擎，则引擎内部数据是分批进行计算的，每个批次的数据称为一个
batch，每个 batch 包含记录数由系统决定。

**outputElapsedMicroseconds** 布尔值，表示是否输出每个 batch
中数据从注入引擎到计算输出的总耗时，以及每个 batch 包含的总记录数，默认为 false。指定参数 *outputElapsedMicroseconds*
= true 后，在定义 *outputTables* 时需要在最后增加两列，详见 *outputTable* 参数说明。

**sortByTime** 布尔值，表示是否按全局时间顺序输出数据。默认值为
false，表示不按全局时间输出数据，仅在组内按时间顺序输出数据。注意：当设置 sortByTime=true 时，必须保证输入的左表和右表的数据全局有序，且不可设置
*maxDelayedTime*。

**closed** 字符串，用于确定窗口边界的开闭情况，仅当 *window*为 0:0 时有效 。可选值为 ‘left’ 或 ‘right’，默认值为 ‘left’。

* closed = ‘left’： 窗口左闭右开。
* closed = ‘right’： 窗口左开右闭。此时必须设置 useSystemTime=false 。

若要开启快照机制 (snapshot)，必须指定 *snapshotDir* 与
*snapshotIntervalInMsgCount*。

**snapshotDir** 可选参数，字符串，表示保存引擎快照的文件目录。

* 指定的目录必须存在，否则系统会提示异常。
* 创建流数据引擎时，如果指定了 *snapshotDir*，会检查该目录下是否存在快照。如果存在，会加载该快照，恢复引擎的状态。
* 多个引擎可以指定同一个目录存储快照，用引擎的名称来区分快照文件。
* 一个引擎的快照可能会使用三个文件名：
* 临时存储快照信息：文件名为 <engineName>.tmp；
* 快照生成并刷到磁盘：文件保存为 <engineName>.snapshot；
* 存在同名快照：旧快照自动重命名为 <engineName>.old。

**snapshotIntervalInMsgCount**
可选参数，为整数类型，表示每隔多少条数据保存一次流数据引擎快照。

**cachedTableCapacity** 可选参数，为正整数，表示引擎为每个不同的分组分别创建的左缓存表和右缓存表的初始容量（以数据条数计）。默认值为
1024。

**keyPurgeFreqInSec** 可选参数，为正整数，单位为秒，表示间隔多久检查一次可以清理的分组。可以清理的分组判断规则如下：

* 左缓存表无未计算的数据，且 `该分组的右缓存表最后一条数据的时间戳 < 右表最新收到的任意一个分组数据的时间戳-
  maxDelayedTime - window长度` 或
  `右缓存表为空`，则该分组可以清理。
* 待清理的分组数大于等于总分组数的 10% 时，触发清理。

## 例子

```
share streamTable(1:0, `time`sym`price, [TIMESTAMP, SYMBOL, DOUBLE]) as leftTable
share streamTable(1:0, `time`sym`val, [TIMESTAMP, SYMBOL, DOUBLE]) as rightTable
share table(100:0, `time`sym`factor1`factor2`factor3, [TIMESTAMP, SYMBOL, DOUBLE, DOUBLE, DOUBLE]) as output

nullFill= [2012.01.01T00:00:00.000, `NONE, 0.0, 0.0, 0.0]
wjEngine=createWindowJoinEngine(name="test1", leftTable=leftTable, rightTable=rightTable, outputTable=output,  window=-2:2, metrics=<[price,val,sum(val)]>, matchingColumn=`sym, timeColumn=`time, useSystemTime=false,nullFill=nullFill)

subscribeTable(tableName="leftTable", actionName="joinLeft", offset=0, handler=appendForJoin{wjEngine, true}, msgAsTable=true)
subscribeTable(tableName="rightTable", actionName="joinRight", offset=0, handler=appendForJoin{wjEngine, false}, msgAsTable=true)

n=10
tp1=table(take(2012.01.01T00:00:00.000+0..10, 2*n) as time, take(`A, n) join take(`B, n) as sym, take(NULL join rand(10.0, n-1),2*n) as price)
tp1.sortBy!(`time)
leftTable.append!(tp1)

tp2=table(take(2012.01.01T00:00:00.000+0..10, 2*n) as time, take(`A, n) join take(`B, n) as sym, take(double(1..n),2*n) as val)
tp2.sortBy!(`time)
rightTable.append!(tp2)

select * from output where time between 2012.01.01T00:00:00.000:2012.01.01T00:00:00.001
```

| time | sym | factor1 | factor2 | factor3 |
| --- | --- | --- | --- | --- |
| 2012.01.01T00:00:00.000 | A | 0 | 1 | 6 |
| 2012.01.01T00:00:00.000 | A | 0 | 2 | 6 |
| 2012.01.01T00:00:00.000 | A | 0 | 3 | 6 |
| 2012.01.01T00:00:00.001 | A | 5.2705 | 1 | 10 |
| 2012.01.01T00:00:00.001 | A | 5.2705 | 2 | 10 |
| 2012.01.01T00:00:00.001 | A | 5.2705 | 3 | 10 |
| 2012.01.01T00:00:00.001 | A | 5.2705 | 4 | 10 |
| 2012.01.01T00:00:00.000 | B | 5.2705 | 2 | 9 |
| 2012.01.01T00:00:00.000 | B | 5.2705 | 3 | 9 |
| 2012.01.01T00:00:00.000 | B | 5.2705 | 4 | 9 |
| 2012.01.01T00:00:00.001 | B | 1.0179 | 2 | 14 |
| 2012.01.01T00:00:00.001 | B | 1.0179 | 3 | 14 |
| 2012.01.01T00:00:00.001 | B | 1.0179 | 4 | 14 |
| 2012.01.01T00:00:00.001 | B | 1.0179 | 5 | 14 |

下例展示特殊窗口的计算：

```
share streamTable(1:0, `time`sym`price, [TIMESTAMP, SYMBOL, DOUBLE]) as leftTable
share streamTable(1:0, `time`sym`val, [TIMESTAMP, SYMBOL, DOUBLE]) as rightTable

v = [1, 5, 10, 15]
tp1=table(2012.01.01T00:00:00.000+v as time, take(`A   , 4) as sym, rand(10.0,4) as price)

v = [1, 2, 3, 4, 5, 6, 9, 15]
tp2=table(2012.01.01T00:00:00.000+v as time, take(`A   , 8) as sym, rand(10.0,8) as val)

share table(100:0, `time`sym`price`val`sum_val, [TIMESTAMP, SYMBOL, DOUBLE, DOUBLE[], DOUBLE]) as output
wjEngine=createWindowJoinEngine(name="test1", leftTable=leftTable, rightTable=rightTable, outputTable=output,  window=0:0, metrics=<[price, val, sum(val)]>, matchingColumn=`sym, timeColumn=`time, useSystemTime=false)

subscribeTable(tableName="leftTable", actionName="joinLeft", offset=0, handler=appendForJoin{wjEngine, true}, msgAsTable=true)
subscribeTable(tableName="rightTable", actionName="joinRight", offset=0, handler=appendForJoin{wjEngine, false}, msgAsTable=true)

leftTable.append!(tp1)
rightTable.append!(tp2)
```

| time | sym | price | val | sum\_val |
| --- | --- | --- | --- | --- |
| 2012.01.01T00:00:00.001 | A | 8.8252 | [] |  |
| 2012.01.01T00:00:00.005 | A | 7.1195 | [7.495792,9.417891,1.419681,...] | 21.3741 |
| 2012.01.01T00:00:00.010 | A | 5.2217 | [4.840462,8.086567,3.495306] | 16.4223 |
| 2012.01.01T00:00:00.015 | A | 9.2517 | [] |  |

当 window=0:0 时，默认情况下，该窗口左闭右开。下例中指定参数 *closed* =
"right"，将窗口设置为左开右闭。

```
unsubscribeTable(tableName="leftTable", actionName="joinLeft")
unsubscribeTable(tableName="rightTable", actionName="joinRight")
undef(`leftTable,SHARED)
undef(`rightTable,SHARED)
dropAggregator(name="test1")

share streamTable(1:0, `time`sym`price, [TIMESTAMP, SYMBOL, DOUBLE]) as leftTable
share streamTable(1:0, `time`sym`val, [TIMESTAMP, SYMBOL, DOUBLE]) as rightTable

v1 = [1, 5, 10, 15]
tp1=table(2012.01.01T00:00:00.000+v1 as time, take(`A, 4) as sym, rand(10.0,4) as price)

v2 = [1, 2, 3, 4, 5, 6, 9, 15]
tp2=table(2012.01.01T00:00:00.000+v2 as time, take(`A, 8) as sym, rand(10.0,8) as val)

share table(100:0, `time`sym`price`val`sum_val, [TIMESTAMP, SYMBOL, DOUBLE, DOUBLE[], DOUBLE]) as output
wjEngine=createWindowJoinEngine(name="test1", leftTable=leftTable, rightTable=rightTable, outputTable=output,  window=0:0, metrics=<[price, val, sum(val)]>, matchingColumn="sym", timeColumn="time", useSystemTime=false, closed="right")

subscribeTable(tableName="leftTable", actionName="joinLeft", offset=0, handler=appendForJoin{wjEngine, true}, msgAsTable=true)
subscribeTable(tableName="rightTable", actionName="joinRight", offset=0, handler=appendForJoin{wjEngine, false}, msgAsTable=true)

leftTable.append!(tp1)
rightTable.append!(tp2)
sleep(100)
select * from output
```

返回：

```
time	                  sym	price	val	                      sum_val
2012.01.01T00:00:00.001	A	9.7366	[7.8310]	                  7.831
2012.01.01T00:00:00.005	A	2.6537	[1.8564,4.6238,8.2536,3.1028]     17.8368
2012.01.01T00:00:00.010	A	3.9586	[0.8413,8.0684]	           8.9098
```

下例展示指定 *sortByTime* = true 时，引擎将按时间顺序输出数据。

```
//清理引擎及变量
unsubscribeTable(tableName="leftTable", actionName="joinLeft")
unsubscribeTable(tableName="rightTable", actionName="joinRight")
undef(`leftTable,SHARED)
undef(`rightTable,SHARED)
dropAggregator(name="test1")

//定义引擎
share streamTable(1:0, `time`sym`price, [TIMESTAMP, SYMBOL, DOUBLE]) as leftTable
share streamTable(1:0, `time`sym`val, [TIMESTAMP, SYMBOL, DOUBLE]) as rightTable
share table(100:0, `time`sym`factor1`factor2`factor3, [TIMESTAMP, SYMBOL, DOUBLE, DOUBLE, DOUBLE]) as output
nullFill= [2012.01.01T00:00:00.000, `NONE, 0.0, 0.0, 0.0]
wjEngine=createWindowJoinEngine(name="test1", leftTable=leftTable, rightTable=rightTable, outputTable=output,  window=-2:2, metrics=<[price,val,sum(val)]>, matchingColumn=`sym, timeColumn=`time, useSystemTime=false,nullFill=nullFill, sortByTime=true)

//定义数据
subscribeTable(tableName="leftTable", actionName="joinLeft", offset=0, handler=appendForJoin{wjEngine, true}, msgAsTable=true)
subscribeTable(tableName="rightTable", actionName="joinRight", offset=0, handler=appendForJoin{wjEngine, false}, msgAsTable=true)

n=10
tp1=table(take(2012.01.01T00:00:00.000+0..10, 2*n) as time, take(`A, n) join take(`B, n) as sym, take(NULL join rand(10.0, n-1),2*n) as price)
tp1.sortBy!(`time)
leftTable.append!(tp1)

tp2=table(take(2012.01.01T00:00:00.000+0..10, 2*n) as time, take(`A, n) join take(`B, n) as sym, take(double(1..n),2*n) as val)
tp2.sortBy!(`time)
rightTable.append!(tp2)

sleep(100)
select * from output where time between 2012.01.01T00:00:00.000:2012.01.01T00:00:00.001
```

| time | sym | factor1 | factor2 | factor3 |
| --- | --- | --- | --- | --- |
| 2012.01.01T00:00:00.000 | A | 0 | 1 | 6 |
| 2012.01.01T00:00:00.000 | A | 0 | 2 | 6 |
| 2012.01.01T00:00:00.000 | A | 0 | 3 | 6 |
| 2012.01.01T00:00:00.000 | B | 3.9389 | 2 | 9 |
| 2012.01.01T00:00:00.000 | B | 3.9389 | 3 | 9 |
| 2012.01.01T00:00:00.000 | B | 3.9389 | 4 | 9 |
| 2012.01.01T00:00:00.001 | A | 3.9389 | 1 | 10 |
| 2012.01.01T00:00:00.001 | A | 3.9389 | 2 | 10 |
| 2012.01.01T00:00:00.001 | A | 3.9389 | 3 | 10 |
| 2012.01.01T00:00:00.001 | A | 3.9389 | 4 | 10 |
| 2012.01.01T00:00:00.001 | B | 4.9875 | 2 | 14 |
| 2012.01.01T00:00:00.001 | B | 4.9875 | 3 | 14 |
| 2012.01.01T00:00:00.001 | B | 4.9875 | 4 | 14 |
| 2012.01.01T00:00:00.001 | B | 4.9875 | 5 | 14 |

