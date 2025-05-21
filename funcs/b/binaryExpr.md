# binaryExpr

## 语法

`binaryExpr(X, Y, optr)`

## 参数

**X** 可以是一个标量/向量/矩阵。

**Y** 可以是一个标量或者和 *X* 具有相同类型的量。

**optr** 是一个二元运算符。

## 详情

使用 *optr* 指定的二元运算符，将 *X* 与 *Y* 连接，成一个二元运算的元代码。使用 [eval](../e/eval.html) 函数可以执行
`binaryExpr` 函数生成的元代码。

## 例子

```
binaryExpr(1, 1, +).eval()
// output
2

binaryExpr(1 2.2 3, 1 2 3, *).eval()
// output
[1 4.4 9]

binaryExpr(`id`st`nm, `fff, +).eval()
// output
["idfff","stfff","nmfff"]

a = matrix(1 2, 3 4)
b = matrix(4 2, 5 1)
binaryExpr(a, b, dot).eval()
```

| #0 | #1 |
| --- | --- |
| 10 | 8 |
| 16 | 14 |

相关函数： [unifiedExpr](../u/unifiedExpr.html)

