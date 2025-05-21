# percentileRank

## 语法

`percentileRank(X, score, [method='excel'])`

## 参数

**X** 是一个数值型向量、矩阵或表。若为矩阵，每列计算百分位，输出一个向量。若为表，每列计算百分位，输出一个表。

**score** 是一个数值型标量，表示需要得到其排位的值。

**method** 是一个字符串，表示计算百分位的方法，包含以下取值，默认值为 "excel"：

* "excel"：小于 *score* 的元素个数占不等于 *score*
  的元素个数的百分比；若 *score* 不在 *X* 中，其百分位计算公式为：

![](../../images/pscore.png)

其中，![xi](../../images/xi.png) 和 ![xp1](../../images/xp1.png) 为数据集X中的紧邻score的前、后两个数值，
![pi](../../images/pi.png)和 ![pi1](../../images/pi1.png)分别为![xi](../../images/xi.png) 和![xp1](../../images/xp1.png)的百分位。

* "rank"：小于等于 *score* 的元素个数占元素总数的百分比。当有多个值相等的
  *score* 时，取它们百分位的平均值；
* "strict"：严格小于 *score* 的元素个数占元素总数的百分比；
* "weak"：小于等于 *score* 的元素个数占元素总数的百分比；
* "mean"："strict" 和 "weak" 的平均值。

## 详情

计算一个数值在数值向量中的百分位数（0~100）。计算时忽略 NULL 值。

## 例子

```
a = 2 3 4 4 5;
percentileRank(a, 4);
// output: 66.666667
percentileRank(a, 3);
// output: 25
percentileRank(a, 4, "rank");
// output: 70
percentileRank(a,4,"weak");
// output: 80
percentileRank(a,5,"strict");
// output: 40
percentileRank(a,5,"mean");
// output: 60

percentileRank(1 5 8, 6, "excel")
// output: 66.666667
```

