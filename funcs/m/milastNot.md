# milastNot

## 语法

`milastNot(X, window, [minPeriods])`

窗口计算规则请参考：[mFunctions](../themes/mFunctions.md)

## 参数

**X** 是一个向量/矩阵/表/由等长向量组成的元组。其中，mmse, mslr 仅支持输入向量。

**window** 是大于等于 2 的正整型或 DURATION 标量。表示滑动窗口的长度。

注： 在流计算引擎中调用滑动窗口函数时，window 的上限为 102400。

**minPeriods** 是一个正整数。为滑动窗口中最少包含的观测值数据。

## 详情

在给定长度（以元素个数或时间长度衡量）的滑动窗口内计算 *X* 的最后一个非空元素的下标。

## 例子

```
v = NULL NULL 2 3 4 8 NULL 5 -2 3 -1 0 NULL
milastNot(v, 3)
// output: [,,2,2,2,2,1,2,2,2,2,2,1]

m = matrix(1 2 3 NULL, 1 2 NULL 3, 1 3 NULL NULL, 1 2 3 4)
milastNot(m, 2)
```

| #0 | #1 | #2 | #3 |
| --- | --- | --- | --- |
|  |  |  |  |
| 1 | 1 | 1 | 1 |
| 1 | 0 | 0 | 1 |
| 0 | 1 | -1 | 1 |

```
T = [2022.01.01, 2022.01.02, 2022.01.03, 2022.01.06, 2022.01.07]
X = NULL 2 NULL 4 5
X1 = indexedSeries(T, X)
milastNot(X1, 2, 1)
```

|  | #0 |
| --- | --- |
| 2022.01.01 | -1 |
| 2022.01.02 | 1 |
| 2022.01.03 | 0 |
| 2022.01.06 | 0 |
| 2022.01.07 | 1 |

**相关信息**

* [mifirstNot](mifirstNot.html "mifirstNot")
* [mFunctions](../themes/mFunctions.html "mFunctions")

