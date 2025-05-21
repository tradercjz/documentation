import QuantLib as ql

# 假设要为 EURUSD的down-and-out看跌障碍期权进行定价，其行权价为1.1，即期汇率为1.12，欧元无风险利率为0.71764, 美元无风险利率为3.85%，名义本金为1000000， 估值日为2023年7月20日，交割日为2023年7月22日，到期日为2023年7月24日，最后交付日为2023年7月27日，障碍汇率为1.05， atm波动率为12.48。

# 首先，将后续计算需要使用到的一些期权合约的基础信息以及市场数据列出来，具体如下：
today = ql.Date(20, ql.July, 2023)
ql.Settings.instance().evaluationDate = today

# option specification
# underlying ： "EURUSD"
option_type = ql.Option.Put
strike = 1.10
barrier_type = ql.Barrier.DownOut
barrier = 1.05
payoff_amt = 1000000.0
trade_dt = ql.Date(20, 7, 2023)
settle_dt = ql.Date(22, 7, 2023)
expiry_dt = ql.Date(24, 7, 2023)
delivery_dt = ql.Date(27, 7, 2023)

# market data
spot = 1.12
vol_atm = 12.48
eur_depo = 0.72
usd_depo = 3.85

# simple quotes
spot_quote = ql.SimpleQuote(spot)
vol_atm_quote = ql.SimpleQuote(vol_atm / 100)
eur_depo_quote = ql.SimpleQuote(eur_depo / 100)
usd_depo_quote = ql.SimpleQuote(usd_depo / 100)

# 构建期限结构,使用ql.FlatForward方法分别根据EUR和USD的无风险利率构建出EUR,USD的无风险利率曲线；使用Black Volatility9（即ql.BlackConstantVol方法），基于当前市场上的ATM波动率构建出波动率曲线：

# term structures
# rates
domesticTS = ql.FlatForward(0, ql.UnitedStates(ql.UnitedStates.Settlement), 
            ql.QuoteHandle(eur_depo_quote), ql.Actual360())
foreignTS = ql.FlatForward(0, ql.UnitedStates(ql.UnitedStates.Settlement), 
            ql.QuoteHandle(usd_depo_quote), ql.Actual360())
# vol 
expanded_volTS = ql.BlackConstantVol(
    0,ql.UnitedStates(ql.UnitedStates.Settlement), ql.QuoteHandle(vol_atm_quote), ql.Actual360())


# 配置出基于exercise和payoff行权条款的欧式down-and-out看跌障碍期权option：
payoff = ql.PlainVanillaPayoff(option_type, strike)
exercise = ql.EuropeanExercise(expiry_dt)
option = ql.BarrierOption(barrier_type, barrier, 0.0, payoff, exercise)

# 将上边生成的利率和波动率曲线期限结构对象封装到YieldTermStructureHandle中，并带入GK模型构建出即期汇率的随机过程：
process = ql.GarmanKohlagenProcess(
    ql.QuoteHandle(spot_quote),
    ql.YieldTermStructureHandle(foreignTS),
    ql.YieldTermStructureHandle(domesticTS),
    ql.BlackVolTermStructureHandle(expanded_volTS),
)

# 上边的一些公用方法和参数配置完成后，就可以分别构建出不同的障碍期权定价引擎

# 4.1 方法一：基于Binomial的障碍期权定价引擎
Binomialengine = ql.BinomialBarrierEngine(process, "crr", 200)
option.setPricingEngine(Binomialengine)
print("Premium is:", option.NPV()*payoff_amt/spot)
# 得到障碍期权的价格为：
# Premium is: 540.3877576005641

# 4.2 方法二：基于BlackScholes过程的障碍期权定价引擎
fdBarrierEngine = ql.FdBlackScholesBarrierEngine(process)
option.setPricingEngine(fdBarrierEngine)
print("Premium is:", option.NPV()*payoff_amt/spot)
# 得到障碍期权的价格为：
# Premium is: 542.7204738124419

# 4.3 方法三：基于Analytic模型的障碍期权定价引擎
engine = ql.AnalyticBarrierEngine(process)
option.setPricingEngine(engine)
print("Premium is:", option.NPV()*payoff_amt/spot)
# 得到障碍期权的价格为：
# Premium is: 540.8117280028365
