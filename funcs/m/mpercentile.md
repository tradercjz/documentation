# mpercentile

## 语法

`mpercentile(X, percent, window, [interpolation='linear'],
[minPeriods])`

窗口计算规则请参考：[mFunctions](../themes/mFunctions.md)

## 参数

**X** 是一个向量/矩阵/表/由等长向量组成的元组。其中，mmse, mslr 仅支持输入向量。

**percent** 是0到100之间的整数或小数。

**window** 是大于等于 2 的正整型或 DURATION 标量。表示滑动窗口的长度。

注： 在流计算引擎中调用滑动窗口函数时，window 的上限为 102400。

**interpolation** 是一个字符串，表示当选中的分位点位于在 *X* 的第 i 和第 i+1
个元素之间时，采用的插值方法。它具有以下取值：

* 'linear'：![linear](../../images/linear.png)，其中，![fraction](../../images/fraction.png)
* 'lower'：![lower](../../images/lower.png)
* 'higher'：![higher](../../images/higher.png)
* 'nearest'：![lower](../../images/lower.png)和![higher](../../images/higher.png)之中最接近分位点的数据
* 'midpoint'：![midpoint](../../images/midpoint.png)

如果没有指定 *interpolation*，默认采用 'linear'。

**minPeriods** 是一个正整数。为滑动窗口中最少包含的观测值数据。

## 详情

在给定长度（以元素个数或时间长度衡量）的滑动窗口内计算 *X* 元素在其对应窗口内的百分位数。

## 例子

```
x=2 1 3 7 6 5 4;
mpercentile(x, percent=50, window=3);
// output
[,,2,3,6,6,5]

mpercentile(x, percent=25, window=3, interpolation="lower");
// output
[,,1,1,3,5,4]

mpercentile(x, percent=75, window=3, interpolation="higher")
// output
[,,3,7,7,7,6]

mpercentile(x, percent=5, window=3, interpolation="nearest")
// output
[,,1,1,3,5,4]

mpercentile(x, percent=15, window=3, interpolation="midpoint")
// output
[,,1.5,2,4.5,5.5,4.5]

mpercentile(x, percent=50, window=3, interpolation="linear", minPeriods=1);
// output
[2,1.5,2,3,6,6,5]

m=matrix(2 1 3 7 6 5 4, 1..7);
m;
```

| #0 | #1 |
| --- | --- |
| 2 | 1 |
| 1 | 2 |
| 3 | 3 |
| 7 | 4 |
| 6 | 5 |
| 5 | 6 |
| 4 | 7 |

```
mpercentile(m, percent=50, window=3, interpolation="linear", minPeriods=1);
```

| #0 | #1 |
| --- | --- |
| 2 | 1 |
| 1.5 | 1.5 |
| 2 | 2 |
| 3 | 3 |
| 6 | 4 |
| 6 | 5 |
| 5 | 6 |

```
m.rename!(date(2020.09.08)+1..7, `A`B)
m.setIndexedMatrix!()
mpercentile(m, percent=50, window=3d, interpolation="linear", minPeriods=1);
```

| label | col1 | col2 |
| --- | --- | --- |
| 2020.09.09 | 2 | 1 |
| 2020.09.10 | 1.5 | 1.5 |
| 2020.09.11 | 2 | 2 |
| 2020.09.12 | 3 | 3 |
| 2020.09.13 | 6 | 4 |
| 2020.09.14 | 6 | 5 |
| 2020.09.15 | 5 | 6 |

```
mpercentile(m, percent=50, window=1w, interpolation="linear", minPeriods=1);
```

| label | col1 | col2 |
| --- | --- | --- |
| 2020.09.09 | 2 | 1 |
| 2020.09.10 | 1.5 | 1.5 |
| 2020.09.11 | 2 | 2 |
| 2020.09.12 | 2.5 | 2.5 |
| 2020.09.13 | 3 | 3 |
| 2020.09.14 | 4 | 3.5 |
| 2020.09.15 | 4 | 4 |

相关函数：[percentile](../p/percentile.md)

