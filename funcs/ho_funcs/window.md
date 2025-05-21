# window

## 语法

`window(func, funcArgs, range)`

## 参数

* **func** 是一个聚合函数。
* **funcArgs** 是 *func* 的参数。*func* 有多个参数时，它是一个元组。
* **range** 是一个整型数据对或 DURATION 数据对，左右边界都包含在内。

注： 如果 *range* 是 DURATION 类型，则 *funcArgs*
必须是一个索引矩阵（indexed matrix）或者是索引序列（indexed series）。

## 详情

应用函数/运算符到给定对象的滑动窗口。对给定对象的每一个元素，滑动窗口由 *range* 决定。结果的维度与 *funcArgs* 的维度相同（若
*funcArgs* 是一个元组， 结果的维度与该元组中每个元素的维度相同）。

滑动窗口的确定规则（假设 *range* 参数为 d1:d2）：

1. 若 *funcArgs* 为向量，*range* 必须为整型。对 *funcArgs* 中第 i
   位的元素，窗口所含元素的位置区间为 [i+d1, i+d2] 。
2. 若 *funcArgs* 为索引序列或索引矩阵：

   * 若 *funcArgs* 的索引为时间类型，对 *funcArgs* 中索引为 fi 的元素，其对应的窗口索引范围为
     [temporalAdd(fi, d1), temporalAdd(fi, d2)]。
   * 若 *funcArgs* 的索引为整型，*range* 必须亦为整型。对 *funcArgs* 中索引为
     fi 的元素，其对应的窗口索引范围为 [fi+d1, fi+d2] 。

与 `moving` 函数相比，`window`
函数具有更灵活的窗口。`moving` 可以视为 `window` 指定 *range*
右边界为 0 的特殊情况。但需要注意以下两点：

1. 元素个数决定窗口长度时，窗口内元素个数不足时，`moving` 函数将输出空值，但
   `window` 会输出计算结果。
2. 时间长度决定窗口长度时，`moving` 确定的窗口左开右闭，但 `window`
   确定窗口左闭右闭。详见以下说明：

假定索引类型为 DATETIME, 需要指定一个长度为 “3d” 的窗口进行滑动窗口计算。对于索引中的某个时间点 “2022.01.05T09:00:00”，
`moving` 函数根据该时间点确定的窗口为
(2022.01.02T09:00:00，2022.01.05T09:00:00]，`window` 指定
*range* 为 “-2d:0d”， 确定的窗口为 [2022.01.03T09:00:00，2022.01.05T09:00:00]。

## 例子

*funcArgs* 为向量, 确定窗口位置区间为 [i+1,i+3], i 是 x 的下标。

```
x = 5 4 NULL -1 2 4
window(min, x, 1:3)
// output
[-1, -1, -1, 2, 4, ]

y = 4.8 9.6 7.1 3.3 5.9 2.7
window(corr, (x, y), 1:3)
// output
[1, 1, -0.623, -1, , ]
```

*funcArgs* 为索引序列, 索引为时间类型，确定的窗口范围为 [temporalAdd(ti, 1d), temporalAdd(ti, 3d)]，ti
是 t 第 i 个元素对应的值。

```
t = 2021.01.02 2021.01.05 2021.01.06 2021.01.09 2021.01.10 2021.01.12
x1 = indexedSeries(t, x)
window(min, x1, 1d:3d)
```

| label | col1 |
| --- | --- |
| 2021.01.02 | 4 |
| 2021.01.05 |  |
| 2021.01.06 | -1 |
| 2021.01.09 | 2 |
| 2021.01.10 | 4 |
| 2021.01.12 |  |

*funcArgs* 为索引矩阵, 索引为时间，确定索引对应的窗口范围 [temporalAdd(ti, 1d), temporalAdd(ti,
3d)]，ti 是 t 第 i 个元素对应的值。 以 a, b 列分组进行滑动窗口计算。

```
t= 2021.01.02 2021.01.05  2021.01.06  2021.01.09 2021.01.10 2021.01.12
m=matrix(5 4 NULL -1 2 4, 3 2 8 1 0 5)
m1=m.rename!(t, `a`b).setIndexedMatrix!()
window(min, m1, 1d:3d)
```

| label | a | b |
| --- | --- | --- |
| 2021.01.02 | 4 | 2 |
| 2021.01.05 |  | 8 |
| 2021.01.06 | -1 | 1 |
| 2021.01.09 | 2 | 0 |
| 2021.01.10 | 4 | 5 |
| 2021.01.12 |  |  |

```
t1 = table(`A`A`B`B`C`C as sym, 09:56:03 09:56:07 09:56:02 09:56:05 09:56:04 09:56:06 as time, 10.6 10.7 20.6 11.6 11.7 19.6 as price)
select *, window(avg, t1.time.indexedSeries(t1.price), 2s:4s) from t1 context by sym
```

| sym | time | price | window\_avg |
| --- | --- | --- | --- |
| A | 09:56:03 | 10.6 | 10.7 |
| A | 09:56:07 | 10.7 |  |
| B | 09:56:02 | 20.6 | 11.6 |
| B | 09:56:05 | 11.6 |  |
| C | 09:56:04 | 11.7 | 19.6 |
| C | 09:56:06 | 19.6 |  |

