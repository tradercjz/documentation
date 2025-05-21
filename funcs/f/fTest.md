# fTest

## 语法

`fTest(X, Y, [ratio=1.0], [confLevel=0.95])`

## 参数

**X** 是一个数值向量，表示用于F检验的样本。

**Y** 是一个数值向量，表示用于独立双样本F检验的另一个样本。它是可选参数。

**ratio** 是一个大于0的浮点数，表示X和Y方差的比例的假设值。默认值是1.0。

**confLevel** 是0到1之间的浮点数，表示置信区间的置信水平。

## 详情

对 *X* 和 *Y* 进行 F 检验。返回的结果是一个字典，包含以下 key：

* numeratorDf：分子的自由度
* stat：一张表，包含三种不同备择假设下的 p 值和置信区间
* denominatorDf：分母的自由度
* confLevel：置信水平
* fValue：F 统计量
* method：字符串 "F test to compare two variances"

## 例子

```
x = norm(10.0, 1.0, 20);
y = norm(1.0, 2.0, 10);
fTest(x, y, 0.5);
// output
numeratorDf->19
stat->
alternativeHypothesis                  pValue    lowerBound upperBound
-------------------------------------- --------- ---------- ----------
ratio of variances is not equal to 0.5 0.002326  0.025844   0.274161
ratio of variances is less than 0.5    0.001163  0          0.230624
ratio of variances is greater than 0.5 0.998837  0.032295   Infinity

denominatorDf->9
confLevel->0.95
fValue->0.190386
method->F test to compare two variances
```

