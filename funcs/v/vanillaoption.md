# vanillaOption

## 语法

`vanillaOption(settlement, maturity, evalDate, spot, strike, riskFree,
divYield, volatility, isCall, style, basis, calendar, [method="BS"], [kwargs],
[mode=0])`

## 详情

对香草期权（Vanilla Option）进行估值计算。

## 参数

**settlement** DATE 类型标量或向量，表示期权交易日。

**maturity** DATE 类型标量或向量，表示期权到期日。

**evalDate** DATE 类型标量或向量，表示估值日。

**spot** 数值标量或向量，表示标的资产的当前价格。

**strike** 数值标量或向量，表示标的资产的行权价格。

**riskFree** 数值标量或向量，表示无风险利率。

**divYield** 数值标量或向量，表示分红利率。

**volatility** 数值标量或向量，表示波动率。

**isCall** BOOL 标量或向量，表示是看涨期权还是看跌期权：

* true：表示看涨期权（call option）。
* false：表示看跌期权（put option）。

**style** 字符串标量或向量，表示可行权时间的类型，有两个可选值：

* ‘european’：表示欧式期权。
* ‘american’：表示美式期权。

**basis** 整型或 STRING 类型的标量或向量，表示要使用的日计数基准类型。可选值为：

| Basis | 日计数基准 |
| --- | --- |
| 0 / "Thirty360US" | US (NASD) 30/360 |
| 1 / "ActualActual" (默认值) | 实际/实际 |
| 2 / "Actual360" | 实际/360 |
| 3 / "Actual365" | 实际/365 |
| 4 / "Thirty360EU" | 欧洲 30/360 |

