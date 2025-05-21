# createReactiveStateEngine

## 语法

```
createReactiveStateEngine(name, metrics, dummyTable, outputTable, [keyColumn], [filter],
        [snapshotDir], [snapshotIntervalInMsgCount], [keepOrder], [keyPurgeFilter],
        [keyPurgeFreqInSecond=0], [raftGroup], [outputElapsedMicroseconds=false],
        [keyCapacity=1024], [parallelism=1], [outputHandler=NULL], [msgAsTable=false])
```

## 详情

创建响应式状态引擎。返回一个表对象，向该表写入数据意味着这些数据进入响应式状态引擎进行计算。

下列状态函数在 DolphinDB
的响应式状态引擎中的实现均得到了优化。需要注意的是，状态引擎不允许使用未经优化的内置状态函数，且需避免使用聚合函数。

* 累计窗口函数：[cumavg](cumavg.md), [cumsum](cumsum.md), [cumprod](cumprod.md), [cumcount](cumcount.md), [cummin](cummin.md), [cummax](cummax.md), [cumvar](cumvar.md), [cumvarp](cumvarp.md), [cumstd](cumstd.md), [cumstdp](cumstdp.md), [cumcorr](cumcorr.md), [cumcovar](cumcovar.md), [cumbeta](cumbeta.md), [cumwsum](cumwsum.md), [cumwavg](cumwavg.md), [cumfirstNot](cumfirstNot.md),
  [cumlastNot](cumlastNot.md), [cummed](cummed.md), [cumpercentile](cumpercentile.md), [cumnunique](cumnunique.md),
  [cumPositiveStreak](cumPositiveStreak.md), [cummdd](cummdd.md)
* 滑动窗口函数：[ema](../e/ema.md), [mavg](../m/mavg.md), [msum](../m/msum.md), [mcount](../m/mcount.md), [mprod](../m/mprod.md), [mvar](../m/mvar.md), [mvarp](../m/mvarp.md), [mstd](../m/mstd.md), [mstdp](../m/mstdp.md), [mskew](../m/mskew.md), [mkurtosis](../m/mkurtosis.md), [mmin](../m/mmin.md), [mmax](../m/mmax.md), [mimin](../m/mimin.md), [mimax](../m/mimax.md), [mmed](../m/mmed.md), [mpercentile](../m/mpercentile.md), [mrank](../m/mrank.md), [mcorr](../m/mcorr.md), [mcovar](../m/mcovar.md), [mbeta](../m/mbeta.md), [mwsum](../m/mwsum.md), [mwavg](../m/mwavg.md), [mmad](../m/mmad.md), [mfirst](../m/mfirst.md), [mlast](../m/mlast.md), [mslr](../m/mslr.md), [tmove](../t/tmove.md), [tmfirst](../t/tmfirst.md), [tmlast](../t/tmlast.md), [tmsum](../t/tmsum.md), [tmsum2](../t/tmsum2.md), [tmavg](../t/tmavg.md), [tmcount](../t/tmcount.md), [tmvar](../t/tmvar.md), [tmvarp](../t/tmvarp.md), [tmstd](../t/tmstd.md), [tmstdp](../t/tmstdp.md), [tmprod](../t/tmprod.md), [tmskew](../t/tmskew.md), [tmkurtosis](../t/tmkurtosis.md), [tmmin](../t/tmmin.md), [tmmax](../t/tmmax.md), [tmmed](../t/tmmed.md), [tmpercentile](../t/tmpercentile.md),
  [tmrank](../t/tmrank.md), [tmcovar](../t/tmcovar.md), [tmbeta](../t/tmbeta.md), [tmcorr](../t/tmcorr.md), [tmwavg](../t/tmwavg.md), [tmwsum](../t/tmwsum.md), [tmoving](../ho_funcs/tmoving.md), [moving](../ho_funcs/moving.md), [sma](../s/sma.md), [wma](../w/wma.md), [dema](../d/dema.md), [tema](../t/tema.md),
  [trima](../t/trima.md), [linearTimeTrend](../l/linearTimeTrend.md), [talib](../ho_funcs/talib.md), [t3](../t/t3.md), [ma](../m/ma.md), [gema](../g/gema.md), [wilder](../w/wilder.md), [mmaxPositiveStreak](../m/mmaxPositiveStreak.md), [movingWindowData](../m/movingWindowData.md), [tmovingWindowData](../t/tmovingWindowData.md)
