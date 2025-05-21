# tmpercentile

## 语法

`tmpercentile(T, X, percent, window, [interpolation='linear'])`

部分通用参数说明和窗口计算规则请参考：[tmFunctions](../themes/tmFunctions.md)

## 参数

**percent** 是0到100之间的整数或小数。

**interpolation** 是一个字符串，表示当选中的分位点位于在 *X* 的第 i 和第 i+1
个元素之间时，采用的插值方法。它具有以下取值：

* 'linear': ![linear](../../images/tmlinear.png) 其中 ![fraction](../../images/tmfraction.png)
* 'lower': ![lower](../../images/xi.png)
* 'higher': ![higher](../../images/higher.png)
* 'nearest': ![lower](../../images/xi.png) 和![higher](../../images/higher.png)之中最接近分位点的数据
* 'midpoint': ![midpoint](../../images/midpoint.png)

如果没有指定 *interpolation*，默认采用 'linear'。

## 详情

在给定长度（以时间 *T* 衡量）的滑动窗口内计算 *X* 元素在其对应窗口内的百分位数。

## 例子

```
T = 1 1 1 2 5 6
X = 1 4 NULL -1 NULL 4
m = table(T as t,X as x)
select *, tmpercentile(t, x, 50, 3) from m
```

| t | x | tmpercentile\_t |
| --- | --- | --- |
| 1 | 1 | 1 |
| 1 | 4 | 2.5 |
| 1 |  | 2.5 |
| 2 | -1 | 1 |
| 5 |  |  |
| 6 | 4 | 4 |

```
T = 2021.01.02 2021.01.02  2021.01.04  2021.01.05 2021.01.07 2021.01.08
X = NULL 4 NULL -1 2 4
m = table(T as t,X as x)
select *, tmpercentile(t, x, 50, 3d) from m
```

| t | x | tmpercentile\_t |
| --- | --- | --- |
| 2021.01.02 |  |  |
| 2021.01.02 | 4 | 4 |
| 2021.01.04 |  | 4 |
| 2021.01.05 | -1 | -1 |
| 2021.01.07 | 2 | 0.5 |
| 2021.01.08 | 4 | 3 |

```
select *, tmpercentile(t, x, 50, 1w) from m
```

| t | x | tmpercentile\_t |
| --- | --- | --- |
| 2021.01.02 |  |  |
| 2021.01.02 | 4 | 4 |
| 2021.01.04 |  | 4 |
| 2021.01.05 | -1 | 1.5 |
| 2021.01.07 | 2 | 2 |
| 2021.01.08 | 4 | 3 |

相关函数：[percentile](../p/percentile.md), [mpercentile](../m/mpercentile.md)

