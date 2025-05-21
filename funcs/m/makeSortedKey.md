# makeSortedKey

## 语法

`makeSortedKey(args...)`

## 参数

**args** 是多个标量或长度相同的向量。

## 详情

对于输入的多个 *args*，将它们的值组合为一个 BLOB 标量或向量。相较于
`makeKey`，`makeSortedKey` 内部会保存组合值的排序结果，但输出结果与
`makeKey` 相同。

## 例子

```
makeSortedKey([`b,`a,`c], [`4,`2,`1])
// output
["b4","a2","c1"]

set(makeSortedKey(1 2, 4 5))
```

