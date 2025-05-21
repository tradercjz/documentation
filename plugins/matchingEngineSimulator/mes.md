# MatchingEngineSimulator

模拟撮合引擎插件（Matching Engine Simulator）用于模拟用户在某个时间点发出或取消订单的操作，并获取相应的交易结果。

该插件以行情数据（快照数据或逐笔数据）和用户委托订单（买方或卖方）作为输入，根据订单撮合规则实现模拟撮合后，将订单成交结果（含部分成交结果、拒绝订单和已撤订单）输出至订单明细输出表，未成交部分等待与后续行情撮合成交，或者等待用户撤单。

## 安装插件

### 版本要求

DolphinDB Server 2.00.12.2 和 3.00.0.2 及更高版本，支持 Linux x86-64, Linux JIT,
Windows, Windows JIT。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins`
   命令查看插件仓库中的插件信息。

   ```
   login("admin", "123456")
   listRemotePlugins("MatchingEngineSimulator")
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("MatchingEngineSimulator")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("MatchingEngineSimulator")
   ```

## 接口介绍

### createMatchEngine

**语法**

```
MatchingEngineSimulator::createMatchEngine(name,
	exchange,
	config,
	dummyQuoteTable,
	quoteColMap,
	dummyUserOrderTable,
	userOrderColMap,
	orderDetailsOutput,
	[orderDetailsAndSnapshotOutput],
	[snapshotOutput])
