# asof

## 语法

`asof(X, Y)`

## 参数

**X** 必须是一个递增的向量、索引序列、索引矩阵；

**Y** 可以是标量、向量、数组向量、元组、矩阵、字典、表。

## 详情

对于每个 *Y* 中的元素 y，`asof` 返回 *X* 中不大于 y
的元素的最大序号（从 0 开始编号）。如果没有找到，则返回-1。

## 例子

```
asof(1..100, 60 200 -10)
// output
[59,99,-1]

0 0 0 1 1 1 1 2 2 3 asof 1
// output
6
```

