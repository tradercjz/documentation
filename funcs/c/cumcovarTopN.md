# cumcovarTopN

## 语法

`cumcovarTopN(X, Y, S, top, [ascending=true],
[tiesMethod='latest'])`

部分通用参数说明和窗口计算规则请参考：[cumTopN 系列](../themes/cumTopN.md)

## 详情

在累计窗口内，根据 *ascending* 指定的排序方式将 *X* 和 *Y* 按照
*S* 进行稳定排序后，取前 *top* 个元素，然后计算 *X* 和 *Y* 的协方差。

返回值：DOUBLE 类型。

## 例子

```
X=1 2 3 10 13 4 3
Y = 1 7 8 9 0 5 8
S = 0.3 0.5 0.1 0.1 0.5 0.2 0.4
cumcovarTopN(X, Y, S, 6)
// output
[,3,3.5,9.6666,-4,-3.2,-3.3333]
```