* 行计算函数： [rowMin](../r/rowMin.md), [rowMax](../r/rowMax.md), [rowAnd](../r/rowAnd.md), [rowOr](../r/rowOr.md), [rowXor](../r/rowXor.md), [rowProd](../r/rowProd.md), [rowSum](../r/rowSum.md), [rowSum2](../r/rowSum2.md), [rowSize](../r/rowSize.md), [rowCount](../r/rowCount.md), [rowAvg](../r/rowAvg.md), [rowKurtosis](../r/rowKurtosis.md), [rowSkew](../r/rowSkew.md), [rowVar](../r/rowVar.md), [rowVarp](../r/rowVarp.md), [rowStd](../r/rowStd.md), [rowStdp](../r/rowStdp.md)
* 序列相关函数：[deltas](../d/deltas.md), [ratios](../r/ratios.md), [ffill](../f/ffill.md), [move](../m/move.md), [prev](../p/prev.md), [iterate](../i/iterate.md), [ewmMean](../e/ewmMean.md), [ewmVar](../e/ewmVar.md), [ewmStd](../e/ewmStd.md), [ewmCov](../e/ewmCov.md), [ewmCorr](../e/ewmCorr.md), [prevState](../p/prevState.md), [percentChange](../p/percentChange.md)
* topN相关函数：[msumTopN](../m/msumTopN.md), [mavgTopN](../m/mavgTopN.md), [mstdpTopN](../m/mstdpTopN.md), [mstdTopN](../m/mstdTopN.md), [mvarpTopN](../m/mvarpTopN.md), [mvarTopN](../m/mvarTopN.md), [mcorrTopN](../m/mcorrTopN.md), [mbetaTopN](../m/mbetaTopN.md), [mcovarTopN](../m/mcovarTopN.md), [mwsumTopN](../m/mwsumTopN.md), [cumsumTopN](cumsumTopN.md), [cumwsumTopN](cumwsumTopN.md), [cumvarTopN](cumvarTopN.md), [cumvarpTopN](cumvarpTopN.md), [cumstdTopN](cumstdTopN.md), [cumstdpTopN](cumstdpTopN.md), [cumcorrTopN](cumcorrTopN.md), [cumbetaTopN](cumbetaTopN.md), [cumavgTopN](../m/mstdpTopN.md), [msumTopN](../m/msumTopN.md), [mavgTopN](../m/mavgTopN.md), [mstdpTopN](../m/mstdpTopN.md), [mstdTopN](../m/mstdTopN.md), [mvarpTopN](../m/mvarpTopN.md), [mvarTopN](../m/mvarTopN.md), [mcorrTopN](../m/mcorrTopN.md), [mbetaTopN](../m/mbetaTopN.md), [mcovarTopN](../m/mcovarTopN.md), [mwsumTopN](../m/mwsumTopN.md), [cumsumTopN](cumsumTopN.md), [cumwsumTopN](cumwsumTopN.md), [cumvarTopN](cumvarTopN.md), [cumvarpTopN](cumvarpTopN.md), [cumstdTopN](cumstdTopN.md), [cumstdpTopN](cumstdpTopN.md), [cumcorrTopN](cumcorrTopN.md), [cumbetaTopN](cumbetaTopN.md), [cumavgTopN](cumavgTopN.md), [cumskewTopN](cumskewTopN.md), [cumkurtosisTopN](cumkurtosisTopN.md), [mskewTopN](../m/mskewTopN.md),
  [mkurtosisTopN](../m/mkurtosisTopN.md),[tmsumTopN](../t/tmsumTopN.md), [tmavgTopN](../t/tmavgTopN.md), [tmstdTopN](../t/tmstdTopN.md), [tmstdpTopN](../t/tmstdpTopN.md), [tmvarTopN](../t/tmvarTopN.md), [tmvarpTopN](../t/tmvarpTopN.md), [tmskewTopN](../t/tmskewTopN.md), [tmkurtosisTopN](../t/tmkurtosisTopN.md), [tmbetaTopN](../t/tmbetaTopN.md), [tmcorrTopN](../t/tmcorrTopN.md), [tmcovarTopN](../t/tmcovarTopN.md), [tmwsumTopN](../t/tmwsumTopN.md)
