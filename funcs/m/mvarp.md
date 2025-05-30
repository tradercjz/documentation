# mvarp

## 语法

`mvarp(X, window, [minPeriods])`

窗口计算规则请参考：[mFunctions](../themes/mFunctions.md)

## 参数

**X** 是一个向量/矩阵/表/由等长向量组成的元组。其中，mmse, mslr 仅支持输入向量。

**window** 是大于等于 2 的正整型或 DURATION 标量。表示滑动窗口的长度。

注： 在流计算引擎中调用滑动窗口函数时，window 的上限为 102400。

**minPeriods** 是一个正整数。为滑动窗口中最少包含的观测值数据。

## 详情

在给定长度（以元素个数或时间长度衡量）的滑动窗口内计算 *X* 的总体方差。

## 例子

```
mvarp(1..6, 5);
// output
[,,,,2,2]

mvarp(1..6, 5, 2);
// output
[,0.25,0.666666666666667,1.25,2,2]

m=matrix(1 6 2 9 4 5, 11 12 18 23 21 10);
m;
```

| #0 | #1 |
| --- | --- |
| 1 | 11 |
| 6 | 12 |
| 2 | 18 |
| 9 | 23 |
| 4 | 21 |
| 5 | 10 |

```
mvarp(m,3);
```

| #0 | #1 |
| --- | --- |
|  |  |
|  |  |
| 4.666666666666667 | 9.555555555555542 |
| 8.222222222222223 | 20.22222222222221 |
| 8.666666666666666 | 4.222222222222248 |
| 4.666666666666667 | 32.666666666666664 |

```
m=matrix(1 NULL 4 NULL 8 6 , 9 NULL NULL 10 NULL 2)
m.rename!(date(2020.04.06)+1..6, `col1`col2)
m.setIndexedMatrix!()
mvarp(m,4d)
```

| label | col1 | col2 |
| --- | --- | --- |
| 2020.04.07 | 0 | 0 |
| 2020.04.08 | 0 | 0 |
| 2020.04.09 | 2.25 | 0 |
| 2020.04.10 | 2.25 | 0.25 |
| 2020.04.11 | 4 | 0 |
| 2020.04.12 | 2.6667 | 16 |

```
mvarp(m,1w)
```

| label | col1 | col2 |
| --- | --- | --- |
| 2020.04.07 | 0 | 0 |
| 2020.04.08 | 0 | 0 |
| 2020.04.09 | 2.25 | 0 |
| 2020.04.10 | 2.25 | 0.25 |
| 2020.04.11 | 8.2222 | 0.25 |
| 2020.04.12 | 6.6875 | 12.6667 |

相关函数：[varp](../v/varp.md)

