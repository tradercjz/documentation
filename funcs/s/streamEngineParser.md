# streamEngineParser

## 语法

`streamEngineParser(name, metrics, dummyTable, outputTable, keyColumn,
[timeColumn], [useSystemTime=false], [snapshotDir],
[snapshotIntervalInMsgCount], [raftGroup], [filter], [keepOrder],
[keyPurgeFilter], [keyPurgeFreqInSecond], [triggeringPattern='perBatch'],
[triggeringInterval=1000], [lastBatchOnly=false], [contextByColumn],
[updateTime], [useWindowStartTime=false], [roundTime=true], [forceTriggerTime],
[sessionBegin], [sessionEnd], [mergeSessionEnd=false], [closed='left'],
[fill='none'], [garbageSize], [forceTriggerSessionEndTime],
[keyPurgeFreqInSec=-1])`

## 详情

在实际场景下，用户的因子可能嵌套横截面、历史状态、时序窗口、表连接等多种复杂逻辑，需要多个计算引擎的级联才能实现。`streamEngineParser`
为只涉及横截面、历史状态、时序窗口三种逻辑嵌套的复杂因子，提供了一个统一的计算入口。用户无需编写复杂的级联代码，只需将嵌套因子按规则改写后传入`streamEngineParser`
，系统将自动解析各层嵌套涉及的计算逻辑，形成流计算引擎流水线，自动分发给对应的引擎进行计算。

为满足各逻辑对应引擎的功能，该函数集合了（日级）时序引擎、响应式状态引擎和横截面引擎的参数。需要注意的是，由于部分为公共参数（如
*keyColumn*），若公共参数在不同计算逻辑下需要指定的值不同（如时序窗口按天分组，状态逻辑要求按股票代码分组，则需要配置不同的
*keyColumn*），不能使用该函数，只能通过级联实现。

返回一个表对象，为解析后流水线上第一个流计算引擎返回的表，向该表写入数据意味着这些数据进入流水线进行计算。删除时，需要根据
`streamEngineParser` 解析出的引擎对应的名称（详见
*name*）单独进行删除。暂不支持通过一个函数删除全部引擎。

根据上文，若要使用 `streamEngineParser`
，必须根据业务场景提供的指标，分析业务中涉及的流计算引擎，将指标改写成 `streamEngineParser` 能够识别分解的
*metrics*。若 *metrics* 中包含了用户自定义函数，引擎对函数体内部的嵌套逻辑进一步进行解析。

改写规则如下：

1. **引擎分解标识**
   * 若指标中的某一层嵌套逻辑要求计算截面数据，需将对应的计算函数改成以 “row开头”
     的函数作为标识，若不添加 row 则该操作默认在响应式状态引擎处理。如：需要在截面计算排名，则需要将该层嵌套改写为
     `rowRank`。

     目前支持的标识函数如下：

     ```
     "byRow", "rowAvg", "rowCount", "count", "rowDenseRank", "rowMax", "rowMin", "rowProd", "rowRank",
     "rowSize", "rowSkew", "rowStd", "rowStdp", "rowSum", "rowSum2", "rowVar", "rowVarp",
     "rowAnd", "rowOr", "rowXor", "rowKurtosis", "rowCorr", "rowCovar", "rowBeta", "rowWsum", "rowWavg"
     ```

     用户自定义函数或者 row 系列函数不支持的逻辑可以通过
     `byRow` 高阶函数实现。
   * 若指标中的某一层嵌套逻辑涉及到时序聚合窗口的计算，必须在指标中以 [rolling](../ho_funcs/rolling.html) 作为标识进行改写。如：窗口为 3，
     步长为 3，窗口内进行求和计算，计算列为 price，空值以前值填充，则可以写为 rolling(sum, price, 3, 3,
     'ffill')。形式如下：

     ```
     rolling(func, funcArgs, window, [step=1], [fill='none'])
     ```
   * 分解时，不包含上述标识的内置函数均在响应式状态引擎中处理。
