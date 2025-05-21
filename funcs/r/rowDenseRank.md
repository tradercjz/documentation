# rowDenseRank

## 语法

`rowDenseRank(X, [ascending=true], [ignoreNA=true], [percent=false])`

## 参数

row 系列函数通用参数说明和计算规则请参考：[rowFunctions](../themes/rowFunctions.html)。

**ascending** 是一个布尔值，表示排序方向。true 表示升序，false 表示降序。默认值为 true。它是一个可选参数。

**ignoreNA** 是一个布尔值，表示是否忽略 NULL 值。true 表示忽略 NULL 值，false 表示 NULL 值参与排名。默认值为
true。它是一个可选参数。NULL 值参与排序时，NULL 值为最小值。

**percent** 是一个布尔值，表示是否以百分比形式显示返回的排名。

## 详情

逐行计算 *X* 的元素连续排名，排名方式请参照 [denseRank](../d/denseRank.html)，返回一个和 *X* 维度相同的矩阵。

## 例子

```
m = matrix(1 5 8 5 9, 2 8 2 5 2, 6 5 3 3 4)
rowDenseRank(m)
```

返回：

| col1 | col2 | col3 |
| --- | --- | --- |
| 0 | 1 | 2 |
| 0 | 1 | 0 |
| 2 | 0 | 1 |
| 1 | 1 | 0 |
| 2 | 0 | 1 |

返回：

```
y=matrix(1 3 3, 6 5 6, NULL 0 9)
rowDenseRank(y)
```

返回：

| col1 | col2 | col3 |
| --- | --- | --- |
| 0 |  | 1 |
| 1 | 2 | 0 |
| 0 | 1 | 2 |

```
rowDenseRank(y, ignoreNA=false)
```

返回：

| col1 | col2 | col3 |
| --- | --- | --- |
| 1 | 2 | 0 |
| 1 | 2 | 0 |
| 0 | 1 | 2 |

**相关信息**

* [denseRank](../d/denseRank.html "denseRank")
* [rowRank](rowRank.html "rowRank")

