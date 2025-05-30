# vectorAR

## 语法

`vectorAR(ds, endogColNames, [exog], [trend='c'], [maxLag],
[ic])`

## 详情

使用向量自回归模型（Vector Autoregression model，简称 VAR 模型）来分析多变量时间序列。

## 参数

**ds** 一张内存表、或者一个 DataSource 类型构成的向量，包含需要分析的多变量时间序列。注意：不可为空。

**endogColNames** 字符串向量，表示需要分析的内生变量(endogenous variable)在 *ds* 中所对应的列名。通过
*endogColNames* 从 *ds* 中取出的列组成的矩阵，即为需要分析的多变量时间序列数据。

**exog** 可选参数，数值矩阵，表示时间序列数据之外的外生变量。矩阵每一列表示一个外生变量的时间序列数据，矩阵行数为时间序列样本数，须与 *ds*
的行数相等。

**trend** 可选参数，表示在回归中使用的常数和趋势阶数。可选值为：

* 'c'：只使用常数，默认值。
* 'ct'：使用常数和趋势。
* 'ctt'：使用常数、线性趋势和二次趋势。
* 'n'：不适用常数和趋势。

**maxLag** 可选参数，非负整数标量，表示在选择阶数时使用的最大滞后期。传入空值或不填时使用默认值：![](../images/vectorar.png) ，nobs 表示样本数量。

**ic** 可选参数，字符串标量，表示在选择阶数时使用的信息准则类型，默认值为空值。可选值为：

* 'aic'：Akaike 信息准则。
* 'bic'：Bayesian 信息准则。
* 'fpe'：Final prediction error，最终预测误差准则。
* 'hqic'：Hannan-Quinn 信息准则。

## 返回值

返回一个字典，表示向量自回归模型的分析结果，字典有以下成员：

* params：浮点数矩阵，表示向量自回归模型拟合得到的参数。
* kAr：整数标量，表示向量自回归过程的阶数。
* kTrend：整数标量，表示向量自回归过程的趋势数。
* nobs：整数标量，表示向量自回归模型分析过程中的观测数量。
* sigmaU：浮点数矩阵，表示白噪声过程方差的估计值。
* sigmaUMle：浮点数矩阵，表示噪声过程协方差的有偏最大似然估计值。
* aic：浮点数标量，表示 Akaike 信息准则。
* bic：浮点数标量，表示 Bayesian 信息准则。
* hqic：浮点数标量，表示 Hannan-Quinn 信息准则。
* fpe：浮点数标量，表示最终预测误差信息准则。
* llf：浮点数标量，表示向量自回归模型的对数似然值。

## 例子

本例提供一个 [macrodata.csv](../data/macrodata.csv) 文件。取该文件中
realgdp, realcons, realinv 三列作为内生变量，并设置最大滞后期 *maxlag* 为 2，使用 VAR
模型来分析其多变量时间序列。

```
data = loadText("macrodata.csv")//该文件需要另外下载，请点击上方文本内的链接
vectorAR(data, [`realgdp, `realcons, `realinv],,,2)

/*
output:
nobs->200
hqic->-27.789187688321
llf->1962.570824044325
kTrend->1
aic->-27.929339439671
fpe->0E-12
params->
#0              #1              #2
0.001526972352  0.005459603048  -0.023902520885
-0.279434735873 -0.100467978082 -1.970973673795
0.675015751748  0.268639552522  4.414162326990
0.033219450793  0.025738726522  0.225478953223
0.008221084912  -0.123173927706 0.380785849237
0.290457628129  0.232499435917  0.800280917529
-0.007320907532 0.023503761040  -0.124079061576
sigmaU->
#0             #1             #2
0.000057113648 0.000029839495 0.000224637467
0.000029839495 0.000042830532 0.000034191732
0.000224637467 0.000034191732 0.001567709895
sigmaUMle->
#0             #1             #2
0.000055114670 0.000028795112 0.000216775156
0.000028795112 0.000041331464 0.000032995021
0.000216775156 0.000032995021 0.001512840049

kAr->2
bic->-27.583016116183
*/
```

