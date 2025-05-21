# 以 200218 为例，计算 2023-07-18 这一天的价格、久期和凸性。

# 价格与现金流
# 首先从中国货币网查询债券的基本信息，用以配置 FloatingRateBond 对象。

# 债券起息日：2020-06-09
# 到期兑付日：2025-06-09
# 债券期限：5 年
# 面值(元)：100.00
# 计息基准：A/A
# 息票类型：附息式浮动利率
# 付息频率：季
# 票面利率（%）：3.1（当前水平）
# 基准利率（%）：3.85（当前水平）
# 基准利差（%）：-0.75
# 基准利率名：LPR1Y
# 利率杠杆：1
# 提前确定利率的天数：1（没有查到该项目，不过此项不影响估值计算）
# 结算方式：T+0（与中债估值的规则保持一致）

import QuantLib as ql
import prettytable as pt
from datetime import date

today = ql.Date(18, ql.July, 2023)
ql.Settings.instance().evaluationDate = today
evalueDate = ql.Settings.instance().evaluationDate

# Schedule Setting
settlementDays = 0
faceAmount = 100.0

effectiveDate = ql.Date(9, ql.June, 2020)
terminationDate = ql.Date(9, ql.June, 2025)
tenor = ql.Period(ql.Quarterly)

#日历采用中国的银行间市场，遇到假期不调整。
calendar = ql.China(ql.China.IB)
convention = ql.Unadjusted
terminationDateConvention = convention
rule = ql.DateGeneration.Backward
endOfMonth = False

schedule = ql.Schedule(
    effectiveDate,
    terminationDate,
    tenor,
    calendar,
    convention,
    terminationDateConvention,
    rule,
    endOfMonth)
 
# QuantLib 中没有挂钩LPR的浮息债的直接实现，但可以用 QuantLib 中的一些组件“模拟”出中债登的估值方法。
# 首先，要把 LPR1Y “想象”成一种类似 Shibor3M 的短期利率。此时的 r 就是最新的 LPR1Y 利率；
# 浮动票息由一个水平的期限结构推算出来，对应利率是 R ，也就是到期利率和点差利率的差（实际上就等于最新的 LPR1Y 利率）；
# 贴现因子也由一个水平的期限结构推算出来，对应利率是 R+y ，也就是到期利率。

# Lastest LPR1Y
nextLpr = 3.55 / 100.0 
nextLprQuote = ql.SimpleQuote(nextLpr)
nextLprHandle = ql.QuoteHandle(nextLprQuote)
fixedLpr = 3.85 / 100.0

compounding = ql.Compounded
frequency = ql.Quarterly
accrualDayCounter = ql.ActualActual(ql.ActualActual.Bond, schedule)
cfDayCounter = ql.ActualActual(ql.ActualActual.Bond)
paymentConvention = ql.Unadjusted
 
# 推算票息和贴现因子的期限结构使用了各自的 day counter，原因出在下面的 IborIndex 上，
# 它和前面的 Schedule 在有关时间的计算上可能产生不一致（不算严重的 bug，算是个quantlib的 flaw）

# 构建平坦远期收益率曲线
cfLprTermStructure = ql.YieldTermStructureHandle(
    ql.FlatForward(
        settlementDays,
        calendar,
        nextLprHandle,
        cfDayCounter,
        compounding,
        frequency))

lprTermStructure = ql.YieldTermStructureHandle(
    ql.FlatForward(
        settlementDays,
        calendar,
        nextLprHandle,
        accrualDayCounter,
        compounding,
        frequency))

lpr3m = ql.IborIndex(
    'LPR1Y',
    ql.Period(3, ql.Months),
    settlementDays,
    ql.CNYCurrency(),
    calendar,
    convention,
    endOfMonth,
    cfDayCounter,
    cfLprTermStructure)

# 由于是对存续债券估值，需要为期限结构添加“历史浮动利率”——历史上 fixing date 上的 LPR1Y 数据。
# 实际上只有最近一次 fixing 的 LPR1Y 利率会参与估值，但我们还是要添加更早期 fixing date 的利率，
# 否则会报错，幸运的是更早期的历史利率不参与估值，可以随便用个数（fixedLpr)来填充，我在这里补充了之前所有的LPR。

