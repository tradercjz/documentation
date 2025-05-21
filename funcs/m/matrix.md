# matrix

## 语法

`matrix(X1, [X2], ...)`

或

`matrix(dataType, rows, cols, [columnsCapacity], [defaultValue])`

或

`matrix(X)`

## 参数

* 第一种情况中，**X1**, **X2**, **...**
  可以是混合类型，包括向量、矩阵、表（不能包含 SYMBOL 字段）、元组或它们的任意组合。
* 第二种情况中：

  **dataType** 是矩阵的数据类型，支持除
  INT128、UUID、IPADDR、POINT 和 DURATION 外的其他数据类型。

  **rows** 是行数。

  **cols**
  是列数。

  **columnsCapacity**
  是正整数，表示矩阵的容量，即新建该矩阵时，系统为该矩阵分配的内存（以列数为单位）。当列数超过 *capacity*
  时，系统会自动扩充容量。系统首先会分配当前容量1.2~2倍的内存，然后复制数据到新的内存空间，最后释放原来的内存。

  **defaultValue**
  是矩阵的默认值。不指定默认值，对于整数或浮点数类型，矩阵中所有的元素都是 0，对于符号类型，所有元素都是 NULL。
* 第三种情况下：**X** 是一个数组向量（arrayVector），且数组向量每个元素的长度必须相等。

## 详情

返回一个矩阵。

## 例子

```
x=matrix(INT,3,2, ,1);
x;
```

| #0 | #1 |
| --- | --- |
| 1 | 1 |
| 1 | 1 |
| 1 | 1 |

```
y = matrix(DECIMAL32(3),2,3)
y
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 0.000 | 0.000 | 0.000 |
| 0.000 | 0.000 | 0.000 |

```
s=matrix(SYMBOL,2,2, ,`T);
s;
```

| #0 | #1 |
| --- | --- |
| T | T |
| T | T |

```
matrix(table(1 2 3 as id, 4 5 6 as value));
```

| #0 | #1 |
| --- | --- |
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |

```
matrix([1 2 3, 4 5 6]);
```

| #0 | #1 |
| --- | --- |
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |

```
matrix([1 2 3, 4 5 6], 7 8 9, table(0.5 0.6 0.7 as id), 1..9$3:3);
```

| #0 | #1 | #2 | #3 | #4 | #5 | #6 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 4 | 7 | 0.5 | 1 | 4 | 7 |
| 2 | 5 | 8 | 0.6 | 2 | 5 | 8 |
| 3 | 6 | 9 | 0.7 | 3 | 6 | 9 |

```
matrix(`AA`BB`CC,`DD`EE`FF)
```

输出为：

| #0 | #1 |
| --- | --- |
| AA | DD |
| BB | EE |
| CC | FF |

当表中含有 SYMBOL 字段时，通过 matrix 进行转换时会出现报错，如下例：

```
t = table(symbol(["a", "b"]) as sym, [1, 2] as val)
matrix(t)
// output: matrix(t) => Failed to append a table object to a matrix.
```

将 SYMBOL 类型转换为 STRING 类型后，可以进行转换，见如下代码：

```
t = table(string(["a", "b"]) as sym, [1, 2] as val)
matrix(t)
```

| #1 | #2 |
| --- | --- |
| a | 1 |
| b | 2 |

**相关信息**

* [array](../a/array.html "array")
* [dict](../d/dict.html "dict")

