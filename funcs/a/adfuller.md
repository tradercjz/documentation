# adfuller

## 语法

`adfuller(X, [maxLag], [regression="c"],
[autoLag="aic"], [store=false], [regResults=false])`

## 详情

进行 Augmented Dickey-Fuller (ADF) 单位根检验。用于在序列相关性存在的情况下测试单变量过程中是否存在单位根。

以字典的形式输出 ADF 检验的结果，字典包括以下内容：

* adfStat：浮点数标量，表示检验的统计值
* pValue：浮点数标量，表示 MacKinnon 近似 p 值
* usedLag：整数标量，使用的滞后期的数值
* nobs：整数标量，用于 ADF 回归和关键值计算的观测数量
* criticalValues：字典，在 1％、5％ 和 10％ 水平上的检验统计量的临界值
* icBest：浮点数标量，仅在 autoLag 不设置为"max" 时返回，表示最大化的信息准则
* resultStore：字典，当 regResults 或者 store 设置为 true 时，把回归结果保存在 resultStore 中返回

## 参数

**X** 数值向量，表示需要进行单位根检验的时间序列数据。*X* 中的所有元素不能完全相同且不能包含空值。

**maxLag** 非负整数，指定检验中使用的最大滞后期，默认值为 12\*(nobs/100)^(1/4)，其中 nobs 代表样本数量。

**regression** 字符串，指定在回归中使用的常数和趋势阶数。取值有如下选择：

* "c"：默认值，表示只使用常数。
* "ct：使用常数和趋势。
* "ctt"：使用常数、线性趋势和二次趋势。
* "n"：不使用常数和趋势。

**autoLag** 字符串，指定在 0~maxLag 中自动确定滞后期长度时使用的方法。取值有如下选择：

* "aic"：默认值，表示使用 Akaike Information Criterion 来确定滞后期数值。
* "bic"：表示使用 Bayesian information criterion 来确定滞后期数值。
* "tstat"：将滞后期初始值设为 maxLag，然后逐步减 1，直到上一个滞后期数值的 t 统计量在 5% 显著性水平上显著。
* "max"：将滞后期数值设置为 maxLag。

**store**：布尔标量。设置为 true 时，除了返回 ADF 统计值，还会把回归结果放在一个字典中返回。默认值为 false。

**regResults**：布尔值。设置为 true 时，返回完整的回归结果，相比于 *store*=true 的结果额外包含一个字典
autoLagResult，记录在自动滞后阶数选择过程中使用的信息准则的结果。默认值为 false。

## 例子

```
data = 234 267 289 301 312 323 334 345 356 367
adfuller(data);
```

输出为字典：

```
pValue->0.000375626192024
usedLag->0
nobs->9
icBest->-195.234657936244450
adfStat->-4.341905848945339
criticalValues->[-4.473135048010974,-3.289880603566529,-2.772382345679012]
```

