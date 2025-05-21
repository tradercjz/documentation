# mmad

## 语法

`mmad(X, window, [useMedian=false], [minPeriods])`

窗口计算规则请参考：[mFunctions](../themes/mFunctions.html)

## 参数

**X** 是一个向量/矩阵/表/由等长向量组成的元组。其中，mmse, mslr 仅支持输入向量。

**window** 是大于等于 2 的正整型或 DURATION 标量。表示滑动窗口的长度。

注： 在流计算引擎中调用滑动窗口函数时，window 的上限为 102400。

**useMedian** 是一个布尔值，默认值是 false，表示计算平均绝对离差（mean absolute deviation）。若为 true
则计算绝对中位差（median absolute deviation）。

* 平均绝对离差：mean(abs(X - mean(X)))
* 绝对中位差：med(abs(X - med(X)))

**minPeriods** 是一个正整数。为滑动窗口中最少包含的观测值数据。

## 详情

在给定长度（以元素个数衡量）的滑动窗口内，计算 *X* 的平均绝对离差或绝对中位差。

## 例子

```
x = 7 4 6 0 -5 32;
mmad(x, window=3);
// output
[,,1.111111111111111,2.222222222222222,3.777777777777777,15.333333333333333]

mmad(x, window=3, useMedian=true)
// output
[,,1,2,5,5]

y = NULL NULL 2 5 1 7 -3 0
mmad(y, window=3, minPeriods=2);
// output
[,,,1.5,1.555555555555555,2.222222222222222,3.555555555555556,3.777777777777778]
```

```
m=matrix(85 90 95, 185 190 195);
m;
```

| #0 | #1 |
| --- | --- |
| 85 | 185 |
| 90 | 190 |
| 95 | 195 |

```
mmad(x, 2)
```

| #0 | #1 |
| --- | --- |
|  |  |
| 2.5 | 2.5 |
| 2.5 | 2.5 |

相关函数： [mad](mad.html)

