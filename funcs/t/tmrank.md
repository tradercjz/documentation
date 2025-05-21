# tmrank

## 语法

`tmrank(T, X, ascending, window, [ignoreNA=true], [tiesMethod='min'],
[percent=false])`

部分通用参数说明和窗口计算规则请参考：[tmFunctions](../themes/tmFunctions.md)

## 参数

**ascending** 是一个布尔值，表示是否按升序排序。默认值是 true。

**ignoreNA** 是一个布尔值，表示是否忽略 NULL 值。true 表示忽略 NULL 值（默认值），false 表示 NULL 值参与排名，此时
NULL 值为最小值。

**tiesMethod** 是一个字符串，表示窗口内若存在重复值时，排名如何选取。

* 'min'表示取最小排名。
* 'max'表示取最大排名。
* 'average'表示取排名的均值。

**percent** 是一个布尔值，表示是否以百分比形式显示返回的排名，默认值为 false。

## 详情

在给定长度（以时间 *T* 衡量）的滑动窗口内计算 *X* 元素在其对应窗口内的排名。

## 例子

```
tmrank(1 1 3 5 8 15 15 20, 5 2 4 1 2 8 9 10, ascending=true, window=3)
// output
[0,0,1,0,0,0,1,0]

index = take(datehour(2019.06.13 13:30:10),4) join (datehour(2019.06.14 13:30:10)+1..6)
data = 1 NULL 3 4 5 NULL 3 NULL 5 3

tmrank(index, data, ascending=true, window=4h)
// output
[0,,1,2,0,,0,,1,0]

tmrank(index, data, ascending=true, window=2d)
// output
[0,,1,2,3,,1,,4,1]
```

相关函数：[mrank](../m/mrank.md), [rank](../r/rank.md)