2. **中间引擎输入表结构**

   在
   `streamEngineParser` 中，用户只能通过参数 *dummyTable*
   指定第一个引擎输入表的 schema ，中间引擎的 *dummyTable* 对用户而言是透明的， 为了能在 *metrics*
   和部分参数中指定中间表的列名，`streamEngineParser` 提供了一套中间引擎
   *dummyTable* 的命名规范：

   * 第一列为时间列。
   * 之后几列对应指定的 *keyColumn*。
   * 后续列为 *metrics* 对应的计算结果列，列名为：“col\_0\_, col\_1\_,
     col\_2\_...”。

   注：
   * 由于响应式状态引擎的输出表没有时间列，而时间序列聚合引擎以及横截面引擎的输出表需包含时间列，因此当流水线中涉及到响应式状态引擎相关操作时，其
     *metrics* 会自动增加时间列作为下一个引擎的 *dummyTable* 的一列。若此时
     *useSystemTime* = true，则其中间表的时间列的列名为 "datatime"。
   * 以下引擎的部分参数需要指定列名，如：
     + 横截面引擎：*contextByColumn*
     + 响应式状态引擎：*filter*, *keyPurgeFilter*若这些参数需要指定中间引擎的 *dummyTable* 的列名，则可以根据如上的命名规则给出的列名进行指定，如
     "*contextByColumn* = col\_0\_"。若指定的列为 *timeColumn* 和
     *keyColumn*，则也可以指定参数对应的列名。

## 必选参数

**name** 是一个字符串，表示指定流水线内引擎名称的前缀，可包含字母，数字和下划线，但必须以字母开头。比如指定 *name* =
"test"，则流水线内部对应的引擎名称为 "test0", "test1", "test2"... 其中，数字代表 *metrics*
分解出的流数据引擎的级联顺序。

**metrics** 以元代码的形式表示计算指标，支持输入元组。有关元代码的更多信息可参考 [Metaprogramming](../../progr/objs/meta_progr.html)。

* metrics 可以是系统内置或用户自定义的函数，如 <[sum(qty),
  avg(price)]>；可以对计算结果使用表达式，如
  <[avg(price1)-avg(price2)]>；也可以对多列进行运算，如
  <[std(price1-price2)]>。
* metrics 内支持具有多个返回值的函数，例如 <func(price) as
  `col1`col2>（可不指定列名）。

在 `streamEngineParser`
中，计算指标通常是一个嵌套的因子，每层嵌套逻辑都被解析后放入特定的引擎进行计算。更多说明见详情。

**dummyTable** 一个表对象，和订阅的流数据表的 schema 一致，可以含有数据，亦可为空表。

**outputTable** 计算结果的输出表，可以是内存表或者分布式表。调用 `streamEngineParser`
之前，需要将输出表预先设立为一个空表，并指定各列列名以及数据类型。各引擎会将计算结果插入该表。 若 *metrics*
分解的流水线上的最后一个操作对应：

* **时序聚合引擎**

  输出表的各列的顺序为：时间列，分组列，计算结果列。

  其中：

  + 第一列必须是时间类型。
    - 若 *useSystemTime* = true，为 TIMESTAMP 类型。
    - 若 *useSystemTime* = false，数据类型与 *timeColumn*
      列一致。
    - 若 *useWindowStartTime* = true，显示时间为数据窗口起始时间。
    - 若 *useWindowStartTime* = false，显示时间为数据窗口终止时间。
  + 如果 *keyColumn* 不为空，则其后几列和 *keyColumn* 设置的列及其顺序保持一致。
  + 最后为计算结果列，可为多列。

  最终的 schema
  为“时间列，分组列(可选)，计算结果列1，计算结果列2...”这样的格式。
* **响应式状态引擎**

  输出表的各列的顺序为：分组列，计算结果列。

  其中：
  + 根据 *keyColumn* 的设置，输出表的前几列必须和 *keyColumn*
    设置的列及其顺序保持一致。
  + 其后为计算结果列，可为多列。
