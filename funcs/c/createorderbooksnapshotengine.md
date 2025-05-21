# createOrderBookSnapshotEngine

## 语法

`createOrderBookSnapshotEngine(name, exchange,
orderbookDepth, intervalInMilli, date, startTime, prevClose, dummyTable,
outputTable, inputColMap, [outputColMap], [outputCodeMap], [snapshotDir],
[snapshotIntervalInMsgCount], [raftGroup], [outputIntervalOffsetMap],
[checkRestrict], [maxPrice], [minPrice], [userDefinedMetrics], [priceNullFill],
[triggerType], [forceTriggerTime], [precision], [orderBySeq],
[skipCrossedMarket=true], [orderBookDetailDepth=0], [orderBookAsArray=false],
[useSystemTime=false],[independentForceTriggerTime],
[includeImmediateExecution=false], [securitySubType='ConvertibleBond'],
[priceScale=10000])`

注：

社区版 License 暂不支持该引擎，如需使用此功能，请联系技术支持。

## 详情

该函数基于一个包含了逐笔委托和逐笔交易数据表，实时合成指定频率（1秒，100ms，30ms
等）的全档位盘口信息、窗口内统计信息、全天累计统计信息等订单薄（或者叫快照）数据。也可通过历史逐笔数据来合成需要的订单薄数据。

目前支持合成深交所股票、深交所可转债、深交所基金、上交所股票、上交所可转债、上交所基金的订单薄数据。请注意，可转债的规则遵循自2022年8月之后发布的新规定。

### 窗口规则

由参数 *intervalInMilli*指定窗口的长度（以时间衡量），输出表中显示的时间为窗口的右边界。最后一个窗口区间为左开右开，且输出窗口显示为右边界的时间戳，其余窗口区间全部左开右闭。其中，最后一个窗口的右边界最大值由
*exchange* 决定：

* *exchange* = “XSHGBOND” 时，最后一个窗口的右边界最大值为 15:00:00.000。
* *exchange* 是其它值时，最后一个窗口的右边界最大值为 14:57:00.000。

### 触发规则

第一条输出记录由输入表中第一条时间戳大于 startTime + intervalInMilli 的记录触发，此时输出表的时间戳为 startTime +
intervalInMili。之后根据参数 *triggerType*的配置值，决定新收到任意一条逐笔数据，当其时间戳大于窗口右边界时，触发输出单个或所有证券代码的快照。

注：

* 一个引擎至多只能输入某一天一个通道的全部股票数据。
* 必须保证注入引擎的数据表内的数据按照交易所的逐笔序号排序。

## 参数

注： 传参时必须指定参数名。

**name** 字符串标量，表示 orderbook 快照引擎的名称，可包含字母，数字和下划线，但必须以字母开头。

**exchange** 字符串标量，表示证券的类型。可选参数：

* "XSHE" 或 "XSHESTOCK"：深交所股票
* "XSHEBOND"：深交所债券
* "XSHEFUND"：深交所基金
* "XSHG" 或 "XSHGSTOCK"：上交所股票
* "XSHGBOND"：上交所债券
* "XSHGFUND"：上交所基金

**orderbookDepth** 正整数，表示 orderbook 中最多能够显示的买卖报价的档位。

**intervalInMilli** 正整数，表示触发输出数据的时间间隔，即合成快照的时间频率，单位为毫秒。

**date** DATE 类型标量，表示交易日期。该参数和窗口右边界组合成输出表的 TIMESTAMP 列。

**startTime** TIME
类型标量，表示触发输出数据的起始时刻。引擎只会输出该参数指定时刻（规整后）之后的数据。

**prevClose** 字典，其 key 为字符串标量或向量，表示股票代码；其 value
为数值类型，表示对应于股票代码的上一个交易日的收盘价格。注意：若 value 为浮点型，则认为是真实价格，引擎处理过程中会乘以
*priceScale*，以匹配输入表中 priceColumn 字段的精度。若为整型，则视为已和 priceColumn
具备相同精度，不再进行缩放。

**dummyTable** 一个表对象，和订阅的流数据表的 schema 一致，可以含有数据，亦可为空表。

**outputTable** 一个表对象。若指定 *userDefinedMetrics*，*outputTable* 根据
`genOutputColumnsForOBSnapshotEngine` 函数指定的
*basic*、*depth* 以及用户自定义的指标来确定表结构。否则，*outputTable* 根据
*outputColMap*的设置来确定表结构。

**inputColMap** 字典，将输入表中列字段的名称映射为引擎计算所需要的列。其中：

* key 为字符串类型，表示引擎所需要的固定的输入字段。具体字段名和含义见下表。注意，这些 key 区分大小写，必须全部指定，但顺序可以不固定。
* value 为字符串类型，表示输入表中对应的列名称。

| key | value 对应的字段类型 | 含义 |
| --- | --- | --- |
| "codeColumn" | SYMBOL | 证券代码（如300010.SZ） |
| "timeColumn" | TIME | 交易时间 |
| "typeColumn" | INT | 交易类型：  * 如果是逐笔委托单，则：1 表示市价；2 表示限价；3 表示本方最优；10 表示撤单（仅上交所）；11   市场状态（仅上交所） * 如果是逐笔成交单，则：0 表示成交；1 表示撤单（仅深交所） |
| "priceColumn" | LONG | 价格，由 *priceScale* 决定，默认是真实价格\*10000 |
| "qtyColumn" | LONG | 数量（股数） |
| "buyOrderColumn" | LONG | * 逐笔成交：对应其原始成交中的买方委托序号。 * 逐笔委托：   + 上交所：填充原始委托中的原始订单号，即上交所在新增、删除订单时用以标识订单的唯一编号（OrderNo     字段）   + 深交所：填充 0。此字段为深交所为了补全上交所数据格式而增加的冗余列 |
| "sellOrderColumn" | LONG | * 逐笔成交：对应其原始成交中的卖方委托序号。 * 逐笔委托：   + 上交所：填充原始委托中的原始订单号，即上交所在新增、删除订单时用以标识订单的唯一编号（OrderNo     字段）   + 深交所：填充 0。此字段深交所为了补全上交所数据格式而增加的冗余列 |
| "sideColumn" | INT | 买卖方向：1 表示买单；2 表示卖单 说明：   * 委托单的 BSFlag，必填 * 撤单的 BSFlag 由原始委托单决定买卖方向，必填 * 成交单的 BSFlag，不影响结果，非必填 |
| "msgTypeColumn" | INT | 数据类型：  * 0 表示逐笔委托； * 1 表示逐笔成交； * -1 表示产品状态。 |
| "seqColumn" | LONG | 一个通道内从 1 开始递增的逐笔数据序号。深交所为 appseqlnum 字段，若深交所数据中包含 index 字段，也可以使用 index；上交所为 bizIndex 字段。 |
| "receiveTime" | NANOTIMESTAMP | 逐笔数据的接收时间 |

