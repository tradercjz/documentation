# rowCovar

## 语法

`rowCovar(X, Y)`

row 系列函数通用参数说明和计算规则请参考：[rowFunctions](../themes/rowFunctions.html)

## 详情

逐行计算 *X* 和 *Y* 之间的协方差，返回一个长度与输入参数行数相同的向量。

## 例子

```
m1=matrix(2 8 9 12, 9 14 11 8,-3 NULL NULL 9)
m2=matrix(11.2 3 5 9, 7 -10 8 5,17 12 18 9)
rowCovar(m1, m2)
// output
[-29.7333, -39, 3, 3.3333]

a= 110 112.3 44 98
b= 57.9 39 75 90
c= 55 64 37 78
x=array(DOUBLE[],0, 10).append!([a, b, c])
y=array(DOUBLE[],0, 10).append!([b, a, c])

rowCovar(x, y)
// output
[-327.9475, -327.9475, 295]
```

```
// 定义一个随机数据集x

x = rand(1.0, 1000000)

// 自定义了一个聚合函数，窗口长度为5，滑动计算窗口内 x 和它排序后数据的协方差
timer moving(defg(x):covar(x, sort(x)), x, 5)
// output
1928.888 ms

// movingWindowIndex 滑动选取 x 的5个元素的索引，movingTopNIndex 滑动选取 x 的5个元素排序后的索引。通过 rowCovar 函数计算
timer rowCovar(x[movingWindowIndex(x, 5)], x[movingTopNIndex(x, 5, 5)])
// output
232.407 ms
```

相关函数：[covar](../c/covar.html)

