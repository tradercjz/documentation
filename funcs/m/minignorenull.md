# minIgnoreNull

## 语法

`minIgnoreNull(X, Y)`

## 参数

**X** 和 **Y** 是数值型、LITERAL 或 TEMPORAL 型的标量/数据对/向量/矩阵。

## 详情

一个二元标量函数，返回两个数（*X* 和 *Y*）中的最小值。

它与 `min` 作为二元标量函数区别在于对空值的处理：

* `min`：当配置项 *nullAsMinValueForComparison=*true
  时，空值被视为最小值进行比较；否则空值不参与比较，结果返回空值。
* `minIgnoreNull`：不受配置项 *nullAsMinValueForComparison*
  的影响。返回 *X* 或 *Y* 中的非空值，或者如果两者都非空，返回最小值。

## 例子

```
minIgnoreNull(2,matrix(1  NULL -4,-1 -4  0))
```

| #0 | #1 |
| --- | --- |
| 1 | -1 |
| 2 | -4 |
| -4 | 0 |

```
minIgnoreNull(matrix(10 3 NULL, 1 7 4),matrix(1  NULL -4,-1 -4  0))
```

| #0 | #1 |
| --- | --- |
| 1 | -1 |
| 3 | -4 |
| -4 | 0 |

使用 `reduce` 结合
`minIgNoreNull`，计算元组中存储的同形状矩阵每个位置的最小值，忽略空值。

```
n1 = matrix(1 1 1, 5 5 5)
n2 = matrix(10 11 12, 0 NULL -5)
n3 = matrix(-1 1 NULL, -3 0 10)
reduce(minIgnoreNull, [n1,n2,n3])
```

相关函数：[min](min.md), [maxIgnoreNull](maxignorenull.md)