注： 引擎规范了枚举类型中各枚举值的具体含义。输入表对应的枚举值必须遵守这个规范。比如枚举类型字段
sideColumn 所对应的输入表中的字段必须使用 1 代表买方向，2 代表卖方向。

**outputColMap** 可选参数，字符串向量，用于指定需要输出的字段名称，不区分大小写。为方便指定
*outputColMap*，用户可通过 `genOutputColumnsForOBSnapshotEngine`
函数生成需要输出的字段名称，将返回值的第一个元素赋值给 *outputColMap* 即可。

**outputCodeMap**
可选参数，字符串向量，表示股票代码，例如："000803.SZ"。指定该参数后，将只输出指定股票对应的数据。

**outputIntervalOffsetMap**
可选参数，向量或字典，用于指定输出表中股票被触发计算的时间偏移量。

* 当为向量时，向量中的元素表示不同的时间偏移量，单位为毫秒。引擎将根据输入的股票数量自动将这些股票均匀分配到这些偏移量上。例如，outputIntervalOffsetMap
  = [400, 500]，表示引擎将自动将输入的股票均匀分成两部分，经过intervalInMilli + 400(ms)
  后触发其中一部分股票的数据输出；经过 intervalInMilli + 500(ms) 后触发另一部分股票的数据输出。
* 当为字典时，其 key 为字符串类型，表示股票代码；其 value
  为整型，表示时间偏移量，单位为毫秒。例如：outputIntervalOffsetMap
  =dict(["127053.sz","123082.SZ"],[400, 500])，表示经过 intervalInMilli + 400(ms)
  后触发 127053.sz 股票的数据输出；经过 intervalInMilli + 500(ms) 后触发 123082.SZ
  股票的数据输出。

**checkRestrict** 可选参数，布尔值，默认值为 true，表示开启价格笼子机制；若设置为
false，则关闭笼子机制，此时会取消对股票交易的限制，创业板合成出的快照可能不正确。

注： 深交所对创业板证券（证券代码以 3 开头）设定了价格笼子。在 *checkRestrict*=true
时，引擎只会将证券代码的首字符是否为 3 作为是否执行价格笼子的判断标准。因此，在向引擎输入创业板数据时，证券代码必须以 3 开头。

**maxPrice** 可选参数，字典。其 key 为字符串类型，表示证券代码；其 value 为 DOUBLE 或 INT
类型，表示涨停价格。注意：若 *maxPrice* 为浮点型，则认为是真实价格，引擎处理过程中会乘以 *priceScale*，以匹配输入表中
priceColumn 字段的精度。若为整型，则视为已和 priceColumn 具备相同精度，不再进行缩放。

**minPrice** 可选参数，字典。其 key 为字符串类型，表示证券代码；其 value 为 DOUBLE 或 INT
类型，表示跌停价格。注意：若 *minPrice* 为浮点型，则认为是真实价格，引擎处理过程中会乘以 *priceScale*，以匹配输入表中
priceColumn 字段的精度。若为整型，则视为已和 priceColumn 具备相同精度，不再进行缩放。

**userDefinedMetrics** 可选参数，一元函数。

* 函数的入参是一个表，表的每一行是一个标的，每一列是标的对应的快照。若指定 *outputColMap*，则表中数据为
  *outputColMap*设置的字段；否则表中数据为基础字段和报价/询价的价格和数量。
* 函数的返回值是一个元组，元组的每一个元素是一个常规向量，代表每个标的经对应指标计算后的结果。

**priceNullFill** 一个数字。该参数值用于填充输出表中多档买/卖价格中缺失档位的价格。例如涨停后卖单的价格都为
NULL，此时如有指定卖单价格为 0 的需求，可以设置 priceNullFill=0。

**triggerType** 可选参数，字符串标量，表示触发方式。可选值为：

* "mutual"（默认值）：新收到任意一条逐笔数据，当其时间戳大于窗口右边界时，就会触发所有股票未计算的快照合成输出。触发计算的数据并不会参与该次计算。
* "independent"：新收到任意一条逐笔数据，当其时间戳大于窗口右边界时，只触发该条数据对应股票未计算的快照合成输出。触发计算的数据并不会参与该次计算。
* "perRow"：每收到一行逐笔数据都会触发该条数据对应股票计算并输出，触发计算的数据并参与该次计算。

**forceTriggerTime**
可选参数，是非负整数，单位为毫秒。除了正常触发合成快照外，有时会出现一些数据因乱序不能触发合成快照，而是被缓存在引擎中。在这种情况下，可通过该参数设置强制触发引擎中长时间未处理的逐笔数据合成快照。触发规则为：

1. 最新收到的逐笔数据的时间戳（t ）减去最后一条已经处理的交易数据的时间戳（t0 ）大于或等于
   *forceTriggerTime*，则触发未处理的数据中序号最小的那条数据合成快照，并更新已经处理的交易数据的时间戳（t1）。
2. 重复上述操作，若判断 t-t1 >=
   *forceTriggerTime*，则触发未处理的数据中序号最小的那条数据合成快照，并更新已经处理的交易数据的时间戳（t2）；直到两个时间戳的差值小于
   *forceTriggerTime* 时，停止触发快照合成。

**precision** 可选参数，整数，表示小数位数，取值范围为[-1,4]。

