# convertibleFixedRateBondDirtyPrice

## 语法

`convertibleFixedRateBondDirtyPrice(settlement, issue,
maturity, redemption, coupon, spread, riskFree, volatility, spot,
conversionPrice, divYield, divDates, callDates, callPrices, putDates, putPrices,
style, calendar, frequency, [basis=1], [convention='Following'],
[method='binomial'], [kwargs])`

## 详情

计算固息可转债每 100 面值的含息价格。

可转换债券（Convertible
Bond），简称可转债，是一种混合债券及期权的产品，可按一定规则转换为债券发行公司的股票；其转换价格会在发行前确定。可转债中往往会嵌入债券赎回或者回售的权利。

**返回值** DOUBLE 类型的标量或向量

## 参数

**注意**：如果输入参数中，部分为标量，其余为向量时，则会将标量当作与向量长度相同，所有元素值等于该标量的向量。所有向量的长度必须一致。若输入参数为数组向量，则其行数必须与其他向量参数的长度相同。

**settlement** DATE 类型标量或向量，表示债券的结算日。

**issue** DATE 类型标量或向量，表示债券的发行日。

**maturity** DATE 类型标量或向量，表示债券的到期日。

**redemption** 数值型标量或向量，表示债券的赎回价格。

**coupon** 数值型标量或向量，表示债券的年息票利率。

**spread** 数值型标量或向量，表示息差。

**riskFree** 数值标量或向量，表示无风险利率。

**volatility** 数值标量或向量，表示波动率。

**spot** 数值标量或向量，表示债券发行公司的股票现价。

**conversionPrice** 数值型标量或向量，表示转股价格，即债券转换为普通股时每股所需支付的价格。该参数决定了每张可转债能换取的股票数量。

**divYield** 数值标量或向量，表示分红利率。

**divDates** DATE 类型向量或数组向量，表示分红日期。

**callDates** DATE 类型向量或数组向量，表示嵌入赎回权利时，约定的提前赎回债券的日期。

**callPrices** 数值型向量或数组向量，表示嵌入赎回权利时，约定的提前赎回债券的价格。必须与callDates一一对应。

**putDates** DATE 类型向量或数组向量，表示嵌入回售权利时，约定的提前回售债券的日期。

**putPrices** 数值型向量或数组向量，表示嵌入回售权利时，约定的提前回售债券的价格。必须与putDates一一对应。

**style** 字符串类型标量或向量，表示可行权时间的类型，有两个可选值：

* ‘european’：表示欧式期权。
* ‘american’：表示美式期权。

**calendar** 字符串类型标量或向量，表示使用的市场日历类型，请参阅[交易日历](../../modules/MarketHoliday/mkt_calendar.md)。

**frequency** 支持以下两种输入类型：

* 整型标量或向量：表示每年的付息次数，如 1 表示每年付息 1 次；
* DURATION 标量或向量：表示间隔多长时间进行一次付息，如 3M，表示每 3 个月付息一次。

| **可选值** | **含义** |
| --- | --- |
| 1 / 1y | 表示每年付息1次 |
| 2 / 6M | 表示每年付息2次 / 每6个月付息1次 |
| 3 / 4M | 表示每年付息3次 / 每4个月付息1次 |
| 4 / 3M | 表示每年付息4次 / 每3个月付息1次 |
| 6 / 2M | 表示每年付息6次 / 每2个月付息1次 |
| 12 / 1M | 表示每年付息12次 / 每月付息1次 |
| 13 / 4w | 表示每年付息13次 / 每4周付息1次 |
| 26 / 2w | 表示每年付息26次 / 每2周付息1次 |
| 52 / 1w | 表示每年付息52次 / 每周付息1次 |
| 365 / 1d | 表示每年付息365次 / 每天付息1次 |

**basis** 可选参数，整型或字符串类型的标量或向量，表示要使用的日计数基准类型。可选值为：

