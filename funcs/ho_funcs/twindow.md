# twindow

## 语法

`twindow(func, funcArgs, T, range, [prevailing=false],
[excludedPeriod])`

## 参数

* **func** 是一个聚合函数。
* **funcArgs** 是 *func* 的参数。*func*
  有多个参数时，它是一个元组。
* **T** 是一个非严格递增的整型或时间类型的向量。
* **range** 是一个整型数据对或 DURATION 数据对，左右边界都包含在内。
* **prevailing** 只能为 0/false，1/true 或 2。
  + 如果 *prevailing* = 0/false，则滑动窗口不对边界重复值做处理，请阅读详情部分。
  + 如果 *prevailing* = 1/true，则滑动窗口边界的选取规则同 [pwj](../../progr/sql/windowjoin.html)。
  + 如果 *prevailing* = 2，（假设 *range* 参数为 d1:d2）：

    - 若 d1 为 0，则滑动窗口将把当前索引对象作为边界，窗口左边的重复值不参与计算。
    - 若 d2 为 0，则滑动窗口将把当前索引对象作为边界，窗口右边的重复值不参与计算。
    - 当前情况下不可以同时设置参数 *excludedPeriod*。
* **excludedPeriod** 是　TIME、NANOTIME、MINUTE 和 SECOND
  类型的数据对。用于设定一个交易日内的非交易时间段（该时间段被排除在计算窗口之外）。若设置该参数，必须同时保证以下3点：

  + 数据对中的右值必须大于左值。
  + 时间段长度必须小于 (24 - *range*)
  + *T* 中不能包含 *excludedPeriod* 区间内的时间，且数据类型必须是 TIMESTAMP,
    NANOTIMESTAMP, TIME 或 NANOTIME。

## 详情

应用函数/运算符到给定对象的滑动窗口。对给定对象的每一个元素，滑动窗口由 *T* 和 *range* 决定。
结果的维度与 *funcArgs* 的维度相同（若 *funcArgs* 是一个元组，结果的维度与该元组中每个元素的维度相同）。

滑动窗口的确定规则（假设 *range* 参数为 d1:d2）：

1. *range* 是整型数据对时：

   * *T* 如果为整型向量，对 *T* 内元素 Ti，可以确定
     *T* 对应的窗口范围为 [Ti+d1,
     Ti+d2]。
   * *T* 如果为时间类型向量，*range* 的精度默认为 *T*
     的精度，对于 *T* 内元素 Ti，确定的窗口范围为
     [temporalAdd(Ti, d1, unit),
     temporalAdd(Ti, d2, unit)]，其中 unit 是
     *T* 的精度。
2. *range* 是 DURATION 数据对时，*T* 只能是时间类型向量，对于
   *T* 内元素 Ti，确定 *T* 对应的窗口元素范围为
   [temporalAdd(Ti, d1), temporalAdd(Ti,
   d2)]。

与 `tmoving` 函数相比，`twindow`
函数具有更灵活的窗口。`tmoving` 可以视为 `twindow` 指定
*range* 右边界为 0 的特殊情况， 但需要注意以时间长度衡量窗口时，两者对窗口边界的处理有区别：

1. `twindow`
   窗口的右边界与多条相同的值匹配时，该窗口会包含所有重复匹配的记录。当其窗口左边界与多条相同的值匹配时， 若 *prevailing* =
   true，则窗口只包含最后一个值；若 *prevailing* = false，则窗口亦会包含所有重复值。
2. `tmoving` 函数的窗口范围为(Ti - window,
   Ti] 或 (temporalAdd(Ti - window), Ti]，即
   `tmoving` 函数只基于当前滑动到的记录，确定一个向前的窗口，
   不考虑右边界是否有重复值；且左边界不包含在内。

## 例子

*prevailing* = false，左边界对应多个重复值，计算窗口会包含所有重复值

```
t = 2021.01.02 2021.01.02 2021.01.06 2021.03.09 2021.03.10 2021.03.12 2021.03.12
x = -5 5 NULL -1 2 4 -8
twindow(func=min,funcArgs=x,T=t,range=0:2)
```

