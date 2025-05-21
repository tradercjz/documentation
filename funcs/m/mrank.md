# mrank

## 语法

`mrank(X, ascending, window, [ignoreNA=true], [tiesMethod='min'],
[percent=false], [minPeriods])`

窗口计算规则请参考：[mFunctions](../themes/mFunctions.html)

## 参数

**X** 是一个向量/矩阵/表/由等长向量组成的元组。其中，mmse, mslr 仅支持输入向量。

**ascending** 是一个布尔值，表示是否按升序排序。默认值是 true。

**window** 是大于等于 2 的正整型或 DURATION 标量。表示滑动窗口的长度。

注： 在流计算引擎中调用滑动窗口函数时，window 的上限为 102400。

**ignoreNA** 是一个布尔值，表示是否忽略 NULL 值。true 表示忽略 NULL 值（默认值），false 表示 NULL 值参与排名，此时
NULL 值为最小值。

**tiesMethod** 是一个字符串，表示窗口内若存在重复值时，排名如何选取。'min' 表示取最小排名，'max' 表示取最大排名，'average'
表示取排名的均值。

**percent** 是一个布尔值，表示是否以百分比形式显示返回的排名，默认值为 false。

**minPeriods** 是一个正整数。为滑动窗口中最少包含的观测值数据。

## 详情

在给定长度（以元素个数或时间长度衡量）的滑动窗口内计算 *X* 元素在其对应窗口内的排名。

## 例子

```
X = 3 2 4 4 4 NULL 1

mrank(X, ascending=false, window=3, ignoreNA=true);
// output: [,,0,0,0,,1]

mrank(X, ascending=false, window=3, ignoreNA=true, minPeriods=2);
// output: [,1,0,0,0,,1]

mrank(X, ascending=false, window=3, ignoreNA=false, tiesMethod='max');
// output: [,,0,1,2,2,1]

mrank(X, ascending=false, window=3, ignoreNA=false, tiesMethod='max', minPeriods=2);
// output: [,1,0,1,2,2,1]

mrank(X, ascending=false, window=3, ignoreNA=false, tiesMethod='min');
// output: [,,0,0,0,2,1]

mrank(X, ascending=false, window=3, ignoreNA=false, tiesMethod='min', minPeriods=3);
// output: [,,0,0,0,,]

mrank(X, ascending=false, window=3, ignoreNA=false, tiesMethod='average');
// output: [,,0,0.5,1,2,1]

mrank(X, ascending=false, window=3, ignoreNA=false, tiesMethod='average', minPeriods=2);
// output: [,1,0,0.5,1,2,1]
```

```
m=matrix(1 2 5 3 4, 5 4 1 2 3);
m;
```

| #0 | #1 |
| --- | --- |
| 1 | 5 |
| 2 | 4 |
| 5 | 1 |
| 3 | 2 |
| 4 | 3 |

```
mrank(m, true, 3);
```

| #0 | #1 |
| --- | --- |
|  |  |
|  |  |
| 2 | 0 |
| 1 | 1 |
| 1 | 2 |

```
mrank(m, true, 3, percent=true);
```

| col1 | col2 |
| --- | --- |
|  |  |
|  |  |
| 1 | 0.3333 |
| 0.6667 | 0.6667 |
| 0.6667 | 1 |

```
m=matrix([1 4 2 4 5 7 4 3 2 5])
m.rename!(2020.01.01..2020.01.10, [`A])
m.setIndexedMatrix!()
mrank(m,window=3d,percent = 1)
```

| label | A |
| --- | --- |
| 2020.01.01 | 1 |
| 2020.01.02 | 1 |
| 2020.01.03 | 0.6667 |
| 2020.01.04 | 0.6667 |
| 2020.01.05 | 1 |
| 2020.01.06 | 1 |
| 2020.01.07 | 0.3333 |
| 2020.01.08 | 0.3333 |
| 2020.01.09 | 0.3333 |
| 2020.01.10 | 1 |

```
mrank(m, window=1w, percent = 1)
```

| label | A |
| --- | --- |
| 2020.01.01 | 1 |
| 2020.01.02 | 1 |
| 2020.01.03 | 0.6667 |
| 2020.01.04 | 0.75 |
| 2020.01.05 | 1 |
| 2020.01.06 | 1 |
| 2020.01.07 | 0.4286 |
| 2020.01.08 | 0.2857 |
| 2020.01.09 | 0.1429 |
| 2020.01.10 | 0.7143 |

相关函数：[rank](../r/rank.html)

