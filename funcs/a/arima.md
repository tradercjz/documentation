# arima

## 语法

`arima(ds, endogColName, order, [seasonalOrder], [exog], [trend],
[enforceStationarity=true], [enforceInvertibility=true],
[concentrateScale=false], [trendOffset=1], [maxIter=50])`

## 详情

差分整合移动平均自回归（ARIMA, Autoregressive Integrated Moving
Average）模型是一种单变量时间序列分析模型，主要由三部分构成，分别为自回归模型（AR）、差分过程（I）和移动平均模型（MA）。

`arima` 函数是 ARIMA 类模型的通用接口，可以通过 `arima`
函数构建以下时间序列分析模型：

* 自回归模型 AR：用于捕捉数据与其历史值的关系
* 移动平均模型 MA：专注于处理随机波动
* 自回归移动平均模型 ARMA
* 差分整合移动平均自回归模型 ARIMA
* 季节性模型 SARIMA：处理周期性数据
* 整合外部回归变量的带误差项模型 ARIMAX

## 参数

**ds**内存表或数据源（DATASOURCE）向量，指定包含单变量时间序列的数据。

**endogColName** 字符串标量，指定 *ds* 中的列名，该列为待分析的单变量时间序列数据。

**order** 长度为 3 的非负整数向量，表示 ARIMA 模型的 (p, d, q) 阶数。其中，p 表示自回归（AR）部分的阶数，d 表示差分阶数，q
表示移动平均（MA）部分的阶数。

**seasonalOrder** 可选参数。长度为 4 的非负整数向量， 表示季节性 ARIMA 模型的 (P, D, Q, s) 阶数。其中，P，D，Q
分别表示模型中季节性成分的 AR、差分、MA 阶数，s 表示该季节性序列的周期大小。默认值为 [0, 0, 0, 0]，表示无季节性。

**exog** 可选参数。数值矩阵，表示外生变量。矩阵每一列表示一个外生变量的时间序列，矩阵行数为时间序列样本数，与 *ds* 的行数相等。

**trend** 可选参数。字符串标量， 用于控制确定性趋势。可选值为：

* “n”：不使用常量和趋势（当 *d* > 0 或者 D>0 时，以此为默认值）；
* ”c”：仅使用常量（当 *d* = 0 且 D = 0 时，以此为默认值）；
* ”t”：仅使用线性趋势；
* ”ct”：同时使用常量和线性趋势；

**enforceStationarity** 可选参数。BOOL 类型标量， 表示是否强制自回归 AR部分满足平稳性条件。默认值为 true。

**enforceInvertibility** 可选参数。BOOL 类型标量， 表示是否强制移动平均 MA 部分满足可逆性条件。默认值为 true。

**concentrateScale** 可选参数。BOOL 类型标量，
表示是否在似然性之外集中标度（误差项的方差），从而减少一个参数。仅在使用数值最大似然估计时适用。默认值为 false。

**trendOffset** 可选参数。整数类型标量， 指定开始时间趋势值的偏移量。默认值为 1，因此如果 *trend*='t'，则趋势等于 1,
2, ..., nobs。

**maxIter** 可选参数。正整数，表示拟合时最大的迭代次数，默认值为 50。

**返回值**

返回一个字典，表示 ARIMA 模型的拟合结果，包含以下键值：

* params：浮点数向量，表示 ARIMA 模型拟合得到的参数
* llf：浮点数标量，表示 ARIMA 模型的对数似然值
* aic：浮点数标量，表示 Akaike 信息准则
* bic：浮点数标量，表示 Bayesian 信息准则
* hqic：浮点数标量，表示 Hannan-Quinn 信息准则

## 例子

以下代码使用 1959-2009 年的季度经济指标数据，对实际 GDP（`realgdp`）进行 ARIMA 模型拟合。假设通过分析确定使用
ARIMA(1,0,0) 模型，即自回归阶数为 1，无需差分，移动平均阶数为 0：

```
data = loadText("./macrodata.csv")
res = arima(data, "realgdp", [1,0,0]);
res;
/*
params->[0.007795600187477,0.306055792984419,0.000069811276429]
llf->679.783769203580163
aic->-1353.567538407160327
bic->-1343.64273531495678
hqic->-1349.551945119058927
*/
```

[macrodata.csv](../data/arima/macrodata.csv)

