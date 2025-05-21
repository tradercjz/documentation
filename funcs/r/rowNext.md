# rowNext

## 语法

`rowNext(X)`

## 详情

逐行将 *X* 向左移动一个位置。

## 参数

row 系列函数通用参数说明和计算规则请参考：[rowFunctions](../themes/rowFunctions.html)。

## 例子

```
m=matrix([4.5 2.6 1.5, 1.5 4.8 5.9, 4.9 2.0 NULL])
rowNext(m)
```

返回：

| col1 | col2 | col3 |
| --- | --- | --- |
| 1.5 | 4.9 |  |
| 4.8 | 2 |  |
| 5.9 |  |  |

```
a=array(INT[], 0, 10).append!([1 2 3, 4 5, 6 7 8]);
rowNext(a)

//output: [[2,3,00i],[5,00i],[7,8,00i]]

tp = [[1.3,2.5,2.3], [4.1,5.3,6.2]]
tp.setColumnarTuple!()
rowNext(tp)

//output: [[2.5,2.3,00F],[5.3,6.2,00F]]
```

