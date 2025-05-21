# encodeShortGenomeSeq

## 语法

`encodeShortGenomeSeq(X)`

别名：`encodeSGS`

## 参数

**X** STRING 类型标量或向量、CHAR 类型向量。

## 详情

对 DNA 序列（由 A, T, C, G 自由组合）进行编码。通过编码，可以减小 DNA 序列的存储空间，提高计算效率。

注意：

* 若 *X* 指定为空字符（""），则函数返回0。
* 若 *X* 中包含了除 A, T, C, G（大小写敏感）以外的字符，则返回空值。
* 若 *X* 指定的字符串所包含的字符个数超过了28，则返回空值。

## 返回值

长整型（LONG）或长整型向量（FAST LONG VECTOR）

## 例子

```
a=encodeShortGenomeSeq("TCGATCG")
a;
// output
465691
typestr(a)
// output
LONG

b=encodeShortGenomeSeq("TCGATCG" "TCGATCGCCC")
// output
[465691,168216298]
typestr(b)
// output
FAST LONG VECTOR

// "TCGATCG"重复5次后，因长度超过了28，所以返回了空值。
encodeShortGenomeSeq(repeat("TCGATCG" "TCGAT", 5))
// output
[,1801916404867712433]

y=toCharArray("TCGATCGCCC")
encodeShortGenomeSeq(y)
// output
168216298

encodeShortGenomeSeq("TC G")
// output
00l
encodeShortGenomeSeq("TCtG")
// output
00l
// 基因序列中出现 N，编码返回空。
encodeShortGenomeSeq("NNNNNNNNTCGGGGCAT")
// output
00l
encodeShortGenomeSeq("TCGGGGCATNGCCCG")
// output
00l
encodeShortGenomeSeq("GCCCGATNNNNN")
// output
00l
```

相关函数：[decodeShortGenomeSeq](../d/decodeShortGenomeSeq.md), [genShortGenomeSeq](../g/genShortGenomeSeq.md)

