# rowDot

## 语法

`rowDot(X, Y)`

## 参数

**X** 和 **Y** 是长度相同的数值型向量或数组向量，或维度相同的矩阵。若 *X* 和
*Y* 为数组向量，它们对应位置的向量必须具有相同长度。

## 详情

若 *X* 和 *Y* 同时为向量/矩阵，按行计算 *X* 和 *Y* 的内积。若
*X* 和 *Y* 同时为索引矩阵，会对齐标签，对标签相同的行进行计算，标签不同的行直接返回 NULL。

若 *X* 和 *Y* 一个为向量，一个为矩阵，则向量的长度必须与矩阵的列数相同，计算向量与矩阵每一行的内积。

若 *X* 和 *Y* 是数组向量，计算 *X* 和
*Y* 对应位置的向量的内积，即 dot(X.row(i),Y.row(i))。

若 *X* 和 *Y*
一个为向量，一个为数组向量，计算向量与数组向量内每个向量的内积。两个向量的长度相同时返回计算结果，长度不相同时返回 NULL。

与所有其它聚合函数一致，计算时忽略 NULL 值。

## 例子

```
rowDot(13.5 15.2 6.3, 18.6 14.8 15.5)
// output
[251.1,224.96,97.65]

s1=indexedSeries(2020.01.01..2020.01.03, 10.4 11.2 9)
s2=indexedSeries(2020.01.01 2020.01.03 2020.01.04, 23.5 31.2 26)
rowDot(s1,s2)
// output
[244.4,349.44,234]

m=matrix(23 56 47, 112 94 59)
m1=matrix(11 15 89, 52 41 63)
rowDot(m,m1)
// output
[6077,4694,7900]

m.rename!(2020.01.01..2020.01.03, `A`B)
m.setIndexedMatrix!()
m1.rename!(2020.01.01 2020.01.03 2020.01.04, `A`B)
m1.setIndexedMatrix!()
rowDot(m,m1)
// output
[6077,NULL,3124,NULL]

a=array(DOUBLE[],0,10)
a.append!([[10.5, 11.8, 9],[15, NULL], [2.5, 2.2, 1.3, 1.5]])
b=array(DOUBLE[],0,10)
b.append!([[1.1, 1.8, 6],[5, 6.9], [3.5, 2, 3, 2.8]])
rowDot(a,b)
// output
[86.79,75,21.25]
```

相关函数：[dot](../d/dot.md)

