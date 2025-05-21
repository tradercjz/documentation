# euclidean

## 语法

`euclidean(X, Y)`

## 参数

**X** 和 **Y** 是长度相同的数值型标量/向量/矩阵。

## 详情

若 *X* 和 *Y* 是标量或向量，计算 *X* 和 *Y* 之间的欧氏距离。

若 *X* 和 *Y* 是矩阵，计算每列元素之间的欧式距离，返回一个向量。 注意，若 *X* 或 *Y*
同时为索引矩阵或索引序列，会自动对齐标签，返回标签相同的行的计算结果，忽略标签不同的行。

与所有其它聚合函数一致，计算时忽略 NULL 值。

## 例子

```
a=[100, 0, 0]
b=[0, 51, NULL]
euclidean(a,b)
// output
112.254176

s1=indexedSeries(1 2 4, 10.4 11.2 9)
s2=indexedSeries(1 2 5, 23.5 31.2 26)
euclidean(s1,s2)
// output
23.9084

m=matrix(23 56 47, 112 94 59)
euclidean(a,m)
// output
[106.1791,111.6288]

m1=matrix(11 15 89, 52 41 63)
euclidean(m,m1)
// output
[59.9083,80.1561]

m.rename!(2020.01.01..2020.01.03, `A`B)
m.setIndexedMatrix!()
m1.rename!(2020.01.01 2020.01.03 2020.01.04, `A`B)
m1.setIndexedMatrix!()
euclidean(m,m1)
// output
[34.176,62.6418]
```

相关函数：[rowEuclidean](../r/rowEuclidean.html)

