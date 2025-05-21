# tanimoto

## 语法

`tanimoto(X, Y)`

## 参数

**X** 和 **Y** 是长度相同的数值型标量/向量/矩阵。

## 详情

若 *X* 和 *Y* 是标量或向量，计算 *X* 和 *Y* 之间的谷本距离。

若 *X* 或 *Y* 是矩阵，计算每列元素之间的谷本距离，返回一个向量。 注意，若 *X* 或 *Y*
同时为索引矩阵或索引序列，会自动对齐标签，返回标签相同的行的计算结果，忽略标签不同的行。

与所有其它聚合函数一致，计算时忽略 NULL 值。

## 例子

```
a=[10.5, 11.8, 9]
b=[11.3, 15.1, 8.9]
tanimoto(a,b)
// output
0.029706

s1=indexedSeries(2020.01.01..2020.01.03, 10.4 11.2 9)
s2=indexedSeries(2020.01.01 2020.01.03 2020.01.04, 23.5 31.2 26)
tanimoto(s1,s2)
// output
0.5585

m=matrix(23 56 47, 112 94 59)
m1=matrix(11 15 89, 52 41 63)
tanimoto(m,m1)
// output
[0.40490.3242]

m.rename!(2020.01.01..2020.01.03, `A`B)
m.setIndexedMatrix!()
m1.rename!(2020.01.01 2020.01.03 2020.01.04, `A`B)
m1.setIndexedMatrix!()
tanimoto(m,m1)
// output
[0.5494,0.3225]
```

相关函数：[rowTanimoto](../r/rowTanimoto.md)