* 当 *precision*=-1 时，引擎输出的价格相关字段为整型。注意：输出表中相应的字段可以是整型或非整型。
* 当 *pricision* 取 [0, 4]
  中的值时，表示小数位数。输出表中所有的价格将按照指定的位数进行四舍五入。否则，按照原始结果输出。

**orderBySeq** 可选参数，布尔值或元组。

* 指定该参数值为布尔值时，表示是否按照逐笔数据中的 seqColumn 列中值的大小顺序处理数据。当 *exchange*="XSHG" 或
  "XSHGFUND" 时，默认值为 true；在其他情况下，默认值为 false。
  + 当 *orderBySeq*=true
    时，会根据逐笔数据的序号有序处理数据，并计算输出。例如引擎先后收到序号为1，3的数据，因为缺少序号为2的数据，引擎先将1和3的数据缓存，待收到序号2的数据时，再进行计算输出。此时也可以指定
    *forceTriggerTime* 强制触发计算输出。
  + 当 *orderBySeq*=false 时，每接收到一条数据都会立即进行计算并输出，此时不可设置
    *forceTriggerTime*。
* 指定该参数值为元组时，以（BOOL, INTEGER, [STRING]）的形式表示，其中：
  + 第一个元素为布尔值，表示是否按照逐笔数据的序号有序输出结果的布尔值，作用同上。
  + 第二个元素为正整数，表示记录缓存输入数据量的时间间隔，单位为毫秒（ms）。
  + 第三个元素为指定输出日志级别的字符串标量，可选参数，其可用值为 DEBUG （默认值）和 INFO，分别对应 Debug 和 Info
    级别的日志输出。

**skipCrossedMarket**可选参数， 布尔值，表示是否输出买一卖一价交叉的计算结果。

* 当 *skipCrossedMarket*=true（默认值）时，若设置 *useSystemTime* =
  false，若出现买一卖一价交叉，即卖一价<=买一价，则不输出该条结果；若设置 *useSystemTime* =
  true，则出现买一卖一交叉时，暂时不输出该条快照，若接下来收到的数据不再有交叉，则立即触发该条快照输出。
* 当 *skipCrossedMarket*=false 时，若出现买一卖一价交叉，仍然输出该条结果。

**orderBookDetailDepth** 可选参数，整型标量，表示 orderbook
明细的深度。默认值为0，表示不输出。该参数必须和 *outputColMap* 中 orderBookDetailDepth 字段的值保持一致。

**orderBookAsArray** 可选参数，布尔值，表示是否以数组向量形式输出报价/询价的价格和数量。默认值为
false，价格和数量将以多列形式输出。

注意，若指定 *userDefinedMetrics*，价格和数量的输出形式由 *orderBookAsArray*
确定。否则，价格和数量的输出形式由 *outputColMap* 确定，该参数失效。

**useSystemTime** 可选参数，布尔值，表示是否使用系统时间来触发快照输出。

* 当 *useSystemTime* = true 时，交易时段内，引擎将基于当前的系统时间，按照
  *intervalInMilli*
  设置的时间间隔触发快照输出。此时，休盘时段（(11:30:00.000，13:00:00.000]）不输出数据，下午盘第一个输出窗口时间戳为
  13:00:00.000+*intervalInMilli*。注意，若设置 *useSystemTime* =
  true，则不能指定 *forceTriggerTime*；可以不指定 *triggerType*，或者指定为
  *triggerType*="mutual"
* 当 *useSystemTime* = false（缺省值）时，引擎根据事件时间来触发快照输出。

**independentForceTriggerTime**
可选参数，非负整数，单位为毫秒。该参数用于设置在长时间未触发快照输出的分组中，强制输出快照的时间间隔。仅当设置
*triggerType*="independent" 时，该参数才会生效。

举例说明：假设在当前已处理的数据中，最新一条数据的时间为 t。各个分组内已处理的应被触发输出的快照时间为 ti。如果满足
t-ti>*independentForceTriggerTime*，则会触发输出相应分组的快照。

**includeImmediateExecution** 可选参数，布尔值，默认值为
false，表示是否将即时成交的信息统计到委托明细（orderDetail）中。此设置仅在合成上交所订单簿时有效（*exchange* 指定为
"XSHG" 或 "XSHGSTOCK"）。

注： 注意：若该配置项设置为 true，则 **inputColMap** 必须保证输入数据中的 OrderNo
全局有序。同时，确保即时成交记录中的未被记录的 orderNo 大于等于当前最新记录的 OrderNo。

**securitySubType** 字符串标量（不区分大小写），用于指定生成订单簿的证券子类型，仅适用于*exchange* 为 "XSHEBOND"
或 "XSHGBOND" 的情况。可选值为：

* "ConvertibleBond"（默认）：对于 "XSHEBOND" 订单簿仅包含代码前缀为 "123"，"127"，"128" 的债券；对于
  “XSHGBOND” 订单簿仅包含代码前缀为 ”110“，”111“，”113“，”118“ 的债券。
* "All"：包含所有债券，无前缀限制。

**priceScale** 一个正整数，表示输入表中 priceColumn 列的缩放比例，默认值为 10000。引擎输出时会将计算结果除以
*priceScale*。

## 例子

运行代码前，先下载 <../data/orderbookDemoInput.zip> 文件。

