# cumbetaTopN

## 语法

`cumbetaTopN(Y, X, S, top, [ascending=true],
[tiesMethod='latest'])`

部分通用参数说明和窗口计算规则请参考：[累计窗口系列（cum 系列）](../themes/cumFunctions.md)

## 详情

在累计窗口内，根据 *ascending* 指定的排序方式将 *X* 和 *Y* 按照
*S* 进行稳定排序后，取前 *top* 个元素，然后计算 *Y* 在 *X* 上的回归系数的最小二乘估计。

返回值：DOUBLE 类型。

## 例子

```
Y=1 2 3 10 100 4 3
X=1 7 8 9 0 5 8
S = 0.3 0.5 0.1 0.1 0.5 0.2 0.4
cumbetaTopN(Y, X, S, 6)
// output
[,0.1666,0.2441,0.7483,-6.4428,-6.4428,-6.2293]
```