| Basis | 日计数基准 |
| --- | --- |
| 0 / "Thirty360US" | US (NASD) 30/360 |
| 1 / "ActualActual" (默认值) | 实际/实际 |
| 2 / "Actual360" | 实际/360 |
| 3 / "Actual365" | 实际/365 |
| 4 / "Thirty360EU" | 欧洲 30/360 |

**convention** 可选参数，字符串标量或向量，用于指定如何调整落在非工作日的现金流支付日期。可选值为：

* 'Following'（默认值）：选择给定假日后的第一个工作日；
* 'ModifiedFollowing'：选择给定假日后的第一个工作日。如果该工作日属于不同的月份，则选择假日前的第一个工作日；
* 'Preceding'：选择给定假日前的第一个工作日；
* 'ModifiedPreceding'：选择给定假日前的第一个工作日。如果该工作日属于不同的月份，则选择假日后的第一个工作日;
* 'Unadjusted'：不作调整；
* 'HalfMonthModifiedFollowing'：选择给定假日后的第一个工作日。如果该工作日跨越了月中（15日）或月末，则选择假日前的第一个工作日；
* 'Nearest'：选择离给定假日最近的工作日。如果前后工作日距离相同，则默认选择后一个工作日。

**method** 可选参数，字符串标量，表示使用的估值方法，目前只支持“binomial”， 即使用二叉树模型（Binomial tree
model）进行估值。

**kwargs** 可选参数，字典标量，表示估值方法对应的其他参数。*method* = 'binomial' 时，*kwargs*应包含成员：

* ‘type’：STRING 类型标量或向量，指定二叉树模型的类型，可选值为：
  + 'crr'（默认值）： Cox-Ross-Rubinstein 模型
  + 'jr'：Jarrow-Rudd 模型。
* ‘timeSteps’：INT 类型标量或向量，表示二叉树模型的时间间隔数，默认值为 100。

## 例子

现有五年期可转换债券A：发行日为 2023 年 8 月 28 日，到期日为 2028 年 8 月 28 日，交易日为 2024 年 8 月 28 日。其赎回价格为
100，年息票利率为 0.05，付息频率为每年一次，息差 0.005。合约转股价格为 26，股票现价为 36，分红利率为 0.02，从 2024 年 10 月 28
日起每隔 6 个月分红一次，共分红 6 次。

债券可在 2025 年 8月 28 日和 2027 年 8 月 3 0日分别按 101.5 和 100.85 价格赎回，或者在 2026 年 8 月 28 日按 105
价格回售。市场无风险利率为 0.06，波动率为 0.2。日计数基准为 Actual365，把非工作日调整到工作日的方法为
ModifiedFollowing。交易日历为上海证交所（XSHG）。

分别计算欧式和美式两种可行权时间类型下，该债券的含息价格。

```
spot = 36.0
conversionPrice = 26.0
redemption = 100
spread = 0.005
divYield = 0.02
riskFree = 0.06
volatility = 0.20
issue = 2023.08.28
settlement = 2024.08.28
maturity = 2028.08.28
convention = `ModifiedFollowing
calendar = `XSHG
style = [`european, `american]
frequency = 1
coupon = 0.05
basis = 3
divFreq = 6M
nextDivDate = 2024.10.28
divDates = []
for (i in 0..5) {
	divDates.append!(nextDivDate)
	nextDivDate = temporalAdd(nextDivDate, divFreq)
}
divDates = divDates$DATE
callDates = [2025.08.28, 2027.08.30]
callPrices = [101.5, 100.85]
putDates = [2026.08.28]
putPrices = [105.0]
convertibleFixedRateBondDirtyPrice(settlement, issue, maturity, redemption, coupon, spread, riskFree, volatility, spot, conversionPrice, divYield, divDates, callDates, callPrices, putDates, putPrices, style, calendar, frequency, basis, convention)
// [100.14675326378128,138.45755887077215]
```

