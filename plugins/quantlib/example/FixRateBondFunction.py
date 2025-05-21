import QuantLib as ql

# 1. Construct a Yield Curve (ZeroCurve class)
calc_date = ql.Date(15, 1, 2015)
ql.Settings.instance().evaluationDate = calc_date
spot_dates = [ql.Date(15, 1, 2015), ql.Date(15, 7, 2015), ql.Date(15, 1, 2016)]
spot_rates = [0.0, 0.005, 0.007]
day_count = ql.Thirty360(ql.Thirty360.BondBasis)
calendar = ql.UnitedStates(ql.UnitedStates.NYSE)
interpolation = ql.Linear()
compounding = ql.Compounded
compounding_frequency = ql.Annual
spot_curve = ql.ZeroCurve(spot_dates, spot_rates, day_count, calendar, 
                    interpolation, compounding, compounding_frequency)
spot_curve_handle = ql.YieldTermStructureHandle(spot_curve)

# 2. Build a fixed rate bond object
issue_date = ql.Date(15, 1, 2015)
maturity_date = ql.Date(15, 1, 2016)
tenor = ql.Period(ql.Semiannual)
calendar = ql.UnitedStates(ql.UnitedStates.NYSE)
business_convention = ql.Unadjusted
date_generation = ql.DateGeneration.Backward
month_end = False
schedule = ql.Schedule(issue_date, maturity_date, tenor, calendar, 
              business_convention, business_convention ,
               date_generation, month_end)

# 3. Create FixedRateBond instrument
coupon_rate = .06
coupons = [coupon_rate]
settlement_days = 0
face_value = 100
fixed_rate_bond = ql.FixedRateBond(settlement_days, face_value, schedule,
                  coupons, day_count)

# 4. A valuation engine in order to price this bond
bond_engine = ql.DiscountingBondEngine(spot_curve_handle)
fixed_rate_bond.setPricingEngine(bond_engine)

# 5. Bond Calculation and Pricing
# a. CashFlow
for cf in fixed_rate_bond.cashflows():
    print(cf.date().ISO(), cf.amount())
    
# b. Basic Information
print(fixed_rate_bond.settlementDate())
print(fixed_rate_bond.maturityDate())

# c. NPV
fixed_rate_bond.NPV()

# d. Clean Price and Dirty Price
fixed_rate_bond.cleanPrice()
fixed_rate_bond.dirtyPrice()

# e. Accrued Interest
fixed_rate_bond.accruedAmount()

# f. BondYield
bondYield = fixed_rate_bond.bondYield(day_count, compounding, compounding_frequency)
print(bondYield)

# 6. BondFunctions
# BondFunctions提供了一系列用于债券定价和计算的函数。这些函数通过对债券对象和其他参数进行操作，提供了估值和分析债券的工具。

# Duration

ql.BondFunctions.duration(
    fixed_rate_bond,
    bondYield,
    day_count,
    compounding,
    compounding_frequency)

# BondFunctions 的 duration 函数可以计算三种久期，分别是简单久期（Simple）、麦考利久期（Macaulay）和修正久期（Modified），只需配置久期类型参数即可，默认计算的是修正久期。

# 程序实现上，麦考利久期的计算依赖于修正久期。

# 所谓简单久期，即现金流的期限关于现金流贴现值的加权平均。如果计息方式是复利，简单久期等于麦考利久期。不过，如果是连续复利，计算麦考利久期将会报错，简单久期依然可以计算出来，更有普适性。连续复利的情况下，简单久期等于修正久期。

durationSimple = ql.BondFunctions.duration(
    fixed_rate_bond,
    bondYield,
    day_count,
    compounding,
    compounding_frequency,
    ql.Duration.Simple)
 
durationModified = ql.BondFunctions.duration(
    fixed_rate_bond,
    bondYield,
    day_count,
    compounding,
    compounding_frequency,
    ql.Duration.Modified) #默认
 
durationMacaulay = ql.BondFunctions.duration(
    fixed_rate_bond,
    bondYield,
    day_count,
    compounding,
    compounding_frequency,
    ql.Duration.Macaulay) 
 
