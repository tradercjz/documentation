# rowMove

## 语法

`rowMove(X, steps)`

## 参数

row 系列函数通用参数说明和计算规则请参考：[rowFunctions](../themes/rowFunctions.html)。

**steps** 是一个整数，表示移动多少位置。

* 如果 *steps* 为正数，*X* 向右移动 *steps* 个位置；
* 如果 *steps* 为负数，*X* 向左移动 *steps* 个位置；
* 如果 *steps* 为 0，不改变 *X* 的位置。

## 详情

根据 *steps* 的设置，逐行移动元素。

## 例子

```
m=matrix([4.5 2.6 1.5, 1.5 4.8 5.9, 4.9 2.0 NULL])
rowMove(m, 2)
```

返回：

| col1 | col2 | col3 |
| --- | --- | --- |
|  |  | 4.5 |
|  |  | 2.6 |
|  |  | 1.5 |

```
rowMove(m, -2)
```

返回：

| col1 | col2 | col3 |
| --- | --- | --- |
| 4.9 |  |  |
| 2 |  |  |
|  |  |  |

```
a=array(INT[], 0, 10).append!([1 2 3, 4 5, 6 7 8]);
rowMove(a, 2)

//output: [[00i,00i,1],[00i,00i],[00i,00i,6]]

tp = [[1.3,2.5,2.3], [4.1,5.3,6.2]]
tp.setColumnarTuple!()
rowMove(tp, -2)

//output: [[2.3,00F,00F],[6.200000000000001,00F,00F]]
```