```
// 登录
login("admin", "123456")

// 释放已有的引擎
try { dropStreamEngine("demo") } catch(ex) { print(ex) }

// 创建引擎参数 outputTable，即指定输出表
suffix = string(1..10)
colNames = `SecurityID`timestamp`lastAppSeqNum`tradingPhaseCode`modified`turnover`volume`tradeNum`totalTurnover`totalVolume`totalTradeNum`lastPx`highPx`lowPx`ask`bid`askVol`bidVol`preClosePx`invalid  join ("bids" + suffix) join ("bidVolumes" + suffix) join ("bidOrderNums" + suffix) join ("asks" + suffix)  join ("askVolumes" + suffix) join ("askOrderNums" + suffix)
colTypes = [SYMBOL,TIMESTAMP,LONG,INT,BOOL,DOUBLE,LONG,INT,DOUBLE,LONG,INT,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,LONG,LONG,DOUBLE,BOOL] join take(DOUBLE, 10) join take(LONG, 10) join take(INT, 10) join take(DOUBLE, 10) join take(LONG, 10) join take(INT, 10)
share table(10000000:0, colNames, colTypes) as outTable

// 创建引擎参数 dummyTable，即指定输入表的表结构
colNames = `SecurityID`Date`Time`SecurityIDSource`SecurityType`Index`SourceType`Type`Price`Qty`BSFlag`BuyNo`SellNo`ApplSeqNum`ChannelNo
colTypes = [SYMBOL, DATE, TIME, SYMBOL, SYMBOL, LONG, INT, INT, LONG, LONG, INT, LONG, LONG, LONG, INT]
dummyOrderStream = table(1:0, colNames, colTypes)

// 创建引擎参数 inputColMap，即指定输入表各字段的含义
inputColMap = dict(`codeColumn`timeColumn`typeColumn`priceColumn`qtyColumn`buyOrderColumn`sellOrderColumn`sideColumn`msgTypeColumn`seqColumn, `SecurityID`Time`Type`Price`Qty`BuyNo`SellNo`BSFlag`SourceType`ApplSeqNum)

// 创建引擎参数 prevClose，即昨日收盘价，prevClose 不影响最终的输出结果中除昨日收盘价以外的其他字段
prevClose = dict(`000587.SZ`002694.SZ`002822.SZ`000683.SZ`301063.SZ`300459.SZ`300057.SZ`300593.SZ`301035.SZ`300765.SZ, [1.66, 6.56, 6.10, 8.47, 38.10, 5.34, 9.14, 48.81, 60.04, 16.52])

// 定义引擎，每1s计算输出深交所股票10档买卖盘口
engine = createOrderBookSnapshotEngine(name="demo", exchange="XSHE", orderbookDepth=10, intervalInMilli = 1000, date=2022.01.10, startTime=09:15:00.000, prevClose=prevClose, dummyTable=dummyOrderStream, outputTable=outTable, inputColMap=inputColMap)

filePath = "./orderbookDemoInput.csv"
colNames = `SecurityID`Date`Time`SecurityIDSource`SecurityType`Index`SourceType`Type`Price`Qty`BSFlag`BuyNo`SellNo`ApplSeqNum`ChannelNo
colTypes = [SYMBOL, DATE, TIME, SYMBOL, SYMBOL, LONG, INT, INT, LONG, LONG, INT, LONG, LONG, LONG, INT]
orderTrade = table(1:0, colNames, colTypes)
orderTrade.append!(select * from loadText(filePath) order by Time)

// 10支股票的逐笔数据批量注入快照合成引擎
engine.append!(orderTrade)
select count(*) from outTable where SecurityID="300593.SZ", timestamp between 2022.01.10T13:15:01.000 and 2022.01.10T13:15:10.000

//output: 10
```

通过 *outputColMap* 指定需要输出的字段。`genOutputColumnsForOBSnapshotEngine`
函数返回值的第一个元素即为 *outputColMap*，返回值的第二个元素可以确定 *outputTable* 的
schema。

```
try { dropStreamEngine("demo") } catch(ex) { print(ex) }

filePath = "./orderbookDemoInput.csv"

// 创建引擎参数 dummyTable，即指定输入表的表结构
colNames = `SecurityID`Date`Time`SecurityIDSource`SecurityType`Index`SourceType`Type`Price`Qty`BSFlag`BuyNo`SellNo`ApplSeqNum`ChannelNo
colTypes = [SYMBOL, DATE, TIME, SYMBOL, SYMBOL, LONG, INT, INT, LONG, LONG, INT, LONG, LONG, LONG, INT]
share table(1:0, colNames, colTypes) as dummyOrderStream

// 创建引擎参数 inputColMap，即指定输入表各字段的含义
inputColMap = dict(`codeColumn`timeColumn`typeColumn`priceColumn`qtyColumn`buyOrderColumn`sellOrderColumn`sideColumn`msgTypeColumn`seqColumn, `SecurityID`Time`Type`Price`Qty`BuyNo`SellNo`BSFlag`SourceType`ApplSeqNum)

// 创建引擎参数 prevClose，即昨日收盘价，prevClose 不影响最终的输出结果中除昨日收盘价以外的其他字段
prevClose = dict(`000587.SZ`002694.SZ`002822.SZ`000683.SZ`301063.SZ`300459.SZ`300057.SZ`300593.SZ`301035.SZ`300765.SZ, [1.66, 6.56, 6.10, 8.47, 38.10, 5.34, 9.14, 48.81, 60.04, 16.52])

//创建使用 outputColMap 和 outputTableSch 接收 genOutputColumnsForOBSnapshotEngine 的返回值。它们分别用于确定 outputColMap 和 outputTable
outputColMap, outputTableSch = genOutputColumnsForOBSnapshotEngine(basic=true, time=false, depth=(10, true), tradeDetail=true, orderDetail=false, withdrawDetail=false, orderBookDetailDepth=0, prevDetail=false)

engine = createOrderBookSnapshotEngine(name="demo", exchange="XSHE", orderbookDepth=10, intervalInMilli = 1000, date=2022.01.10, startTime=09:15:00.000, prevClose=prevClose, dummyTable=dummyOrderStream, outputTable=outputTableSch, inputColMap=inputColMap, outputColMap=outputColMap, orderBookAsArray=true)

// 10支股票的逐笔数据批量注入快照合成引擎
engine.append!(select * from loadText(filePath) order by Time)
select top 10 * from outputTableSch where code="300593.SZ", timestamp between 2022.01.10T13:15:01.000 and 2022.01.10T13:15:10.000
```

部分结果展示如下：

![](../../images/orderBook1.png)

```
try { dropStreamEngine("demo") } catch(ex) { print(ex) }

filePath = "./orderbookDemoInput.csv"

