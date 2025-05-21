# chiSquareTest

## 语法

`chiSquareTest(X, [Y])`

## 参数

**X** 是一个数值向量、矩阵或表。

如果 *X* 是一个向量，那么 *Y* 是一个与 *X* 长度相同的向量；如果 *X*
是矩阵或表，那么无需指定 *Y*。

## 详情

如果 *X* 是一个向量，进行 Chi-square Goodness-of-fit 检验 *X* 是否与
*Y* 的概率分布一致；如果 *X* 是矩阵或表，对 *X* 进行 Pearson's Chi-squared
检验。返回的结果是一个字典，包含以下 key：

* pValue：p 值
* df：自由度
* chiSquaredValue：chi-square 统计量
* method：如果 *X* 为向量，*method* 为字符串 "Chi-square
  goodness of fit test"；如果 *X* 为矩阵或表，*method* 为字符串 "Pearson's
  Chi-squared test"。

## 例子

例1. *X* 是一个向量。

```
x=rand(10.0,50)
y=rand(10.0,50)
chiSquareTest(x,y);

// output
pValue->0
df->49
chiSquaredValue->947.388015
method->Chi-square goodness of fit test
```

例2. *X* 是一个矩阵。

```
x = matrix([762, 484], [327, 239], [468, 477])
x.rename!(`female`male, `Democrat`Independent`Republican)
x;
```

|  | Democrat | Independent | Republican |
| --- | --- | --- | --- |
| female | 762 | 327 | 468 |
| male | 484 | 239 | 477 |

```
chiSquareTest(x);
// output
pValue->2.953589E-7
df->2
chiSquaredValue->30.070149
method->Pearson's Chi-squared test
```

