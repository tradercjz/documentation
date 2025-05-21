# mannWhitneyUTest

## 语法

`mannWhitneyUTest(X, Y, [correct=true])`

## 参数

**X** 是一个数值向量。

**Y** 是一个数值向量。

**correct** 是一个布尔值，表示在求 p 值时是否考虑连续性校正。默认值为 true。

## 详情

对 *X* 和 *Y* 进行 Mann-Whitney U 检验。返回的结果是一个字典，包含以下
key：

* stat：一张表，包含三种不同备择假设下的 p 值
* correct：求 p 值时是否考虑连续性校正
* method：字符串 "Mann-Whitney U test"
* U：U统计量

## 例子

```
mannWhitneyUTest(5 1 4 3 5, 2 4 7 -1 0 4);

// output
stat->

alternativeHypothesis                 pValue
------------------------------------- --------
true location shift is not equal to 0 0.518023
true location shift is less than 0    0.259011
true location shift is greater than 0 0.797036

correct->true
method->Mann-Whitney U test
U->11
```

