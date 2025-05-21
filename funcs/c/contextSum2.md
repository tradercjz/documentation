# contextSum2

## 语法

`contextSum2(X, Y)`

## 参数

**X** 和 **Y** 是向量、矩阵或表。

## 详情

找出 *X* 和 *Y* 中元素都不为 NULL 的位置，并计算 *X* 中这些位置对应的元素的平方和。

即使 *X* 的数据类型是 INT 或 LONG，返回结果的数据类型总是 DOUBLE 类型。

## 例子

```
contextSum2(1 2 3, 10 NULL 30);
// output
10

contextSum2(1 2 3, true false true);
// output
14
```

相关函数：[contextCount](contextCount.md), [contextSum](contextSum.md)

