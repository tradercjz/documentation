# tmsum2

## 语法

`tmsum2(T, X, window)`

参数说明和窗口计算规则请参考：[tmFunctions](../themes/tmFunctions.md)

## 详情

在给定长度（以时间 *T* 衡量）的滑动窗口内计算 *X* 元素的平方和。请注意，该函数的返回值是 DOUBLE 类型。

## 例子

```
tmsum2(1 1 3 5 8 15 15 20, 5 2 4 1 2 8 9 10, 3)
// output
[25,29,45,17,4,64,145,100]

index = take(datehour(2019.06.13 13:30:10),4) join (datehour(2019.06.13 13:30:10)+1..6)
data = 1 NULL 3 4 5 NULL 3 NULL 5 3
tmsum2(index, data, 4h)
// output
[1,1,10,26,51,51,60,34,34,43]

tmsum2(index, data, 1d)
// output
[1,1,10,26,51,51,60,60,85,94]
```

相关函数：[msum2](../m/msum2.md), [sum2](../s/sum2.md)

