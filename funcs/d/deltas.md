# deltas

## 语法

`deltas(X,[n])`

## 参数

**X** 是一个向量、矩阵或表。

**n** 可选参数，一个整数，用于减数相较于被减数的索引偏移。默认是1。

## 详情

对于 *X* 中的每一个元素，计算 *X*i-*X*i-n，NULL 值不参与计算。

* 若 *X* 是向量，返回一个包含 *X* 中两个元素之差的向量。
* 若 *X* 是矩阵，在每列内进行上述计算，返回一个与 *X* 维度相同的矩阵。
* 若 *X* 是表，在每列内进行上述计算，返回一个与 *X* 行数与列数都相同的表。

## 例子

```
x=7 4 5 8 9;
deltas(x);
//output: [,-3,1,3,1]
//等价于 [, 4-7, 5-4, 8-5, 9-8]

x=NULL 1 2 NULL 3;
deltas(x);
//output： [,,1,,]

m=matrix(1 3 2 5 6, 0 8 NULL 7 6);
m;
```

| #0 | #1 |
| --- | --- |
| 1 | 0 |
| 3 | 8 |
| 2 |  |
| 5 | 7 |
| 6 | 6 |

```
deltas(m);
```

| #0 | #1 |
| --- | --- |
|  |  |
| 2 | 8 |
| -1 |  |
| 3 |  |
| 1 | -1 |

*n* 是正整数时：

```
deltas(m,2)
```

| 0 | 1 |
| --- | --- |
|  |  |
|  |  |
| 1 |  |
| 2 | -1 |
| 4 |  |

*n* 为负整数时：

```
deltas(m,-2)
```

| 0 | 1 |
| --- | --- |
| -1 |  |
| -2 | 1 |
| -4 |  |
|  |  |
|  |  |

