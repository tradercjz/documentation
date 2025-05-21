# fminNCG

## 语法

`fminNCG(func, X0, fprime, fhess, [xtol=1e-5], [maxIter],
[c1=1e-4], [c2=0.9])`

## 详情

使用牛顿共轭梯度法（Newton conjugate gradient；也称为截断牛顿法，Truncated Newton
method）对目标函数进行无约束最小化。本方法适用于解决大型非线性优化问题。

## 参数

**func** 函数名，表示需要最小化的目标函数。注意：函数返回值须是数值标量类型。

**X0** 数值类型的标量或向量，表示使目标函数最小化的参数的初始猜测。

**fprime** 函数名，表示计算 *func* 梯度的函数。

**fhess** 函数名，表示计算 *func* 的 Hessian 矩阵的函数。

**xtol** 可选参数，正数值标量，用于判断是否结束迭代的步长衡量值。如果两次迭代间参数变化量的范数小于
`xtol*size(X0)`，则认为算法收敛，停止迭代。默认值为 1e-5。

**maxIter** 可选参数，非负整数标量，表示执行的最大迭代次数。

**c1** 可选参数，数值标量，值域为(0,1)，*c1* 应小于 *c2*，表示 Armijo 条件规则的参数。默认值为 1e-4。

**c2** 可选参数，数值标量，值域为(0,1)，*c2* 应大于 *c1*，表示曲率条件规则参数。默认值为 0.9。

## 返回值

返回一个字典，字典有以下成员：

* xopt：浮点数向量，使目标函数最小化的参数值。
* fopt：浮点数标量，目标函数最小值。fopt=func(xopt)。
* iterations：整数标量，优化过程中执行的总迭代数。
* fcalls：整数标量，优化过程中的目标函数调用次数。
* gcalls：整数标量，优化过程中的梯度函数调用次数。
* hcalls：整数标量，优化过程中的计算 Hessian 函数的调用次数。
* warnFlag：整数标量，有四个可能值：

  + 0：表示成功执行算法全过程。
  + 1：表示已达最大迭代次数，算法停止执行。
  + 2：表示由于精度损失问题，线搜索失败。
  + 3：表示结果产生 NULL 值。

## 例子

本例自定义条件，传入参数 *f*, *X0*, *fprime*, *fhess*，使用牛顿共轭梯度法找到目标函数
`rosen` 的最小值。

```
def rosen(x) {
	N = size(x);
	return sum(100.0*power(x[1:N]-power(x[0:(N-1)], 2.0), 2.0)+power(1-x[0:(N-1)], 2.0));
}

def rosen_der(x) {
	N = size(x);
	xm = x[1:(N-1)]
	xm_m1 = x[0:(N-2)]
	xm_p1 = x[2:N]
	der = array(double, N)
	der[1:(N-1)] = (200 * (xm - xm_m1*xm_m1) - 400 * (xm_p1 - xm*xm) * xm - 2 * (1 - xm))
	der[0] = -400 * x[0] * (x[1] - x[0]*x[0]) - 2 * (1 - x[0])
	der[N-1] = 200 * (x[N-1] - x[N-2]*x[N-2])
	return der
}

def diag1(x, k) {
	N = size(x)
	m = matrix(type(x), N+1,N+1)
	if (k == 1) {
		for(i in 0:N){
			m[i, i+1] = x[i]
		}
	} else {
		for(i in 0:N){
			m[i+1, i] = x[i]
		}
	}

	return m
}

def rosen_hess(x) {
	N = size(x);
	x1= x[0:(N-1)] * 400
	H = diag1(-x1, 1) - diag1(x1, -1)
	diagonal = array(type(x), N)
	diagonal[0] = 1200 * x[0]*x[0] - 400 * x[1] + 2
	diagonal[N-1] = 200
	diagonal[1:(N-1)] = 202 + 1200 * x[1:(N-1)]*x[1:(N-1)] - 400 * x[2:N]
	H = H + diag(diagonal)
	return H
}

X0 = [4, -2.5]
fminNCG(rosen, X0, rosen_der, rosen_hess)

/* Ouput:（返回顺序可能略有不同）
xopt->[0.999999966120496,0.999999932105584]
fopt->1.149654357653714E-15
iterations->34
fcalls->45
gcalls->45
hcalls->34
warnFlag->0
*/
```

