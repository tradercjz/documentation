# boxcox

## 语法

`boxcox(X, [lmbda])`

## 参数

**X** 数值型向量，表示要转换的输入向量。如果未指定 *lmbda* 参数，*X* 不能包含空值或非正数，且 *X*
的所有元素不能相同。

**lmbda**可选参数，数值类型标量或向量，表示 lambda 参数。若为向量，*X* 与 *lmbda* 的长度必须相同。

## 详情

使用 Box-Cox 变换方法对 *X* 进行转换。

Box-Cox 变换由下式给出：

![](../images/boxcox.png)

**返回值：**

* 如果指定了 *lmbda* 参数，返回值为与 *X* 等长的 DOUBLE 类型向量。
  + 如果 *lmbda* 是标量，则返回值是使用 *lmbda* 对 *X* 进行 Box-Cox
    转换的结果。
  + 如果 *lmbda* 是向量，则返回值的每个元素分别为 boxcox(Xi,
    lmbdai)。
* 如果未指定 *lmbda* 参数，返回值为元组，包含两个元素：
  + 第一个元素为 DOUBLE 类型的向量，表示对 *X* 进行 Box-Cox 转换的结果。
  + 第二个元素为 DOUBLE 类型的标量，表示最优的 lambda 参数。

## 例子

```
data = [1.5, 2.3, 3.1, 4.8, 5.5, 6.7, 8.2, 9.0, 10.1, 12.4]
lmb = 2
boxcox(data)
// output: ([0.4541,1.0562,1.5689,2.4892,2.82394,3.3559,3.9636,4.267,4.6653,5.4393],0.5495)
boxcox(data, lmb)
// output: [0.625,2.145,4.305,11.02,14.625,21.945,33.12,40,50.505,76.38]
```

