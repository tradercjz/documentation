# 接口说明

本节将介绍 DolphinDB 的回测引擎接口。用户可以基于自定义的策略创建回测引擎并执行回测，获取每日持仓、每日权益、收益概述、成交明细等回测结果。

## createBacktester

**语法**

```
Backtest::createBacktester(name, config, eventCallbacks, [jit=false], [securityReference])
```

**详情**

创建回测引擎，同时设置所有的回调函数。该接口仅支持股票、期货、期权。

返回创建的回测引擎句柄。

**参数**

**name** STRING 类型标量，表示回测引擎名称。

**config** 一个字典，表示回测引擎的配置项。字典的 key 是 STRING 类型，代表配置项的名称，value
是该配置项的具体配置，详情请参考[股票](stock.md)，[期权](option.md)，[期货](futures.md)。

**eventCallbacks** 一个字典，表示策略回调函数。字典的 key 是 STRING 类型，代表回调函数，value 为对应函数的定义。key
的可选值为：

* "initialize" 策略初始化回调函数，回测开始时触发调用。
* "beforeTrading" 每日盘前回调函数，每日开盘前触发调用。
* "onTick" 逐笔行情回调函数，可选参数。订阅逐笔行情时触发调用。
* "onSnapshot" 快照行情回调函数，订阅快照行情时触发调用。
* "onBar" 分钟或者日线行情回调函数，可选参数，订阅快照行情时触发调用。
* "onOrder" 委托回报通知函数，订单变更时触发调用。
* "onTrade" 成交回报通知函数，订单交易时触发调用。
* "afterTrading" 每日盘后回调函数，每日收盘时触发调用。
* "finalize" 策略结束回调函数，回测结束时会触发调用。
* "onTimer" 定时回调，value 为一个字典：
  + dataType=1，2，3，5，6 时字典的键是触发时间，对应的值是该时间触发调用的回调函数。
  + dataType=4 时，字典的键包括
    dataList，对应值为日期标量或向量；onTimeCallback，对应值为定时回调函数。

上述回调函数中，onTick, onBar, onSnapshot 的触发条件如下，使用时应根据 *config*参数的配置，指定对应的回调函数，无需全部指定：

| **输入数据类型** | **frequency 参数设置** | **可触发的函数** |
| --- | --- | --- |
| dataType=0 | frequency=0 | onTick |
| frequency>0 | onTick, onSnapshot |
| dataType=1或2 | frequency=0 | onSnapshot |
| frequency>0 | onSnapshot, onBar |

**jit** BOOL 类型标量，表示是否开启 JIT 优化。默认值为 false，表示不开启。当前版本暂不支持债券品种开启 JIT 优化，暂不支持定时回调函数
onTimer 开启 JIT 优化。

**securityReference** 合约的基本信息表。仅当资产为股票时是可选参数，其他资产均为必选参数。

## createBacktestEngine

注：

此接口为 createBacktester 的旧版本接口。

**语法**

```
Backtest::createBacktestEngine(name, config, [securityReference], initialize, beforeTrading, onTick/onBar, onSnapshot, onOrder, onTrade, afterTrading, finalize)
```

**详情**

创建回测引擎，同时设置所有的回调函数。此接口为 `createBacktester` 的旧版本接口，适用于所有资产。

返回创建的回测引擎句柄。

**参数**

**name** STRING 类型标量，表示回测引擎名称。

**config** 一个字典，表示回测引擎的配置项。key 是 STRING 类型，代表配置项的名称，value 是该配置项的具体配置。详情请参考[股票](stock.md)，[期权](option.md)，[期货](futures.md)，[债券](interbank_bonds.md)，[数字货币](digital_currency.md)。

**securityReference** 基础信息表，仅当资产为股票时是可选参数，其他资产均为必选参数。

**initialize** 初始化回调函数，回测开始时触发调用。

**beforeTrading** 每日盘前回调函数，每日开盘前触发调用。

**onTick/onBar** 逐笔/分钟或者日线行情回调函数，可选参数，订阅快照行情时触发调用。

**onSnapshot** 快照行情回调函数，订阅快照行情时触发调用。

**onOrder** 委托回报通知函数，订单变更时触发调用。

**onTrade** 成交回报通知函数，订单交易时触发调用。

**afterTrading** 每日盘后回调函数，每日收盘时触发调用。

**finalize** 策略结束回调函数，回测结束时会触发调用。

上述回调函数中，onTick, onBar, onSnapshot 的触发条件如下，使用时应根据 *config*参数的配置，指定对应的回调函数，无需全部指定：

| **输入数据类型** | **frequency 参数设置** | **可触发的函数** |
| --- | --- | --- |
| dataType=0 | frequency=0 | onTick |
| frequency>0 | onTick, onSnapshot |
| dataType=1 或 2 | frequency=0 | onSnapshot |
| frequency>0 | onSnapshot, onBar |

## appendQuotationMsg

**语法**

```
Backtest::appendQuotationMsg(engine, msg)
```

**详情**

插入行情执行策略回测。

**参数**

**engine** 回测引擎句柄。

