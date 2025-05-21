# covarMatrix

## 语法

`covarMatrix(X)`

## 参数

**X** 是一个矩阵。

## 详情

设矩阵 *X* 有 n 列，将其每一列作为一维向量，求 n 维随机变量的协方差矩阵（covariance
matrix）。

注：

* 如果矩阵中含有空值，会默认将空值转化为0，然后进行计算。而由于 [covar](covar.html) 函数计算时忽略 NULL 值，因此调用 [cross/pcross(covar, X)](../ho_funcs/cross.html)
  函数计算相关矩阵时也会忽略 NULL 值。
* 在不含 NULL 值的情况下，虽然该函数计算结果等价于 `cross(covar,
  X)`，但该函数内部进行了优化，其性能较 [cross/pcross](../ho_funcs/cross.html) 函数有大幅提升。

## 例子

```
m = rand(10.0, 30)$10:3
covarMatrix(m)
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 6.116181845352529 | 1.107026927999891 | 1.306707566911273 |
| 1.107026927999891 | 7.162534080771522 | -0.758517799304199 |
| 1.306707566911273 | -0.758517799304199 | 5.516744365930221 |

```
a = rand(1.0, 30000000).reshape(10000:3000)
a.rename!("s" + string(1..3000))
timer covarMatrix(a)
// output
Time elapsed: 2927.264 ms
timer pcross(covar, a)
// output
Time elapsed: 29484.85 ms
```

相关函数： [corrMatrix](corrMatrix.html)