输出返回：[-5, -5, , -1, -8, -8, -8]

*prevailing* = true，左边界对应多个重复值，计算窗口只包含最后一个值

```
twindow(func=min, funcArgs=x, T=t, range=0:3, prevailing=true)
```

输出返回：[5, 5, ,-8, -8, -8, -8]

```
twindow(func=max, funcArgs=x, T=t, range=0d:3d)
```

输出返回：[5, 5, , 4, 4, 4, 4]

```
twindow(func=max, funcArgs=x, T=t, range=0:3, prevailing=true)
```

输出返回：[5, 5, , 4, 4, -8, -8]

```
twindow(func=max, funcArgs=x, T=t, range=0M:3M)
```

输出返回：[5, 5, 4, 4, 4, 4, 4]

```
twindow(func=max, funcArgs=x, T=t, range=0M:3M, prevailing=true)
```

输出返回：[5, 5, 4, 4, 4, -8, -8]

```
y = 4.8 9.6 7.1 3.3 5.9 2.7 6.9
twindow(func=corr, funcArgs=(x,y), T=t, range=0:3)
```

输出返回：[1, 1, , -0.685, -0.7893, -1, -1]

```
t1 = table(`A`A`B`B`C`C as sym, 09:56:03 09:56:07 09:56:02 09:56:05 09:56:04 09:56:06 as time, 10.6 10.7 20.6 11.6 11.7 19.6 as price)
select *, twindow(func=avg, funcArgs=t1.price, T=t1.time, range=2s:4s) from t1 context by sym
```

返回：

| sym | time | price | window\_avg |
| --- | --- | --- | --- |
| A | 09:56:03 | 10.6 | 10.7 |
| A | 09:56:07 | 10.7 |  |
| B | 09:56:02 | 20.6 | 11.6 |
| B | 09:56:05 | 11.6 |  |
| C | 09:56:04 | 11.7 | 19.6 |
| C | 09:56:06 | 19.6 |  |

下例通过 *excludedPeriod* 参数指定股市上午的休市时间，计算长度为一分钟的滑动窗口内的价格平均值。

```
excludedPeriod=(11:30:00:13:00:00)
ts=timestamp(2023.11.01T11:21:00+1..500) join timestamp(2023.11.01T13:00:00+1..500)
t=table(ts, rand(10.0,size(ts)) as price)

// 通过 excludedPeriod 指定休市时间为11:30:00 到 13:00:00，则此段时间被忽略，不会被作为计算窗口。
res1=select ts, twindow(func=avg, T=ts, funcArgs=price, range=-1m:0m, excludedPeriod=excludedPeriod) from t
// 不指定 excludedPeriod 时，休市时间也会被考虑为计算窗口。
res2=select ts, twindow(func=avg, T=ts, funcArgs=price, range=-1m:0m) from t

// 对比是否指定 excludedPeriod 的计算结果。
select * from res1 where ts between timestamp(2023.11.01T13:00:00) and timestamp(2023.11.01T13:01:00)

select * from res2 where ts between timestamp(2023.11.01T13:00:00) and timestamp(2023.11.01T13:01:00)
```

只传入前四个参数，且设置 *prevailing* 为
2。

```
t=[09:30:00.020,09:30:00.020,09:30:00.020,09:30:00.030,09:30:00.040,09:30:00.040]
v=0 1 2 3 5 4
twindow(min,v,t,0ms:10ms,prevailing = 2)
//Output: [0,1,2,3,4,4]
twindow(min,v,t,-10ms:0ms,prevailing = 2)
//Output: [0,0,0,0,3,3]

//非法输入
twindow(min,v,t,-10ms:10ms,prevailing = 2)
//Output: Usage: twindow(func, funcArgs, T, range, [prevailing=0], [excludedPeriod]). left offset or right offset must be zero when prevailing =2.
twindow(min,v,t,0ms:0ms,prevailing = 2)
//Output: Usage: twindow(func, funcArgs, T, range, [prevailing=0], [excludedPeriod]). 0:0 is illegal window when prevailing =2.
```

