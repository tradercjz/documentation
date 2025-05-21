# gmd5

## 语法

`gmd5(X)`

## 参数

**X** 可以是标量、向量、元组、数组向量、数据对或矩阵。

## 详情

根据 MD5 算法，对 X 的所有元素进行哈希。当 X 是元组/数组向量/数据对/矩阵时，对其平铺后计算 MD5 哈希值。

**返回值：**INT128 类型标量

## 例子

```
gmd5([1 2 3])
// output: 2a1dd1e1e59d0a384c26951e316cd7e6

gmd5([[1, 2], 3])
// 因为构建 MD5 的数据完全一致，所以输出也一致
// output: 2a1dd1e1e59d0a384c26951e316cd7e6

xs = array(INT[], 0, 10).append!([1 2 3, 4 5, 6 7 8, 9 10])
gmd5(xs)
// output: c457b6addd2869161f8a853c0f247aaf

ys = [1 2 3, 4 5, 6 7 8, 9 10]
gmd5(ys)
// output: c457b6addd2869161f8a853c0f247aaf

m=matrix(1 2 3, 8 7 0)
gmd5(m)
// output: 660a82bc074f9dccc5c9fbb806f44f5c
```

相关函数：[rowGmd5](../r/rowgmd5.html)