// 创建引擎参数 dummyTable，即指定输入表的表结构
colNames = `SecurityID`Date`Time`SecurityIDSource`SecurityType`Index`SourceType`Type`Price`Qty`BSFlag`BuyNo`SellNo`ApplSeqNum`ChannelNo`ReceiveTime
colTypes = [SYMBOL, DATE, TIME, SYMBOL, SYMBOL, LONG, INT, INT, LONG, LONG, INT, LONG, LONG, LONG, INT, NANOTIMESTAMP]
share table(1:0, colNames, colTypes) as dummyOrderStream

// 创建引擎参数 inputColMap，即指定输入表各字段的含义
inputColMap = dict(`codeColumn`timeColumn`typeColumn`priceColumn`qtyColumn`buyOrderColumn`sellOrderColumn`sideColumn`msgTypeColumn`seqColumn`receiveTime, `SecurityID`Time`Type`Price`Qty`BuyNo`SellNo`BSFlag`SourceType`ApplSeqNum`ReceiveTime)

// 创建引擎参数 prevClose，即昨日收盘价，prevClose 不影响最终的输出结果中除昨日收盘价以外的其他字段
prevClose = dict(`000587.SZ`002694.SZ`002822.SZ`000683.SZ`301063.SZ`300459.SZ`300057.SZ`300593.SZ`301035.SZ`300765.SZ, [1.66, 6.56, 6.10, 8.47, 38.10, 5.34, 9.14, 48.81, 60.04, 16.52])

//此处只定义 outputColMap 接收 genOutputColumnsForOBSnapshotEngine 的第一个返回值。因 userDefinedMetrics 定义的指标中需要使用委托明细和回撤明细，因此 genOutputColumnsForOBSnapshotEngine  需要指定 orderDetail=false, withdrawDetail=true
outputColMap = genOutputColumnsForOBSnapshotEngine(basic=true, time=false, depth=(10, true), tradeDetail=true, orderDetail=false, withdrawDetail=true, orderBookDetailDepth=0, prevDetail=false)[0]

//// 定义用户自定义因子
def userDefinedFunc(t){
        AvgBuyDuration = rowAvg(t.TradeMDTimeList-t.TradeOrderBuyNoTimeList).int()
        AvgSellDuration = rowAvg(t.TradeMDTimeList-t.TradeOrderSellNoTimeList).int()
        BuyWithdrawQty = rowSum(t.WithdrawBuyQtyList)
        SellWithdrawQty = rowSum(t.WithdrawSellQtyList)
        return (AvgBuyDuration, AvgSellDuration, BuyWithdrawQty, SellWithdrawQty)
}

// 定义 orderbook 引擎的输出表，需要包含基础字段（basic），报价/询价的多档价格和数量（depth），userDefinedMetrics 自定义指标的输出结果
outputTableSch = genOutputColumnsForOBSnapshotEngine(basic=true, time=false, depth=(10, true), tradeDetail=false, orderDetail=false, withdrawDetail=false, orderBookDetailDepth=0, prevDetail=false)[1]
colNames = outputTableSch.schema().colDefs.name join (`AvgBuyDuration`AvgSellDuration`BuyWithdrawQty`SellWithdrawQty)
colTypes = outputTableSch.schema().colDefs.typeString join (`INT`INT`INT`INT)
outputTable = table(1:0, colNames, colTypes)

// 创建引擎，每1s计算输出深交所股票10档 orderbook

engine = createOrderBookSnapshotEngine(name="demo", exchange="XSHE", orderbookDepth=10, intervalInMilli = 1000, date=2022.01.10, startTime=09:30:00.000, prevClose=prevClose, dummyTable=dummyOrderStream, outputTable=outputTable, inputColMap=inputColMap, outputColMap=outputColMap, orderBookAsArray=true, userDefinedMetrics=userDefinedFunc)

t = select * from loadText(filePath) order by Time
update t set ReceiveTime = now(true) // 构造接收时间列

getStreamEngine("demo").append!(t)

