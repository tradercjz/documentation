# rowBeta

## 语法

`rowBeta(Y, X)`

row 系列函数通用参数说明和计算规则请参考：[rowFunctions](../themes/rowFunctions.html)

## 详情

逐行计算 *Y* 在 *X* 上的回归系数的最小二乘估计，返回一个长度与输入参数行数相同的向量。

## 例子

```
m1=matrix([4.5 2.6 1.5, 1.5 4.8 5.9, 4.9 2.0 NULL])
m2=matrix(49.6 NULL 29.52, 50.32 51.29 26.23, NULL 74.97 23.75)
rowBeta(m1, m2)
// output
[-4.1667,-0.1182, -1.3374]

m3=matrix(8 NULL 10, 8 NULL 4, 14 NULL NULL)
rowBeta(m3, m2)
// output
[0, , 1.8237]

a= 110 112.3 44 98
b= 57.9 39 75 90
c= 55 64 37 78
x=array(DOUBLE[],0, 10).append!([a, b, c])
y=array(DOUBLE[],0, 10).append!([b, a, c])
rowBeta(x, y)
// output
[0.6783, 1 , -0.3202, 1]
```

相关函数：[beta](../b/beta.html)

