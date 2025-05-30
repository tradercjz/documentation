# moving

## 语法

`moving(func, funcArgs, window, [minPeriods])`

## 详情

应用函数/运算符到给定对象的一个滚动窗口上。

`moving`
高阶函数总是返回一个向量，长度与输入参数的长度相同。当第一个滑动窗口出现时高阶函数开始计算，每计算一次，滑动窗口向右移动一个元素。

内置函数 [msum](../m/msum.md), [mcount](../m/mcount.md) 和 [mavg](../m/mavg.md)
为各自的计算场景进行了优化，因此比 `moving` 高阶函数有更好的性能。

## 参数

* **func** 是一个**聚合**函数。

  注： 使用该参数时，用于定义相应聚合函数的关键词为 **defg**。有关 **defg**
  的详细用法，参考：[自定义聚合函数](../../tutorials/udaf.md)。
* **funcArgs** 是函数 func
  的参数。可为向量、字典或矩阵。如果有多个参数，则用元组表示，并且每个参数的长度（向量/字典的元素个数）必须相同。
* **window** 是正整型 或 DURATION 标量。

  + 当 *window* 是整型时，表示以窗口内元素个数衡量的滑动窗口的长度。
  + 当 *window* 是 DURATION
    时，表示以时间衡量的滑动窗口的长度。此时，*X* 必须是带有时间类型行索引的索引矩阵或者索引序列。
* **minPeriods** 是一个正整数。为滑动窗口中最少包含的观测值数据。如果滑动窗口中的观测值小于
  *minPeriods*，那么该窗口的结果为 NULL 值。默认值与 *window* 相等。 如果
  *window* 是 DURATION，且需要设置 *minPeriods* 时，*minPeriods* 必须是
  1。

有关其他 m 系列函数的参数说明和窗口计算规则，参考: [滑动窗口系列（m 系列）](../themes/mFunctions.md)

## 例子

计算 APPL 相对于市场（SPY） 的 moving beta，移动窗口长度为 10。

```
date=2016.08.01..2016.08.31
date=date[1<=weekday(date)<=5]
aaplRet=0.0177 -0.0148 0.0125 0.0008 0.0152 0.0083 0.0041 -0.0074 -0.0006 0.0023 0.0120 -0.0009 -0.0015 -0.0013 0.0026 -0.0078 0.0031 -0.0075 -0.0043 -0.0059 -0.0011 -0.0077 0.0009
spyRet=-0.0008 -0.0064 0.0029 0.0011 0.0082 -0.0006 0.0006 -0.0025 0.0046 -0.0009 0.0029 -0.0052 0.0019 0.0022 -0.0015 0.0000 0.0020 -0.0051 -0.0007 -0.0019 0.0049 -0.0016 -0.0028
t=table(date, aaplRet, spyRet);
t;
```

输出返回：

| date | aaplRet | spyRet |
| --- | --- | --- |
| 2016.08.01 | 0.0177 | -0.0008 |
| 2016.08.02 | -0.0148 | -0.0064 |
| 2016.08.03 | 0.0125 | 0.0029 |
| 2016.08.04 | 0.0008 | 0.0011 |
| 2016.08.05 | 0.0152 | 0.0082 |
| 2016.08.08 | 0.0083 | -0.0006 |
| 2016.08.09 | 0.0041 | 0.0006 |
| 2016.08.10 | -0.0074 | -0.0025 |
| 2016.08.11 | -0.0006 | 0.0046 |
| 2016.08.12 | 0.0023 | -0.0009 |
| 2016.08.15 | 0.012 | 0.0029 |
| 2016.08.16 | -0.0009 | -0.0052 |
| 2016.08.17 | -0.0015 | 0.0019 |
| 2016.08.18 | -0.0013 | 0.0022 |
| 2016.08.19 | 0.0026 | -0.0015 |
| 2016.08.22 | -0.0078 | 0 |
| 2016.08.23 | 0.0031 | 0.002 |
| 2016.08.24 | -0.0075 | -0.0051 |
| 2016.08.25 | -0.0043 | -0.0007 |
| 2016.08.26 | -0.0059 | -0.0019 |
| 2016.08.29 | -0.0011 | 0.0049 |
| 2016.08.30 | -0.0077 | -0.0016 |
| 2016.08.31 | 0.0009 | -0.0028 |

通过以下语句计算移动 beta：

```
update t set beta_value=moving(beta, [aaplRet, spyRet],10);
t;
```

输出返回：

| date | aaplRet | spyRet | beta\_value |
| --- | --- | --- | --- |
| 2016.08.01 | 0.0177 | -0.0008 |  |
| 2016.08.02 | -0.0148 | -0.0064 |  |
| 2016.08.03 | 0.0125 | 0.0029 |  |
| 2016.08.04 | 0.0008 | 0.0011 |  |
| 2016.08.05 | 0.0152 | 0.0082 |  |
| 2016.08.08 | 0.0083 | -0.0006 |  |
| 2016.08.09 | 0.0041 | 0.0006 |  |
| 2016.08.10 | -0.0074 | -0.0025 |  |
| 2016.08.11 | -0.0006 | 0.0046 |  |
| 2016.08.12 | 0.0023 | -0.0009 | 1.601173 |
| 2016.08.15 | 0.012 | 0.0029 | 1.859846 |
| 2016.08.16 | -0.0009 | -0.0052 | 1.248804 |
| 2016.08.17 | -0.0015 | 0.0019 | 1.114282 |
| 2016.08.18 | -0.0013 | 0.0022 | 1.064296 |
| 2016.08.19 | 0.0026 | -0.0015 | 0.512656 |
| 2016.08.22 | -0.0078 | 0 | 0.614963 |
| 2016.08.23 | 0.0031 | 0.002 | 0.642491 |
| 2016.08.24 | -0.0075 | -0.0051 | 0.70836 |
| 2016.08.25 | -0.0043 | -0.0007 | 0.977279 |
| 2016.08.26 | -0.0059 | -0.0019 | 1.064465 |
| 2016.08.29 | -0.0011 | 0.0049 | 0.422221 |
| 2016.08.30 | -0.0077 | -0.0016 | 0.793236 |
| 2016.08.31 | 0.0009 | -0.0028 | 0.588027 |

*minPeriods* 的作用：

```
moving(avg, 1..4, 3);
```

输出返回：[,,2,3]

```
moving(avg, 1..4, 3, 1);
```

输出返回：[1,1.5,2,3]

```
v1=indexedSeries(2020.08.01..2020.08.04,1..4)
moving(avg, v1, 3d, 1);
```

输出返回：

| label | col1 |
| --- | --- |
| 2020.08.01 | 1 |
| 2020.08.02 | 1.5 |
| 2020.08.03 | 2 |
| 2020.08.04 | 3 |

*moving* 高阶函数的参数 *func* 的所有参数必须要有相同的长度。如果 *func*
的参数长度不等，例如 [percentile](../p/percentile.md) 函数，可以使用 [部分应用](../../progr/partial_app.md) 产生一个新的函数以满足此要求。请见下例：

```
moving(percentile{,50},1..20, 10);
```

输出返回：[,,,,,,,,,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5]

## 性能提示

计算移动均值时，应该使用内置函数 `mavg` 而不是 `moving`
高阶函数，这是因为内置版本是经过优化的版本，运行速度比高阶函数更快。

```
n=1000000
x=norm(0,1, n);
timer mavg(x, 10);
```

输出返回：Time elapsed: 3.501ms

```
timer moving(avg, x, 10);
```

输出返回：Time elapsed: 976.03ms