# Convexity

ql.BondFunctions.convexity(
    fixed_rate_bond,
    bondYield,
    day_count,
    compounding,
    compounding_frequency)

# BPS

# BondFunctions 的函数可以计算三种BPS

# basisPointValue函数计算的是债券价格相对于1个基点利率变动的变化量，并根据债券的久期进行调整。

# yieldValueBasisPoint函数计算的是基点变动引起的债券价格变动的绝对值。

# bps函数计算的是债券价格相对于1个基点利率变动的绝对变化量，也被称为基点价值。


ql.BondFunctions.basisPointValue(
    fixed_rate_bond,
    bondYield,
    day_count,
    compounding,
    compounding_frequency)

ql.BondFunctions.bps(
    fixed_rate_bond,
    bondYield,
    day_count,
    compounding,
    compounding_frequency)

ql.BondFunctions.yieldValueBasisPoint(
    fixed_rate_bond,
    bondYield,
    day_count,
    compounding,
    compounding_frequency) 

# 后续函数为方便查看输出结果，重新构建一个FixedRateBond
s = ql.Schedule(ql.Date(15, 12, 2019), ql.Date(15, 12, 2024), ql.Period('1Y'), ql.TARGET(), ql.Unadjusted, ql.Unadjusted, ql.DateGeneration.Backward, False)
bond = ql.FixedRateBond(2, 100.0, s, [0.05], ql.ActualActual(ql.ActualActual.Bond))

# Date Inspectors
print(ql.BondFunctions.startDate(bond))
print(ql.BondFunctions.maturityDate(bond))
print(ql.BondFunctions.isTradable(bond))
 
# Cashflow Inspectors
print(ql.BondFunctions.previousCashFlowDate(bond, ql.Date(15,12,2020)))
print(ql.BondFunctions.previousCashFlowAmount(bond, ql.Date(15,12,2020)))
print(ql.BondFunctions.nextCashFlowDate(bond, ql.Date(15,12,2020)))
print(ql.BondFunctions.nextCashFlowAmount(bond, ql.Date(15,12,2020)))

# Coupon Inspectors
print(ql.BondFunctions.previousCouponRate(bond))
print(ql.BondFunctions.nextCouponRate(bond))
print(ql.BondFunctions.accrualStartDate(bond))
print(ql.BondFunctions.accrualEndDate(bond))
print(ql.BondFunctions.accrualPeriod(bond))
print(ql.BondFunctions.accrualDays(bond))
print(ql.BondFunctions.accruedPeriod(bond))
print(ql.BondFunctions.accruedDays(bond))
print(ql.BondFunctions.accruedAmount(bond))

# YieldTermStructure

crv = ql.FlatForward(2, ql.TARGET(), 0.04, ql.Actual360())
print(ql.BondFunctions.cleanPrice(bond, crv))
print(ql.BondFunctions.bps(bond, crv))
print(ql.BondFunctions.atmRate(bond, crv))

# 计算给定固定利率债券（bond）在指定收益率曲线（crv）下的净价（Clean Price）等。

# Yield (a.k.a. Internal Rate of Return, i.e. IRR) functions

rate = ql.InterestRate(0.05, ql.Actual360(), ql.Compounded, ql.Annual)
print(ql.BondFunctions.cleanPrice(bond, rate))
print(ql.BondFunctions.bps(bond, rate))
print(ql.BondFunctions.duration(bond, rate))
print(ql.BondFunctions.convexity(bond, rate))
print(ql.BondFunctions.basisPointValue(bond, rate))
print(ql.BondFunctions.yieldValueBasisPoint(bond, rate))

# 计算给定固定利率债券（bond）在指定利率（rate）下的净价（Clean Price）等。

# Z-spread functions

crv = ql.FlatForward(2, ql.TARGET(), 0.04, ql.Actual360())
print(ql.BondFunctions.zSpread(bond, 101, crv, ql.Actual360(), ql.Compounded, ql.Annual))