* 高阶函数：[segmentby](../ho_funcs/segmentby.md) (参数 *func* 暂支持 cumsum, cummax, cummin, cumcount,
  cumavg, cumstd, cumvar, cumstdp, cumvarp), [moving](../ho_funcs/moving.md), [byColumn](../ho_funcs/byColumn.md), [accumulate](../ho_funcs/accumulate.md), [window](../ho_funcs/window.md)
* 其他函数：[talibNull](../t/talibNull.md), [dynamicGroupCumsum](../d/dynamicGroupCumsum.md), [dynamicGroupCumcount](../d/dynamicGroupCumcount.md), [topRange](../t/topRange.md), [lowRange](../l/lowRange.md), [trueRange](../t/trueRange.md), [sumbars](../s/sumbars.md)
* 特殊函数（仅支持在引擎内使用）：[stateIterate](../s/stateIterate.md), [conditionalIterate](conditionalIterate.md), [genericStateIterate](../g/genericStateIterate.md), [genericTStateIterate](../g/genericTStateIterate.md)

注： [talib](../ho_funcs/talib.md)
作为状态函数时，第一个参数 *func* 只能是响应式状态引擎支持的状态函数。

有关更多流数据引擎的应用场景说明，参考：[流计算引擎](../themes/streamingEngine.md)。

## 计算规则

每注入一条数据都会计算并产生一条结果。用户可以通过设置参数 *filter* 过滤计算结果后输出。 若指定了
*keyColumn* 进行分组，则计算将在组内进行。

注： 状态引擎的输出结果可能和输入顺序不一致，建议配置参数 *keepOrder* =
true，保持输出结果的有序性。

## 引擎的其它功能

* 支持数据/状态清理：状态引擎内部的状态数据是按分组保存的，为避免分组过多，导致引擎内部内存开销过大，可以将历史分组数据进行清理。用户可以通过配置参数
  *keyPurgeFilter* 设置清理条件，配置 *keyPurgeFreqInSecond*
  设置清理时间间隔。
* 快照机制：启用快照机制之后，系统若出现异常，可及时将流数据引擎恢复到最新的快照状态。（详情请参考
  *snapshotDir* 和 *snapshotIntervalInMsgCount* 的参数说明）
* 流数据引擎高可用：若要启用引擎高可用，需在订阅端 raft 组的 leader 节点创建引擎并通过
  *raftGroup* 参数开启高可用。开启高可用后，当 leader 节点宕机时，会自动切换新 leader
  节点重新订阅流数据表。

## 参数

**name**
字符串标量，表示响应式状态引擎的名称，作为其在一个数据节点/计算节点上的唯一标识。可包含字母，数字和下划线，但必须以字母开头。

**metrics**
以元代码的形式表示计算公式，可以是一个或多个表达式、系统内置或用户自定义函数、一个常量标量/向量。当指定为常量向量时，对应的输出列应该设置为数组向量类型。有关元代码的详情可参考
[Metaprogramming](../../progr/objs/meta_progr.md)。若需使用用户自定义函数，请注意以下事项：

1. 需在定义前添加声明 "@state"。状态函数只能包含赋值语句和 return 语句。

   自 2.00.9 版本起，支持使用 if-else
   条件语句，且条件只能是标量。

   自2.00.11 版本起，支持使用 for 循环（包含 break, continue
   语句），请注意不支持嵌套 for 循环，且循环次数须小于 100 次。
2. 状态引擎中可以使用无状态函数或者状态函数。但不允许在无状态函数中嵌套使用状态函数。
3. 若赋值语句的右值是一个多返回值的函数（内置函数或自定义函数），则需要将多个返回值同时赋予多个变量。例如：两个返回值的函数 linearTimeTrend
   应用于自定义状态函数中，正确写法为：

   ```
   @state
   def forcast2(S, N){
         linearregIntercept, linearregSlope = linearTimeTrend(S, N)
         return (N - 1) * linearregSlope + linearregIntercept
   }
   ```

**dummyTable** 一个表对象，和订阅的流数据表的 schema 一致，可以含有数据，亦可为空表。

