# decodeShortGenomeSeq

## 语法

`decodeShortGenomeSeq(X)`

别名：`decodeSGS`

## 参数

**X** 整型标量或向量。

## 详情

将经过 `encodeShortGenomeSeq` 编码的整型数字解码为一个 DNA 序列。

## 返回值

字符串（STRING）或字符串向量（STRING VECTOR）

## 例子

```
a=encodeShortGenomeSeq("TCGATCG")
decodeShortGenomeSeq(a)
// output
"TCGATCG"

b=encodeShortGenomeSeq("TCGATCG" "TCGATCGCCC")
decodeShortGenomeSeq(b)
// output
["TCGATCG","TCGATCGCCC"]

// 当输入为空时，返回空字符串。
decodeShortGenomeSeq(int(NULL))
// output
""

// 因"TCGATCG"重复5次后，长度超过了28，所以返回了空的整型向量，再通过 decodeSGS 解码时，会返回为空字符。
c=encodeShortGenomeSeq(repeat("TCGATCG" "TCGAT", 5))
decodeShortGenomeSeq(c)
// output
[,"TCGATTCGATTCGATTCGATTCGAT"]
```

相关函数：[encodeShortGenomeSeq](../e/encodeShortGenomeSeq.html), [genShortGenomeSeq](../g/genShortGenomeSeq.html)

