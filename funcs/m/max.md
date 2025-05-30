# max

## 语法

`max(X, [Y])`

## 参数

**X** 可以是标量、向量、矩阵或表。

**Y** 为可选参数，可以是标量或者是和 *X* 长度相同的向量或者矩阵。

## 详情

对于只输入一个参数的情况，函数的返回值说明如下：

* 若 *X* 是向量，返回 *X* 中所有元素的最大值。
* 若 *X* 为矩阵，计算每列的最大值，返回一个向量。
* 若 *X* 为表，计算每列的最大值，返回一个表。

对于输入两个参数的情况，函数返回值说明如下：

* 若 *Y* 是标量，则与 *X* 中所有元素进行比较，用较大值替换 *X* 中的元素并返回。
* 若 *Y* 和 *X* 类型和长度一致，则将两者对应位置的元素进行比较，返回较大的结果。

请注意，从 2.00.8 版本开始，`max`
处理时间类型数据的行为（之前版本统一转换为长整型）修改为：

* 若 *X* 和 *Y* 是时间类型标量，系统会将时间类型统一为两者中较高精度对应的类型，再比较大小。
* 若 *X* 或 *Y* 是向量、矩阵或表，则必须具有相同的时间类型。

## 例子

```
max(1 2 3);
// output
3

max(7.8 9 5.4);
// output
9

(5 8 2 7).max();
// output
8

m=matrix(1 2 3, 4 5 6);
m;
```

| #0 | #1 |
| --- | --- |
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |

```
max(m);
// output
[3,6]
```

```
max(1 2 3, 2)
// output
2 2 3

n = matrix(1 1 1, 5 5 5)
n;
```

| #0 | #1 |
| --- | --- |
| 1 | 5 |
| 1 | 5 |
| 1 | 5 |

```
max(m, n);
```

| #0 | #1 |
| --- | --- |
| 1 | 5 |
| 2 | 5 |
| 3 | 6 |

`max` 可以搭配 select 使用, 返回某列的最大值：

```
t = table(`abb`aac`aaa as sym, 1.8 2.3 3.7 as price);
select max price from t;
```

| max\_price |
| --- |
| 3.7 |

max 可以应用于字符串，返回字典序最大的字符串：

```
select max sym from t;
```

| max\_sym |
| --- |
| abb |

相关函数：[mmax](mmax.md)

