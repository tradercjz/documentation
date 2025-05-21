# 债券

回测平台支持债券资产，包括银行间债券和上交所债券。

## 银行间债券

### 引擎配置说明

接口 `createBacktester` 的参数 *config* 和接口
`createBacktestEngine` 的参数 *userConfig* 的配置可参考下表：

| **key** | **说明** | **备注** |
| --- | --- | --- |
| "startDate" | 开始日期 | 必须配置，DATE 类型 例如 “2020.01.01” |
| "endDate" | 结束日期 | 必须配置，DATE 类型 例如 “2020.01.01” |
| "strategyGroup" | 策略类型 | 必须配置，“CFETSBond” |
| "cash" | 初始资金 | 必须配置，DOUBLE 类型 |
| "dataType" | 行情类型 | 必须配置，INT 类型，可选值为： 2：快照+逐笔成交明细 |
| “matchingMode“ | 订单撮合模式 | INT 类型，默认按模拟撮合引擎撮合订单。若设置为 3 ，则以委托价格成交，设置为 1 或 2 时无效 |
| "msgAsTable" | 行情的数据格式 | BOOL 类型，默认为 false false：字典  true：表（只能通过接口createBacktestEngine 创建引擎） |
| “benchmark” | 基准标的 | 如”000300.XSHG“ 。在接口`getReturnSummary` 中使用 |
| "latency" | 订单延时 | 单位为毫秒，用来模拟用户订单从发出到被处理的时延 |
| “enableIndicatorOptimize” | 是否开启指标优化 | BOOL 类型，默认为 false true：开启  false：不开启 |
| ”addTimeColumnInIndicator“ | 指标订阅时是否给指标数表增加时间列 | BOOL 类型，默认为 false true：增加  false：不增加 |
| “isBacktestMode“ | 是否为回测模式 | BOOL 类型，默认为 true true：回测模式  false：模拟交易模式 |
| dataRetentionWindow | 开始指标优化时数据保留的窗口 | STRING 类型或 INT 类型。 当 enableIndicatorOptimize = true 时，该参数生效。  * isBacktestMode = true 时，默认 “None” ，可设置为：    + “ALL“：全部数据保留   + “20d”：支持按天保留数据，即交易日天数，如 “20d” 代表 20 个交易日   + “None”：不保留数据   + 20：支持按条数保留数据，如 20 代表每个 symbol 保留最新的 20 条 * isBacktestMode = false 时，无需设置 |
| "context" | 策略逻辑上下文类结构 | DICT 类型，策略全局变量构成的字典，如：  ``` context=dict(STRING,ANY) context["buySignalRSI"]=70. context["buySignalRSI"]=30.  userConfig["context"]=context ``` |
| “orderBookMatchingRatio” | 与行情订单薄的成交百分比 | DOUBLE 类型，默认 1.0，取值0~1.0 之间 |
| “matchingRatio” | 区间撮合比例 | DOUBLE 类型，默认 1.0，取值0~1.0 之间。默认和成交百分比 orderBookMatchingRatio 相等 |

#### 基本信息表说明

接口 `createBacktester` 的参数 `securityReference`
和接口 `createBacktestEngine` 的参数
`securityReference` 的基本信息表字段可参考下表：

| **字段** | **类型** | **含义** |
| --- | --- | --- |
| symbol | STRING | 标的 |
| couponRate | DOUBLE | 票面利率 / 票息率 |
| frequency | INT | 付息频率 |
| valueDate | DATE | 起息日 |
| maturityDate | DATE | 到期日 |

### 行情数据结构说明

支持快照+逐笔成交明细，通过接口 `appendQuotationMsg` 向引擎中插入数据时，*msg* 结构：

执行回测时输入表 messageTable 结构:
`Backtest::appendQuotationMsg(engine,messageTable)`

