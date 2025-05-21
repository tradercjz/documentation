# 多账户

回测平台支持多账户回测，目前支持的资产包括股票、期权、期货。

## 引擎配置说明

接口 createBacktester 的参数 *config* 和接口 createBacktestEngine 的参数 *userConfig*
的配置可参考下表：

| **key** | **说明** | **备注** |
| --- | --- | --- |
| "startDate" | 开始日期 | 必须配置，DATE 类型 例如 “2020.01.01” |
| "endDate" | 结束日期 | 必须配置，DATE 类型 例如 “2020.01.01” |
| "strategyGroup" | 策略类型 | 必须配置，"multiAsset" |
| "cash" | 初始资金 | 必须配置，字典，key 为账户类型，例如： {  “stock”：100000.，  “futures“:100000.，  “option“:100000.  } |
| “commission” | 股票等现货的手续费 | DOUBLE 类型，默认为 0.0 |
| “tax” | 股票等现货的印花税 | DOUBLE 类型，默认为 0.0 |
| “frequency” | 将快照行情合成 frequency 频率的行情触发 onBar | INT 类型，默认为0 |
| ”callbackForSnapshot“ | 快照行情触发回调模式 | INT 类型，默认为 0 ，可选值为：  0：表示只回调onSnapshot，  1 ：表示既回调onSnpshot 又回调 onbar，  2 ：表示只回调 onbar |
| "dataType" | 行情类型： 1：快照  3: 分钟频率  4：日频 | frequency>0 and dataType=1或者 2 时，行情为快照，引擎内部合成 frequency 频率的快照行情触发 onBar |
| “matchingMode“ | 订单撮合模式 | 日频：模式一，以收盘价撮合订单；模式二，以开盘价撮合订单。 分钟频率：模式一，行情时间大于订单时间时撮合订单；模式二，行情时间等于订单时间时以当前行情的收盘价撮合订单，后续未完成订单撮合订单同模式一 |
| “benchmark” | 基准标的 | STRING 或 SYMBOL 类型 |
| "latency" | 订单延时 | INT 类型，单位为毫秒，用来模拟用户订单从发出到开始进行撮合的时延 |
| “orderBookMatchingRatio” | 与行情订单薄的成交百分比 | DOUBLE 类型，默认 1.0，取值 0~1.0 之间 |
| “matchingRatio” | 区间撮合比例 | DOUBLE 类型，默认 1.0，取值 0~1.0 之间。默认和成交百分比 orderBookMatchingRatio 相等 |
| “maintainanceMargin” | 维保比例 | FLOAT 类型，资产为融资融券时是数组，三个元素分别为警戒线、追保线、最低线；为期货时是标量。 |
| “outputQueuePosition” | 是否需要获取订单在行情中的位置  如果输出该信息，则在成交明细和未成交订单接口中会增加以下 5 个指标：   * 优于委托价格的行情未成交委托单总量 * 次于委托价格的行情未成交委托单总量 * 等于委托价格的行情未成交委托单总量 * 等于委托价格且早于用户订单时间的行情未成交委托单总量 * 优于委托价格的行情档位数 | dataType = 0 、5、6 且enableSubscriptionToTickQuotes = true 时仅有。 INT 类型，可选值为：  0：默认值，表示不输出  1：表示订单撮合成交计算上述指标的时候，把最新的一条行情纳入订单薄  2：表示订单撮合成交计算上述指标的时候，把最新的一条行情不纳入订单薄，即统计的是撮合计算前的位置信息 |
| stockDividend | 分红除权基本信息表 | TABLE 类型，字段说明见下文 |

红除权基本信息表说明如下：

| 字段 | 名称 |
| --- | --- |
| symbol | 股票代码 |
| endDate | 分红年度 |
| annDate | 预案公告日 |
| recordDate | 股权登记日 |
| exDate | 除权除息日 |
| payDate | 派息日 |
| divListDate | 红股上市日 |
| bonusRatio | 每股送股比例 |
| capitalConversion | 每股转增比例 |
| afterTaxCashDiv | 每股分红（税后） |
| allotPrice | 配股价格 |
| allotRatio | 每股配股比例 |

## 基本信息表

接口 createBacktester 和 createBacktestEngine 的参数 *securityReference*
的基本信息表字段可参考下表：

