# rowCorr

## 语法

`rowCorr(X, Y)`

row 系列函数通用参数说明和计算规则请参考：[rowFunctions](../themes/rowFunctions.md)

## 详情

逐行计算 *X* 和 *Y* 之间的相关性，返回一个长度与输入参数行数相同的向量。

## 例子

```
m1=matrix(2 -1 4, 8 3 2, 9 0 1)
m2=matrix(8 11 10, 8 17 4, 14 6 4)
rowCorr(m1, m2)
// output
[0.61, 0.7559, 0.9449]

m3=matrix(8 NULL 10, 8 NULL 4, 14 NULL NULL)
rowCorr(m1, m3)
// output
[0.61, , 1]

a=array(DOUBLE[], 0, 10).append!([1 2 3, 4 NULL 5, 6 7 8, NULL 3 10]);
b=array(DOUBLE[], 0, 10).append!([[1.3,1.2, 4], [1.0,1.4, 2], [1.1, 1.4, 3],[1, 4, 7]]);

rowBeta(a, b)
// output
[0.535, 1 , 0.9105, 2.3333]
```

相关函数：[corr](../c/corr.md)

