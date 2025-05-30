# mmed

## 语法

`mmed(X, window, [minPeriods])`

窗口计算规则请参考：[mFunctions](../themes/mFunctions.md)

## 参数

**X** 是一个向量/矩阵/表/由等长向量组成的元组。其中，mmse, mslr 仅支持输入向量。

**window** 是大于等于 2 的正整型或 DURATION 标量。表示滑动窗口的长度。

注： 在流计算引擎中调用滑动窗口函数时，window 的上限为 102400。

**minPeriods** 是一个正整数。为滑动窗口中最少包含的观测值数据。

## 详情

在给定长度（以元素个数或时间长度衡量）的滑动窗口内计算 *X* 元素的中位数。

## 例子

```
X = 2 1 3 7 6 5 4
Y = 2 1 3 NULL 6 5 4

mmed(X, 3);
// output
[,,2,3,6,6,5]

mmed(Y, 3);
// output
[,,2,2,4.5,5.5,5]

mmed(Y, 3, minPeriods=1);
// output
[2,1.5,2,2,4.5,5.5,5]
```

```
m = matrix(1 5 9 0 2, 9 10 2 NULL 2)
m.rename!(date(2020.09.08)+1..5, `A`B)
m.setIndexedMatrix!()
m.mmed(3d)
```

| label | col1 | col2 |
| --- | --- | --- |
| 2020.09.09 | 1 | 9 |
| 2020.09.10 | 3 | 9.5 |
| 2020.09.11 | 5 | 9 |
| 2020.09.12 | 5 | 6 |
| 2020.09.13 | 2 | 2 |

```
m.mmed(1w)
```

| label | col1 | col2 |
| --- | --- | --- |
| 2020.09.09 | 1 | 9 |
| 2020.09.10 | 3 | 9.5 |
| 2020.09.11 | 5 | 9 |
| 2020.09.12 | 3 | 9 |
| 2020.09.13 | 2 | 5.5 |

相关函数：[med](med.md)

