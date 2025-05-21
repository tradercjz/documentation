# symbolCode

## 语法

`symbolCode(X)`

## 参数

**X** 是 SYMBOL 类型的向量或矩阵。

## 详情

返回一个与 *X* 相同维度的整型向量或矩阵，表示 SYMBOL 类型数据的内部编码。空字符串的内部编码为0。

SYMBOL 类型是特殊的字符串类型，在系统内部的存储结构为一个编码字典。将设备名，股票名等字符串重复较多的向量存储为 SYMBOL
类型，可以达到向量压缩的目的。

## 例子

```
a=symbol(`IBM`APPL)
symbolCode(a)
```

输出返回：[1,2]

```
x=symbol(`MS`AMZN`AAPL`MS`IBM`AAPL)$3:2
symbolCode(x)
```

输出返回：

| #0 | #1 |
| --- | --- |
| 1 | 1 |
| 2 | 4 |
| 3 | 3 |