```

**详情**

创建一个模拟撮合引擎。

**返回值**

一个模拟撮合引擎。

**参数**

* name：名称，字符串标量，全局唯一。
* exchange：交易所标识，股票类型可以为深交所 "XSHE" 或上交所 "XSHG"，期货期权类型可以为商品期货和期权
  “commodity”、国债期货股指期货和权益类的期权“equity” 或 无时间限制 “universal”。

  | 取值 | 说明 |
  | --- | --- |
  | "XSHE" | 深交所股票 |
  | "XSHG" | 上交所股票 |
  | ”commodity” | 商品期货或者期权 |
  | ”equity” | 国债期货、股指期货或权益类的期权 |
  | “universal” | 无交易时间限制的品种 |
  | “CFFEX” | 上交所债券 |
  | “CFETS” | 银行间 Xbond 债券 |
* config： 一个字典标量，包含配置的键值对，类型为(STRING, DOUBLE)。详细说明如下：

| 字典 key | 含义 |
| --- | --- |
| dataType | 行情类别：  股票逐笔：0  股票快照：1  银行间现券/上交所债券快照：3  股票分钟：4  股票日频：5  期货期权快照：6  期货期权分钟：7  期货期权分钟：8  数字货币快照：13  数字货币分钟：14  数字货币日频：15 |
| depth | 匹配的订单簿深度，5 - 50 |
| outputOrderBook | 是否输出订单簿：0（不输出），1（输出） |
| outputInterval | 输出订单簿的最小时间间隔，单位为毫秒 |
| latency | 模拟时延，单位为毫秒，用来模拟用户订单从发出到被处理的时延。  * latency=-1   ，订单会即时撮合。目前仅股票逐笔、股票快照、银行间现券/上交所债券快照支持 * latency > 0 ， 当最新行情时间 >订单时间+ latency   时，开始撮合该用户订单 * latency = 0 ，当最新行情时间>=订单时间+ latency   时，开始撮合用户订单 |
| orderBookMatchingRatio | 与盘口撮合的成交百分比，不能小于 0。 |
| matchingMode | 根据快照行情是否带有区间成交明细信息，可以有两种撮合模式，可设置为 1 或者 2：   * 1：与最新成交价以及对手方盘口按配置的比例撮合（快照行情无区间成交明细信息时） * 2：与区间的成交列表以及对手方盘口撮合成交（快照行情带有区间成交明细信息时） |
| matchingRatio | 快照模式下，快照的区间成交百分比，默认和成交百分比 *orderBookMatchingRatio* 相等。 |
| enableOrderDetailsAndSnapshotOutput | 是否需要输出到复合输出表 |
| outputTimeInfo | 成交输出表中是否需要订单收到时的行情最新时间，“匹配开始时间”“匹配完成时间”：0（不需要）， 1（需要） |
| outputQueuePosition | 是否输出订单在真实行情数据的位置信息。该参数可设置为如下值：   * 0：默认值，表示不输出。 * 1：表示订单撮合成交计算上述指标的时候，把最新的一条行情纳入订单薄。 * 2：表示订单撮合成交计算上述指标的时候，把最新的一条行情不纳入订单薄，即统计的是撮合计算前的位置信息。   如果输出该信息，则在成交明细和未成交订单接口中会增加以下 5 个指标：   * 优于委托价格的行情未成交委托单总量 * 次于委托价格的行情未成交委托单总量 * 等于委托价格的行情未成交委托单总量 * 等于委托价格且早于用户订单时间的行情未成交委托单总量 * 优于委托价格的行情档位数 |
| outputOrderConfirmation | 是否输出委托回报，默认为 true。 |
| outputRejectDetails | 是否输出用户订单、用户撤单被拒绝的具体原因。默认为 false。 |
| cpuId | 绑定到的 CPU 核的 ID，只在第一次接收到行情或者用户订单的时候绑定该线程 |
| userDefinedOrderId | 该参数为 true 时，insertMsg 的 orderId 为用户设置的外部订单号，订单明细表新增一列 userOrderId，为此订单号。默认为 false。 |
| orderByPrice | 银行间现券模式，选择撮合价格还是利率委托。该参数为 true 表示撮合价格，false 撮合到期收益率。 |
| outputOrderTradeFlag | 该参数为 true 时，输出订单是挂单成交或者主动成交（吃单）成交标志。默认为 false。 |
| immediateOrderConfirmation | 该参数为 true 时，立即返回委托回报。默认为 false。目前只支持银行间现券快照。 |
| immediateCancel | 该参数为 true 时，立即撤单。默认为 false。目前只支持银行间现券快照。 |
| tradeInLots | * 当 *tradeInLots*=true（默认值） 时，订单的最小委托或成交量为 10   万，并且成交量必须是 5 万的倍数。 * 当 *tradeInLots*=false 时，订单的最小委托或成交量为 1000   万，并且成交量必须是 1000 万的整数倍。   仅银行间现券快照支持该设置。 |
| outputSeqNum | outputSeqNum=true 时，订单明细表中新增 seqNum列，该列为从 1 到 N 的递增序列。 |

* dummyQuoteTable：插入行情数据的表的实际结构，对于一些引擎内部使用到的列，由参数 *quoteColMap*
  提供列名映射关系。
* quoteColMap：行情数据表的列名映射关系，一个字典标量，类型为(STRING, DOUBLE)。

其中，对于逐笔模式，行情表必须提供的列如下：

| 名称 | 类型 | 含义 |
| --- | --- | --- |
| symbol | SYMBOL | 股票标的 |
| symbolSource | SYMBOL | 证券市场：深交所、上交所 |
| timestamp | TIMESTAMP | 时间戳 |
| sourceType | INT | 0（order） ，1（transaction） |
| orderType | INT | order：   * 1：市价 * 2：限价 * 3：本方最优 * 10：撤单（仅上交所，即上交所撤单记录在 order 中）   transaction：   * 0：成交 * 1：撤单（仅深交所，即深交所撤单记录在 transaction 中） |
| price | DOUBLE | 订单价格 |
| qty | LONG | 订单数量 |
| buyNo | LONG | transaction 对应其原始数据；order 填充原始订单号，无意义，深交所数据为了补全上交所数据格式增加的冗余列 |
| sellNo | LONG | transaction 对应其原始数据；order 填充原始委托订单号，无意义，深交所数据为了补全上交所数据格式增加的冗余列 |
| direction | INT | 1（买 ），2（卖） |
| seqNum | LONG | 逐笔数据序号 |

对于快照模式，行情表必须提供的列如下：

注：

* 股票行情撮合模式二中必须提供 tradePrice（成交价格）和
  tradeQty（成交数量）列表字段，撮合模式一中可以不包含这两列。

* 期货期权和通用版本有 highPrice 和 lowPrice 两个字段。

| 名称 | 类型 | 含义 |
| --- | --- | --- |
| symbol | SYMBOL | 股票标的 |
| symbolSource | SYMBOL | 证券市场：深交所、上交所 |
| timestamp | TIMESTAMP | 时间戳 |
| lastPrice | DOUBLE | 最新价 |
| upLimitPrice | DOUBLE | 涨停板价 |
| downLimitPrice | DOUBLE | 跌停板价 |
| totalBidQty | LONG | 区间买单成交数量总和 |
| totalOfferQty | LONG | 区间卖单成交数量总和 |
| bidPrice | DOUBLE[] | 买单价格列表 |
| bidQty | LONG[] | 买单数量列表 |
| offerPrice | DOUBLE[] | 卖单价格列表 |
| offerQty | LONG[] | 卖单数量列表 |
| tradePrice | DOUBLE[] | 成交价格列表（撮合模式二时必须有） |
| tradeQty | LONG[] | 成交数量列表（撮合模式二时必须有） |
| highPrice | DOUBLE | 最高价（期货期权品种和通用版本带有的字段） |
| lowPrice | DOUBLE | 最低价（期货期权品种和通用版本带有的字段） |

对于银行间现券的快照模式，行情表必须提供的列如下：

| 名称 | 类型 | 含义 |
| --- | --- | --- |
| symbol | SYMBOL | 标的代码 |
| symbolSource | SYMBOL | 市场：  * 银行间 "CFETS" 的 X\_BOND * 上交所的 "CFFEX\_BOND" |
| timestamp | TIMESTAMP | 时间 |
| bidSettlType | INT[] | 买清算速度 |
| bidMDEntrySize | LONG[] | 报买量（元） |
| bidMDEntryPx | DOUBLE[] | 报买净价（元) |
| bidYield | DOUBLE[] | 报买到期 |
| bidParty | columnar tuple | 买报价方（上交所债券） |
| askSettlType | INT[] | 卖清算速度 |
| askMDEntrySize | LONG[] | 报卖量（元） |
| askMDEntryPx | DOUBLE[] | 报卖净价（元) |
| askYield | DOUBLE[] | 报卖到期 |
| askParty | columnar tuple | 卖报价方（上交所债券） |
| tradePrice | DOUBLE[] | 区间成交价格列表 |
| tradeQty | LONG[] | 区间成交数量列表 |
| settlType | INT[] | 清算速度 |
| yield | DOUBLE[] | 到期收益率 |

对于数字货币的快照模式，行情表必须提供的列如下：

| 名称 | 类型 | 含义 |
| --- | --- | --- |
| symbol | SYMBOL | 标的代码 |
| symbolSource | SYMBOL | 交易所： |
| timestamp | TIMESTAMP | 时间戳 |
| lastPrice | DECIMAL128 | 最新价 |
| upLimitPrice | DECIMAL128 | 涨停板价 |
| downLimitPrice | DECIMAL128 | 跌停板价 |
| totalBidQty | DECIMAL128 | 区间买单成交数量总和 |
| totalOfferQty | DECIMAL128 | 区间卖单成交数量总和 |
| bidPrice | DECIMAL128[] | 买单价格列表 |
| bidQty | DECIMAL128[] | 买单数量列表 |
| offerPrice | DECIMAL128[] | 卖单价格列表 |
| offerQty | DECIMAL128[] | 卖单数量列表 |
| highPrice | DECIMAL128 | 最高价 |
| lowPrice | DECIMAL128 | 最低价 |
| tradePrice | DECIMAL128[] | 区间成交价（快照模式二） |
| tradeQty | DECIMAL128[] | 区间成交量（快照模式二） |

注：

* 数字货币的分钟频、日频模式必须提供 symbolSource 字段，期货、股票类型的分钟频、日频模式可以不包含
  symbolSource 字段。
* 数字货币的价格和量的数据类型都为 DECIMAL128。

| 字段 | 类型 | 名称 |
| --- | --- | --- |
| symbol | SYMBOL | 标的代码 |
| symbolSource | SYMBOL | 证券市场 |
| tradeTime | TIMESTAMP | 时间 |
| open | DOUBLE | 开盘价 |
| low | DOUBLE | 最低价 |
| high | DOUBLE | 最高价 |
| close | DOUBLE | 收盘价 |
| volume | LONG | 成交量 |
| amount | DOUBLE | 成交额 |
| upLimitPrice | DOUBLE | 涨停价 |
| downLimitPrice | DOUBLE | 跌停价 |

* dummyUserOrderTable：插入用户订单数据的表的实际结构，对于一些引擎内部使用到的列，由参数
  *userOrderColMap* 提供列名映射关系。
* userOrderColMap：用户订单表的列名映射关系，一个字典标量，类型为(STRING, DOUBLE)。

  + 股票，用户订单表必须提供的列如下：

| 名称 | 类型 | 含义 |
| --- | --- | --- |
| symbol | STRING | 股票标的。取消订单时股票标的无效，以 orderId 为准。 |
| symbolSource | SYMBOL | 证券市场 |
| timestamp | TIMESTAMP | 时间戳 |
| orderType | INT | 上交所：   * 0：市价单中最优五档即时成交剩余撤销委托订单 * 1：市价单中最优五档即时成交剩余转限价委托订单 * 2：市价单中本方最优价格委托订单 * 3：市价单中对手方最优价格委托订单 * 5：限价单 * 6：撤单 * 7：市价单中最优五档即时成交剩余撤销委托订单（保护限价） * 8：市价单中最优五档即时成交剩余转限价委托订单（保护限价） * 9：市价单中本方最优价格委托订单（保护限价） * 10：市价单中对手方最优价格委托订单（保护限价）   深交所：   * 0：市价单中最优五档即时成交剩余撤销委托订单 * 1：市价单中即时成交剩余撤销委托订单 * 2：市价单中本方最优价格委托订单 * 3：市价单中对手方最优价格委托订单 * 4：市价单中全额成交或撤销委托订单 * 5：限价单 * 6：撤单   分钟频率、日频模式：   * 0：市价单 * 5：限价单 * 6：撤单 |
| price | DOUBLE | 订单委托价格 |
| orderQty | LONG | 委托数量 |
| direction | INT | 1（买 ），2（卖） |
| orderId | LONG | 用户订单 ID，仅撤单时起作用 |

* 期货期权，用户订单表必须提供的列如下：

| 名称 | 类型 | 含义 |
| --- | --- | --- |
| symbol | SYMBOL | 期货标的 |
| symbolSource | SYMBOL | 交易所代码 |
| timestamp | TIMESTAMP | 时间 |
| orderType | INT | 订单类型：默认 5 表示限价单  5：限价单  6：撤单  0：市价单，以涨跌停价委托，并遵循时间优先原则  1：市价止损单  　　市价止损单是指某标的市场价格一旦达到委托设定的价格水平时即转变为市价单。市价止损单既可以是平仓单，也可以是开仓单  2：市价止盈单  市价止盈单是指某标的市场价格一旦达到委托设定的价格水平时即转变为市价单。市价止盈单既可以是平仓单，也可以是开仓单  3：限价止损单  限价止损单是指委托订单指定某合约成交的价格波动区间。价格一旦触发后即转变为价格波动区间极值的限价单。限价止损单既可以是平仓单，也可以是开仓单。  4：限价止盈单  限价止盈单是指委托订单指定某合约成交的价格波动区间。价格一旦触发后即转变为价格波动区间极值的限价单。限价止盈单既可以是平仓单，也可以是开仓单。 |
| price | DOUBLE | 委托订单价格 |
| stopPrice | DOUBLE | 止损价/止盈价 |
| orderQty | LONG | 委托订单数量 |
| direction | INT | 买卖方向：1：买开；2：卖开；3：卖平；4：买平 |
| timeInForce | INT | 委托订单有效性：  0：当日有效（默认）  1：立即全部成交否则自动撤销（FOK）  2：立即成交剩余自动撤销（FAK） |
| orderId | LONG | 用户订单ID，仅撤单时起作用 |

* 数字货币，用户订单表必须提供如下列：

| 名称 | 类型 | 含义 |
| --- | --- | --- |
| symbol | SYMBOL | 标的代码 |
| symbolSource | SYMBOL | 交易所代码 |
| timestamp | TIMESTAMP | 时间 |
| orderType | INT | 分钟频率、日频模式：  0：市价单  5：限价单  6：撤单 |
| price | DECIMAL128 | 委托订单价格 |
| stopPrice | DECIMAL128 | 止损价/止盈价 |
| orderQty | DECIMAL128 | 委托订单数量 |
| direction | INT | 买卖方向：1：买开；2卖开；3：卖平；4：买平 |
| orderId | LONG | 用户订单 ID，仅撤单时起作用 |

* 银行间现券，用户订单表必须提供如下列：

| 名称 | 类型 | 含义 |
| --- | --- | --- |
| symbol | SYMBOL | 标的 |
| time | TIMESTAMP | 时间 |
| orderType | INT | 1：限价单：限单价是投资者设定的买入或卖出价格。  2：双边报价：同时提供买入价和卖出价的报价方式。  3: 市转撤：将市价单转换为撤单。  4：市转限：将市价单转换为限价单。  5：弹性：允许投资者根据市场变化调整订单参数。  6：撤单：主动取消已提交的订单。  7：FAK：按用户指定的价格立即撮合，不能成交的部分马上撤单  8：FOK：按用户指定的价格立即完全成交撮合，不能完全成交就撤单 |
| settlType | INT | 清算速度 |
| bidYield | DOUBLE | 委托买单到期收益率 |
| bidPrice | DOUBLE | 委托买单订单价格 |
| bidQty | LONG | 委托买订单数量 |
| askYield | DOUBLE | 委托卖单到期收益率 |
| askPrice | DOUBLE | 委托卖单订单价格 |
| askQty | LONG | 委托卖订单数量 |
| direction | INT | 1（买）， 2（卖），3（双边报价） |
| orderID | LONG | 用户订单 ID，仅撤单时起作用 |
| channel | STRING | 撮合渠道：目前支持 X-BOND，也可以 “ESP” |

* orderDetailsAndSnapshotOutput：复合输出表，包含订单簿及用户订单成交委托详细情况表。需要调用
  `extractInfo` 接口（详见后文该接口说明）来解析出具体数据。

| 名称 | 类型 | 含义 |
| --- | --- | --- |
| msgType | INT | 1（成交结果）或 2（订单簿） |
| content | BLOB | 具体数据 |

* orderDetailsOutput：订单详情结果输出表(包括用户订单委托回报，成交、拒单以及撤单状态)。

  + 在配置项 *outputRejectDetails* 为 true 时（详见本接口的 *config*
    参数说明），启用 outputRejectDetails 列。
  + 在配置项 *outputQueuePosition* 为 1 时（同上），启用
    openVolumeWithBetterPrice, openVolumeWithWorsePrice,
    openVolumeAtOrderPrice, priorOpenVolumeAtOrderPrice 和
    depthWithBetterPrice 五列。
  + 在配置项 *outputTimeInfo 为* 1 时（同上），启用 receiveTime,
    startMatchTime, endMatchTime 列。

| 名称 | 类型 | 含义 |
| --- | --- | --- |
| orderId | LONG | 成交的用户订单 ID |
| symbol | STRING | 股票标的 |
| direction | INT | 1（买 ），2（卖） |
| sendTime | TIMESTAMP | 订单发送时间 |
| orderPrice | DOUBLE | 委托价格 |
| orderQty | LONG | 订单委托数量 |
| tradeTime | TIMESTAMP | 成交时间 |
| tradePrice | DOUBLE | 成交价格 |
| tradeQty | LONG | 成交量 |
| orderStatus | INT | 用户订单是否完全成交   * 4：已报 * -2：表示撤单被拒绝 * -1：表示订单被拒绝 * 0：表示订单部分成交 * 1：表示订单完全成交 * 2：表示订单被撤单 |
| sysReceiveTime | NANOTIMESTAMP | 订单收到时的时间（系统时间） |
| yield | DOUBLE | 到期收益率（银行间现券） |
| quoteParty | STRING | 报价方（上交所债券） |
| userOrderId | LONG | 用户指定的订单号 |
| rejectDetails | STRING | 用户订单、用户撤单的具体拒单原因 |
| openVolumeWithBetterPrice | LONG | 优于委托价格的行情未成交委托单总量 |
| openVolumeWithWorsePrice | LONG | 次于委托价格的行情未成交委托单总量 |
| openVolumeAtOrderPrice | LONG | 等于委托价格行情未成交委托单总量 |
| priorOpenVolumeAtOrderPrice | LONG | 等于委托价格行情且比自己早的行情未成交委托单总量 |
| depthWithBetterPrice | INT | 优于委托价格的行情档位数 |
| orderTradeFlag | INT | 委托回报：0  挂单撮合：1  即时撮合成交：2  撤单等其它状态：3 |
| seqNum | LONG | 序号列（ 从 1 到 N）。仅当 *config* 中指定 outputSeqNum=true 时才显示该列。 |
| receiveTime | TIMESTAMP | 订单收到时的行情最新时间 |
| startMatchTime | NANOTIMESTAMP | 匹配开始时间 |
| endMatchTime | NANOTIMESTAMP | 匹配完成时间 |

注：

订单状态 orderStatus 为 -1 即订单被拒绝的场景：

1. 委托的用户订单不在交易所交易时间内。
2. 股票行情（逐笔/快照/分钟/日频）中委托的数量不符合要求，例如：volume <0；买单的 volume 不是100
   的倍数；科创版“68”的限价单小于 200 股或超过 10 万股；科创版“68”的市价单小于 200 股或超过 5
   万股；上交“11”或深交”12”的 volume 不是 10 的倍数。
3. 上交所债券中，买单用户订单的委托数量不是 100 的倍数。
4. 银行间现券中，用户订单的委托数量少于 10 万，用户订单的委托数量不是 5 万的倍数。
5. 用户订单的价格大于涨停价或者小于跌停价。
6. 在 dataType=5 时，行情的价格必须低于涨停价和高于跌停价。
7. 在 dataType=0 和 dataType =1 时，用户订单开始处理时，没有时间早于用户订单的行情。
8. 在 dataType=4 时，插入市价的用户订单前没有行情。
9. 在 dataType=0 和 dataType=1 时，市价用户订单在 9:15-9:25 或 14:57 以后。

订单状态 orderStatus 为 -2 即撤单被拒绝的场景：

1. 撤单时，撤单时间早于或等于用户订单时间。
2. 回撤了一个不存在的订单或者是已经完全交易的订单。
3. 用户撤单发生在 9:20-9:25、14:57-15:00。

* snapshotOutput：行情快照输出表。

| 名称 | 类型 | 含义 |
| --- | --- | --- |
| symbol | STRING | 股票标的 |
| timestamp | TIMESTAMP | 时间 |
| avgBidPrice | DOUBLE | 买单成交均价 |
| avgOfferPrice | DOUBLE | 卖单成交均价 |
| totalBidQty | LONG | 买单成交数量总和 |
| totalOfferQty | LONG | 卖单成交数量总和 |
| bidPrice | DOUBLE[] | 买单价格列表 |
| bidQty | LONG[] | 买单数量列表 |
| offerPrice | DOUBLE[] | 卖单价格列表 |
| offerQty | LONG[] | 卖单数量列表 |
| lastPrice | DOUBLE | 最新价 |
| highPrice | DOUBLE | 最高价 |
| lowPrice | DOUBLE | 最低价 |

### getOpenOrders

**语法**

```
MatchingEngineSimulator::getOpenOrders(engine, [symbolList]);
```

**详情**

获取未成交的用户订单信息。

**参数**

* engine：通过 `createMatchEngine` 接口创建的撮合引擎。
* symbolList：可选参数，股票标的列表，表示获取所有的未成交订单。

**返回值**

返回一个表。包含如下列：

注： 仅当 *outputQueuePosition*=1 时，包含
openVolumeWithBetterPrice, openVolumeWithWorsePrice, openVolumeAtOrderPrice,
priorOpenVolumeAtOrderPrice, depthWithBetterPrice，updateTime 五列。（详见
`createMatchEngine` 接口的 *config* 参数说明）

| 名称 | 类型 | 含义 |
| --- | --- | --- |
| orderId | LONG | 订单 ID |
| timestamp | TIMESTAMP | 时间 |
| symbol | STRING | 股票标的 |
| price | DOUBLE | 委托价格 |
| totalQty | LONG | 用户订单数量 |
| openQty | LONG | 用户订单余量 |
| direction | INT | 1（买 ），2（卖） |
| isMacthing | INT | 订单是否到达撮合时间 |
| openVolumeWithBetterPrice | LONG | 优于委托价格的行情未成交委托单总量 |
| openVolumeWithWorsePrice | LONG | 次于委托价格的行情未成交委托单总量 |
| openVolumeAtOrderPrice | LONG | 等于委托价格行情未成交委托单总量 |
| priorOpenVolumeAtOrderPrice | LONG | 等于委托价格行情且比自己早的行情未成交委托单总量 |
| depthWithBetterPrice | INT | 优于委托价格的行情档位数 |
| updateTime | TIMESTAMP | 最新更新时间 |

### resetMatchEngine

**语法**

```
MatchingEngineSimulator::resetMatchEngine(engine, [cancelOrder])
```

**详情**

清空内部缓存的所有订单信息以及行情信息。

**参数**

* engine：通过 `createMatchEngine` 接口创建的撮合引擎。

* cancelOrder：可选参数，布尔类型，表示是否撤销所有撤销所有的用户订单，并将订单信息输出到
  orderDetailsOutput。默认为 false，表示不撤销。

**返回值**

无。

### getEngineList

**语法**

```
MatchingEngineSimulator::getEngineList()
```

**详情**

获取所有的 engine。

**返回值**

返回一个 engine 列表。类型为字典，key 为 ID，value 为 engine 对象。

**示例**

```
engines = MatchingEngineSimulator::getEngineList()
for(tag in engines.keys()){
    MatchingEngineSimulator::dropMatchEngine(engines[tag])
}
```

### getSymbolList

**语法**

```
MatchingEngineSimulator::getSymbolList(engine)
```

**参数**

* engine：通过 `createMatchEngine` 接口创建的撮合引擎。

**详情**

获取某引擎中当前存在的股票 symbol 列表。

**返回值**

返回一个
STRING 类型的向量，包含当前存在的股票标的。

### dropMatchEngine

**语法**

```
MatchingEngineSimulator::dropMatchEngine(engine);
```

**详情**

停止模拟撮合引擎。

**参数**

* engine：通过 `createMatchEngine` 接口创建的撮合引擎。

**返回值**

无。

### stopMatchEngine

**语法**

```
MatchingEngineSimulator::stopMatchEngine(engine, symbolList)
```

**详情**

停止模拟撮合引擎。

**参数**

* engine：通过 `createMatchEngine` 接口创建的撮合引擎。
* symbolList：可选参数，字符串标量，表示需要停止模拟的股票。若不填，则停止所有股票模拟。

**返回值**

无。

### extractInfo

**语法**

```
MatchingEngineSimulator::extractInfo(msgType, msg, [table])
```

**详情**

解析 orderDetailsAndSnapshotOutput 表中的内容。（详见 `createMatchEngine`
接口的 *orderDetailsAndSnapshotOutput* 参数说明）

**参数**

* msgType：1 表示订单状态详情表，2 表示订单簿。
* msg：待解析的 BLOB 类型的数据。
* table：与 orderDetailsAndSnapshotOutput 相同结构的表。

**返回值**

* 如果指定 table，则将解析结果 append 到 table 的末尾中，并返回 true。
* 如果未指定 table，则返回解析结果。

### insertMsg

**语法**

```
MatchingEngineSimulator::insertMsg(engine, msgBody, msgType)
```

**详情**

插入行情和用户订单数据。

**参数**

* engine：通过 `createMatchEngine` 接口创建的撮合引擎。
* msgBody：行情或用户订单数据。
* msgType：数据类型。1 表示行情，2 表示用户订单。

**返回值**

* 如果插入的是行情数据，返回 Void。
* 如果插入的是用户订单数据，返回用户的订单 ID（LONG 类型的向量）。

### setLimitPrice

**语法**

```
MatchingEngineSimulator::setLimitPrice(engine, data)
```

**详情**

设置模拟撮合引擎的涨停价和跌停价。

注： 价格超过涨停价和跌停价范围内的用户订单都会被拒绝。如果 upLimitPrice 为
0，表示涨停价没有限制。

**参数**

* engine：通过 `createMatchEngine` 接口创建的撮合引擎。
* data：一个表。包含 3 列(symbol, upLimitPrice, downLimitPrice)，分别是
  STRING，DOUBLE，DOUBLE 类型。

**返回值**

如果设置成功，返回 true。

### setPrevClose

**语法**

```
MatchingEngineSimulator::setPrevClose(engine, prevClose);
```

**详情**

设置模拟撮合引擎的前收盘价。

注： 深交所的逐笔模式且有创业版的股票时，必须设置前收盘价。

**参数**

* engine：通过 `createMatchEngine` 接口创建的撮合引擎。
* prevClose：一个字典。键值类型为 STRING-DOUBLE。字典的 key 为股票号，value 为对应股票的前收盘价。

**返回值**

如果设置成功，返回 true。

### getSnapshot

**语法**

```
MatchingEngineSimulator::getSnapshot(engine, symbolList);
```

**详情**

获取逐笔引擎中的行情快照信息。

**参数**

* engine：是通过 `createMatchEngine` 接口创建的逐笔撮合引擎。
* symbolList： 股票标的，字符串向量。如果没有填该参数，表示获取所有股票标的快照。

**返回值**

返回一个表 ，结构如下：

| 名称 | 类型 | 含义 |
| --- | --- | --- |
| symbol | STRING | 股票标的 |
| timestamp | TIMESTAMP | 时间 |
| avgTradePriceAtBid | DOUBLE | 买单成交均价 |
| avgTradePriceAtOffer | DOUBLE | 卖单成交均价 |
| totalTradeQtyAtBid | LONG | 买单成交数量总和 |
| totalTradeQtyAtOffer | LONG | 卖单成交数量总和 |
| bidPrice | DOUBLE[] | 买单价格列表 |
| bidQty | LONG[] | 买单数量列表 |
| offerPrice | DOUBLE[] | 卖单价格列表 |
| offerQty | LONG[] | 卖单数量列表 |
| lastPrice | DOUBLE | 最新价 |
| highPrice | DOUBLE | 最高价 |
| lowPrice | DOUBLE | 最低价 |

## 例子

### 例 1：通过自定义函数指定模拟撮合需要的参数

```
login("admin", "123456") //登录
loadPlugin("MatchingEngineSimulator") //加载插件
go

