# fminBFGS

## 语法

`fminBFGS(func, X0, [fprime], [gtol=1e-5], [norm],
[epsilon], [maxIter], [xrtol=0], [c1=1e-4], [c2=0.9])`

## 详情

使用 BFGS 算法找到目标函数的最小值。

## 参数

**func** 函数名，表示需要最小化的目标函数。注意：函数返回值须是数值标量类型。

**X0** 数值类型的标量或向量，表示使目标函数最小化的参数的初始猜测。

**fprime** 可选参数，函数名，表示计算 *func* 梯度的函数。如果为空，则使用数值微分方法来获取函数梯度。

**gtol** 可选参数，正数值标量，判断是否停止迭代的梯度范数衡量值。如果梯度的范数小于 *gtol*，则停止迭代。默认值为 1e-5。

**norm** 可选参数，正数值标量，表示范数的阶数，默认使用最大值范数。

**epsilon** 可选参数，正数值标量，表示当使用数值近似方法来求解函数梯度时使用的步长。默认值为
*1.4901161193847656e-08*。

**maxIter** 可选参数，非负整数标量，表示执行的最大迭代次数，默认值为 *X0* 的长度乘以200。

**xrtol** 可选参数，非负数值标量，用于判断是否结束迭代的步长衡量值。如果步长小于`xk *
xrtol`（`xk`为当前参数向量），则停止迭代。默认值为 0。

**c1** 可选参数，数值标量，值域为(0,1)，*c1* 应小于 *c2*，表示 Armijo 条件规则的参数。默认值为 1e-4。

**c2** 可选参数，数值标量，值域为(0,1)，*c2* 应大于 *c1*，表示曲率条件规则参数。默认值为 0.9。

## 返回值

返回一个字典，字典有以下成员：

* xopt：浮点数向量，使目标函数最小化的参数值。
* fopt：浮点数标量，目标函数最小值，fopt=func(xopt)。
* gopt：浮点数向量，目标函数最小值处的梯度，func'(xopt)，应接近 0。
* Hinv：浮点数矩阵，目标函数最小值处Hessian矩阵的逆矩阵。
* iterations：整数标量，优化过程中执行的总迭代数。
* fcalls：整数标量，优化过程中的目标函数调用次数。
* gcalls：整数标量，优化过程中的梯度函数调用次数。
* warnFlag：整数标量，有四个可能值：

  + 0：表示成功执行算法全过程。
  + 1：表示已达最大迭代次数，算法停止执行。
  + 2：表示线搜索失败或者目标函数值出现极值。
  + 3：表示计算结果中出现 NULL 值。

## 例子

本例自定义条件，传入参数 *func*, *X0*, *fprime*，使用 BFGS 算法找到目标函数
`quadratic_cost` 的最小值。

```
def quadratic_cost(x, Q) {
	return dot(dot(x, Q), x)
}

def quadratic_cost_grad(x, Q) {
	return 2 * dot(Q, x)
}

x0 = [-3, -4]
cost_weight = diag([1., 10.])

fminBFGS(quadratic_cost{,cost_weight}, x0, quadratic_cost_grad{,cost_weight})

/* Ouput:
fcalls->8
warnFlag->0
xopt->[0.000002859166,-4.54371E-7]
Hinv->
#0              #1
0.508225788096  -0.001307222772
-0.001307222772 0.050207740748

gopt->[0.000005718332,-0.000009087439]
fopt->1.0E-11
gcalls->8
iterations->7
*/
```

相关函数：[fminBFGSB](fminlbfgsb.md)

