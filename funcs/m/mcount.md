# mcount

## 语法

`mcount(X, window, [minPeriods=1])`

窗口计算规则请参考：[mFunctions](../themes/mFunctions.md)

## 参数

**X** 是一个向量/矩阵/表/由等长向量组成的元组。其中，mmse, mslr 仅支持输入向量。

**window** 是大于等于 2 的正整型或 DURATION 标量。表示滑动窗口的长度。

注： 在流计算引擎中调用滑动窗口函数时，window 的上限为 102400。

**minPeriods** 是一个正整数。为滑动窗口中最少包含的观测值数据。

## 详情

在给定长度（以元素个数或时间长度衡量）的滑动窗口内统计 *X* 中的非 NULL 元素个数。

## 例子

```
x = 7 4 5 8 9;

mcount(x, 3);
// output: [1,2,3,3,3]

mcount(x, 3, minPeriods=2);
// output: [,2,3,3,3]

x1 =1 2 3 NULL 5;

mcount(x1, 3);
// output: [1,2,3,2,2]

mcount(x1, 3, minPeriods=3);
// output: [,,3,,]

m=matrix(1 2 NULL 4 5, 6 7 8 9 NULL);
m;
```

| #0 | #1 |
| --- | --- |
| 1 | 6 |
| 2 | 7 |
|  | 8 |
| 4 | 9 |
| 5 |  |

```
mcount(m,3);
```

| #0 | #1 |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 2 | 3 |
| 2 | 3 |
| 2 | 2 |

```
s=indexedSeries(date(2020.05.26)+1..8, 3 4 9 NULL 4 6 NULL 8)
mcount(s,4d)
```

| label | col1 |
| --- | --- |
| 2020.05.27 | 1 |
| 2020.05.28 | 2 |
| 2020.05.29 | 3 |
| 2020.05.30 | 3 |
| 2020.05.31 | 3 |
| 2020.06.01 | 3 |
| 2020.06.02 | 2 |
| 2020.06.03 | 3 |

```
mcount(s,1w)
```

| label | col1 |
| --- | --- |
| 2020.05.27 | 1 |
| 2020.05.28 | 2 |
| 2020.05.29 | 3 |
| 2020.05.30 | 3 |
| 2020.05.31 | 4 |
| 2020.06.01 | 5 |
| 2020.06.02 | 5 |
| 2020.06.03 | 5 |

相关函数：[count](../c/count.md)

