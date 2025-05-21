# tmskew

## 语法

`tmskew(T, X, window, [biased=true])`

部分通用参数说明和窗口计算规则请参考：[tmFunctions](../themes/tmFunctions.md)

## 参数

**biased** 是一个布尔值，表示是否是有偏估计。默认值为 true，表示有偏估计。

## 详情

在给定长度（以时间 *T* 衡量）的滑动窗口内计算 *X* 的斜度。

## 例子

```
tmskew(1 1 3 5 8 15 15 20, 5 2 4 1 2 8 9 10, 3)
// output
[,0,-0.381801774160607,0,,,0,]
index = take(datehour(2019.06.13 13:30:10),4) join (datehour(2019.06.13 13:30:10)+1..6)
data = 1 NULL 3 4 5 NULL 3 NULL 5 3
tmskew(index, data, 4h)
// output
[,,,-0.3818,,,0,0,0,0.7071]
tmskew(index, data, 2d)
// output
[,,0,-0.3818,-0.4347,-0.4347,-0.37,-0.37,-0.5653,-0.4363]
```

相关函数：[mskew](../m/mskew.md), [skew](../s/skew.md)

