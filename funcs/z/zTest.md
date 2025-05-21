# zTest

## 语法

`zTest(X, [Y], [mu=0.0], [sigmaX=1.0], [sigmaY=1.0],
[confLevel=0.95])`

## 参数

**X** 是一个数值向量，表示用于 Z 检验的样本。

**Y** 是一个数值向量，表示用于独立双样本 Z 检验的另一个样本。它是一个可选参数。

**mu** 是一个浮点数，默认值是0。如果没有指定 *Y*，*mu* 表示 *X* 的均值的假设值；如果指定了
*Y*，*mu* 表示 *X*、*Y* 均值之差的假设值。

**sigmaX** 是一个浮点数，表示 *X* 的标准差。默认值是1。

**sigmaY** 是一个浮点数，表示 *Y* 的标准差。默认值是1。

**confLevel** 是0到1之间的浮点数，表示置信区间的置信水平。

## 详情

如果没有指定 *Y*，对正态分布 *X* 进行单样本 Z 检验。如果指定了 *Y*，对独立正态分布
*X* 和 *Y* 进行双样本 Z 检验。返回的结果是一个字典，包含以下 key：

* stat：一张表，包含三种不同备择假设下的 p 值和置信区间
* confLevel：置信水平
* method：如果没有指定 *Y*，为字符串 "One sample z-test"；如果指定了
  *Y*，为字符串 "Two sample z-test"
* zValue：z 的统计量

## 例子

单样本 Z 检验：

```
x = norm(5.0, 2.0, 30)
zTest(x, , 5.0, 2.0);

// output
stat->

alternativeHypothesis       pValue   lowerBound upperBound
--------------------------- -------- ---------- -----------
true mean is not equal to 5 0.035765 3.517659   4.949014
true mean is less than 5    0.017882 -Infinity  4.833952
true mean is greater than 5 0.982118 3.632721   Infinity

confLevel->0.95
method->One sample z-test
zValue->-2.099594
```

双样本 Z 检验：

```
x = norm(5.0, 2.0, 30)
y = norm(10.0, 3.0, 40)
zTest(x, y, -5.0, 2.0, 3.0);

// output
stat->

------------------------------------- -------- ---------- -----------
alternativeHypothesis                 pValue   lowerBound upperBound
difference of mean is not equal to -5 0.976133 -6.191162  -3.844655
difference of mean is less than -5    0.488067 -Infinity  -4.033283
difference of mean is greater than -5 0.511933 -6.002533  Infinity

confLevel->0.95
method->Two sample z-test
zValue->-0.029917
```

