# kernelRidge

## 语法

`kernelRidge(ds, yColName, xColNames, [alpha=1.0], [kernel='linear'],
[gamma=0], [degree=3], [coef0=1], [swColName])`

## 参数

**ds** 是内存表或由 [sqlDS](../s/sqlDS.md) 生成的数据源。

**yColName** 是字符串，表示数据源中因变量的列名，对应目标函数中的 y 。

**xColNames** 是字符串标量或向量，表示数据源中自变量的列名。对应目标函数中的 X。

**alpha** 可选参数，是正数，表示正则化强度。默认值为 1.0。 对应目标函数中的 alpha。

**kernel** 可选参数，是字符串，表示核函数的类型。对应目标函数中的 `Φ`。支持以下核函数：

* 'linear'：线性核函数 `<x, y>`
* 'rbf'：径向基函数核（高斯核）`exp(-gamma * ||x - y||²)`
* 'poly'/'polynomial'：多项式核函数 `(gamma * <x, y> +
  coef0)^degree`
* 'sigmoid'：Sigmoid核函数 `tanh(gamma * <x, y> + coef0)`
* 'laplacian'：拉普拉斯核函数 `exp(-gamma * ||x - y||₁)`
* 'cosine'：余弦相似度核函数 `<x, y> / (||x|| * ||y||)`
* 'additive\_chi2'：加性卡方核函数 `-∑[(x - y)² / (x + y)]`
* 'chi2'：卡方核函数 `exp(-gamma * ∑[(x - y)² / (x + y)])`

**gamma** 可选参数，是数值标量，表示核函数参数。默认值为 0，此时根据特征数自动设置。

**degree** 可选参数，是数值标量，表示多项式核函数的次数。默认值为 3 。

**coef0** 可选参数，是数值标量，表示核函数中的常数项系数。默认值为 1.0 。

**swColName** 可选参数，是字符串，指定 *ds* 中的一个列名，将该列作为样本权重。默认所有样本的权重都为 1 。

## 详情

该函数基于核函数和岭回归的正则化技术，拟合数据间的复杂非线性关系，输出回归预测模型。

目标函数为：

![](../images/kernelRidge.png)

返回一个字典，包含以下键：

* modelName: 字符串标量，表示模型名称，即 kernelRidge 方法对应的模型名为 “kernelRidge”。
* coefficients: 数值向量，表示参数向量，对应目标函数中的 w 向量。
* xColNames: 字符串向量，表示特征变量列名。
* xFit: 数值矩阵，用于存储输入数据源中的自变量。
* alpha: 数值标量，与参数中的 *alpha* 相同。
* kernel: 字符串标量，与参数中的 *kernel* 相同。
* gamma: 数值标量，与参数中的 *gamma* 相同。
* degree: 数值标量，与参数中的 *degree* 相同。
* coef0: 数值标量，与参数中的 *coef0* 相同。
* predict: 模型的预测函数。

## 例子

```
x1 = [-1.5, 2.3, 4.2, 1.6];
x2 = [-2.2, 3.9, 2.8, 0.5];
sw = [2, 5, 8, 1];
y = [0.0, 0.9, 3.2, 3.1];
t = table(y, x1, x2, sw);

m = kernelRidge(t, `y, `x1`x2, 1, 'laplacian', 0, 3, 1, `sw);
m
/*
modelName->kernelRidge
coefficients->#0
------------------
-0.061436450468451
0.09192514209272
2.716894143137368
1.428547958639275

xColNames->["x1","x2"]
xFit->#0                #1
----------------- ----
-1.5              -2.2
2.3               3.9
4.200000000000001 2.8
1.6               0.5

alpha->1
kernel->laplacian
gamma->0.5
degree->3
coef0->1
predict->kernelRidgePredict
*/

x1 = [-1.2, 4.6, 2.4];
x2 = [-1.0, 2.8, -4.7];
t_test = table(x1, x2);
predict(m, t_test);
/*
#0
-----------------
0.166070925673076
2.34188781136904
0.095783250622374
*/

```

