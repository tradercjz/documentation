# tmLowRange

## 语法

`tmLowRange(T, X, window)`

参数说明和窗口计算规则请参考：[tmFunctions](../themes/tmFunctions.md)

## 详情

在给定长度（以时间 *T* 衡量）的滑动窗口内，统计每个元素 Xi 左侧相邻且连续大于它的元素个数。NULL 被视为最小值。

## 例子

```
t = [0, 1, 2, 3, 7, 8, 9, 10, 11]
x = [NULL, 3.1, NULL, 3.0, 2.9, 2.8, 3.1, NULL, 3.2]
tmLowRange(t, x, window=3)
// output: [,0,1,0,0,1,0,2,0]

tmLowRange(t, x, window=4)
// output: [,0,1,0,0,1,0,3,0]

index = take(datehour(2019.06.13 13:30:10),4) join (datehour(2019.06.13 13:30:10)+1..6)
data = 1 NULL 3 4 5 NULL 3 NULL 5 3
tmLowRange(index, data, 4h)
// output: [0,1,0,0,0,3,0,1,0,1]
```

