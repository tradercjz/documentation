# mmaxPositiveStreak

## 语法

`mmaxPositiveStreak(X, window)`

窗口计算规则请参考：[mFunctions](../themes/mFunctions.html)

## 参数

**X** 是一个向量/矩阵/表/由等长向量组成的元组。其中，mmse, mslr 仅支持输入向量。

**window** 是大于等于 2 的正整型或 DURATION 标量。表示滑动窗口的长度。

注： 在流计算引擎中调用滑动窗口函数时，window 的上限为 102400。

## 详情

在给定长度（以元素个数衡量）的滑动窗口内统计 *X* 中连续正数之和的最大值。

## 例子

```
x = 1 -1 1 -2 10 3 3 9 0 6 5
w = 5
mmaxPositiveStreak(x, w)
// output
[,,,,10,13,16,25,25,15,12]

x = 5 NULL 3 2 1 5 10 9 NULL 9 10 -1 NULL
w = 5
mmaxPositiveStreak(x, w)
// output
[,,,,6,11,21,27,25,24,19,19,19]

// 搭配 signum 函数用于统计向量中出现的连续正数的最大个数
mmaxPositiveStreak(signum(x), w)
// output
[,,,,3,4,5,5,4,3,2,2,2]
```

