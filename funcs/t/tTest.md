# tTest

## 语法

`tTest(X, [Y], [mu=0.0], [confLevel=0.95], [equalVar=false])`

## 参数

**X** 是一个数值向量，表示用于t检验的样本。

**Y** 是一个数值向量，表示用于独立双样本t检验的另一个样本。它是可选参数。

**mu** 是一个浮点数，默认值是0。如果没有指定 *Y* ，*mu* 表示 *X* 的均值的假设值；如果指定了
*Y*，*mu* 表示 *X*, *Y* 均值之差的假设值。

**confLevel** 是0到1之间的浮点数，表示置信区间的置信水平。

**equalVar** 是一个布尔值，表示 *X*, *Y* 的方差是否相等。

## 详情

对未知方差的数据进行t检验。

如果没有指定 *Y*，对正态分布 *X* 进行单样本 t 检验；如果指定了 *Y*，对独立正态分布
*X* 和 *Y* 进行双样本 t 检验。返回的结果是一个字典，包含以下 key：

* stat：一张表，包含三种不同备择假设下的 p 值和置信区间
* df：t 分布的自由度
* confLevel：置信水平
* tValue：t 统计量

## 例子

单样本 t 检验：

```
x = norm(10.0, 1.0, 20)
tTest(x, , 10.0);

// output
stat->
alternativeHypothesis        pValue   lowerBound upperBound
---------------------------- -------- ---------- ----------
true mean is not equal to 10 0.499649 9.68582    10.621998
true mean is less than 10    0.750176 -Infinity  10.540616
true mean is greater than 10 0.249824 9.767202   Infinity

df->19
confLevel->0.95
method->One sample t-test
tValue->0.688192
```

独立同方差双样本 t 检验：

```
x = norm(10.0, 1.0, 20)
y = norm(4.0, 1.0, 10)
tTest(x, y, 6.0, , true);

// output
stat->
alternativeHypothesis                pValue   lowerBound upperBound
------------------------------------ -------- ---------- ----------
difference of mean is not equal to 6 0.438767 5.539812   7.03262
difference of mean is less than 6    0.780616 -Infinity  6.906078
difference of mean is greater than 6 0.219384 5.666354   Infinity

df->28
confLevel->0.95
method->Two sample t-test
tValue->0.785483
```

独立不同方差双样本 t 检验：

```
x = norm(10.0, 1.0, 20)
y = norm(1.0, 2.0, 10)
tTest(x, y, 9.0);

// output
stat->
alternativeHypothesis          pValue   lowerBound upperBound
------------------------------ ----------------- ---------- ----------
true difference of mean is n...0.983376 7.752967   10.271656
true difference of mean is l...0.508312 -Infinity  10.04285
true difference of mean is g...0.491688 7.981773   Infinity

df->12.164434
confLevel->0.95
method->Welch two sample t-test
tValue->0.021269
```

