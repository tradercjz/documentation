# garch

## 语法

`garch(ds, endogColName, order, [maxIter=50])`

## 详情

使用广义自回归条件异方差模型（Generalized Autoregressive Conditional Heteroskedasticity，简称 GARCH
模型）来分析单变量时间序列。返回一个字典，表示 GARCH 模型的分析结果，详细说明请参见“返回值”小节。

## 参数

**ds** 一张内存表或者一个 DataSource 类型构成的向量，包含需要分析的单变量时间序列。注意：不可为空。

**endogColName** 字符串标量，表示 *ds* 中需要分析的时间序列所对应的列名。

**order** 长度为 2 的正整数向量，表示 GARCH 模型的阶数。比如 `order=[1,2]` 表示 GARCH 模型的
p=1，q=2，其中 p 为 GARCH 项个数，q 为 ARCH 项阶数。

**maxIter** 可选参数，正整数标量，表示优化时的最大迭代次数，默认值为 50。

## 返回值

返回一个字典，表示 GARCH 模型的分析结果，字典有以下成员：

* volConstant：浮点数标量，表示优化得到的 Vol Constant。
* returnsConstant：浮点数标量，表示优化得到的 Returns Constant。
* archTerm：浮点数向量，表示优化得到的 ARCH Term。
* garchTerm：浮点数向量，表示优化得到的 GARCH Term。
* iterations：整数标量，表示优化迭代次数。
* aic：浮点数标量，表示 aic 准则的值。
* bic：浮点数标量，表示 bic 准则的值。
* nobs：整数标量，表示时间序列的观测数量，即拟合使用的数据量。
* model：字典类型，包含拟合后模型的基本信息，有以下成员：

  + order：长度为 2 的正整数向量，表示模型的阶数。
  + endog：浮点数矩阵类型，表示从 *ds* 中转换而来的观测数据。
  + start：浮点数向量类型，表示经过拟合后的外生变量的值。
* predict：函数指针， 指向预测函数，使用方法为 `model.predict(x)`。其中，*model*
  表示 garch 函数的输出结果，*x* 为一个正整数，表示预测的步长。预测函数返回一个数组，数组中每个元素分别表示每一步的预测值。

## 例子

传入 [macrodata.csv](../data/macrodata.csv)
文件，自定义相关参数，计算其使用 GARCH 模型进行分析的结果。

```
data = loadText("macrodata.csv");
model = garch(data, "realgdp", [1,1]);
print(model)

// out:

volConstant->0.000005999433551
returnsConstant->0.008474617943101
archTerm->[0.70725452294378]
garchTerm->[0.248859733003604]
aic->-1353.789403416915774
bic->-1340.576183784679415
nobs->201
iterations->38
predict->garchPredict
model->order->[1,1]
endog->#0
------------------
0.024942130816387
-0.001192952110668
0.003494532654372
...

coefficients->[-12.023845501294935,-1.104702991485461,0.882087052766567,0.008474617943101]

```

