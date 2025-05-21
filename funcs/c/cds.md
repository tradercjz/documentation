# cds

## 语法

`cds(settlement, maturity, evalDate, notional, spread, riskFree, recovery,
isSeller, frequency, calendar, [convention='Following'],
[termDateConvention='Following'], [rule='CDS'], [basis=1])`

## 详情

本函数对信用违约互换（Credit Default Swap，CDS）进行估值计算。成功执行后将返回 CDS 的估值，是一个 DOUBLE 类型的标量或向量。

## 参数

**settlement** DATE 类型标量或向量，表示 CDS 合约的生效日。

**maturity** DATE 类型标量或向量，表示 CDS 合约的到期日。

注意：*settlement*应早于对应的 *maturity*。

**evalDate**DATE 类型标量或向量，表示估值日。

注意：*evalDate* 不应晚于对应的 *settlement*。

**notional**数值类型标量或向量，非负数，表示 CDS 合约的名义本金。

**spread** 数值类型标量或向量，表示 CDS 利差，是 CDS 买方每期需支付给 CDS 卖方的金额，以 CDS
的名义本金的百分比形式报价，以基点（bps）表示。

**riskFree**数值类型标量或向量，非负数，表示无风险利率。

**recovery**数值类型标量或向量，表示回收率，有效范围是(0,1)，指的是在发生信用事件（如违约）后，债券持有人预计能够收回的金额占违约债券面值的百分比。

**isSeller** 整数类型标量或向量，表示交易方为买方还是卖方，有两个可选值：

* 1：表示交易方为卖方。
* 0：表示交易方为卖方。

**frequency** 表示买方向卖方支付金额的频率，支持两种输入类型：

* 整数标量或向量：表示买方每年向卖方支付金额的次数；比如输入 1，表示每年付息 1 次，即按年支付；输入 2，表示每年付息 2 次，即按半年期支付。
* DURATION 标量或向量：表示买方每隔多久向卖方进行一次支付。比如输入 duration(`3M)，表示每隔 3 个月支付一次，即按季度支付。

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

* 'Following'：表示选择给定假日后的第一个工作日，默认值。
* 'ModifiedFollowing'：表示选择给定假日后的第一个工作日，除非该工作日属于不同的月份，此时应选择假日前的第一个工作日。
* 'Preceding'：表示选择给定假日前的第一个工作日。
* 'ModifiedPreceding'：表示选择给定假日前的第一个工作日，除非该工作日属于不同的月份，此时应选择假日后的第一个工作日。
* 'Unadjusted'：表示不做调整。
* 'HalfMonthModifiedFollowing'：表示选择给定假日后的第一个工作日，除非该工作日跨越了月中（15
  日）或月末，此时应选择假日前的第一个工作日。
* 'Nearest'：表示选择离给定假日最近的工作日。如果前一个和后一个工作日距离给定假日同样远，则默认选择后一个工作日。

**termDateConvention** 可选参数，字符串标量或向量，表示如果最后一个日期是非工作日，将其调整到工作日的方法，可选值同
convention。默认值为'Following'。

**rule** 可选参数，字符串标量或向量，表示日期列表的生成规则，可选值为：

* 'Backward'：表示从终止日期向生效日期倒向生成。
* 'Forward'：表示从生效日期向终止日期正向生成。
* 'Zero'：表示在生效日期和终止日期之间不生成中间日期。
* 'ThirdWednesday'：表示除了生效日期和终止日期，其他日期落在当月的第三个星期三（正向生成）。
* 'ThirdWednesdayInclusive'：表示所有日期，包括生效日期和终止日期，均落在当月的第三个星期三（正向生成）。
* 'Twentieth'：表示除生效日期外，所有日期均落在当月 20 日（用于新兴市场 CDS 时间表）。终止日期也相应调整。
* 'TwentiethIMM'：表示除生效日期外，所有日期均落在 IMM（International Money Market）月份的 20 日（用于
  CDS 时间表）。终止日期也相应调整。
* 'OldCDS'：表示除生效日期外，所有日期均落在 IMM（International Money Market）月份的 20
  日（用于CDS时间表）。终止日期也相应调整。但日期端点不受限制，并允许短尾或长尾票息期（旧 CDS 惯例）。
* 'CDS'：表示使用[自 2009
  年“大爆炸”改革以来的信用衍生品标准规则](https://www.isda.org/2009/03/12/big-bang-protocol/)。默认值。
* 'CDS2015'：表示[使用自 2015 年 12 月 20
  日以来的信用衍生品标准规则](https://www.isda.org/2015/07/07/amending-when-single-name-cds-roll-to-new-on-the-run-contracts/)。

**basis** 可选参数，整型或 STRING 类型的标量或向量，表示要使用的日计数基准类型。可选值为：

| Basis | 日计数基准 |
| --- | --- |
| 0 / "Thirty360US" | US (NASD) 30/360 |
| 1 / "ActualActual" (默认值) | 实际/实际 |
| 2 / "Actual360" | 实际/360 |
| 3 / "Actual365" | 实际/365 |
| 4 / "Thirty360EU" | 欧洲 30/360 |

注意：如果输入参数中，部分为标量，其余为向量时，则会将标量当作与向量长度相同、所有元素值等于该标量的向量；且所有向量的长度必须一致。

## 例子

自定义参数，计算 CDS 的估值。

```
valDate = 2007.05.15
settlement = 2007.05.16
maturity = 2007.08.16
notional = 1000000.0
spread = 0.0150
riskFreeRate = 0.01
recoveryRate = 0.5
isSeller = true
frequency = 4
convention = 'Following'
termDateConvention = 'Unadjusted'
rule = 'TwentiethIMM'
basis = 3
cds(settlement, maturity, valDate, notional, spread, riskFreeRate, recoveryRate, isSeller, frequency, 'CCFX', convention, termDateConvention, rule, basis)
// Output: -5.448913728297157
```