//用户订单
MARKET_OTHER_BEST = 3
MARKET_THIS_BEST = 2
MARKET_BEST_FIVE = 0
MARKET_INSTANT_DEAL = 1
MARKET_ALL_DEAL = 4
LIMIT_ORDER = 5
ORDER_CANCEL = 6

def initArgsSnapshotmode2(){

    dummyQuoteTable = table(1:0, `symbol`symbolSource`timestamp`lastPrice`highestPrice2`lowestPrice2`highestPrice`lowestPrice`openPrice`preClosePrice`upLimitPrice`downLimitPrice`avgBidPrice`avgOfferPrice`totalBidQty`totalOfferQty`bidPrice`bidQty`offerPrice`offerQty`tradePrice`tradeQty, [STRING, STRING, TIMESTAMP,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE, DOUBLE, LONG, LONG, DOUBLE[], LONG[], DOUBLE[], LONG[],DOUBLE[],LONG[]])
    quoteColMap = dict( `symbol`symbolSource`timestamp`lastPrice`highestPrice`lowestPrice`highestPrice2`lowestPrice2`openPrice`preClosePrice`upLimitPrice`downLimitPrice`avgBidPrice`avgOfferPrice`totalBidQty`totalOfferQty`bidPrice`bidQty`offerPrice`offerQty`tradePrice`tradeQty, `symbol`symbolSource`timestamp`lastPrice`highestPrice`lowestPrice`highestPrice2`lowestPrice2`openPrice`preClosePrice`upLimitPrice`downLimitPrice`avgBidPrice`avgOfferPrice`totalBidQty`totalOfferQty`bidPrice`bidQty`offerPrice`offerQty`tradePrice`tradeQty)
    dummyUserOrderTable = table(1:0, `symbol`timestamp`orderType`price`orderQty`direction`orderId, [STRING, TIMESTAMP, INT, DOUBLE, LONG, INT, LONG])
    userOrderColMap = dict( `symbol`timestamp`orderType`price`orderQty`direction`orderId, `symbol`timestamp`orderType`price`orderQty`direction`orderId)
    orderDetailsOutput  = table(1:0, `orderId`symbol`direction`sendTime`orderPrice`orderQty`tradeTime`tradePrice`tradeQty`orderStatus`sysReceiveTime, [LONG, STRING, INT,TIMESTAMP,DOUBLE,LONG, TIMESTAMP,DOUBLE,LONG, INT,NANOTIMESTAMP])
    orderDetailsAndSnapshotOutput = table(1:0, `msgType`content, [INT, BLOB])
    snapshotOutput  = table(1:0, `symbol`timestamp`avgBidPrice`avgOfferPrice`totalBidQty`totalOfferQty`bidPrice`bidQty`offerPrice`offerQty`lastPrice`highPrice`lowPrice, [STRING, TIMESTAMP,DOUBLE,DOUBLE, LONG, LONG,DOUBLE[],LONG[], DOUBLE[], LONG[],DOUBLE,DOUBLE,DOUBLE])
    return [dummyQuoteTable,quoteColMap,dummyUserOrderTable,userOrderColMap,orderDetailsOutput,orderDetailsAndSnapshotOutput,snapshotOutput]
}
```

在上述代码中，

1. 登录 DolphinDB 客户端(`login("admin", "123456")`)并使用
   `loadPlugin` 载入模拟撮合引擎插件。
2. 在 `go` 语句后指定用户订单。

定义了 `initArgsSnapshotmode2` 函数，并为各个命名函数指定需要执行的语句。

`initArgsSnapshotmode2` 返回一个包含多个表格和字典的列表，其中：

* `dummyQuoteTable`：报价表。
* `quoteColMap`：字典，用于映射报价表中的列名。
* `dummyUserOrderTable`：用户订单表。
* `userOrderColMap`：字典，用于映射用户订单表中的列名。
* `orderDetailsOutput`、`snapshotOutput`、`orderDetailsAndSnapshotOutput`
  分别代表了交易输出、快照输出、复合输出表。

### 例 2：快照模式下以模式二模拟撮合委托订单

下例展示了在快照模式下以模式二（`matchingMode = 2`，详见
`createMatchEngine` 接口的 *config*
参数说明）模拟撮合证券交易市场委托订单的关键过程。

```
config = dict(STRING, DOUBLE); //定义了一个包含多个配置参数的字典
config["latency"] = 0; //模拟时延
config["orderBookMatchingRatio"] = 0.12; //成交百分比
config["dataType"] = 1; // 行情类别为快照
config["outputOrderBook"] = 1; //是否输出订单，此处1表示输出
config["depth"] = 6; //匹配的订单簿的深度，区间为5到50，此处为6
config["matchingMode"] = 2; //快照模式下的匹配模式，此处为按照模式二撮合订单

name = "engine_snapshot" //指定引擎名称
exchange = "XSHE" //指定交易所名称
symbol = "AAA123" //指定证券代码

try{dropStreamEngine(name)}catch(ex){}
args = initArgsSnapshotmode2()
engine = MatchingEngineSimulator::createMatchEngine(name, exchange, config, args[0], args[1], args[2], args[3], args[4], args[5], args[6])
MatchingEngineSimulator::resetMatchEngine(engine)
appendMsg(engine, (symbol, "XSHE", 2021.01.08 10:14:01.400,23.5,,,25.0,23.0,,,,, 23.51, 23.59, 100, 100, [23.45  23.4  23.3  23.2  23.1  23.0],  [1000 1000 1000 1000 1000 1000], [23.72  23.78  23.8  23.9  24.0 24.1], [1000 1000 1000 1000 1000 1000],[23.441 23.1235 23.653 23.771],[100 100 100 100]), 1)
appendMsg(engine, (symbol, 2021.01.08 10:14:01.400, MARKET_THIS_BEST, 23.2, 200, ORDER_SEL, 1), 2)   // 23.72
appendMsg(engine, (symbol, 2021.01.08 10:14:01.400, MARKET_THIS_BEST, 23.3, 400, ORDER_SEL, 2), 2)  // 272
res = MatchingEngineSimulator::getOpenOrders(engine)
ex = table([1,2] as orderId, [2021.01.08 10:14:01.400,2021.01.08 10:14:01.400] as timestamp, ["AAA123","AAA123"] as symbol, [23.72,23.72] as price, [200,400] as totalQty, [200,400] as openQty, [2,2] as BsFlag,  [true, true] as isMatching)
assert 1, each(eqObj, res.values(), ex.values())
appendMsg(engine, (symbol, 2021.01.08 10:14:01.450, LIMIT_ORDER, 23.68, 400, ORDER_SEL, 2), 2)  // 23.68
appendMsg(engine, (symbol, "XSHE", 2021.01.08 10:14:01.500,24.3,,,25.0,23.0,,,,, 23.51, 23.59, 1000, 1000, [23.45  23.4  23.3  23.2  23.1  23.0],  [1000 1000 1000 1000 1000 1000], [23.72  23.78  23.8  23.9  24.0 24.1], [1000 1000 1000 1000 1000 1000],[23.65 23.81 23.73 23.72 23.45],[100 100 100 200 100]), 1)
appendMsg(engine, (symbol, "XSHE", 2021.01.08 10:14:01.600,24.3,,,25.0,23.0,,,,, 23.51, 23.59, 1000, 1000, [23.45  23.4  23.3  23.2  23.1  23.0],  [1000 1000 1000 1000 1000 1000], [23.67  23.78  23.8  23.9  24.0 24.1], [1000 1000 1000 1000 1000 1000],[23.72 0],[1200 0]), 1)
res = select orderId, symbol, direction, sendTime, orderPrice, orderQty, tradeTime, tradePrice, tradeQty, orderStatus, sysReceiveTime from args[4]
```

在上述代码中，

* 定义了一个名为 `config`
  的字典，它包含了一些配置参数，如模拟时延、成交百分比、行情类别、是否输出订单、订单簿深度等。
* 指定了引擎名称、交易所名称和证券代码。
* 还定义了一些函数，如 `appendMsg` 和
  `getOpenOrders`，用于向引擎中添加消息和获取当前未完成的订单。
* 使用 `assert` 函数来验证结果是否符合预期。

其中，函数 `dropStreamEngine` 用于释放已创建的流数据引擎的定义，例如上述例子中的
`name = "engine_snapshot"`。

## 参考

[命名函数](../../progr/named_func.html)

[模拟撮合教程](../../tutorials/matching_engine_simulator.html)