**outputTable** 计算结果的输出表，可以是内存表或分布式表。使用
`createReactiveStateEngine`
函数之前，需要将输出表预先设立为一个空表，并指定各列列名以及数据类型。响应式状态引擎会将计算结果注入该表。输出表的各列的顺序如下：

1. 分组列。若指定 *keyColumn*，则根据 *keyColumn* 的设置，输出表的前几列必须和
   *keyColumn* 设置的列及其顺序保持一致。
2. 耗时列和记录数。若指定 *outputElapsedMicroseconds* = true，则需要指定一个 LONG 类型和一个 INT
   类型的列，分别用于存储引擎内部每个 batch 的数据耗时（单位：微秒）和记录数。
3. 计算结果列。可为多列。

**keyColumn** 可选参数，字符串标量或向量表示分组列名。若指定该参数，计算将在各分组进行。

**filter** 可选参数，以元代码的形式表示过滤条件。过滤条件只能是一个表达式，并且只能包含 *dummyTable*中的列。设置多个条件时，用逻辑运算符（and, or）连接。引擎会先计算指标，然后根据 *filter*指定的过滤条件，输出满足条件的输入数据对应的计算结果。

若要开启快照机制（snapshot），必须指定 *snapshotDir* 与
*snapshotIntervalInMsgCount*。

**snapshotDir** 可选参数，字符串，表示保存引擎快照的文件目录。

* 指定的目录必须存在，否则系统会提示异常。
* 创建流数据引擎时，如果指定了 *snapshotDir*，会检查该目录下是否存在快照。如果存在，会加载该快照，恢复引擎的状态。
* 多个引擎可以指定同一个目录存储快照，用引擎的名称来区分快照文件。
* 一个引擎的快照可能会使用三个文件名：
  + 临时存储快照信息：文件名为 *<engineName>.tmp*；
  + 快照生成并刷到磁盘：文件保存为 *<engineName>.snapshot*；
  + 存在同名快照：旧快照自动重命名为 *<engineName>.old*。

**snapshotIntervalInMsgCount**
可选参数，为整数类型，表示每隔多少条数据保存一次流数据引擎快照。

**keepOrder** 可选参数，表示输出表数据是否按照输入时的顺序排序。设置 *keepOrder* =
true，表示输出表按照输入时的顺序排序。当 *keyColumn* 包含有时间列时，*keepOrder* 默认值为 true，否则默认值为
false。

**keyPurgeFilter** 可选参数，是一个由布尔表达式组成的元代码，表示清理条件。各表达式只能引用
*outputTable* 中的字段。必须指定 *keyColumn* 才能使用该参数。

**keyPurgeFreqInSecond** 正整数，表示触发数据清理需要满足的时间间隔（以秒为单位）。必须指定
*keyColumn* 才能使用该参数。

响应式状态引擎提供了 *keyPurgeFilter*, *keyPurgeFreqInSecond*
两个参数，用来清理不再需要的分组数据。每次数据注入时，系统会依次根据以下条件决定是否触发数据清理：

1. 检测本次数据注入与上一次数据注入的时间间隔是否大于等于 *keyPurgeFreqInSecond*
   （第一次数据注入时，检测注入时间和引擎创建时间的间隔）；
2. 若满足上述条件，系统将根据 *keyPurgeFilter* 指定的条件，过滤出待清理的数据；
3. 若待清理的数据所属的分组数大于等于所有分组数的 10%，则触发清理。

若需要查看清理前后的状态，可以通过调用 [getStreamEngineStat](../g/getStreamEngineStat.md) 函数查看 ReactiveStreamEngine 引擎状态的 numGroups
列，来对比响应式状态引擎清理前后分组数的变化。

**raftGroup** 是流数据高可用订阅端 raft 组的 ID (大于1的整数，由流数据高可用相关的配置项
*streamingRaftGroups*\*指定)。设置该参数表示开启计算引擎高可用。在 leader 节点创建流数据引擎后，会同步在
follower 节点创建该引擎。每次保存的 snapshot 也会同步到 follower。当 raft 组的 leader 节点宕机时，会自动切换新 leader
节点重新订阅流数据表。请注意，若要指定 *raftGroup*，必须同时指定 *snapshotDir*。
若同时有一批数据注入响应式状态引擎，则引擎内部数据是分批进行计算的，每个批次的数据称为一个 batch，每个 batch 包含记录数由系统决定。