**calendar** 字符串类型标量或向量，表示使用的市场日历类型，请参阅[交易日历](../../modules/MarketHoliday/mkt_calendar.html#11-%E6%9F%A5%E8%AF%A2%E4%BA%A4%E6%98%93%E6%97%A5%E5%8E%86-getmarketcalendar)。

**method** 可选参数，字符串标量，表示使用的期权估值方法，可选值有：

* ‘BS’：表示 Black-Scholes 方法，默认值，只能用于欧式期权估值。
* 'FDBS'：表示结合有限差分法（Finite Difference Method, FDM）和 Black-Scholes 方法的数值求解方法。
* 'heston'：表示 Heston 模型方法，只能用于欧式期权估值。
* 'FDHeston'：表示结合有限差分法（Finite Difference Method, FDM）和 Heston 模型方法的数值求解方法。
* 'PTDHeston'：表示分段时间依赖的 Heston 模型方法。分段时间依赖：Piecewise Time
  Dependent，PTD。该方法只能用于欧式期权估值。

**kwargs** 可选参数，字典标量，表示期权估值的其他参数，不同的估值方法有不同的参数要求。当 method =
'BS'时无需填写该参数，其他方法的具体参数要求如下：

* method = 'FDBS'，kwargs应包含以下成员：

  + 'xGrid'：整数标量或向量，表示有限差分法在进行离散化时使用的空间网格数；xGrid 应大于 1。
  + 'tGrid'：整数标量或向量，表示有限差分法在进行离散化时使用的时间网格数。tGrid 应大于 0。
  + 'dampingSteps'：整数标量或向量，表示有限差分求解过程中应用的阻尼步骤数。dampingSteps 应大于等于 0。
* method = 'heston'，kwargs应包含以下成员：

  + 'theta'：数值标量或向量，表示波动率平方的长期均值。
  + 'kappa'：数值标量或向量，表示波动率平方的均值回归速度。
  + 'rho'：数值标量或向量，表示资产价格和波动率的相关系数。
  + 'sigma'：数值标量或向量，表示波动率的波动率。
* method = 'FDHeston'，kwargs 应包含以下成员：

  + 'theta'：数值标量或向量，表示波动率平方的长期均值。
  + 'kappa'：数值标量或向量，表示波动率平方的均值回归速度。
  + 'rho'：数值标量或向量，表示资产价格和波动率的相关系数。
  + 'sigma'：数值标量或向量，表示波动率的波动率。
  + 'xGrid'：整数标量或向量，表示有限差分法在进行离散化时使用的空间网格数；xGrid 应大于 1。
  + 'vGrid'：整数标量或向量，表示有限差分法在进行离散化时使用的波动率网格数；vGrid 应大于 1。
  + 'tGrid'：整数标量或向量，表示有限差分法在进行离散化时使用的时间网格数；tGrid 应大于等于 0。
  + 'dampingSteps'：整数标量或向量，表示有限差分求解过程中应用的阻尼步骤数。dampingSteps 应大于等于 0。
* method = 'PTDHeston'，kwargs 应包含以下成员：

  + 'times'：数值向量或数组向量，表示条件发生变化的时间点。
  + 'theta'：数值向量或数组向量，表示各时间点对应的波动率平方的长期均值。
  + 'kappa'：数值向量或数组向量，表示各时间点对应的波动率平方的均值回归速度。
  + 'rho'：数值向量或数组向量，表示各时间点对应的资产价格和波动率的相关系数。
  + 'sigma'：数值向量或数组向量，表示各时间点对应的波动率的波动率。
  + 注意：所有成员长度应保持一致。

**mode** 选参数，整型标量或向量，表示输出的模式，可选值为：

* 0：只输出期权净现值（npv only），默认值。
* 1：输出期权的净现值和希腊字母，用元组存储，每个元组中依次存放 npv, delta, gamma, theta, vega 和 rho。
* 2：输出期权的净现值和希腊字母，用有序字典存储。

注意：如果输入参数中，部分为标量，其余为向量时，则会将标量当作与向量长度相同，所有元素值等于该标量的向量。所有向量的长度必须一致。

## 返回值

* 当 mode=0，返回一个浮点数标量或向量，表示期权的净现值。
* 当 mode=1，返回一个浮点数tuple或浮点数tuple构成的向量，表示期权定价结果，包含期权的净现值和希腊字母，顺序是 npv,
  delta, gamma, theta, vega 和 rho。
* 当 mode=2，返回一个字典标量，表示期权定价结果，包含期权的净现值和希腊字母。

  + 'npv'：DOUBLE 类型标量或向量，表示期权的净现值。
  + 'delta'：DOUBLE 类型标量或向量，希腊字母 Delta 衡量期权价格对标的资产价格小幅变化的敏感度。
  + 'gamma'：DOUBLE 类型标量或向量，希腊字母 Gamma 衡量 Delta 随标的资产价格变化的速率。
  + 'theta'：DOUBLE 类型标量或向量，希腊字母 Theta 衡量期权价格随时间流逝（时间衰减）的敏感度。
  + 'vega'：DOUBLE 类型标量或向量，希腊字母 Vega 衡量期权价格对标的资产隐含波动率小幅变化的敏感度。
  + 'rho'：DOUBLE 类型标量或向量，希腊字母 Rho 衡量期权价格对无风险利率小幅变化的敏感度。

## 例子

**例1 使用 BS 方法进行估值**

本例对 1998 年 5 月 17 日至 1999 年 5 月 17 日的期权交易，估值日在 1998 年 5 月 15 日；标的资产的当前价格为 36，行权价格为
40；无风险利率为 6%，无分红，波动率为 2%；可行权时间的类型为欧式看跌期权；使用实际/365 的日计数基准类型，中金所交易日历；使用 Black-Scholes
方法，输出期权的净现值和希腊字母的设定下，对其进行估值计算。

```
settlement = 1998.05.17
maturity = 1999.05.17
valDay = 1998.05.15
spot = 36
strike = 40
riskFree = 0.06
dividend = 0
volatility = 0.2
isCall = false
style = 'european'
basis = 3
calendar = 'CCFX'

vanillaOption(settlement, maturity, valDay, spot, strike, riskFree, dividend, volatility, isCall, style, basis, calendar, mode=2)

/* Output:
npv->[2.080759333948596,2.080759333948596]
delta->[-0.727790750119184,-0.727790750119184]
gamma->[0.130419967911091,0.130419967911091]
theta->[1.274320988976569,1.274320988976569]
vega->[11.951706726567239,11.951706726567239]
rho->[-28.281226338239189,-28.281226338239189]
*/
```

**例2 使用 PTDHeston 方法进行估值**

本例对 1998 年 5 月 17 日至 1999 年 5 月 17 日的期权交易，估值日在 1998 年 5 月 15 日；标的资产的当前价格为 36，行权价格为
40；无风险利率为 6%，无分红，波动率为 2%；可行权时间的类型为欧式看跌期权；使用实际/365 的日计数基准类型，中金所、上交所交易日历；使用 PTDHeston
方法并传入相关参数，只输出期权净现值的设定下，对其进行估值计算。

```
settlement = 1998.05.17
maturity = 1999.05.17
valDay = 1998.05.15
spot = 36
strike = 40
riskFree = 0.06
dividend = 0
isCall = false
times = array(DOUBLE[], 0).append!( [1.0 2.0 3.0, 1.0 2.0 3.0])
volatility = 0.07071
style = 'european'
basis = 3
theta = [0.010, 0.015, 0.02]
kappa = [0.600, 0.500, 0.400]
sigma = [0.400, 0.350, 0.300]
rho = [-0.15, -0.10, -0.00]
calendar = 'CCFX' 'XSHG'
kwargs = dict(STRING,ANY)
kwargs[`times] = times
kwargs[`theta] = theta
kwargs[`kappa] = kappa
kwargs[`sigma] = sigma
kwargs[`rho] = rho
method = 'PTDHeston'
vanillaOption(settlement, maturity, valDay, spot, strike, riskFree, dividend, volatility, isCall, style, basis, calendar, method, kwargs)

// Output: [1.99693345461036,1.99693345461036]
```

