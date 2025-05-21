# tmsum

## 语法

`tmsum(T, X, window)`

参数说明和窗口计算规则请参考：[tmFunctions](../themes/tmFunctions.md)

## 详情

在给定长度（以时间 *T* 衡量）的滑动窗口内计算 *X* 的元素和。

## 例子

```
tmsum(1 1 3 5 8 15 15 20, 5 2 4 1 2 8 9 10, 3)
// output
[5,7,11,5,2,8,17,10]
index = take(datehour(2019.06.13 13:30:10),4) join (datehour(2019.06.13 13:30:10)+1..6)
data = 1 NULL 3 4 5 NULL 3 NULL 5 3
tmsum(index, data, 4h)
// output
[1,1,4,8,13,13,16,8,8,11]
tmsum(index, data, 1d)
// output
[1,1,4,8,13,13,16,16,21,24]
```

相关函数：[msum](../m/msum.md), [sum](../s/sum.md)

