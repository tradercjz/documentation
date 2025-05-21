# irs

## 语法

```
irs(settlement, resetInterval, start, maturity, notional, fixedRate, spread, curve, frequency, calendar, [convention='ModifiedFollowing'], [basis=1], [rateType=0])
```

## 描述

本函数返回对于浮动利率支付方的利率互换估值，该估值是一个 DOUBLE 类型的标量或向量。

利率互换是一种金融交易，交易双方同意交换未来一段时间内的利率支付流，一方支付固定利率，另一方支付浮动利率（通常是基于某个利率基准，如
SHIBOR），持续多个周期，直到合约结束。市场上的利率互换产品的互换间隔有1个月、3个月、半年、一年等。

## 参数

**settlement** DATE 类型标量或向量，表示交易日，即利率互换估值日。

**resetInterval** DURATION 标量或向量，表示利率的重置间隔。比如对于标的利率 FR007 来说，resetInterval 应设置为
7d，表示每 7 天重置一次利率。

**start** DATE 类型标量或向量，表示第一次利率互换的日期。

**maturity** DATE 类型标量或向量，表示最后一次利率互换的日期。

**notional** 数值型标量或向量，表示利率互换所基于的本金。

**fixedRate** 数值型标量或向量，表示利率互换中固定利率支付方所支付的利率，在整个利率互换期间该利率不变。

**spread** 数值型标量或向量，表示浮动利率的利差。

**curve** 字典类型标量或向量，表示拟合后的利率曲线。

**frequency** 表示利率互换的频率，支持两种输入类型：

* 整型标量或向量：表示一年内进行利率互换的次数；比如输入 1，表示每年互换 1 次；输入 2，表示每年互换 2 次。
* DURATION 标量或向量：表示隔多久进行一次利率互换。比如输入 3M，表示每隔 3 个月互换一次。

| 可选值 | 含义 |
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

**calendar** 字符串类型标量或向量，表示使用的市场日历类型，请参阅[交易日历](../../modules/MarketHoliday/mkt_calendar.html#11-%E6%9F%A5%E8%AF%A2%E4%BA%A4%E6%98%93%E6%97%A5%E5%8E%86-getmarketcalendar)。

**convention** 可选参数，字符串标量或向量，表示把非工作日调整到工作日的方法，可选值为：

* 'Following'：表示选择给定假日后的第一个工作日。
* 'ModifiedFollowing'：表示选择给定假日后的第一个工作日，除非该工作日属于不同的月份，此时应选择假日前的第一个工作日，默认值。
* 'Preceding'：表示选择给定假日前的第一个工作日。
* 'ModifiedPreceding'：表示选择给定假日前的第一个工作日，除非该工作日属于不同的月份，此时应选择假日后的第一个工作日。
* 'Unadjusted'：表示不作调整。
* 'HalfMonthModifiedFollowing'：表示选择给定假日后的第一个工作日，除非该工作日跨越了月中（15日）或月末，此时应选择假日前的第一个工作日。
* 'Nearest'：表示选择离给定假日最近的工作日。如果前一个和后一个工作日距离给定假日同样远，则默认选择后一个工作日。

**basis** 可选参数，整型或 STRING 类型的标量或向量，表示要使用的日计数基准类型。如果省略此参数，则使用默认值 1。可选值为：

| Basis | 日计数基准 |
| --- | --- |
| 0 / "Thirty360US" | US (NASD) 30/360 |
| 1 / "ActualActual" (默认值) | 实际/实际 |
| 2 / "Actual360" | 实际/360 |
| 3 / "Actual365" | 实际/365 |
| 4 / "Thirty360EU" | 欧洲 30/360 |

**rateType** 可选参数，整型或 STRING 类型的标量或向量，表示估值过程使用的复利类型，可选值为：

* 0 / "CC"：表示使用连续复利，默认值。
* 1 / "C"：表示使用普通复利。

注意：如果输入参数中，部分为标量，其余为向量时，则会将标量当作与向量长度相同，所有元素值等于该标量的向量。所有向量的长度必须一致。

## 例子

本例为 2023 年 7 月 10 日交易的一笔利率互换进行估值。其本金为 100 万人民币，利率互换频率为每周一次，2023 年 1 月 10
日进行第一次互换，5年后（2028 年 1 月 10 日）到期，采用上交所的交易日历。固定利率为 2.765%，浮动利率规定在
*curveRateValue*中，日计数基准为 US (NASD)
30/360，估值过程使用连续复利。

```
settlement = 2023.07.10
calendar = `SSE
day0 = temporalAdd(settlement, 0, calendar)
curveRateTime = [10y, 14d, 1d, 1M, 1y, 2y, 3M, 3y, 4y, 5y, 6M, 7d, 7y, 9M]
curveRateValue = [ 2.7013, 1.8, 1.27, 1.9425, 2.0263, 2.1265, 1.9725, 2.2438, 2.3575, 2.4538, 1.9938, 1.86, 2.5863, 2.0088] * 0.01
dates = []
for (dur in curveRateTime) {
	dates.append!(temporalAdd(settlement, dur))
}
X = (dates - day0)$INT
// a curve for base rate (without spread)
curve = linearInterpolateFit(X, curveRateValue)
resetIntv = 7d
startDay = 2023.01.10
endDay = 2028.01.10
par = 100.0
fixRate = 0.02765
spread = 0.0
freq = 3M
basis = 0
irs(settlement, resetIntv, startDay, endDay, par, fixRate, spread, curve, freq, calendar, basis=basis)
// -1.5451083233900798
```