```
colName=[`symbol,`symbolSource,`timestamp,`bidSettlType,`bidQty,`bidPrice,
`bidYield,`askSettlType,`askQty,`askPrice,`askYield,`tradePrice,
`tradeQty,`settlType,`yield]
colType=["SYMBOL","SYMBOL","TIMESTAMP","INT[]","LONG[]","DOUBLE[]","DOUBLE[]",
"INT[]","LONG[]","DOUBLE[]","DOUBLE[]","DOUBLE[]","LONG[]","INT[]","DOUBLE[]"]
messageTable=table(10000000:0, colName, colType)
```

快照+逐笔成交明细数据表结构：

| **名称** | **类型** | **含义** |
| --- | --- | --- |
| symbol | SYMBOL | 标的代码 |
| symbolSource | SYMBOL | 市场：银行间 ”X\_BOND” |
| timestamp | TIMESTAMP | 时间 |
| bidSettlType | INT[] | 买清算速度 |
| bidQty | LONG[] | 报买量（元） |
| bidPrice | DOUBLE[] | 报买净价（元) |
| bidYield | DOUBLE[] | 报买到期 |
| askSettlType | INT[] | 卖清算速度 |
| askQty | LONG[] | 报卖量（元） |
| askPrice | DOUBLE[] | 报卖净价（元) |
| askYield | DOUBLE[] | 报卖到期 |
| tradePrice | DOUBLE[] | 区间成交价格列表 |
| tradeQty | LONG[] | 区间成交数量列表 |
| settlType | INT[] | 清算速度 |
| yield | DOUBLE[] | 到期收益率 |

回测行情回放结束时，发送一条 symbol 为 “END” 的消息:

```
messageTable=select top 1* from messageTable where timestamp=max(timestamp)
update messageTable set symbol="END"
//update messageTable set msgTime=concatDateTime(timestamp.date(),16:00:00)
Backtest::appendQuotationMsg(engine,messageTable)
```

### 策略回调函数说明

快照行情回调函数 `onSnapshot`：输入参数 msg

msg 为字典时，是以 symbol 为 key 值的 snapShot 数据字典，每个 snapShot 对象包含字段如下：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 标的代码 |
| messageSource | SYMBOL | 市场：银行间 ”X\_BOND” |
| byield | TIMESTAMP | 时间戳 |
| ayield | DOUBLE[] | 报买到期 |
| bmdEntryPrice | DOUBLE[] | 报买净价（元） |
| amdEntryPrice | DOUBLE[] | 报卖净价（元） |
| bmdEntrySize | LONG[] | 报买量（元） |
| amdEntrySize | LONG[] | 报卖量（元） |
| bsettlType | LONG[] | 买清算速度 |
| asettlType | LONG[] | 卖清算速度 |
| settlType | LONG[] | 区间清算速度 |
| tradePrice | DOUBLE[] | 区间成交价格列表 |
| tradeYield | DOUBLE[] | 到期收益率 |
| tradeQty | LONG[] | 区间成交数量列表 |

## 上交所债券

### 引擎配置说明

接口 `createBacktester` 的参数 *config* ：

| **key** | **说明** | **备注** |
| --- | --- | --- |
| "startDate" | 开始日期 | 必须配置，DATE 类型 例如 “2020.01.01” |
| "endDate" | 结束日期 | 必须配置，DATE 类型 例如 “2020.01.01” |
| "strategyGroup" | 策略类型 | 必须配置，“XSHGBond” |
| "cash" | 初始资金 | 必须配置，DOUBLE 类型 |
| "commission" | 手续费 | 必须配置，DOUBLE 类型 |
| "tax" | 印花税 | 必须配置，DOUBLE 类型 |
| "dataType" | 行情类型 | 必须配置，INT 类型，可选值为： 2：快照+逐笔成交明细 |
| "orderBookMatchingRatio" | 与行情订单薄的成交百分比 | DOUBLE 类型，默认 1.0，取值0~1.0 之间 |
| "matchingRatio" | 区间撮合比例 | DOUBLE 类型，默认 1.0，取值0~1.0 之间。默认和成交百分比 orderBookMatchingRatio 相等 |
| "setLastDayPosition" | 底仓设置 | 底仓信息表，表结构见下表 |

底仓信息表结构如下：

| **字段** | **类型** | **含义** |
| --- | --- | --- |
| symbol | SYMBOL | 股票代码 |
| longPosition | LONG 或者 INT | 买入持仓量 |
| costPrice | DOUBLE | 成本价 |

#### 基本信息表说明

接口 `createBacktester` 的参数 `securityReference`
的基本信息表字段可参考下表：

| **字段** | **类型** | **含义** |
| --- | --- | --- |
| symbol | STRING | 标的 |
| couponRate | DOUBLE | 票面利率 / 票息率 |
| frequency | INT | 付息频率 |
| valueDate | DATE | 起息日 |
| maturityDate | DATE | 到期日 |

### 行情数据结构说明

输入的行情支持由“确定报价行情”和“成交明细”组成的宽表，表结构如下：

| **字段** | **数据类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL 或 STRING | 证券代码 |
| timestamp | TIMESTAMP | 时间戳 |
| msgType | INT | 行情类型，可选值为：  * 0：确定报价行情 * 1：成交明细 |
| symbolName | STRING | 证券简称 |
| bidId | INT | 买入订单编号 |
| bidTime | TIMESTAMP | 买入报价时间 |
| bidParty | SYMBOL 或 STRING | 买入报价方 |
| bidClean | DOUBLE | 买入价（净价） |
| bidQty | LONG | 买入数量 |
| bidDirty | DOUBLE | 买入全价 |
| bidYield | DOUBLE | 买入到期收益 率 |
| askId | INT | 卖出订单编号 |
| askTime | TIMESTAMP | 卖出报价时间 |
| askParty | SYMBOL 或 STRING | 卖出报价方 |
| askClean | DOUBLE | 卖出价（净价） |
| askQty | LONG | 卖出数量 |
| askDirty | DOUBLE | 卖出全价 |
| askYield | DOUBLE | 卖出到期收益率 |
| accruedInterest | DOUBLE | 应计利息 |
| tradeTime | TIMESTAMP | 成交时间 |
| tradeClean | DOUBLE | 成交净价 |
| tradeAccruedInterest | DOUBLE | 应计利息 |
| tradeDirty | DOUBLE | 成交全价 |
| yield | DOUBLE | 到期收益率 |
| tradeVolume | INT | 成交量 |
| tradeValue | DOUBLE | 成交金额 |
| tradeType | INT | 成交方式，可选值为： 1：确定报价成交  2：待定报价成交  3：询价成交  4：协议交易  6：协商成交（含合并申报）  7：竞买 |

