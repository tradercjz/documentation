# atImax

## 语法

`atImax(location, value)`

## 参数

**location** 和 **value** 是向量、矩阵或表。

## 详情

找出 *location* 中最大值所在的位置，然后返回 *value* 中该位置对应的值。如果 *location*
中有多个相同的最大值，则取第一个最大值所在的位置。

若 *location* 和 *value* 是矩阵，则 *location* 和 *value* 的每列一一对应，分别计算
`atImax`。

atImax(location, value) 相当于 value[imax(location)]。

## 例子

```
atImax(3 5 1 2, 9 7 5 3)
// output
7

m1=matrix(9 2 1 5 6 9, 3 1 3 NULL 5 2, 2 8 1 2 3 4)
m2=matrix(1..6, 1..6, 1..6)
atImax(m1,m2)
// output
[1,5,2]
```

相关函数：[imax](../i/imax.md), [atImin](atImin.md)

