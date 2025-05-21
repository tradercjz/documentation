# differentialEvolution

## 语法

`differentialEvolution(func, bounds, [X0], [maxIter=1000], [popSize=15],
[mutation], [recombination=0.7], [tol=0.01], [atol=0], [polish=true],
[seed])`

## 详情

使用差分进化算法（Differential Evolution）求解多元函数的全局最小值。返回一个字典，表示求解结果，详细说明请参见“返回值”小节。

## 参数

**func** 函数名，表示需要最小化的目标函数。注意：其返回值应为标量数值。

**bounds** 数值类型矩阵，形状为(N,2)，其中 N 为需要优化的参数数量。

**X0** 可选参数，数值向量，表示使目标函数最小化的参数的初始猜测。

注意：

* 参数 *bounds* 中每一行的两个值（min, max），分别定义了 *X0* 中对应参数的下、上边界。即参数 *X0*
  的每个元素值均在 *bounds* 的范围内。
* 参数 *X0* 应与 *bounds* 保持相同长度，即 N=size(*X0*)。

**maxIter** 可选参数，非负整数标量，表示执行的最大迭代次数，默认值为 1000。

**popSize** 可选参数，正整数标量，用于设置种群大小的乘数。种群包含 popSize\*(N - N\_equal) 个个体，其中，N\_equal 表示
*bounds* 中上下限相等的参数个数。默认值为 15。

**mutation** 可选参数，输入形式为数值数据对 pair(min, max)，表示变异常数的范围。应满足 0<= min <=max
<2。默认值为(0.5, 1)。

**recombination** 可选参数，数值标量，表示重组常数，又称为交叉概率。取值范围为[0, 1]。

**tol** 可选参数，非负浮点数标量，表示收敛的相对容忍度。默认值为 0.01。

**atol** 可选参数，非负浮点数标量，表示收敛的绝对容忍度。默认值为 0。当满足条件 stdev(population\_energies) <=
*atol* + *tol* \* abs(mean(population\_energies)) 时，停止算法迭代，其中
population\_energies 表示种群中每个个体求得的目标函数值构成的向量。

**polish** 可选参数，布尔标量，表示是否在差分进化算法结束后进一步使用 L-BFGS-B 算法优化参数。默认值为 true，表示使用。

**seed**
可选参数，整数标量，表示差分进化算法中使用的随机数种子。如果不设置，则使用非确定性的随机数生成器。该参数的作用在于让用户可以复现运行结果。默认不设置。

## 返回值

返回一个字典，包含以下成员：

* xopt：浮点数向量，使目标函数最小化的参数值。
* fopt：浮点数标量，目标函数最小值，fopt=f(xopt)。
* iterations：整数标量，优化过程中执行的总迭代数。
* fcalls：整数标量，优化过程中的目标函数调用次数。
* converged：布尔值标量，表示优化过程的收敛状态。

  + true：表示优化结果已收敛至满足预定条件，算法停止执行。
  + false：表示已达最大迭代次数，算法未收敛而停止执行。

## 例子

自定义函数 `rosen`，在上下界 *bounds* 约束下使用
`differentialEvolution` 求解 `rosen`
函数的全局最小值。

```
def rosen(x) {
	N = size(x);
	return sum(100.0*power(x[1:]-power(x[:N-1], 2.0), 2.0)+power(1-x[:N-1], 2.0));
}
bounds = matrix([0 0 0 0 0, 2 2 2 2 2])
differentialEvolution(rosen, bounds)

/* Ouput:
fcalls->43656
xopt->[1.000000000000,1.000000000000,1.000000000000,1.000000000000,1.000000000000]
fopt->0.0
iterations->581
converged->true
*/
```