**outputElapsedMicroseconds** 布尔值，可选参数，表示是否输出每个 batch 中数据从注入引擎到计算输出的总耗时，以及每个 batch
包含的总记录数，默认为 false。指定参数 *outputElapsedMicroseconds* 后，在定义 *outputTable*
时需要指定耗时列和记录数两列，详见 *outputTable* 参数说明。

**keyCapacity** 正整数，可选参数，表示建表时系统为该表预分配的 key 分组数量，用于调整状态表中 key
的函数。通过该参数的合理设置，能够降低在 key 分组较多时可能出现的延迟。

**parallelism** 不超过63的正整数，可选参数，表示并行计算的工作线程数，默认值为
1。在计算量较大时，合理地调整该参数能够有效利用计算资源，降低计算耗时。

注： *parallelism* 不能超过 min(许可核数, 逻辑核数)-1。

**outputHandler** 一元函数。设置此参数时，引擎计算结束后，不再将计算结果写到输出表，而是会调用此函数处理计算结果。默认值为
NULL，表示仍将结果写到输出表。

**msgAsTable** 布尔标量，表示在设置了参数 outputHandler 时，将引擎的计算结果以表的结构调用函数。默认值为
false，此时将计算结果的每一列作为元素组成元组。

## 例子

例1.

```
def sum_diff(x, y){
 return (x-y)/(x+y)
}
factor1 = <ema(1000 * sum_diff(ema(price, 20), ema(price, 40)),10) -  ema(1000 * sum_diff(ema(price, 20), ema(price, 40)), 20)>
share streamTable(1:0, `sym`time`price, [STRING,DATETIME,DOUBLE]) as tickStream
share table(1000:0, `sym`time`factor1, [STRING,DATETIME,DOUBLE]) as result
rse = createReactiveStateEngine(name="reactiveDemo", metrics =[<time>, factor1], dummyTable=tickStream, outputTable=result, keyColumn="sym", filter=<sym in ["000001.SH", "000002.SH"]>)
subscribeTable(tableName=`tickStream, actionName="factors", handler=tableInsert{rse})

