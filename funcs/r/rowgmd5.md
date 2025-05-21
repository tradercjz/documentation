# rowGmd5

## 语法

`rowGmd5(args...)`

## 参数

**args** 是数组向量或列式元组。

## 详情

逐行计算 gmd5。

**返回值：**一个长度与 *args* 行数相同的 INT128 向量。

## 例子

```
xs = array(INT[], 0, 10).append!([1 2 3, 4 5, 6 7 8, 9 10])
rowGmd5(xs)
// output: [2a1dd1e1e59d0a384c26951e316cd7e6,678157bbe4fd35371e047b4cadf9c46a,ff93cd8c0033f2ab93726d48661d1221,10986ac9310ecb2f10c3a5524eb38999]
// 输出四行，每个元素对应array vector中的每行，如1 2 3对应2a1dd1e1e59d0a384c26951e316cd7e6

gmd5(1 2 3)
// output: 2a1dd1e1e59d0a384c26951e316cd7e6

rowGmd5(xs, xs)
// output: [50420aa84aa547ebc24dfa3ef8fffa57,de90d6c74c0b99f5656b95563a9a35b7,376579b27ec7c2f6eed7347ef0e5a15b,78bf6752e93cbca5fd1dcc3519fc6c55]

ys = [1 2 3, 4 5, 6 7 8, 9 10]
ys.setColumnarTuple!(true)
rowGmd5(xs, ys)
// output: [50420aa84aa547ebc24dfa3ef8fffa57,de90d6c74c0b99f5656b95563a9a35b7,376579b27ec7c2f6eed7347ef0e5a15b,78bf6752e93cbca5fd1dcc3519fc6c55]
```

相关函数：[gmd5](../g/gmd5.html)

