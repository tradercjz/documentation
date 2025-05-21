import QuantLib as ql

dates = [ql.Date(5000), ql.Date(100000)]
yields = [0.24, 0.75]
dayCounter = ql.Actual360()
calendar = ql.UnitedStates(ql.UnitedStates.NYSE)
linear = ql.Linear()
compounding = ql.Continuous
frequency = ql.Annual

curve = ql.ZeroCurve(dates, yields, dayCounter, calendar, linear, compounding, frequency)

date = ql.Date(40000)

print(curve.zeroRate(date, dayCounter, compounding, frequency).rate())
