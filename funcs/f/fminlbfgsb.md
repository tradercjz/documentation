# fminLBFGSB

## 语法

`fminLBFGSB(func, X0, [fprime], [bounds], [m=10],
[factr=1e7], [pgtol=1e-5], [epsilon=1e-8], [maxIter=15000], [maxFun=15000],
[maxLS=20])`

## 详情

使用 L-BFGS-B 算法找到目标函数的最小值。

## 参数

**func** 函数名，表示需要最小化的目标函数。注意：该函数的返回值须是数值标量类型。

**X0** 数值类型的标量或向量，表示使目标函数最小化的参数的初始猜测。

**fprime** 可选参数，函数名，表示计算 *func* 梯度的函数。如果为空，则使用数值微分方法来获取函数梯度。

**bounds** 可选参数，数值类型矩阵，形状为(N,2)，其中 N 为需要优化的参数数量，即 N=size(X0)。每一行的两个值（min, max），定义了
X0 中对应参数的边界。可以用 `float("inf")` 来表示不设边界。

**m** 可选参数，正整数标量，表示有限内存矩阵的最大可变度量修正数。默认值为 10。

**factr** 可选参数，数值标量，正数，用于衡量迭代是否结束的指标值。当满足条件![](../images/fminLBFGSB1.png)时，算法将停止迭代，其中 eps 是机器精度。*factr* 的典型值有：1e12 代表低精度；1e7
代表中等精度；10.0 代表极高的精度。默认值为 1e7。

**pgtol** 可选参数，数值标量，正数，用于衡量迭代是否结束的指标值。当满足条件![](../images/fminLBFGSB2.png)时，算法将停止迭代，其中![](../images/fminLBFGSB3.png)是投影梯度的第 i 个分量。默认值为 1e-5。

**epsilon** 可选参数，数值标量，正数，表示当使用数值近似方法来求解函数梯度时使用的步长。默认值为 1e-8。

**maxIter** 可选参数，非负整数标量，表示执行的最大迭代次数，默认值为 15000。

**maxFun** 可选参数，非负整数标量，表示最大目标函数调用次数，默认值为 15000。

**maxLS** 可选参数，非负整数标量，表示每轮迭代的最大线搜索步数，默认值为 20。

## 返回值

返回一个字典，字典有以下成员：

* xopt：浮点数向量，使目标函数最小化的参数值。
* fopt：浮点数标量，目标函数最小值。fopt=func(xopt)。
* gopt：浮点数向量，目标函数最小值点处的函数梯度。gopt=func'(xopt)。
* iterations：整数标量，优化过程中执行的总迭代数。
* fcalls：整数标量，优化过程中的目标函数调用次数。
* warnFlag：整数标量，有三个可能值：

  + 0：表示成功执行算法全过程。
  + 1：表示已达最大目标函数调用次数或已达最大迭代次数，算法停止执行。
  + 2：表示由于其他原因算法停止执行。

## 例子

本例自定义约束条件，传入参数 *func*, *X0*，使用 L-BFGS-B 算法找到目标函数 `fun`
的最小值。

```
X = double(0..9)
M = 2
B = 3
Y = double(M * X + B)

def fun(params, x, y) {
	m = params[0]
	b = params[1]
	y_model = m*x + b
	error = sum(square(y - y_model))
	return error
}

initial_values = [0.0, 1.0]
fminLBFGSB(fun{,X,Y}, initial_values)

/* Ouput:

fcalls->27
warnFlag->0
xopt->[1.999999985435,3.000000060585]
gopt->[8.05E-10,8.84E-10]
fopt->0E-12
iterations->6

*/
```

相关函数：[fminBFGS](fminbfgs.html)

