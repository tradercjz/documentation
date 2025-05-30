# rowRank

## 语法

`rowRank(X, [ascending=true], [groupNum], [ignoreNA=true],
[tiesMethod='min'], [percent=false], [precision])`

## 详情

逐行计算 *X* 的元素排名或组排名，排名方式请参照 [rank](rank.md)，返回一个和 *X* 维度相同的矩阵。

## 参数

row 系列函数通用参数说明和计算规则请参考：[rowFunctions](../themes/rowFunctions.md)。

**ascending** 是一个布尔值，表示排序方向。true 表示升序，false 表示降序。默认值为 true。它是一个可选参数。

**groupNum** 是一个正整数，表示排序形成的组的数量。它是一个可选参数。

**ignoreNA** 是一个布尔值，表示是否忽略 NULL 值。true 表示忽略 NULL 值，false 表示 NULL 值参与排名。默认值为
true。它是一个可选参数。NULL 值参与排序时，NULL 值为最小值。

**tiesMethod** 是一个字符串，表示如何对具有相同值的元素进行排名。

* 'min'表示取最小排名。
* 'max'表示取最大排名。
* 'average'表示取排名的均值。
* 'first' 表示按照原数据的顺序排名。

**percent** 是一个布尔值，表示是否以百分比形式显示返回的排名。

**precision** 是一个 [1, 15] 范围内的整数，用于设置参与排序的值的精度。若两个值之差的绝对值小于等于 10^(-precision)
，则认为两值相等。

注： 指定 *precision* 参数后，*X* 只能是数值型对象。且
*tiesMethod* 不能指定为 'first'。

## 例子

```
m=matrix(3 1 2 4 7 6 9 8 5, 9 NULL 2 3 5 6 3 2 8).transpose();
m
```

返回：

| #0 | #1 | #2 | #3 | #4 | #5 | #6 | #7 | #8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 1 | 2 | 4 | 7 | 6 | 9 | 8 | 5 |
| 9 |  | 2 | 3 | 5 | 6 | 3 | 2 | 8 |

```
m.rowRank();
```

返回：

| #0 | #1 | #2 | #3 | #4 | #5 | #6 | #7 | #8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 0 | 1 | 3 | 6 | 5 | 8 | 7 | 4 |
| 7 |  | 0 | 2 | 4 | 5 | 2 | 0 | 6 |

```
m.rowRank(false);
```

返回：

| #0 | #1 | #2 | #3 | #4 | #5 | #6 | #7 | #8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6 | 8 | 7 | 5 | 2 | 3 | 0 | 1 | 4 |
| 0 |  | 6 | 4 | 3 | 2 | 4 | 6 | 1 |

```
m.rowRank(groupNum=3);
```

返回：

| #0 | #1 | #2 | #3 | #4 | #5 | #6 | #7 | #8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 1 | 2 | 1 | 2 | 2 | 1 |
| 2 |  | 0 | 0 | 1 | 1 | 0 | 0 | 2 |

```
m.rowRank(ignoreNA=false);
```

返回：

| #0 | #1 | #2 | #3 | #4 | #5 | #6 | #7 | #8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 0 | 1 | 3 | 6 | 5 | 8 | 7 | 4 |
| 8 | 0 | 1 | 3 | 5 | 6 | 3 | 1 | 7 |

```
m.rowRank(ignoreNA=false, tiesMethod='max');
```

返回：

| #0 | #1 | #2 | #3 | #4 | #5 | #6 | #7 | #8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 0 | 1 | 3 | 6 | 5 | 8 | 7 | 4 |
| 8 | 0 | 2 | 4 | 5 | 6 | 4 | 2 | 7 |

```
m.rowRank(ignoreNA=false, tiesMethod='first');
```

返回：

| col1 | col2 | col3 | col4 | col5 | col6 | col7 | col8 | col9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 0 | 1 | 3 | 6 | 5 | 8 | 7 | 4 |
| 8 | 0 | 1 | 3 | 5 | 6 | 4 | 2 | 7 |

**相关信息**

* [rowDenseRank](rowDenseRank.html "rowDenseRank")
* [rank](rank.html "rank")