* **横截面引擎**

  输出表的 schema 需要遵循以下规范:

  + 如果没有指定 *contextByColumn*， 输出表的列数为 *metrics* 数量+1，第一列为
    TIMESTAMP 类型，用于存放发生计算的时间戳（如果指定了 *timeColumn* 则是对应记录的时间戳），其他列为
    *metrics* 计算结果对应的列，其数据类型必须与 *metrics*
    返回结果的数据类型一致。
  + 如果指定 *contextByColumn*， 输出表的列数为 *metrics* 数量+2。第一列为
    TIMESTAMP 类型，用于存放发生计算的时间戳（如果指定了 *timeColumn* 则是对应记录的时间戳）；第二列为
    *contextByColumn* 指定的列；最后几列为 *metrics*
    计算结果对应的列，其数据类型必须与 *metrics* 返回结果的数据类型一致。

**keyColumn** 是一个字符串标量或向量。

* 时序聚合引擎/响应式状态引擎：表示分组列名。若设置，计算按分组进行，例如以每支股票为一组进行聚合计算。
* 横截面引擎：表示将某列值作为横截面引擎的 key，横截面引擎的每次计算，只使用每个 key
  对应的最新一条记录。

## 可选参数

**timeColumn** 指定订阅的流数据表中时间列的名称。当 *useSystemTime* = false 时，必须指定该参数。

* 时序聚合引擎/响应式状态引擎：是一个字符串标量或向量。请注意，若为字符串向量，必须是 date 和 time
  组成的向量，date 类型为 DATE，time 类型为 TIME, SECOND 或 NANOTIME。此时，输出表第一列的时间类型必须与
  [concatDateTime(date,
  time)](../c/concatDateTime.html) 的类型一致。
* 横截面引擎：是一个字符串，仅支持 TIMESTAMP 类型。

**useSystemTime** 表示是否使用系统时间作为时间戳。

* 横截面引擎：可选参数。表示 *outputTable* 中第一列（时间列）为系统当前时间(
  *useSystemTime* = true)或数据中时间列( *useSystemTime* =
  false)。
* 时间序列聚合引擎：可选参数，表示时间序列引擎计算的触发方式。若指定该参数为 true，不能指定
  *timeColumn*。

  a. 当 *useSystemTime* = true
  时，时间序列引擎会按照数据进入时间序列引擎的时刻（毫秒精度的本地系统时间，与数据中的时间列无关），每隔固定时间截取固定长度窗口的流数据进行计算。只要一个数据窗口中含有数据，数据窗口结束后就会自动进行计算。结果中的第一列为计算发生的时间戳，与数据中的时间无关。
  b. 当 *useSystemTime* = false（缺省值）时，时间序列引擎根据流数据中的 timeColumn
  列来截取数据窗口。一个数据窗口结束后的第一条新数据才会触发该数据窗口的计算。请注意，触发计算的数据并不会参与该次计算。

若要开启快照机制 （snapshot），必须指定 *snapshotDir* 与
*snapshotIntervalInMsgCount*。启用快照机制之后，系统若出现异常，可及时将流数据引擎恢复到最新的快照状态。

**snapshotDir** 可选参数，字符串，表示保存引擎快照的文件目录。

* 指定的目录必须存在，否则系统会提示异常。
* 创建流数据引擎时，如果指定了
  *snapshotDir*，会检查该目录下是否存在快照。如果存在，会加载该快照，恢复引擎的状态。
* 多个引擎可以指定同一个目录存储快照，用引擎的名称来区分快照文件。
* 一个引擎的快照可能会使用三个文件名：
* 临时存储快照信息：文件名为 <engineName>.tmp；
* 快照生成并刷到磁盘：文件保存为 <engineName>.snapshot；
* 存在同名快照：旧快照自动重命名为 <engineName>.old。

**snapshotIntervalInMsgCount** 可选参数，为整数类型，表示每隔多少条数据保存一次流数据引擎快照。

**raftGroup** 是流数据高可用订阅端 raft 组的 ID (大于1的整数，由流数据高可用相关的配置项
*streamingRaftGroups* 指定)。设置该参数表示开启计算引擎高可用。在 leader 节点创建流数据引擎后，会同步在
follower 节点创建该引擎。每次保存的 snapshot 也会同步到 follower。当 raft 组的 leader 节点宕机时，会自动切换新 leader
节点重新订阅流数据表。请注意，若要指定 *raftGroup*，必须同时指定 *snapshotDir*。