**msg** 行情输入表，表结构请参考[行情数据结构说明](../backtest.html#quotation)。

## subscribeIndicator

**语法**

```
Backtest::subscribeIndicator(engine, marketDataType, metrics)
```

**详情**

设置订阅的行情指标。

**参数**

**engine** 回测引擎句柄。

**marketDataType** STRING 类型标量，表示要订阅指标的行情类型，可选值为：

* "snapshot" 快照。
* "entrust" 逐笔委托。
* "kline"或"ohlc" K 线。
* "trade"或"transaction" 逐笔成交明细。
* "snapshot\_kline"或"snapshot\_ohlc" 快照合成的 K 线。

**metrics** 一个字典，key 是 STRING 类型，代表指标名；value 是以元代码的形式表示计算公式，代表如何计算指标。状态因子的编写请参考
[DolphinDB
响应式状态引擎介绍教程](../../stream/reactive_state_engine.md)。

**示例**

```
d=dict(STRING,ANY)
d["mavg"]=<mavg(lastPrice,20)>
Backtest::subscribeIndicator(contextDict["engine"], "snapshot", d)
Backtest::subscribeIndicator(contextDict["engine"], "tick", d)
d=dict(STRING,ANY)
d["mavg"]=<mavg(trade,20)>
Backtest::subscribeIndicator(contextDict["engine"], "trade", d)
d=dict(STRING,ANY)
d["mavg"]=<mavg(clsoe,20)>
Backtest::subscribeIndicator(contextDict["engine"], "kline", d)
```

## setUniverse

**语法**

```
Backtest::setUniverse(engine, symbolList)
```

**详情**

为引擎设置标的池。

**参数**

**engine** 回测引擎句柄。

**symbolList** STRING 类型向量，表示标的。

## setBacktestMode

**语法**

```
Backtest::setBacktestMode(engine, isBacktestMode)
```

**详情**

设置回测引擎的模式。

**参数**

**engine** 回测引擎句柄。

**isBacktestMode** BOOL 标量，true 代表回测模式， false 代表模拟交易模式。

## dropBacktestEngine

**语法**

```
Backtest::dropBacktestEngine(engine)
```

**详情**

删除回测引擎。

**参数**

**engine** 回测引擎句柄。

## getTradeDetails

**语法**

```
Backtest::getTradeDetails(engine)
```

**参数**

**engine** 回测引擎句柄。

**详情**

获取订单交易明细，表结构如下：

| 字段 | 含义 |
| --- | --- |
| orderId | 订单号 |
| symbol | 证券代码 |
| direction | 订单委托买卖标志 1：买开；2：卖开；3：卖平；4：买平 |
| sendTime | 订单委托时间 |
| orderPrice | 订单委托价格 |
| orderQty | 订单委托数量 |
| tradeTime | 订单成交时间 |
| tradePrice | 成交价格 |
| tradeQty | 成交数量 |
| orderStatus | 表示订单状态： 4：已报  2：撤单成功  1：已成  0：部成  -1：审批拒绝  -2：撤单拒绝  -3：未成交的订单 |
| label | 标签 |
| outputOrderInfo | 风控日志，仅当引擎配置参数 *outputOrderInfo*=true 时包含此列 |
| seqNum | 序号列，仅当引擎配置参数 *outputSeqNum*=true 时包含此列 |

## getAvailableCash

**语法**

```
Backtest::getAvailableCash(engine)
```

**详情**

查询账户可用现金。

**参数**

**engine** 回测引擎句柄。

## getDailyPosition

**语法**

```
Backtest::getDailyPosition(engine, [symbol])
```

**参数**

**engine** 回测引擎句柄。

**symbol** STRING 类型标量，可选参数，表示要获取的标的。默认为空，此时获取所有标的的持仓数据。

**详情**

通常在回测结束调用，返回每日盘后的持仓数据详情。盘中调用会丢失当日信息，返回前一天的持仓数据。

当资产为股票、期货、期权时，持仓数据详情表结构如下：

| 字段 | 含义 |
| --- | --- |
| symbol | 标的代码 |
| tradeDate | 交易日 |
| lastDayLongPosition | 昨日买持仓 |
| lastDayShortPosition | 昨日卖持仓 |
| longPosition | 买持仓量 |
| longPositionAvgPrice | 买成交均价 |
| shortPosition | 卖持仓量 |
| shortPositionAvgPrice | 卖成交均价 |
| todayBuyVolume | 当日买成交数量 |
| todayBuyValue | 当日买成交金额 |
| todaySellVolume | 当日卖成交数量 |
| todaySellValue | 当日卖成交金额 |

当为融资融券模式时，持仓数据详情表结构如下：

| **字段** | **名称** |
| --- | --- |
| symbol | 标的代码 |
| tradeDate | 交易日 |
| lastDayMarginSecuPosition | 昨日担保品买入持仓量 |
| lastDayMarginDebt | 昨日收盘融资负债 |
| lastDaySecuLendingDebt | 昨日收盘融券负债 |
| marginSecuPosition | 担保品买入持仓量 |
| marginSecuAvgPrice | 买持仓均价 |
| marginBuyPosition | 融资买入持仓量 |
| marginBuyValue | 融资买入金额 |
| secuLendingPosition | 融券卖出持仓量 |
| secuLendingSellValue | 融券卖出金额 |
| closePrice | 收盘价 |
| longPositionConcentration | 多头集中度 |
| shortPositionConcentration | 净空头集中度 |
| marginBuyProfit | 融资盈亏 |
| financialFee | 融资利息 |
| secuLendingProfit | 融券盈亏 |
| secuLendingFee | 融券费用 |

当资产为债券时，持仓数据详情表结构如下：

| **字段** | **名称** |
| --- | --- |
| symbol | 标的代码 |
| tradeDate | 交易日 |
| lastDayLongPosition | 昨买持仓数量 |
| longPosition | 买持仓量 |
| longPositionAvgPrice | 买成交均价 |
| todayBuyVolume | 当日买成交数量 |
| todayBuyValue | 当日买成交金额 |
| totalValue | 持仓总额 |
| accruedInterest | 应计利息 |
| fullBondPrice | 债券全价 |
| lastPrice | 债券净价 |
| yield | 收益率 |
| interestIncome | 利息收入 |
| floatingProfit | 浮动损益 |
| realizedProfit | 实际损益 |
| totalProfit | 总损益 |
| duration | 久期 |
| convexity | 凸性 |
| DV01 | DV01 |

## setTradingOutput

**语法**

```
Backtest::setTradingOutput(engine, ouput)
```

**参数**

**engine** 回测引擎句柄。

**output** 一个字典，每个键值对代表一个输出表，key 的可选值包括：

* snapshot，对应的 value 为订阅的快照指标输出表，其表结构可通过 `getIndicatorSchema`
  获取。
* tick，对应的 value 为订阅的逐笔指标输出表，其表结构可通过 `getIndicatorSchema`
  获取。
* ohlc（或 kline），对应的 value 为订阅的 K 线指标输出表，其表结构可通过
  `getIndicatorSchema` 获取。
* transaction（或 trade），对应的 value 为订阅的逐笔成交指标输出表，其表结构可通过
  `getIndicatorSchema` 获取。
* snapshot\_kline（或 snapshot\_ohlc），对应的 value 为订阅的快照合成的 K 线的指标输出表，其表结构可通过
  `getIndicatorSchema` 获取。
* position，对应的 value 为实时更新持仓信息的表，可以通过 `getPosition`
  获取相应引擎指标表结构。
* totalPortfolios，对应的 value 为实时获取账户权益的表，可以通过
  `getTotalPortfolios` 获取相应引擎指标表结构。
* tradeDetails，对应的 value 为实时更新成交明细的表，可以通过 `getTradeDetails`
  获取相应引擎指标表结构。
* dailyPosition，对应的 value 为获取每日持仓的表，可以通过 `getTradeDetails`
  获取相应引擎指标表结构。
* dailyTotalPortfolios，对应的 value 为更新账户每日权益的表，可以通过
  `getDailyTotalPortfolios` 获取相应引擎指标表结构。

**详情**

为回测引擎设置实时输出表，信息将实时写入对应的表。

## getIndicatorSchema

**语法**

```
Backtest::getIndicatorSchema(engine,[marketDataType])
```

**参数**

**engine** 回测引擎句柄。

**marketDataType** STRING
类型标量，表示订阅指标的行情类型，如果该引擎只订阅了一种行情类型指标，则该参数可省略，否则必须指定该参数。

**详情**

返回一张策略指标空表，表结构如下：

| **列名** | **数据类型** | **说明** |
| --- | --- | --- |
| symbol | SYMBOL | 标的代码 |
| timestamp | TIMESTAMP | 时间戳 |
| 订阅的指标名称 | DOUBLE | 订阅的指标 |
| … | … | … |

## getTotalPortfolios

**语法**

```
Backtest::getTotalPortfolios(engine)
```

**参数**

**engine** 回测引擎句柄。

**详情**

获取当前策略权益指标表。表结构如下：

* 股票：

  | **字段名称** | **字段说明** |
  | --- | --- |
  | tradeDate | 日期 |
  | cash | 可用资金 |
  | totalMarketValue | 账户总市值 |
  | totalEquity | 账户总权益 |
  | netValue | 账户单位净值 |
  | totalReturn | 截至当日的累计收益率 |
  | ratio | 账户每日收益率 |
  | pnl | 账户当日盈亏 |
  | frozenFunds | 冻结资金 |
* 融资融券：

  | **字段名称** | **字段说明** |
  | --- | --- |
  | tradeDate | 日期 |
  | lineOfCredit | 授信额度 |
  | availableCash | 可用资金 |
  | lastDayMarginDebt | 昨日收盘融资负债 |
  | lastDaySecuLendingDebt | 昨日收盘融券负债 |
  | marginSecuMarketValue | 担保品买入市值 |
  | marginDebt | 融资负债 |
  | secuLendingSellValue | 融券卖出金额（融券负债） |
  | marginBalance | 融资融券余额 |
  | secuLendingDebt | 融券负债 |
  | financialFee | 融资利息 |
  | secuLendingFee | 融券费用 |
  | maintainanceMargin | 维保比例 |
  | availableMarginBalance | 保证金可用余额 |
  | totalMarketValue | 账户总市值 |
  | totalEquity | 账户总权益 |
  | netValue | 账户单位净值 |
  | totalReturn | 截至当日的累计收益率 |
  | yield | 账户每日收益率 |
  | pnl | 账户当日盈亏 |
  | frozenFunds | 冻结资金 |
* 期货/期权：

  | **字段名称** | **字段说明** |
  | --- | --- |
  | tradeDate | 日期 |
  | margin | 保证金占用 |
  | floatingPnl | 浮动盈亏 |
  | realizedPnl | 已实现累计盈亏 |
  | totalPnl | 累计盈亏 |
  | cash | 可用资金 |
  | totalEquity | 账户总权益 |
  | marginRatio | 保证金占用比例 |
  | pnl | 账户当日盈亏 |
  | netValue | 账户单位净值 |
  | totalReturn | 截至当日的累计收益率 |
  | ratio | 账户每日收益率 |
* 债券

  |  |  |
  | --- | --- |
  | **字段名称** | **字段说明** |
  | tradeDate | 日期 |
  | cash | 可用资金 |
  | totalMarketValue | 账户总市值 |
  | totalEquity | 账户总权益 |
  | netValue | 账户单位净值 |
  | totalReturn | 截至当日的累计收益率 |
  | ratio | 每日收益率 |
  | pnl | 账户当日盈亏 |
  | totalProfit | 总损益 |

## getDailyTotalPortfolios

**语法**

```
Backtest::getDailyTotalPortfolios(engine)
```

**参数**

**engine** 回测引擎句柄。

**详情**

通常在回测结束调用，获取策略每日权益指标表。回测的资产不同，返回表的结构也有所差异：

* 股票：

  | **字段名称** | **字段说明** |
  | --- | --- |
  | tradeDate | 日期 |
  | cash | 可用资金 |
  | totalMarketValue | 账户总市值 |
  | totalEquity | 账户总权益 |
  | netValue | 账户单位净值 |
  | totalReturn | 截至当日的累计收益率 |
  | ratio | 账户每日收益率 |
  | pnl | 账户当日盈亏 |
  | frozenFunds | 冻结资金 |
* 融资融券：

  | **字段名称** | **字段说明** |
  | --- | --- |
  | tradeDate | 日期 |
  | lineOfCredit | 授信额度 |
  | availableCash | 可用资金 |
  | lastDayMarginDebt | 昨日收盘融资负债 |
  | lastDaySecuLendingDebt | 昨日收盘融券负债 |
  | marginSecuMarketValue | 担保品买入市值 |
  | marginDebt | 融资负债 |
  | secuLendingSellValue | 融券卖出金额（融券负债） |
  | marginBalance | 融资融券余额 |
  | secuLendingDebt | 融券负债 |
  | financialFee | 融资利息 |
  | secuLendingFee | 融券费用 |
  | maintainanceMargin | 维保比例 |
  | availableMarginBalance | 保证金可用余额 |
  | totalMarketValue | 账户总市值 |
  | totalEquity | 账户总权益 |
  | netValue | 账户单位净值 |
  | totalReturn | 截至当日的累计收益率 |
  | yield | 账户每日收益率 |
  | pnl | 账户当日盈亏 |
* 期货/期权：

  | **字段名称** | **字段说明** |
  | --- | --- |
  | tradeDate | 日期 |
  | margin | 保证金占用 |
  | floatingPnl | 浮动盈亏 |
  | realizedPnl | 已实现累计盈亏 |
  | totalPnl | 累计盈亏 |
  | totalMarketValue | 总市值（仅期权） |
  | cash | 可用资金 |
  | totalEquity | 账户总权益 |
  | marginRatio | 保证金占用比例 |
  | pnl | 账户当日盈亏 |
  | netValue | 账户单位净值 |
  | totalReturn | 截至当日的累计收益率 |
  | ratio | 账户每日收益率 |
* 债券

  | **字段名称** | **字段说明** |
  | --- | --- |
  | tradeDate | 日期 |
  | cash | 可用资金 |
  | totalMarketValue | 账户总市值 |
  | totalEquity | 账户总权益 |
  | netValue | 账户单位净值 |
  | totalReturn | 截至当日的累计收益率 |
  | ratio | 账户每日收益率 |
  | pnl | 账户当日盈亏 |
  | totalProfit | 总损益 |

## getReturnSummary

**语法**

```
Backtest::getReturnSummary(engine)
```

**参数**

**engine** 回测引擎句柄。

**详情**

用于回测结束时计算策略的收益概述，返回一张收益概述表。收益表结构如下：

* **股票/期货/期权/债券：**

  | **字段名称** | **字段说明** |
  | --- | --- |
  | totalReturn | 总收益 |
  | annualReturn | 年化收益率 |
  | annualVolatility | 年化波动率 |
  | annualSkew | 收益率偏度 |
  | annualKur | 收益率峰度 |
  | sharpeRatio | 夏普率 |
  | maxDrawdown | 最大回撤 |
  | drawdownRatio | 收益回撤比 |
  | beta | beta系数 |
  | alpha | a系数 |
  | benchmarkReturn | 基准收益 |
  | annualExcessReturn | 年化超额收益 |
  | turnoverRate | 换手率 |
  | dailyWinningRate | 日胜率 |
  | maxMarginRatio | 策略最大保证金占用比例（期货期权独有字段） |
* 融资融券模式，返回的收益表除上述字段外 ，还包含以下字段：

  | **字段名称** | **字段说明** |
  | --- | --- |
  | totalFee | 佣金与手续费之和 |
  | financialFee | 融资利息 |
  | secuLendingFee | 融券费用 |
  | bottomRet | 底仓收益 |
  | bottomExcessRet | 底仓超额收益 |

## getBacktestEngineList

**语法**

```
Backtest::getBacktestEngineList()
```

**详情**

获取所有的回测引擎。

## getBacktestEngineStat

**语法**

```
Backtest::getBacktestEngineStat(engine)
```

**详情**

查看回测引擎状态。

返回一个表，包含以下字段：

* name：回测引擎名称
* user：回测引擎的创建者
* status：回测引擎的状态，可能的值包括 OK（可用），END（正常结束），FATAL（不可用）
* lastErrMsg：最后一条错误信息
* numIndicators：订阅的指标数量
* snapshotTimestamp：回测引擎当前处理过的最新数据的时间戳

## getContextDict

**语法**

```
Backtest::getContextDict(engine)
```

**参数**

**engine** 回测引擎句柄。

**详情**

返回逻辑上下文。

## setSecurityReference

**语法**

```
Backtest::setSecurityReference(engine, securityReferenceData)
```

**参数**

**engine** 回测引擎句柄。

**securityReferenceData** 该品种对应的基础信息表。

**详情**

设置基本信息表。

## getTodayPnl

**语法**

```
Backtest::getTodayPnl(engine, symbol)
```

**参数**

**engine** 回测引擎句柄。

**symbol** STRING 类型标量，表示股票标的。

**详情**

该接口仅可用于股票，获取账户盈亏。

返回一个字典，结构如下：

| **key** | **value** |
| --- | --- |
| symbol | 标的代码 |
| pnl | 当前账户中该标的的盈亏金额 |
| todayPnl | 当日账户中该标的的盈亏金额 |

## submitOrder

**语法**

```
Backtest::submitOrder(engine, msg, label="", orderType=0)
```

**详情**

可在回调函数中调用此函数提交订单，返回订单号。

**参数**

**engine** 回测引擎句柄，在回调函数中可通过 `contextDict["engine"]` 获取。

**msg** 一个元组或表，表示订单信息。

* *orderType*=0 时，格式如下：

  | **品种** | **格式** | **说明** |
  | --- | --- | --- |
  | 股票（包括股票、可转债、基金） | (股票代码, 下单时间, 订单类型, 订单价格, 订单数量, 买卖方向) | **买卖方向：**1：买开；2卖开；3：卖平；4：买平 **订单类型：**  上交所：  0：市价单中最优五档即时成交剩余撤销委托订单  1：市价单中最优五档即时成交剩余转限价委托订单  2：市价单中本方最优价格委托订单  3：市价单中对手方最优价格委托订单  5：限价单  6：撤单  深交所：  0：市价单中最优五档即时成交剩余撤销委托订单  1：市价单中即时成交剩余撤销委托订单  2：市价单中本方最优价格委托订单  3: 市价单中对手方最优价格委托订单  4：市价单中全额成交或撤销委托订单  5：限价单  6：撤单 |
  | 期货/期权 | (标的代码, 交易所代码, 时间, 订单类型, 委托订单价格, 止损价/止盈价，委托订单数量，买卖方向，委托订单有效性) | **买卖方向：**1：买开；2卖开；3：卖平；4：买平；5：期权行权（仅支持多账户回测模式的期权品种，且基本信息表的 underlyingCode 项必须配置）  **订单类型：**  0：市价单，以涨跌停价委托，并遵循时间优先原则  1：市价止损单  2：市价止盈单  3：限价止损单  4：限价止盈单  5：限价单（默认值）  6：撤单  **委托订单有效性：**  0：当日有效（默认值）  1：立即全部成交否则自动撤销（FOK）  2：立即成交剩余自动撤销（FAK）  止损价/止盈价暂不支持，默认 0. |
  | 融资融券 | (股票代码、下单时间、订单类型、订单价格、订单数量、买卖标志) | **订单类型：**  0：市价单  5：限价单  **买卖标志：**  1：担保品买入  2：担保品卖出  3：融资买入  4：融券卖出  5：直接还款  6：卖券还款  7：直接还券  8：买券还券 |
  | 银行间债券 | （标的代码，下单时间，订单类型，清算速度，委托买单到期收益率，委托买单订单价格，委托买订单数量，委托卖单到期收益率，委托卖单订单价格，委托卖订单数量，买卖标志，用户订单ID，撮合渠道） | **订单类型：**  1：限价单  2：双边报价  3 : 市价单转撤单  4：市价单转限单  5：弹性  6：撤单 |
  | 上交所债券 | （标的代码，下单时间，订单类型，清算速度，买价，买量，卖价，卖量，买卖方向，用户指定的订单号，渠道） | 买卖标志： 1：买开  2：卖平  3：双边报价  订单类型：  1：限价单  3：市价单转撤单  4：市价单转限单  5：弹性  7: FAK：按用户指定的价格立即撮合，不能成交的部分马上撤单  8：FOK：按用户指定的价格立即完全成交撮合，不能完全成交就撤单 |
  | 数字货币 | (标的代码, 交易所代码, 时间, 订单类型, 委托订单价格, 止损价，止盈价，委托订单数量，买卖方向，滑点，委托订单有效性，委托订单到期时间) | **买卖方向：**1：买开；2卖开；3：卖平；4：买平  **订单类型：**  5：限价单（默认值）  0：市价单，以涨跌停价委托，并遵循时间优先原则  **委托订单有效性：**  0：当日有效（默认值）  1：立即全部成交否则自动撤销（FOK）  2：立即成交剩余自动撤销（FAK） |
* orderType>0 时，格式为 `(期货代码, 交易所代码, 时间, 订单类型, 委托订单价格,
  止损价，止盈价，委托订单数量，买卖方向，滑点，委托订单有效性，委托订单到期时间)`。

**label** STRING 类型标量，对该订单设置标签，对该订单分类。

**orderType** INT 类型标量，可选值如下：

* 0 ：默认值，表示一般订单
* 1：现价止盈订单
* 2：市价止盈订单
* 3：限价止损订单
* 4：市价止损订单
* 5：限价止盈止损订单
* 6：市价止盈止损订单

其中 1-6 为算法订单，仅支持股票、期货、期权，可通过配置项 openAlgoOrder 开启。

## cancelOrder

**语法**

```
Backtest::cancelOrder(engine, symbol="", orders=NULL, label="")
```

**详情**

取消订单。

* 若 *symbol* 不为空，则取消该标的的所有订单。
* 若 *symbol* 为空，*orders* 不为空，则取消 *orders* 中的订单。
* 若 *symbol* 为空，orders 为空，则取消 *label* 指定的订单。

**参数**

**engine** 回测引擎句柄，在回调函数中可通过 `contextDict["engine"]` 获取。

**symbol** STRING 类型标量，要取消的订单的证券代码，可选参数。

**orders** INTEGRAL 类型向量，要取消的订单 ID 列表，可选参数。

**label** STRING 类型标量，要取消的订单的备注信息。

## getOpenOrders

**语法**

```
Backtest::getOpenOrders(engine, symbol=NULL, orders=NULL, label="", outputQueuePosition=false)
```

**参数**

**engine** 回测引擎句柄，在回调函数中可通过 `contextDict["engine"]` 获取。

**symbol** STRING 类型标量，证券代码，可选参数。

**orders** INTEGRAL 类型向量，订单 ID 列表，可选参数。

**label** STRING 类型标量，用作备注，可选参数。

**outputQueuePosition** BOOL 类型标量，是否输出详细信息（包括 openVolumeWithBetterPrice,
openVolumeWithWorsePrice, openVolumeAtOrderPrice, priorOpenVolumeAtOrderPrice,
depthWithBetterPrice）。可选参数，默认为 false，表示不输出。仅支持股票和期货品种设置此参数。

**详情**

查询未成交订单。

* 若 *symbol* 不为空，则查询该标的的未成交订单。
* 若 *symbol* 为空，*orders* 不为空，则查询 *orders* 中未成交的订单。
* 若 *symbol* 为空，orders 为空，则查询 *label* 指定的未成交订单。

查询未成交订单信息。返回一个字典或表。

对于除上交所债券外的其它资产，结构如下：

| key | value 类型 | value 说明 |
| --- | --- | --- |
| orderId | LONG | 订单 ID |
| timestamp | TIMESTAMP | 时间 |
| symbol | STRING | 标的代码 |
| price | DOUBLE | 委托价格 |
| totalQty | LONG | 用户订单数量 |
| openQty | LONG | 用户订单余量 |
| direction | INT | 1（买开 ），2（卖开），3（卖平），4（买平） |
| isMacthing | INT | 订单是否到达撮合时间 |
| openVolumeWithBetterPrice | LONG | 优于委托价格的行情未成交委托单总量（仅当 *outputQueuePosition=true* 时返回） |
| openVolumeWithWorsePrice | LONG | 次于委托价格的行情未成交委托单总量（仅当 *outputQueuePosition=true* 时返回） |
| openVolumeAtOrderPrice | LONG | 等于委托价格行情未成交委托单总量（仅当 *outputQueuePosition=true* 时返回） |
| priorOpenVolumeAtOrderPrice | LONG | 等于委托价格行情且比自己早的行情未成交委托单总量（仅当 *outputQueuePosition=true*时返回） |
| depthVolumeWithBetterPrice | INT | 优于委托价格的行情未成交价格档位深度（仅当 *outputQueuePosition=true*时返回） |
| updateTime | TIMESTAMP | 最新更新时间 |

对于上交所债券，结构如下：

| **名称** | **类型** | **含义** |
| --- | --- | --- |
| orderId | LONG | 订单id |
| time | TIMESTAMP | 时间 |
| symbol | STRING | 股票标的 |
| bidPrice | DOUBLE | 委买价格 |
| bidTotalQty | LONG | 用户订单委买数量 |
| bidRemainQty | LONG | 用户订单委买余量 |
| askPrice | DOUBLE | 委卖委托价格 |
| askTotalQty | LONG | 用户订单委卖数量 |
| askRemainQty | LONG | 用户订单委卖余量 |
| direction | INT | 1：买 2：卖  3：双边 |
| label | STRING | 备注 |

## getPosition

**语法**

```
Backtest::getPosition(engine, symbol="")
```

**参数**

**engine** 回测引擎句柄，在回调函数中可通过逻辑上下文 `context["engine"]` 获取。

**symbol** STRING 类型标量，证券代码，可选参数。

**详情**

获取持仓信息。

* 若不指定 *symbol*，返回表；
* 若指定 *symbol*，返回字典；
* 开启 JIT 优化时必须指定 *symbol*。

对于除上交所债券外的其它资产，返回结构如下：

| 字段 | 名称 |
| --- | --- |
| symbol | 标的代码 |
| lastDayLongPosition | 昨买持仓数量 |
| lastDayShortPosition | 昨卖持仓数量 |
| longPosition | 买持仓量 |
| longPositionAvgPrice | 买成交均价 |
| shortPosition | 卖持仓量 |
| shortPositionAvgPrice | 卖成交均价 |
| todayBuyVolume | 当日买成交数量 |
| todayBuyValue | 当日买成交金额 |
| todaySellVolume | 当日卖成交数量 |
| todaySellValue | 当日卖成交金额 |

对于上交所债券，返回结构如下：

| **字段** | **名称** |
| --- | --- |
| symbol | 标的代码 |
| lastDayLongPosition | 昨买持仓数量 |
| longPosition | 买持仓量 |
| longPositionAvgPrice | 买成交均价 |
| todayBuyVolume | 当日买成交数量 |
| todayBuyValue | 当日买成交金额 |
| totalValue | 持仓总额 |
| accruedInterest | 应计利息 |
| fullBondPrice | 债券全价 |
| lastPrice | 债券净价 |
| yield | 收益率 |
| interestIncome | 利息收入 |
| floatingProfit | 浮动损益 |
| realizedProfit | 实际损益 |
| totalProfit | 总损益 |
| duration | 久期 |
| convexity | 凸性 |
| DV01 | DV01 |

## updatePosition

**语法**

```
Backtest::updatePosition (engine, symbol, qty, [price])
```

**参数**

**engine** 回测引擎句柄，在回调函数中可通过逻辑上下文 `context["engine"]` 获取。

**symbol** STRING 类型标量，表示标的。

**qty** INT 类型标量，正数代表增加持仓，负数代表减少持仓。

**price** DOUBLE 类型标量，表示成交价格。当参数为 0 或为空时，取行情的最新价。

**详情**

更新持仓，返回订单号。该接口仅支持在模拟交易模式下调用。

## getStockTotalPortfolios

**语法**

```
Backtest::getStockTotalPortfolios(engine)
```

**参数**

**engine** 回测引擎句柄，在回调函数中可通过逻辑上下文 `context["engine"]` 获取。

**详情**

获取当前的股票策略权益指标，返回一个字典，结构如下：

| **key** | **value** |
| --- | --- |
| tradeDate | 日期 |
| cash | 可用资金 |
| totalMarketValue | 账户总市值 |
| totalEquity | 账户总权益 |
| netValue | 账户单位净值 |
| totalReturn | 截至当日的累计收益率 |
| ratio | 账户每日收益率 |
| pnl | 账户当日盈亏 |

## getFuturesTotalPortfolios

**语法**

```
Backtest::getFuturesTotalPortfolios(engine)
```

**参数**

**engine** 回测引擎句柄，在回调函数中可通过逻辑上下文 `context["engine"]` 获取。

**详情**

查询每日期货盈亏情况，返回表结构如下：

| **字段名称** | **字段说明** |
| --- | --- |
| tradeDate | 日期 |
| margin | 保证金占用 |
| floatingPnl | 浮动盈亏 |
| realizedPnl | 已实现累计盈亏 |
| totalPnl | 累计盈亏 |
| cash | 可用资金 |
| totalEquity | 账户总权益 |
| marginRatio | 保证金占用比例 |
| pnl | 账户当日盈亏 |
| netValue | 账户单位净值 |
| totalReturn | 截至当日的累计收益率 |
| ratio | 账户每日收益率 |

## getOptionTotalPortfolios

**语法**

```
Backtest::getOptionTotalPortfolios(engine)
```

**参数**

**engine** 回测引擎句柄，在回调函数中可通过逻辑上下文 `context["engine"]` 获取。

**详情**

查询每日期权盈亏情况，返回表结构如下：

| **字段名称** | **字段说明** |
| --- | --- |
| tradeDate | 日期 |
| margin | 保证金占用 |
| floatingPnl | 浮动盈亏 |
| realizedPnl | 已实现累计盈亏 |
| totalPnl | 累计盈亏 |
| cash | 可用资金 |
| totalEquity | 账户总权益 |
| marginRatio | 保证金占用比例 |
| pnl | 账户当日盈亏 |
| netValue | 账户单位净值 |
| totalReturn | 截至当日的累计收益率 |
| ratio | 账户每日收益率 |

## getMarginSecuPosition

**语法**

```
Backtest::getMarginSecuPosition(engine,[symbolList])
```

**参数**

**engine** 回测引擎句柄，在回调函数中可通过逻辑上下文 `context["engine"]` 获取。

**symbolList** 可选参数，STRING 类型向量，表示股票代码列表。省略时默认返回所有股票担保品买入持仓信息。

**详情**

查询担保品买入持仓信息。

若 *engine* 由接口 `createBacktester` 创建，则

* *symbolList* 的长度为 1 时返回字典
* *symbolList* 的长度不为 1 时报错
* *symbolList* 省略时返回表

若 *engine* 由接口 `createBacktester` 创建，则返回表。

返回表结构如下：

| **字段** | **名称** |
| --- | --- |
| symbol | 标的代码 |
| lastDayLongPosition | 昨日收盘时担保品买入持仓量 |
| lastDayBuyValue | 昨日收盘时担保品买入金额 |
| longPosition | 担保品买入持仓量 |
| buyValue | 担保品买入金额 |
| todayBuyVolume | 当日担保品买入成交数量 |
| todayBuyValue | 当日担保品买入成交金额 |

## getMarginTradingPosition

**语法**

```
Backtest::getMarginTradingPosition(engine,symbolList)
```

**参数**

**engine** 回测引擎句柄，在回调函数中可通过逻辑上下文 `context["engine"]` 获取。

**symbolList**可选参数，STRING 类型向量，表示股票代码列表。省略时默认返回所有股票融资买入持仓信息。

**详情**

查询融资买入持仓信息。

若 *engine* 由接口 `createBacktester` 创建，则

* *symbolList* 的长度为 1 时返回字典
* *symbolList* 的长度不为 1 时报错
* *symbolList* 省略时返回表

若 *engine* 由接口 `createBacktester` 创建，则返回表。

返回表结构如下：

| **字段** | **名称** |
| --- | --- |
| symbol | 标的代码 |
| lastDayLongPosition | 昨日收盘时融资买入持仓量 |
| lastDayBuyValue | 昨日收盘时融资买入金额 |
| lastDayMarginDebt | 昨日收盘时融资买入负债 |
| longPosition | 融资买入持仓量 |
| buyValue | 融资买入金额 |
| todayBuyVolume | 当日融资买入成交数量 |
| todayBuyValue | 当日融资买入金额 |
| marginBuyProfit | 融资盈亏 |
| financialFee | 融资利息 |

## getSecuLendingPosition

**语法**

```
Backtest::getSecuLendingPosition(engine,symbolList)
```

**参数**

**engine** 回测引擎句柄，在回调函数中可通过逻辑上下文 `context["engine"]` 获取。

**symbolList** 可选参数，STRING 类型向量，表示股票代码列表。省略时默认返回所有股票融券卖出信息。

**详情**

查询融券卖出信息。

若 *engine* 由接口 `createBacktester` 创建，则

* *symbolList* 的长度为 1 时返回字典
* *symbolList* 的长度不为 1 时报错
* *symbolList* 省略时返回表

若 *engine* 由接口 `createBacktester` 创建，则返回表。

返回表结构如下：

| **字段** | **名称** |
| --- | --- |
| symbol | 标的代码 |
| lastDayShortPosition | 昨日融券卖出持仓量 |
| lastDayShortValue | 昨日融券卖出金额 |
| lastDaySecuLendingDebt | 昨日收盘时融券卖出负债 |
| shortPosition | 融券卖出持仓量 |
| shortValue | 融券卖出金额 |
| todayShortVolume | 当日融券卖出成交量 |
| todayShortValue | 当日融券卖出金额 |
| secuLendingProfit | 融券盈亏 |
| secuLendingFee | 融券费用 |

## 数字货币接口

数字货币引擎支持单个引擎中同时管理现货和期货的多个账户，其使用方式与单账户引擎有所不同。多账户设计遵循以下原则：

1. 数字货币行情中可以存在不同的合约类型，onBar 回调会一次性提供对应时间段内所有合约类型的数据，便于用户根据不同合约的行情设计策略。
2. 数字货币接口支持可选的 *accountType*
   参数，用于指定需要操作的账户。在省略该参数时，原则上策略中使用的接口(下单撤单、获取未成交订单、获取持仓等)默认为现货账户，回测结束后调用的接口(成交明细、每日持仓等)默认返回所有账户的结果。

在数字货币回测中，多数引擎接口与其他资产一致。用户仍可通过这些接口创建引擎、执行回测、获取回测结果。需要注意，部分接口增加了相关参数：

**contractType** STRING 类型标量，表示订阅行情品种类型。可选值为 "spot", "futures",
"option"，分别代表现货、期货和永续合约、期权。

**accountType** STRING 类型标量，表示账户类型。可选值为 "spot", "futures",
"option"，分别代表现货账户、期货和永续合约账户、期权账户。默认值为 "spot"。

相关接口如下表所示：

| **接口** | **语法详情** |
| --- | --- |
| subscribeIndicator | 订阅指标：   ``` Backtest::subscribeIndicator(contextDict["engine"], "snapshot", d,contractType) ``` |
| submitOrder | 下单接口：   ``` Backtest::submitOrder(engine, msg,label="",orderType=0,accountType) ``` |
| getAvailableCash | 查询账户可用资金：   ``` Backtest::getAvailableCash(long(engine),accountType) ``` |
| getPosition | 获取当前持仓：   ``` Backtest::getPosition(engine,symbol="",accountType) ``` |
| getDailyPosition | 获取每日持仓：   ``` Backtest::getDailyPosition(engine，accountType) ``` |
| getDailyTotalPortfolios | 获取策略每日权益指标：   ``` Backtest::getDailyTotalPortfolios(engine,accountType) ``` |
| getReturnSummary | 获取策略的收益概述：   ``` Backtest::getReturnSummary(engine,accountType) ``` |
| getTradeDetails | 获取订单交易明细：   ``` Backtest::getTradeDetails(engine,accountType) ``` |

## 多账户接口

多账户回测支持在一个引擎中，同时管理股票、期货、期权的多个账户。

多账户回测接口与一致。用户仍可通过这些接口创建引擎、执行回测、获取回测结果。这里仅介绍有所变动的接口。

部分接口增加了参数：

**contractType** STRING 类型标量，表示订阅的行情品种类型。可选值为 "stock", "futures",
"option"，分别代表股票、期货、期权。

**accountType** STRING 类型标量，表示账户类型。可选值为 "stock", "futures",
"option"，分别代表股票、期货、期权账户。接口
getDailyPosition，getDailyTotalPortfolios，getReturnSummary，getTradeDetails
中该参数默认为空，此时返回所有账户的对应信息，其他接口默认值为 "stock"。

| 接口 | 语法详情 |
| --- | --- |
| subscribeIndicator | 订阅指标：  ``` Backtest::subscribeIndicator(engine, marketDataType, metrics, [contractType="stock"]) ``` |
| submitOrder | 下单接口：  ``` Backtest::submitOrder(engine, msg, [label=""], [orderType=0], [accountType="stock"]) ```   *msg* 的格式为 (标的代码, 交易所代码, 时间, 订单类型, 委托订单价格, 止损价，止盈价，委托订单数量，买卖方向，滑点，委托订单有效性，委托订单到期时间) |
| getAvailableCash | 查询账户可用资金：  ``` Backtest::getAvailableCash(engine, [accountType="stock"]) ``` |
| getPosition | 获取当前持仓：  ``` Backtest::getPosition(engine, [symbol], [accountType="stock"]) ``` |
| getDailyPosition | 获取每日持仓：  ``` Backtest::getDailyPosition(engine, [symbol], [accountType) ``` |
| getDailyTotalPortfolios | 获取策略每日权益指标：  ``` Backtest::getDailyTotalPortfolios(engine, [accountType]) ``` |
| getReturnSummary | 获取策略的收益概述：  ``` Backtest::getReturnSummary(engine, [accountType]) ``` |
| getTradeDetails | 获取订单交易明细：  ``` Backtest::getTradeDetails(engine, [accountType]) ``` |
| getOpenOrders | 获取未成交订单：  ``` Backtest::getOpenOrders(engine, [symbol=""], [orders], [label=""], [outputQueuePosition=false], [accountType="stock"]) ``` |
| getIndicatorSchema | 获取策略指标表：  ``` backtest::getIndicatorSchema(engine,marketDataType,accountType="stock") ```   *marketDataType* 可为 “snapshot”，“ohlc”，“kline”，“trade” 或 “transaction” |
| setTradingOutput | 设置实时输出表：  ``` backtest::setTradingOutput(engine, ouput) ```   output 是一个嵌套字典，key 是账户类型，value 为字典。子字典 value 的键是输出表名， 对应的值为表对象。 |

