# makeKey

## 语法

`makeKey(args...)`

## 参数

**args** 是多个标量或长度相同的向量。

## 详情

对于输入的多个 *args*，将它们的值组合为一个 BLOB 标量或向量。返回的结果可用作字典或集合的 key。相较于
`makeSortedKey`，`makeKey` 不会保存组合值的排序结果。

## 例子

```
makeKey(`a1,`b1,`c1)
// output
a1b1c1

set(makeKey(1 2, 4 5))

re=makeKey(`a1`a2, `_1`_2)
dict(re,100 200)

// output
a2_2->200
a1_1->100
```

相关函数：[makeSortedKey](makeSortedKey.html)

