import QuantLib as ql

rate = ql.InterestRate(0.05, ql.Actual360(), ql.Compounded, ql.Annual)
print(rate.discountFactor(ql.Date(367), ql.Date(109574)))
print(rate.compoundFactor(ql.Date(367), ql.Date(109574)))
print(rate.rate())
print(rate.dayCounter())
print(rate.compounding())
print(rate.frequency())
