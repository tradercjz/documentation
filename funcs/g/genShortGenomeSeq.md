# genShortGenomeSeq

## 语法

`genShortGenomeSeq(X, window)`

别名：`genSGS`

## 参数

**X** STRING 类型标量或 CHAR 类型的向量。

**window** 正整数，范围为[2,28]。

## 详情

对给定长度（以字符个数衡量）的滑动窗口内的 DNA 序列进行编码，不忽略空值。返回一个整型向量，其长度与 *X*
包含的字符个数相同。

注：

* 该函数使用向后的窗口，即从当前元素开始向后选取元素。
* 若 *window* 大于 *X*
  中所有字符的个数，则返回一个空的整型向量。

返回值：

| window 范围 | 返回值类型 |
| --- | --- |
| [2,4] | 短整型向量（FAST SHORT VECTOR） |
| [5,12] | 整型向量（FAST INT VECTOR） |
| [13,28] | 返回长整型向量（FAST LONG VECTOR） |

## 例子

```
genShortGenomeSeq("NNNNNNNNTCGGGGCAT",3)
// output
[,,,,,,,,795,815,831,831,830,824,801,,]

genShortGenomeSeq("TCGGGGCATNGCCCG",4)
// output
[1135,1215,1279,1278,1272,1249,,,,,1258,1195,,,]

genShortGenomeSeq("GCCCGATNNNNN",6)
// output
[396972,395953,,,,,,,,,,]
genShortGenomeSeq("TCGATCGTCGATCGTCGATCGTCGATCGG",5)
// output
[328113,328390,328475,327789,328118,328411,328556,328113,328390,328475,327789,328118,328411,328556,328113,328390,328475,327789,328118,328411,328556,328113,328390,328475,327791,,,,]
genShortGenomeSeq("ACTT",8)
// output
[,,,]
```

相关函数：[encodeShortGenomeSeq](../e/encodeShortGenomeSeq.html), [decodeShortGenomeSeq](../d/decodeShortGenomeSeq.html)