data1 = table(take("000001.SH", 100) as sym, 2021.02.08T09:30:00 + 1..100 *3 as time, 10+cumsum(rand(0.1, 100)-0.05) as price)
data2 = table(take("000002.SH", 100) as sym, 2021.02.08T09:30:00 + 1..100 *3 as time, 20+cumsum(rand(0.2, 100)-0.1) as price)
data3 = table(take("000003.SH", 100) as sym, 2021.02.08T09:30:00 + 1..100 *3 as time, 30+cumsum(rand(0.3, 100)-0.15) as price)
data = data1.unionAll(data2).unionAll(data3).sortBy!(`time)

replay(inputTables=data, outputTables=tickStream, timeColumn=`time)
```

查看结果表 *result*，可见只有过滤条件中的 "000001.SH" 与 "000002.SH"
这两只股票的计算结果被输出。

若要重复调试以上代码，需要先执行以下代码。

```
unsubscribeTable(tableName=`tickStream, actionName="factors")
dropStreamEngine(`reactiveDemo)
undef(`tickStream, SHARED)
```

例2. *keyColumn* 设置以股票和日期进行分组计算，并设置输出时间在 "2012.01.01"
和"2012.01.03" 之间的计算结果。

```
share streamTable(1:0, `date`time`sym`market`price`qty, [DATE, TIME, SYMBOL, CHAR, DOUBLE, INT]) as trades
share table(100:0, `date`sym`factor1, [DATE, STRING, DOUBLE]) as outputTable
engine = createReactiveStateEngine(name="test", metrics=<mavg(price, 3)>, dummyTable=trades, outputTable=outputTable, keyColumn=["date","sym"], filter=<date between 2012.01.01 : 2012.01.03>, keepOrder=true)
subscribeTable(tableName=`trades, actionName="test", msgAsTable=true, handler=tableInsert{engine})

n=100
tmp = table(rand(2012.01.01..2012.01.10, n) as date, rand(09:00:00.000..15:59:59.999, n) as time, rand("A"+string(1..10), n) as sym, rand(['B', 'S'], n) as market, rand(100.0, n) as price, rand(1000..2000, n) as qty)
trades.append!(tmp)
select * from outputTable

//若要重复调试以上代码，需要先执行以下代码
unsubscribeTable(tableName=`trades, actionName="test")
dropStreamEngine(`test)
undef(`trades, SHARED)
```

例3. 2.00.9 版本后，支持在响应式状态引擎中调用 `moving` 高阶函数计算 array
vector。

```
defg myFactor(x){
   return avg(var(x));
}
share streamTable(1:0, `DateTime`SecurityID`Trade, [TIMESTAMP, SYMBOL, DOUBLE[]]) as tickStream
share table(1000:0, `SecurityID`DateTime`result, [SYMBOL, DATETIME, DOUBLE]) as result
rse = createReactiveStateEngine(name="reactiveDemo", metrics =<[DateTime, moving(myFactor, Trade, 3, 1)]>, dummyTable=tickStream, outputTable=result, keyColumn="SecurityID")
DateTime = 2022.09.15T09:00:00.000+1..12
SecurityID = take(`600021, 12)
Trade = [[10.06, 10.06], [10.04], [10.05, 10.06, 10.05, 10.08],[10.02,10.01], [10.06, 10.06, 10.05, 10.05], [10.04], [10.05,10.08, 10.09],[10.02,10.01],[10.06, 10.06, 10.05], [10.04, 10.03], [10.05, 10.06, 10.05, 10.08, 10.09],[10.02]]
t = table(1:0, `DateTime`SecurityID`Trade, [TIMESTAMP, SYMBOL, DOUBLE[]])
tableInsert(t, DateTime, SecurityID, Trade)
rse.append!(t)
select * from result
dropStreamEngine("reactiveDemo")
```

例4. 本例对例3进行改造，在指标中指定一个常数，表示因子名称。此时，输出表中会包含一个因子名称列。

```
defg myFactor(x){
   return avg(var(x));
}
share streamTable(1:0, `DateTime`SecurityID`Trade, [TIMESTAMP, SYMBOL, DOUBLE[]]) as tickStream
share table(1000:0, `SecurityID`DateTime`factorName`result, [SYMBOL, DATETIME, STRING, DOUBLE]) as result
rse = createReactiveStateEngine(name="reactiveDemo", metrics =<[DateTime,"factor1", moving(myFactor, Trade, 3, 1)]>, dummyTable=tickStream, outputTable=result, keyColumn="SecurityID")
DateTime = 2022.09.15T09:00:00.000+1..12
SecurityID = take(`600021, 12)
Trade = [[10.06, 10.06], [10.04], [10.05, 10.06, 10.05, 10.08],[10.02,10.01], [10.06, 10.06, 10.05, 10.05], [10.04], [10.05,10.08, 10.09],[10.02,10.01],[10.06, 10.06, 10.05], [10.04, 10.03], [10.05, 10.06, 10.05, 10.08, 10.09],[10.02]]
t = table(1:0, `DateTime`SecurityID`Trade, [TIMESTAMP, SYMBOL, DOUBLE[]])
tableInsert(t, DateTime, SecurityID, Trade)
rse.append!(t)
select * from result
```

| SecurityID | DateTime | factorName | result |
| --- | --- | --- | --- |
| 600021 | 2022.09.15 09:00:00 | factor1 | 0 |
| 600021 | 2022.09.15 09:00:00 | factor1 | 0.0001 |
| 600021 | 2022.09.15 09:00:00 | factor1 | 0.0002 |
| 600021 | 2022.09.15 09:00:00 | factor1 | 0.0006 |
| 600021 | 2022.09.15 09:00:00 | factor1 | 0.0004 |
| 600021 | 2022.09.15 09:00:00 | factor1 | 0.0004 |
| 600021 | 2022.09.15 09:00:00 | factor1 | 0.0003 |
| 600021 | 2022.09.15 09:00:00 | factor1 | 0.001 |
| 600021 | 2022.09.15 09:00:00 | factor1 | 0.0007 |
| 600021 | 2022.09.15 09:00:00 | factor1 | 0.0004 |

