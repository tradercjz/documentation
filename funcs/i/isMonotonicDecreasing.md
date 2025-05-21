# isMonotonicDecreasing

## 语法

`isMonotonicDecreasing(X)`

## 参数

**X** 可以是标量或向量。

## 详情

判断 *X* 是否为单调递减。

## 例子

```
a=[10,7,5,2,int()];
isMonotonicDecreasing(a);
// output
true

a=[10.5,8.7,int(),5.3,1.0];
isMonotonicDecreasing(a);
// output
false

a=[5,10,14,20,int()];
isMonotonicDecreasing(a);
// output
false
```

相关函数：[isMonotonicIncreasing](isMonotonicIncreasing.md), [isMonotonic](isMonotonic.md)

