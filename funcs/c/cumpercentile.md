# cumpercentile

## 语法

`cumpercentile(X, percent,
[interpolation='linear'])`

部分通用参数说明和窗口计算规则请参考：[累计窗口系列（cum 系列）](../themes/cumFunctions.html)

## 参数

**percent** 是 0 到 100 之间的整数或小数。

**interpolation** 是一个字符串，表示当选中的分位点位于在 *X* 的第 i 和第 i+1
个元素之间时，采用的插值方法。它具有以下取值：

* 'linear': ![linear](../../images/linear.png), 其中 ![fraction](../../images/fraction_cumpercentile.png)
* 'lower': ![lower](../../images/lower.png)
* 'higher': ![higher](../../images/higher.png)
* 'nearest': ![lower](../../images/lower.png)和![higher](../../images/higher.png)之中最接近分位点的数据
* 'midpoint': ![midpoint](../../images/midpoint.png)

如果没有指定 *interpolation*，默认采用 'linear'。

## 详情

计算 *X* 元素的累计百分位。

## 例子

```
a=1..10;

cumpercentile(a,25);

[1,1.25,1.5,1.75,2,2.25,2.5,2.75,3,3.25]

cumpercentile(a,25,'lower');

[1,1,1,1,2,2,2,2,3,3]

cumpercentile(a,25,'higher');

[1,2,2,2,2,3,3,3,3,4]

cumpercentile(a,25,'midpoint');

[1,1.5,1.5,1.5,2,2.5,2.5,2.5,3,3.5]

cumpercentile(a,25,'nearest');

[1,1,1,2,2,2,2,3,3,3]

cumpercentile(a,50.5);

[1,1.505,2.01,2.515,3.02,3.525,4.03,4.535,5.04,5.545]

m=matrix(1..10, 11..20);
m;
```

| #0 | #1 |
| --- | --- |
| 1 | 11 |
| 2 | 12 |
| 3 | 13 |
| 4 | 14 |
| 5 | 15 |
| 6 | 16 |
| 7 | 17 |
| 8 | 18 |
| 9 | 19 |
| 10 | 20 |

```
cumpercentile(m,25);
```

| #0 | #1 |
| --- | --- |
| 1 | 11 |
| 1.25 | 11.25 |
| 1.5 | 11.5 |
| 1.75 | 11.75 |
| 2 | 12 |
| 2.25 | 12.25 |
| 2.5 | 12.5 |
| 2.75 | 12.75 |
| 3 | 13 |
| 3.25 | 13.25 |

相关函数：[percentile](../p/percentile.html)