select top 10 * from outputTable where code="300593.SZ", timestamp between 2022.01.10T13:15:01.000 and 2022.01.10T13:15:10.000
```

部分结果展示如下：

![](../../images/orderBook2.png)

相关函数：[genOutputColumnsForOBSnapshotEngine](../g/genoutputcolumnsforobsnapshotengine.html)

相关教程：[基于逐笔数据合成高频 Orderbook：DolphinDB Orderbook 引擎](../../tutorials/orderBookSnapshotEngine.html)

## 附录

**basic（基础字段）**

不指定 *outputColMap* 和 *userDefinedMetrics* 时，输出除 openPrice，maxPrice，minPrice
外的字段。

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| code | SYMBOL | 证券代码 |
| timestamp | TIMESTAMP | 快照时间戳，如以1s间隔合成快照：2022.08.01T09:20:00.000，2022.08.01T09:20:01.000 |
| lastSeq | LONG | 最后一条逐笔数据的序号（lastAppSeqNum） |
| tradingPhaseCode | INT | 交易阶段代码（tradingPhaseCode）。枚举值：0（开盘前，启动）、1（开盘集合竞价）、2（开盘集合竞价阶段结束至连续竞价阶段开始之前）、3（连续竞价）、4（中午午休）、5（收盘集合竞价） |
| modified | BOOL | 各证券代码当前周期无输入数据，则对应输出表中的该字段显示为 false，否则显示为 true。 |
| turnover | DOUBLE | 当前周期内的成交金额 |
| volume | LONG | 当前周期内的成交量 |
| tradeNum | INT | 当前周期内的成交笔数 |
| ttlTurnover | DOUBLE | （totalTurnover）开盘到现在的成交金额 |
| ttlVolume | LONG | （totalVolume）开盘到现在的成交量 |
| ttlTradeNum | INT | （totalTradeNum）开盘到现在的成交笔数 |
| lastPrice | DOUBLE | （lastPx）最近成交价 |
| highPrice | DOUBLE | （highPx）开盘到现在的最高价 |
| lowPrice | DOUBLE | （lowPx）开盘到现在的最低价 |
| openPrice | DOUBLE | （openPx）开盘价 |
| avgAskPrice | DOUBLE | （ask）卖出加权平均价 = 卖单的每一档价格\*量 / 卖单的总量 |
| avgBidPrice | DOUBLE | （bid）买入加权平均价 = 买单的每一档价格\*量 / 买单的总量 |
| askQty | LONG | （askVol）当前卖盘加权挂单量 |
| bidQty | LONG | （bidVol）当前买盘加权挂单量 |
| preClosePrice | DOUBLE/INT | （preClosePx）昨收价。  引擎外部定义昨收价，并以字典的方式传入引擎。 |
| abnormal | BOOL | （invalid）输入数据是否异常：   * true 表示输入数据异常，或在设置了*forceTriggerTime*   后对不连续的数据进行了强制合成得到的第一批订单簿快照数据及其后续数据；其中，数据异常是指收到了逐笔成交或者撤单，却找不到对应的委托单。 * false 表示输入数据正常。 |
| maxPrice | DOUBLE/INT | 涨停价。  引擎外部定义涨停价，并以字典的方式传入引擎。 |
| minPrice | DOUBLE/INT | 跌停价。  引擎外部定义跌停价，并以字典的方式传入引擎。 |

**time（时间字段）**

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| mdTime | TIME | 快照时间戳，如以1s间隔合成快照：09:20:00.000，09:20:01.000 |
| mdDate | DATE | 快照日期。  引擎外部定义快照日期，通过 date 参数传入引擎。 |
| UpdateTime1 | NANOTIMESTAMP | 触发窗口关闭的那条输入数据的 receiveTime |
| UpdateTime2 | NANOTIMESTAMP | 触发窗口关闭后计算完成的系统时刻，即输出计算结果时的系统时间。 |

**depth（报价/询价档位）**

不指定 *outputColMap* 和 *userDefinedMetrics* 时，会输出 depth 中的所有字段。提供两种方式存储 depth
数据。两种方式只能选其一：

* 每个档位输出一列。比如 bidsPrice 有10个档位，则会输出10个 bidsPrice
  字段：bidsPrice1、bidsPrice2、…、bidsPrice10。

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| bidsPrice | DOUBLE (多个) | （bids）多个字段，分别存放多档买入价格，档位由 *depth*确定 |
| bidsQty | LONG (多个) | （bidVolumes）多个字段，分别存放多档买入数量，档位由 *depth* 确定 |
| bidsCount | INT (多个) | （bidOrderNums）多个字段，分别存放多档买入委托笔数，档位由 *depth* 确定 |
| asksPrice | DOUBLE (多个) | （asks）多个字段，分别存放多档卖出价格，档位由 *depth* 确定 |
| asksQty | LONG (多个) | （askVolumes）多个字段，分别存放多档卖出数量，档位由 *depth* 确定 |
| asksCount | INT (多个) | （askOrderNums）多个字段，分别存放多档卖出委托笔数，档位由 *depth* 确定 |

* 多个档位输出到一个列字段，该列的类型为数组向量。比如 bidsPrice
  有10个档位，则会将这10个档位以数组向量的形式输出到一个字段：bidsPriceList。

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| bidsPriceList | DOUBLE[] | 数组向量，存放多档买入价格，档位由 *depth* 确定 |
| bidsQtyList | LONG[] | 数组向量，存放多档买入数量，档位由 *depth* 确定 |
| bidsCountList | INT[] | 数组向量，存放多档买入委托笔数，档位由 *depth* 确定 |
| asksPriceList | DOUBLE[] | 数组向量，存放多档卖出价格，档位由 *depth* 确定 |
| asksQtyList | LONG[] | 数组向量，存放多档卖出数量，档位由 *depth* 确定 |
| asksCountList | INT[] | 数组向量，存放多档卖出委托笔数，档位由 *depth* 确定 |

**tradeDetail（成交明细）**

注：

* 对于上交所订单簿，若指定参数 *includeImmediateExecution* =
  true，则委托明细中将会统计即时成交的订单。此时，系统将 trade 记录的成交时间作为 order 的下单时间，并在
  tradeOrderBuyNoTimeList/tradeOrderSellNoTimeList 字段中显示。
* 在调用 `genOutputColumnsForOBSnapshotEngine` 函数时，当
  *tradeDetail*=true 时，默认不会输出 tradeBuyOrderTypeList 和
  tradeSellOrderTypeList 两个字段。

| 基础衍生字段 | 类型 | 含义 |
| --- | --- | --- |
| buyQty | LONG | 当前周期内的买入总量 = sum( BSFlag=1 的成交的量） |
| sellQty | LONG | 当前周期内的卖出总量 = sum( BSFlag=2的成交的量） |
| buyMoney | DOUBLE | 当前周期内的买入总金额 = sum( BSFlag=1的成交的量\*价格） |
| sellMoney | DOUBLE | 当前周期内的卖出总金额 = sum( BSFlag=2的成交的量\*价格） |
| tradePriceList | DOUBLE[] | 当前周期内成交价格列表 |
| tradeQtyList | LONG[] | 当前周期内成交量列表 |
| tradeTypeList | INT[] | 当前周期内成交类型列表 |
| tradeBSFlagList | INT[] | 当前周期内成交方向列表 |
| tradeMDTimeList | TIME[] | 当前周期内成交时间列表 |
| tradeBuyNoList | LONG[] | 当前周期内买方委托序号列表 |
| tradeSellNoList | LONG[] | 当前周期内卖方委托序号列表 |
| tradeOrderBuyNoTimeList | TIME[] | 当前周期内的有效成交对应的委托的买单下单时间 |
| tradeOrderSellNoTimeList | TIME[] | 当前周期内的有效成交对应的委托的卖单下单时间 |
| tradeBuyOrderTypeList | INT[] | 当前周期内的有效成交对应的委托的买单类型 |
| tradeSellOrderTypeList | INT[] | 当前周期内的有效成交对应的委托的卖单类型 |

**orderDetail （委托明细）**

注意：对于上交所订单簿，若指定参数 *includeImmediateExecution* = true，则委托明细中将会统计即时成交的订单。

| 基础衍生字段 | 类型 | 含义 |
| --- | --- | --- |
| orderPriceList | DOUBLE[] | 当前周期内委托价格列表 |
| orderQtyList | LONG[] | 当前周期内成交量列表 |
| orderTypeList | INT[] | 当前周期内委托类型列表 |
| orderBSFlagList | INT[] | 当前周期内委托方向列表 |
| orderMDTimeList | TIME[] | 当前周期内委托时间列表 |
| orderNoList | LONG[] | 当前周期内委托序号列表 |

**withdrawDetail（撤单明细）**

注： 对于上交所订单簿，若指定参数
*includeImmediateExecution* =
true，则委托明细中将会统计即时成交的订单。此时，withdrawBuyOrderQtyList/WithdrawSellOrderQtyList
字段中将包括即时成交的数量。

| 基础衍生字段 | 类型 | 含义 |
| --- | --- | --- |
| withdrawBuyPriceList | DOUBLE[] | 当前周期内买方撤单的委托价格 |
| withdrawBuyQtyList | LONG[] | 当前周期内买方撤单的委托量 |
| withdrawBuyOrderTypeList | INT[] | 当前周期内买方撤单的委托的订单类型 |
| withdrawBuyMDTimeList | TIME[] | 当前周期内买方撤单的订单时间 |
| withdrawBuyOrderMDTimeList | TIME[] | 当前周期内买方撤单对应的委托下单时间 |
| WithdrawBuyOrderQtyList | LONG[] | 当前周期内买方撤单对应的原始委托数据中的委托量 |
| withdrawSellPriceList | DOUBLE[] | 当前周期内卖方撤单的委托价格 |
| withdrawSellQtyList | LONG[] | 当前周期内卖方撤单的委托量 |
| withdrawSellOrderTypeList | INT[] | 当前周期内卖方撤单的委托的订单类型 |
| withdrawSellMDTimeList | TIME[] | 当前周期内卖方撤单的订单时间 |
| withdrawSellOrderMDTimeList | TIME[] | 当前周期内卖方撤单对应的委托下单时间 |
| WithdrawSellOrderQtyList | LONG[] | 当前周期内卖方撤单对应的原始委托数据中的委托量 |

**prevDetail（上一笔交易明细）**

注： 对于上交所订单簿，若指定参数
*includeImmediateExecution* =
true，则委托明细中将会统计即时成交的订单。此时，当即时成交的价格和上一笔快照的价格（BuyPrice1/SellPrice1）相同，则
prevBuyAddQtyList1/prevSellAddQtyList1 字段中将包括即时成交的申购明细。

| 基础衍生字段 | 类型 | 含义 |
| --- | --- | --- |
| prevBuyPrice1 | DOUBLE | 上一笔快照的 BuyPrice1 价格 |
| prevSellPrice1 | DOUBLE | 上一笔快照的 SellPrice1 价格 |
| prevBuyAddQtyList1 | LONG[] | 价格为上一笔快照的 BuyPrice1，在当前周期内的申购明细 |
| prevSellAddQtyList1 | LONG[] | 价格为上一笔快照的 SellPrice1，在当前周期内的申购明细 |
| prevBuyWithdrawQtyList1 | LONG[] | 价格为上一笔快照的 BuyPrice1，在当前周期内的撤单明细 |
| prevSellWithdrawQtyList1 | LONG[] | 价格为上一笔快照的 SellPrice1，在当前周期内的撤单明细 |

**orderBookDetailDepth（ orderbook 明细档位）**

每个档位输出一列，该列的类型是数组向量。比如 buyQtyList 有20个档位，则会输出20个 buyQtyList
字段：buyQtyList1、buyQtyList2、…、buyQtyList20。buyValueList，sellQtyList 和 sellValueList
同理。

| 基础衍生字段 | 类型 | 含义 |
| --- | --- | --- |
| buyQtyList | LONG[]（多个） | 当前最新盘口各档位买入的每一笔委托的数量 |
| buyValueList | DOUBLE[]（多个） | 当前最新盘口各档位买入的每一笔委托的金额 |
| sellQtyList | LONG[]（多个） | 当前最新盘口各档位卖出的每一笔委托的数量 |
| sellValueList | DOUBLE[]（多个） | 当前最新盘口各档位卖出的每一笔委托的金额 |

**seqDetail（sequence 明细）**

注： 对于上交所订单簿，若指定参数
*includeImmediateExecution* = true，则委托明细中将会统计即时成交的订单。此时，orderSeqList
字段中将会包含即时成交的委托记录。

| 基础衍生字段 | 类型 | 含义 |
| --- | --- | --- |
| tradeSeqList | LONG[] | 当前周期内的成交序号列表 |
| orderSeqList | LONG[] | 当前周期内的委托序号列表 |
| withdrawBuySeqList | LONG[] | 当前周期内的买方撤单序号列表 |
| withdrawSellSeqList | LONG[] | 当前周期内的卖方撤单序号列表 |

**residualDetail（剩余委托明细）**

注意：

* 卖方字段（ResidualAskPriceList, ResidualAskQtyList, ResidualAskTimeList,
  ResidualAskApplSeqNumList）中每个档位的信息按照价格和交易时间升序排序。若价格和交易时间相同，则按数据进入引擎的时间升序排序。
* 买方字段（ResidualBidPriceList, ResidualBidQtyList, ResidualBidTimeList,
  ResidualBidApplSeqNumList）中每个档位的信息按价格降序和交易时间升序排序，若价格和交易时间相同，则按数据进入引擎的时间升序排序。

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| ResidualAskPriceList | DOUBLE[] | 卖方剩余委托价格列表 |
| ResidualAskQtyList | LONG[] | 卖方剩余委托量列表 |
| ResidualAskTimeList | TIME[] | 卖方剩余委托时间列表 |
| ResidualAskApplSeqNumList | LONG[] | 卖方剩余委托单 ApplSeqNum 列表 |
| ResidualBidPriceList | DOUBLE[] | 买方剩余委托价格列表 |
| ResidualBidQtyList | LONG[] | 买方剩余委托量列表 |
| ResidualBidTimeList | TIME[] | 买方剩余委托时间列表 |
| ResidualBidApplSeqNumList | LONG[] | 买方剩余委托单 ApplSeqNum 列表 |

**tradeDetail（成交明细）**

注意：对于上交所订单簿，若指定参数 *includeImmediateExecution* = true，则委托明细中将会统计即时成交的订单。此时，系统将
trade 记录的成交时间作为 order 的下单时间，并在 tradeOrderBuyNoTimeList/tradeOrderSellNoTimeList
字段中显示。

| 基础衍生字段 | 类型 | 含义 |
| --- | --- | --- |
| buyQty | LONG | 当前周期内的买入总量 = sum( BSFlag=1 的成交的量） |
| sellQty | LONG | 当前周期内的卖出总量 = sum( BSFlag=2的成交的量） |
| buyMoney | DOUBLE | 当前周期内的买入总金额 = sum( BSFlag=1的成交的量\*价格） |
| sellMoney | DOUBLE | 当前周期内的卖出总金额 = sum( BSFlag=2的成交的量\*价格） |
| tradePriceList | DOUBLE[] | 当前周期内成交价格列表 |
| tradeQtyList | LONG[] | 当前周期内成交量列表 |
| tradeTypeList | INT[] | 当前周期内成交类型列表 |
| tradeBSFlagList | INT[] | 当前周期内成交方向列表 |
| tradeMDTimeList | TIME[] | 当前周期内成交时间列表 |
| tradeBuyNoList | LONG[] | 当前周期内买方委托序号列表 |
| tradeSellNoList | LONG[] | 当前周期内卖方委托序号列表 |
| tradeOrderBuyNoTimeList | TIME[] | 当前周期内的有效成交对应的委托的买单下单时间 |
| tradeOrderSellNoTimeList | TIME[] | 当前周期内的有效成交对应的委托的卖单下单时间 |

**orderDetail （委托明细）**

注意：对于上交所订单簿，若指定参数 *includeImmediateExecution* = true，则委托明细中将会统计即时成交的订单。

| 基础衍生字段 | 类型 | 含义 |
| --- | --- | --- |
| orderPriceList | DOUBLE[] | 当前周期内委托价格列表 |
| orderQtyList | LONG[] | 当前周期内成交量列表 |
| orderTypeList | INT[] | 当前周期内委托类型列表 |
| orderBSFlagList | INT[] | 当前周期内委托方向列表 |
| orderMDTimeList | TIME[] | 当前周期内委托时间列表 |
| orderNoList | LONG[] | 当前周期内委托序号列表 |

**withdrawDetail（撤单明细）**

注意：对于上交所订单簿，若指定参数 *includeImmediateExecution* =
true，则委托明细中将会统计即时成交的订单。此时，withdrawBuyOrderQtyList/WithdrawSellOrderQtyList
字段中将包括即时成交的数量。

| 基础衍生字段 | 类型 | 含义 |
| --- | --- | --- |
| withdrawBuyPriceList | DOUBLE[] | 当前周期内买方撤单的委托价格 |
| withdrawBuyQtyList | LONG[] | 当前周期内买方撤单的委托量 |
| withdrawBuyOrderTypeList | INT[] | 当前周期内买方撤单的委托的订单类型 |
| withdrawBuyMDTimeList | TIME[] | 当前周期内买方撤单的订单时间 |
| withdrawBuyOrderMDTimeList | TIME[] | 当前周期内买方撤单对应的委托下单时间 |
| WithdrawBuyOrderQtyList | LONG[] | 当前周期内买方撤单对应的原始委托数据中的委托量 |
| withdrawSellPriceList | DOUBLE[] | 当前周期内卖方撤单的委托价格 |
| withdrawSellQtyList | LONG[] | 当前周期内卖方撤单的委托量 |
| withdrawSellOrderTypeList | INT[] | 当前周期内卖方撤单的委托的订单类型 |
| withdrawSellMDTimeList | TIME[] | 当前周期内卖方撤单的订单时间 |
| withdrawSellOrderMDTimeList | TIME[] | 当前周期内卖方撤单对应的委托下单时间 |
| WithdrawSellOrderQtyList | LONG[] | 当前周期内卖方撤单对应的原始委托数据中的委托量 |

**prevDetail（上一笔交易明细）**

注意：对于上交所订单簿，若指定参数 *includeImmediateExecution* =
true，则委托明细中将会统计即时成交的订单。此时，当即时成交的价格和上一笔快照的价格（BuyPrice1/SellPrice1）相同，则
prevBuyAddQtyList1/prevSellAddQtyList1 字段中将包括即时成交的申购明细。

| 基础衍生字段 | 类型 | 含义 |
| --- | --- | --- |
| prevBuyPrice1 | DOUBLE | 上一笔快照的 BuyPrice1 价格 |
| prevSellPrice1 | DOUBLE | 上一笔快照的 SellPrice1 价格 |
| prevBuyAddQtyList1 | LONG[] | 价格为上一笔快照的 BuyPrice1，在当前周期内的申购明细 |
| prevSellAddQtyList1 | LONG[] | 价格为上一笔快照的 SellPrice1，在当前周期内的申购明细 |
| prevBuyWithdrawQtyList1 | LONG[] | 价格为上一笔快照的 BuyPrice1，在当前周期内的撤单明细 |
| prevSellWithdrawQtyList1 | LONG[] | 价格为上一笔快照的 SellPrice1，在当前周期内的撤单明细 |

**seqDetail（sequence 明细）**

注意：对于上交所订单簿，若指定参数 *includeImmediateExecution* =
true，则委托明细中将会统计即时成交的订单。此时，orderSeqList 字段中将会包含即时成交的委托记录。

| 基础衍生字段 | 类型 | 含义 |
| --- | --- | --- |
| tradeSeqList | LONG[] | 当前周期内的成交序号列表 |
| orderSeqList | LONG[] | 当前周期内的委托序号列表 |
| withdrawBuySeqList | LONG[] | 当前周期内的买方撤单序号列表 |
| withdrawSellSeqList | LONG[] | 当前周期内的卖方撤单序号列表 |

