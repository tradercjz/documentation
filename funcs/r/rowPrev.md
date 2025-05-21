# rowPrev

## 语法

`rowPrev(X)`

## 详情

逐行将 *X* 向右移动一个位置。

## 参数

row 系列函数通用参数说明和计算规则请参考：[rowFunctions](../themes/rowFunctions.md)。

## 例子

```
m=matrix([4.5 2.6 1.5, 1.5 4.8 5.9, 4.9 2.0 NULL])
rowPrev(m)
```

返回：

| col1 | col2 | col3 |
| --- | --- | --- |
|  | 4.5 | 1.5 |
|  | 2.6 | 4.8 |
|  | 1.5 | 5.9 |

```
a=array(INT[], 0, 10).append!([1 2 3, 4 5, 6 7 8]);
rowPrev(a)

//output: [[00i,1,2],[00i,4],[00i,6,7]]

tp = [[1.3,2.5,2.3], [4.1,5.3,6.2]]
tp.setColumnarTuple!()
rowPrev(tp)

//output: [[00F,1.3,2.5],[00F,4.1,5.3]]
```

