# rowWavg

## 语法

`rowWavg(X, Y)`

row 系列函数通用参数说明和计算规则请参考：[rowFunctions](../themes/rowFunctions.md)

## 详情

逐行计算 *X* 以 *Y* 为权重的加权平均，返回一个长度与输入参数行数相同的向量。

## 例子

```
m1=matrix(2 -1 4, 8 3 2, 9 0 1)
m2=matrix(8 11 10, 8 17 4, 14 6 4)
rowWavg(m1, m2)
// output
[6.8667, 1.1765, 2.8889]

m3=matrix(2 NULL 4, 8 NULL 2, 9 NULL NULL)
rowWavg(m3, m2)
// output
[6.8667, , 3.4286]

a= -10 12.3 -10 -8
b= 17.9 9 7.5 -4
c= 5.5 5.5 -7 8

rowWavg(matrix(a, b, c), matrix(b, a, c))
// output
[-24.459, 9.3899, 10.6316, -32]

x=array(DOUBLE[],0, 10).append!([a, b, c])
y=array(DOUBLE[],0, 10).append!([b, a, c])
rowWavg(x, y)
// output
[-3.6612, 7.0892, 14.4583]
```

相关函数：[wavg](../w/wavg.md)

