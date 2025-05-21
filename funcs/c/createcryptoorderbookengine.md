# createCryptoOrderBookEngine

## 语法

`createCryptoOrderBookEngine(name, dummyTable, inputColMap,
[outputTable], depth, [updateRule='direct'], [errorHandler=NULL],
[cachingInterval=5000], [timeout=-1], [outputHandler=NULL], [msgAsTable=false],
[cachedDepth])`

注：

社区版 License 暂不支持该引擎，如需使用此功能，请联系技术支持。

## 详情

根据数字货币全量深度快照和增量深度信息，实时更新订单簿。

**返回值：**一个表

## 参数

**name** 字符串标量，表示 CryptoOrderBook 引擎的名称，可包含字母，数字和下划线，但必须以字母开头。

**dummyTable** 一个表对象，表示输入表。*dummyTable* 需要通过 *inputColMap* 映射为如下列：

必需列1：

| **列名** | **类型** | **含义** |
| --- | --- | --- |
| symbol | SYMBOL | 数字货币代码。 |
| isIncremental | BOOL | 是否为增量数据。true 表示增量数据，false 表示全量数据。 |
| eventTime | TIMESTAMP | 事件时间。 |
| askQty | DECIMAL[] / DOUBLE[] | 卖出数量的列表。 |
| askPrice | DECIMAL[] / DOUBLE[] | 卖出价格的列表。 |
| bidQty | DECIMAL[] / DOUBLE[] | 买入数量的列表。 |
| bidPrice | DECIMAL[] / DOUBLE[] | 买入价格的列表。 |

必需列2：根据 updateRule 的取值进行调整。

当 *updateRule* ="direct" 时，不需要指定必需列2。

当 *updateRule* ="general" 时，指定以下列：

| **列名** | **类型** | **含义** |
| --- | --- | --- |
| prevUpdateId | LONG | 上一条数据的 ID。 |
| updateId | LONG | 当前收到数据的 ID。 |

当 *updateRule* ="Binance-spot" 时，指定以下列：

| **列名** | **类型** | **含义** |
| --- | --- | --- |
| lastUpdateId | LONG | 从上次推送至今新增的最后一个 update Id。 |
| firstUpdateId | LONG | 从上次推送至今新增的第一个 update Id。 |

当 *updateRule* ="Binance-futures" 时，指定以下列：

| **列名** | **类型** | **含义** |
| --- | --- | --- |
| lastUpdateId | LONG | 从上次推送至今新增的最后一个 update Id。 |
| firstUpdateId | LONG | 从上次推送至今新增的第一个 update Id。 |
| prevLastUpdateId | LONG | 上次推送的最后一个 update Id (即上条消息的 lastUpdateId)。 |

其它列：除上述必需列外的列。引擎会将这些列简单拷贝到 *outputTable* 的对应列中。

**inputColMap** 字典，将 *dummyTable* 中列字段的名称映射为引擎计算所需要的列。

**outputTable** 可选参数，一个表对象，用于输出最新的订单簿。其结构必须与 *dummyTable*
相同。*outputTable* 和 *outputHandler* 只需指定其一。

**depth** 正整数或字典，用于指定订单簿的深度。

* 正整数：所有数字货币的订单簿深度都为该设置值。
* 字典：键是字符串标量或向量，表示数字货币代码；值是整型，表示订单簿深度。对于指定的数字货币，将按照设定的深度输出订单簿。未被指定的数字货币将不输出订单簿结果。

**updateRule** 可选参数，字符串标量，表示订单簿更新规则。可选值为：

* "direct"：默认值，表示直接更新，系统将不进行数据丢失判断，仅根据 isIncremental 字段的值绝对是更新（isIncremental
  为 true）还是覆盖（isIncremental 为 false）订单簿结果。
* "general"：表示通用的更新规则。要求按顺序插入增量数据，并确保数据中 updateId 单调递增。
* "Binance-spot"：表示适用于币安交易所现货的更新规则。
* "Binance-futures"：表示适用于币安交易所期货的更新规则。

**errorHandler** 可选参数，自定义函数。当增量数据出现缺失时，可通过该函数进行错误处理。包含 2 个参数：

* 第一个是字符串标量，表示数字货币代码。
* 第二个是整型标量，表示错误码，包括以下情况：
  + 1：接收到历史数据。
  + 2：接收到应在未来时间点到达的乱序数据。
  + 3：超时错误，指定时间间隔内没有新的订单簿合成。
  + 4：买卖价格交叉错误。判断交叉的条件为最高买价大于等于最低卖价。

**cachingInterval** 可选参数，整型标量，表示缓存增量深度数据的时间间隔。默认值为
5000，单位为毫秒。对于每个数字货币，当缓存中的数据时间与当前最新一条数据时间的差值小于等于 *cachingInterval*
时，该数据才会被保留在缓存中。

**timeout** 可选参数，整型标量，表示超时时间。单位为毫秒，默认值为 -1，表示不设置超时时间。在
*timeout* 指定的时间内未合成新的订单簿时，将触发超时错误，此时会通过 *errorHandler* 进行错误处理。

**outputHandler** 可选参数，一元函数。设置此参数时，引擎计算结束后，不再将计算结果写到输出表，而是会调用此函数处理计算结果。默认值为
NULL，表示仍将结果写到输出表。

**msgAsTable** 可选参数，布尔标量，表示在设置了参数 *outputHandler* 时，将引擎的计算结果以表的结构调用函数。默认值为
false，此时将计算结果的每一列作为元素组成元组。

**cachedDepth** 可选参数，正整数或字典，用于指定缓存中价格和数量（包括 askQty, askPrice,
bidQty, bidPrice）的深度。

