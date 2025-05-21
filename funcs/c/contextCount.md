# contextCount

## 语法

`contextCount(X, Y)`

## 参数

**X** 和 **Y** 必须是相同长度的向量。

## 详情

计算 *X* 和 *Y* 中相同位置都不为 NULL 的元素个数。

## 例子

```
contextCount(1 2 3, 1 NULL 3)
// output
2

contextCount(1..3,true false true)
// output
3

contextCount(1 2 NULL, 1 NULL 3)
// output
1
```

相关函数：[contextSum](contextSum.md), [contextSum2](contextSum2.md)

