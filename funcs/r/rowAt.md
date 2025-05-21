# rowAt

## 语法

`rowAt(X, [Y])`

row 系列函数通用参数说明和计算规则请参考：[rowFunctions](../themes/rowFunctions.md)

## 参数

**X** 矩阵、数组向量或列式元组。

**Y**
整型向量、布尔型矩阵、整型或布尔型数组向量或列式元组。

## 详情

逐行取出 *X* 中对应索引的元素，返回一个与 *Y*
长度相同的向量。若索引无对应元素或索引超出 *X* 的有效索引范围，则返回空值。

* 若 *Y* 是整型向量，*Y* 的每个元素表示 *X* 每行的列索引，逐行取出
  *X* 中对应索引的元素，返回一个与 *Y* 长度相同的向量。若索引无对应元素或索引超出 *X*
  的有效索引范围，则返回空值。
* 若 *Y* 是布尔类型的矩阵或数组向量（或列式元组），则取出 *X* 对应于 *Y*
  中 true 值的元素，返回一个与 *Y* 行数相同的数组向量。若 *Y* 中某一行的所有元素值都是
  false，则该行返回空值。其中，当 Y 是布尔类型矩阵时，X 只能是矩阵。
* 若 *Y* 是整型数组向量（或列式元组），*Y* 的每个元素表示 *X*
  每行的列索引，逐行取出 *X* 中对应索引的元素，返回一个与 *Y* 维度相同的数组向量（或列式元组）。若索引无对应元素或索引超出
  *X* 的有效索引范围，则返回空值。
* 若 *Y* 不指定，*X* 必须是布尔类型的矩阵或数组向量（或列式元组）。该函数逐行取出
  *X* 中元素值是 true 的索引。返回一个整型数组向量（或列式元组），其行数和 *X* 的行数相同。若 *X*
  中某一行的所有元素值都是空值或 false，则该行返回空值。

## 例子

```
m = matrix(3.1 4.5 2.2, 4.2 4.3 5.1, 6.2 7.1 2.2, 1.8 6.1 5.3, 7.1 8.4 3.5)
index = 4 0 2
rowAt(m, index)
// output
[7.1,4.5,2.2]

trades = table(10:0,`time`sym`p1`p2`p3`p4`p5`vol1`vol2`vol3`vol4`vol5,[TIMESTAMP,SYMBOL,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,INT,INT,INT,INT,INT])
insert into trades values(2022.01.01T09:00:00, `A, 33.2, 33.8, 33.6, 33.3, 33.1, 200, 180, 180, 220, 200)
insert into trades values(2022.01.01T09:00:00, `A, 33.1, 32.8, 33.2, 34.3, 32.3, 150, 280, 190, 100, 220)
insert into trades values(2022.01.01T09:00:00, `A, 31.2, 32.6, 33.6, 35.3, 34.5, 220, 160, 130, 100, 110)
insert into trades values(2022.01.01T09:00:00, `A, 30.2, 32.5, 33.6, 35.3, 34.1, 200, 180, 150, 140, 120)
insert into trades values(2022.01.01T09:00:00, `A, 33.2, 33.8, 33.6, 33.3, 33.1, 180, 160, 160, 180, 200)
select rowAt(matrix(p1, p2, p3, p4, p5), rowImin(vol1, vol2, vol3, vol4, vol5)) as price1, rowAt(matrix(p1, p2, p3, p4, p5), rowImax(vol1, vol2, vol3, vol4, vol5)) as price2 from trades
```

表 1. 查询返回

| price1 | price2 |
| --- | --- |
| 33.8 | 33.3 |
| 34.3 | 32.8 |
| 35.3 | 31.2 |
| 34.1 | 30.2 |
| 33.8 | 33.1 |

```
index = array(INT[], 0, 10).append!([0 1, 2 4, 3 4 5])
rowAt(m, index)
// output
[[3.1,4.2],[7.1,8.4],[5.3,3.5,]]

x = array(DOUBLE[], 0, 10).append!([3.3 3.6 3.8, 3.7 3.4 3.5, 3.4 3.4 3.5])
index = array(INT[], 0, 10).append!([0 1, 2, 0 2])
rowAt(x, index)
// output
[[3.3,3.6],[3.5],[3.4,3.5]]
```

2.00.10.2 及以上版本，当 *X* 是布尔类型矩阵或数组向量时，*Y* 可以不指定，此时
`rowAt` 返回每行中 true 元素的索引。

```
m = matrix(true false false, false true false, true true false)
R=rowAt(m)
R
// output
[[0,2],[1,2],]
typestr(R)
// output
FAST INT[] VECTOR

m = matrix(3.1 4.5 2.2, 2.2 4.3 5.1, 1.2 7.1 2.2, 1.8 6.1 5.3, 1 4 3)
rowAt(m, m>4)
// output
[,[4.5,4.3,7.1,6.1],[5.1,5.3]]

x = array(DOUBLE[], 0, 10).append!([3.3 3.6 3.8, 3.7 3.4 3.5, 3.4 3.4 3.5])
rowAt(x, x>3.5)
// output
[[3.6,3.8],[3.7],]
```

对列式元组与数组向量应用 `rowAt`：

```
x = ([1, 2, 3], [4, 5, 6]).setColumnarTuple!()
y = fixedLengthArrayVector([1, 4], [2, 5], [3, 6])

rowAt(x, x > 1)
// output
([2,3],[4,5,6])

rowAt(y, y>1)
// output
[[2,3],[4,5,6]]
```

**相关信息**

* [at](../a/at.html "at")