| **列名** | **类型** | **说明** |
| --- | --- | --- |
| symbol | SYMBOL 或 STRING | 品种代码 |
| contractType | INT | 品种类型 0：股票  1：期货  2：商品期权  3：股指期权  4：ETF 期权 |
| underlyingCode | STRING | 标的代码 |
| optType | INT | 期权类型 1：看涨（call）  2：看跌（put） |
| strikePrice | DOUBLE | 行权价 |
| multiplier | DOUBLE | 合约乘数 |
| marginRatio | DOUBLE | 保证金比例 |
| tradeUnit | DOUBLE | 合约单位 |
| priceUnit | DOUBLE | 报价单位 |
| priceTick | DOUBLE | 价格最小变动单位 |
| commission | DOUBLE | 手续费 |
| deliveryCommissionMode | INT | 1：commission/手 2：成交额\*commission |
| lastTradingDay | DATE | 合约最后交易日 |
| exerciseDate | DATE | 期权行权日 |
| exerciseSettlementDate | DATE | 行权交收日 |
| underlyingCode | STRING | 标的代码，配置此项后才允许提交期权行权订单。 |

## 行情

### 快照行情

通过接口 appendQuotationMsg 向引擎中插入数据时，*msg* 结构必需包含的字段如下：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 标的代码 上交所以 ".XSHG" 结尾  深交所以 ".XSHE" 结尾 |
| symbolSource | STRING | "XSHG"（上交所）或者 "XSHE"（深交所） |
| timestamp | TIMESTAMP | 时间戳 |
| tradingDay | DATE | 交易日/结算日期 |
| lastPrice | DOUBLE | 最新成交价 |
| upLimitPrice | DOUBLE | 涨停价 |
| downLimitPrice | DOUBLE | 跌停价 |
| totalBidQty | LONG | 区间买量 |
| totalOfferQty | LONG | 区间卖量 |
| bidPrice | DOUBLE[] | 委买价格列表 |
| bidQty | LONG[] | 委买量列表 |
| offerPrice | DOUBLE[] | 委卖价格列表 |
| offerQty | LONG[] | 委卖量列表 |
| highPrice | DOUBLE | 最高价 |
| lowPrice | DOUBLE | 最低价 |
| underlyingPrice | DOUBLE | 标的价格（仅对期权品种必需） |
| contractType | INT | 品种类型： 0：股票  1：期货  2：商品期权  3：股指期权  4：ETF 期权 |

建表语句如下：

```
colName=["symbol","symbolSource","timestamp","tradingDay","lastPrice","upLimitPrice",
        "downLimitPrice","totalBidQty","totalOfferQty","bidPrice","bidQty","offerPrice",
        "offerQty","highPrice","lowPrice"，"contractType"]
colType= ["STRING","STRING","TIMESTAMP","DATE","DOUBLE","DOUBLE","DOUBLE","DOUBLE","DOUBLE",
        "DOUBLE[]","LONG[]","DOUBLE[]","LONG[]","DOUBLE","DOUBLE", "INT"]
messageTable=table(10000000:0, colName, colType)
```

字段名须严格与表中一致，字段顺序除首列必须为 symbol 列外，无其它要求，此外还支持 INT，DOUBLE，STRING 类型的列，或名为 signal 的
DOUBLE ARRAY VECTOR 类型的列作为扩展字段。

### 分钟频率或日频行情

通过接口 appendQuotationMsg 向引擎中插入数据时，*msg* 结构必需包含的字段如下：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 标的代码 |
| symbolSource | STRING | "XSHG"（上交所）或者 "XSHE"（深交所） |
| tradeTime | TIMESTAMP | 时间戳 |
| tradingDay | DATE | 交易日/结算日期 |
| lastPrice | DOUBLE | 最新成交价 |
| upLimitPrice | DOUBLE | 涨停价 |
| downLimitPrice | DOUBLE | 跌停价 |
| totalBidQty | LONG | 区间成交买数量 |
| totalOfferQty | LONG | 区间成交卖数量 |
| bidPrice | DOUBLE[] | 委托买价 |
| bidQty | LONG[] | 委托买量 |
| offerPrice | DOUBLE[] | 委托卖价 |
| offerQty | LONG[] | 委托卖价 |
| highPrice | DOUBLE | 最高价 |
| lowPrice | DOUBLE | 最低价 |
| contractType | INT | 品种类型： 0：股票  1：期货  2：商品期权  3：股指期权  4：ETF 期权 |

建表语句如下：

```
colName=[`symbol,`symbolSource,`tradeTime,`tradingDay,`open,`low,`high,`close,`volume,`amount,`upLimitPrice,
        `downLimitPrice,`contractType]
colType=[SYMBOL,SYMBOL,TIMESTAMP,DATE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,LONG,
DOUBLE,DOUBLE,INT]
messageTable=table(10000000:0, colName, colType)
```

字段名须严格与表中一致，字段顺序除首列必须为 symbol 列外，无其它要求，此外还支持 INT，DOUBLE，STRING 类型的列，或名为 signal 的
DOUBLE ARRAY VECTOR 类型的列作为扩展字段。