lpr3m.addFixing(ql.Date(8, ql.June, 2020), fixedLpr)
lpr3m.addFixing(ql.Date(8, ql.September, 2020), fixedLpr)
lpr3m.addFixing(ql.Date(8, ql.December, 2020), fixedLpr)

lpr3m.addFixing(ql.Date(8, ql.March, 2021), fixedLpr)
lpr3m.addFixing(ql.Date(8, ql.June, 2021), fixedLpr)
lpr3m.addFixing(ql.Date(8, ql.September, 2021), fixedLpr)
lpr3m.addFixing(ql.Date(8, ql.December, 2021), fixedLpr)

lpr3m.addFixing(ql.Date(8, ql.March, 2022), 3.7/100)
lpr3m.addFixing(ql.Date(8, ql.June, 2022), 3.7/100)
lpr3m.addFixing(ql.Date(8, ql.September, 2022), 3.65/100)
lpr3m.addFixing(ql.Date(8, ql.December, 2022), 3.65/100)

lpr3m.addFixing(ql.Date(8, ql.March, 2023), 3.65/100)
lpr3m.addFixing(ql.Date(8, ql.June, 2023), 3.65/100)

# 使用fixing()方法获取指定日期的利率值
fixing_date = ql.Date(8, 6, 2023)
rate = lpr3m.fixing(fixing_date)
print("利率值：", rate)

# 建立FloatingRateBond
bond = ql.FloatingRateBond(
    settlementDays = settlementDays,
    faceAmount = faceAmount,
    schedule = schedule,
    index = lpr3m,
    paymentDayCounter = accrualDayCounter,
    paymentConvention = convention,
    fixingDays = 1,
    gearings = ql.DoubleVector(1, 1.0),
    spreads = ql.DoubleVector(1, -0.75 / 100.0))

bondYield = 2.35 / 100.0
basisSpread = bondYield - nextLpr
basisSpreadQuote = ql.SimpleQuote(basisSpread)
basisSpreadHandle = ql.QuoteHandle(basisSpreadQuote)

# 注：开发不需要考虑，关于计算bondYield。
# 在另一个浮动利率债券的估值实务 中，估值收益率=估值日基准利率+△y+sp，
# △y - 设该债券待偿期为T，点差收益率曲线T期限对应的点差
# 根据点差收益率曲线，利用线性插值和期限求出。
# sp - 估值价差，估值价差sp是根据新券发行利率、每日交易行情、隐含评级等数据计算所得，交易行情数据包括本币交易系统报价/成交价、货币经纪报价/成交价等。
# 计算贴现因子用到了 ZeroSpreadedTermStructure，这里的利差就是点差利率y.

zeroSpreadedTermStructure = ql.YieldTermStructureHandle(
    ql.ZeroSpreadedTermStructure(
        lprTermStructure,
        basisSpreadHandle,
        compounding,
        frequency,
        accrualDayCounter))

zeroSpreadedTermStructure.enableExtrapolation()
engine = ql.DiscountingBondEngine(zeroSpreadedTermStructure)
bond.setPricingEngine(engine)

#CashFlow
cfTab = pt.PrettyTable(['Date', 'Amount'])
 
for c in bond.cashflows():
    dt = date(c.date().year(), c.date().month(), c.date().dayOfMonth())
    cfTab.add_row([dt, c.amount()])
 
cfTab.float_format = '.4'
 
print(cfTab)

cleanPrice = bond.cleanPrice()
dirtyPrice = bond.dirtyPrice()
accruedAmount = bond.accruedAmount()
 
tab = pt.PrettyTable(['item', 'value'])
tab.add_row(['clean price', cleanPrice])
tab.add_row(['dirty price', dirtyPrice])
tab.add_row(['accrued amount', accruedAmount])
 
tab.float_format = '.4'
 
print(tab)