该流水线引擎只能在 raft 组的 leader 节点创建。

各引擎特有的参数如下：

* 响应式状态引擎 [createReactiveStateEngine](../c/createReactiveStateEngine.html): *filter*, *keepOrder*,
  *keyPurgeFilter*, *keyPurgeFreqInSecond*
* 横截面引擎参数 [createCrossSectionalEngine](../c/createCrossSectionalEngine.html): *triggeringPattern*,
  *triggeringInterval*, *lastBatchOnly*,
  *contextByColumn*
* 时间序列聚合引擎 [createTimeSeriesEngine](../c/createTimeSeriesEngine.html): *updateTime*,
  *useWindowStartTime*, *roundTime*, *forceTriggerTime*,
  closed, fill, garbageSize, keyPurgeFreqInSec
* 日级时间序列聚合引擎 [createDailyTimeSeriesEngine](../c/createDailyTimeSeriesEngine.html): *sessionBegin*,
  *sessionEnd*, *mergeSessionEnd*, closed, fill, garbageSize,
  forceTriggerSessionEndTime, keyPurgeFreqInSec

注： 如果 *triggeringPattern*='keyCount'，则 *keepOrder*
的默认值为 true，且不可设置为 false。

## 例子

下面的例子是 World Quant 101 个 Alpha
因子中的1号因子公式的流数据实现。`rank` 函数是一个横截面操作。`rank`
的参数部分用响应式状态引擎实现。`rank` 函数本身用横截面引擎实现。横截面引擎作为状态引擎的输出。

```
n = 100
sym = rand(`aaa`bbb`ccc, n)
time = 2021.01.01T13:30:10.008 + 1..n
maxIndex=rand(100.0, n)
data = table(sym as sym, time as time, maxIndex as maxIndex)
```

```
rank(Ts_ArgMax(SignedPower((returns<0?stddev(returns,20):close), 2), 5))-0.5

// 创建横截面引擎，计算每个股票的rank
dummy = table(1:0, `sym`time`maxIndex, [SYMBOL, TIMESTAMP, DOUBLE])
resultTable = streamTable(10000:0, `time`sym`factor1, [TIMESTAMP, SYMBOL, DOUBLE])
ccsRank = createCrossSectionalAggregator(name="alpha1CCS", metrics=<[sym, rank(maxIndex, percent=true) - 0.5]>,  dummyTable=dummy, outputTable=resultTable,  keyColumn=`sym, triggeringPattern='keyCount', triggeringInterval=3000, timeColumn=`time, useSystemTime=false)

@state
def wqAlpha1TS(close){
    ret = ratios(close) - 1
    v = iif(ret < 0, mstd(ret, 20), close)
    return mimax(signum(v)*v*v, 5)
}

// 创建响应式状态引擎，输出到前面的横截面引擎ccsRank
input = table(1:0, `sym`time`close, [SYMBOL, TIMESTAMP, DOUBLE])
rse = createReactiveStateEngine(name="alpha1", metrics=<[time, wqAlpha1TS(close)]>, dummyTable=input, outputTable=ccsRank, keyColumn="sym")
rse.append!(data)

dropStreamEngine("alpha1CCS")
dropStreamEngine("alpha1")
```

上述操作可以通过直接构建流水线引擎进行替代：

```
input = table(1:0, `sym`time`close, [SYMBOL, TIMESTAMP, DOUBLE])
resultTable = streamTable(10000:0, `time`sym`factor1, [TIMESTAMP, SYMBOL, DOUBLE])

// 构建计算因子
metrics=<[sym, rowRank(wqAlpha1TS(close), percent=true)- 0.5]>

streamEngine=streamEngineParser(name=`alpha1_parser, metrics=metrics, dummyTable=input, outputTable=resultTable, keyColumn=`sym, timeColumn=`time, triggeringPattern='keyCount', triggeringInterval=3000)
streamEngine.append!(data)

dropStreamEngine("alpha1_parser0")
dropStreamEngine("alpha1_parser1")
```