* 正整数：缓存中所有数字货币的价格和数量将按照该值的深度进行缓存。
* 字典：键是字符串标量或向量，表示数字货币代码；值是整型，表示对应的深度。对于指定的数字货币，将按照设定的深度缓存价格和数量。未被指定的数字货币将保留实际收到的所有价格和数量信息。

## 例子

运行代码前，先下载 <../data/CryptoOrderBookInput.zip> 文件。

例1. 创建一个加密货币订单簿引擎，使用 "Binance-futures" 规则处理来自 Binance 交易所 U 本位合约的深度数据。根据 Binance
交易所数据发送规则，示例数据中首先为增量深度数据，在 68 行插入 1000 档全量快照数据后，引擎开始输出订单簿。

```
// 定义输入输出表结构
colNames = `isIncremental`exchange`eventTime`transactionTime`symbol`firstUpdateId`lastUpdateId`prevLastUpdateId`bidPrice`bidQty`askPrice`askQty
colTypes = [BOOL, SYMBOL, TIMESTAMP, TIMESTAMP, SYMBOL, LONG, LONG, LONG, DECIMAL128(18)[], DECIMAL128(8)[], DECIMAL128(18)[], DECIMAL128(8)[]]

// 创建输入输入输出表
share table(1:0, colNames, colTypes) as outputTable
share table(1:0, colNames, colTypes) as inputTable

inputTarget = ["symbol", "eventTime", "isIncremental", "bidPrice", "bidQty", "askPrice", "askQty", "lastUpdateId", "firstUpdateId", "prevLastUpdateId"]
inputSource = ["symbol", "eventTime", 'isIncremental', 'bidPrice', 'bidQty', 'askPrice', 'askQty', 'lastUpdateId', 'firstUpdateId', 'prevLastUpdateId']

inputColMap = dict(inputTarget, inputSource)

depth = dict(["BTCUSDT"], [1000])
cachedDepth = dict(["BTCUSDT"], [1500])

def errorHandler(instrument, code) {
    if (code == 1) {
        writeLog("handle hisotorical msg...")
    } else if (code == 2) {
        writeLog("handle unordered msg...")
    } else if (code == 3) {
        writeLog("handle timeout...")
    } else if (code == 4) {
        writeLog("handle corssed price...")
    } else {
        writeLog("unknown error!")
    }
}

// 创建引擎
engine = createCryptoOrderBookEngine(name="binanceFutures", dummyTable=inputTable, inputColMap=inputColMap, outputTable=outputTable,
                                        depth=depth, updateRule="Binance-futures", errorHandler=errorHandler, cachingInterval=5000,
                                        timeout=6000, msgAsTable=true, cachedDepth=cachedDepth)

// 加载示例数据
fin=file("binanceFuturesTestData.bin")
binanceFuturesTestData = fin.readObject()
fin.close();
// 数据插入引擎进行合成
getStreamEngine("binanceFutures").append!(binanceFuturesTestData)

// 清除环境
undef("inputTable", SHARED)
undef("outputTable", SHARED)
dropStreamEngine("binanceFutures")

```

例2. 创建一个加密货币订单簿引擎，使用 "general" 规则处理来自 OKX 交易所永续合约的深度数据。根据 OKX 交易所数据发送规则，示例数据中首行为 400
档快照数据，之后为增量快照数据。

```

// 定义输入输出表结构
colNames=['isIncremental', 'symbol', 'askPrice', 'askVolume', 'askNum', 'bidPrice', 'bidVolume', 'bidNum', 'checksum', 'prevSeqId', 'seqId', 'updateTime'];
colTypes=[BOOL, SYMBOL, DECIMAL128(18)[], DECIMAL128(8)[], INT[], DECIMAL128(18)[], DECIMAL128(8)[], INT[], LONG, LONG, LONG, TIMESTAMP];

// 创建输入输入输出表
share table(1:0, colNames, colTypes) as inputTable
share table(1:0, colNames, colTypes) as outputTable

inputTarget = ["symbol", "eventTime", "isIncremental", "bidPrice", "bidQty", "askPrice", "askQty", "prevUpdateId", "updateId"];
inputSource = ["symbol", "updateTime", 'isIncremental', 'bidPrice', 'bidVolume', 'askPrice', 'askVolume', 'prevSeqId', 'seqId'];

inputColMap = dict(inputTarget, inputSource)

depth = dict(["BTC-USD-SWAP"], [400])
cachedDepth = dict(["BTC-USD-SWAP"], [800])

def errorHandler(instrument, code) {
    if (code == 1) {
        writeLog("handle hisotorical msg...")
    } else if (code == 2) {
        writeLog("handle unordered msg...")
    } else if (code == 3) {
        writeLog("handle timeout...")
    } else if (code == 4) {
        writeLog("handle corssed price...")
    } else {
        writeLog("unknown error!")
    }
}

// 创建引擎
engine = createCryptoOrderBookEngine(name="okxSwap", dummyTable=inputTable, inputColMap=inputColMap, outputTable=outputTable,
                                        depth=depth, updateRule="general", errorHandler=errorHandler, cachingInterval=5000,
                                        timeout=6000, msgAsTable=true, cachedDepth=cachedDepth)

// 加载示例数据
fin=file("okxTestData.bin")
okxTestData = fin.readObject()
fin.close();
// 数据插入引擎进行合成
getStreamEngine("okxSwap").append!(okxTestData)

// 清除环境
undef("inputTable", SHARED)
undef("outputTable", SHARED)
dropStreamEngine("okxSwap")

```

