# rowProd

## 语法

`rowProd(args...)`

row 系列函数通用参数说明和计算规则请参考：[rowFunctions](../themes/rowFunctions.md)

## 详情

逐行进行元素求乘积操作，返回一个长度与输入参数行数相同的向量。

## 例子

```
m=matrix([4.5 2.6 1.5, 1.5 4.8 5.9, 4.9 2.0 NULL])
rowProd(m);
// output
[33.075,24.96,8.85]

v1=1 0 2 -2 5
v2=-8 1 2 4 2
rowProd(v1, v2);
// output
[-8,0,4,-8,10]

t=table(`AAPL`MS`IBM`IBM`C as sym, 49.6 29.46 29.52 30.02 174.97 as price1, 175.23 50.76 50.32 51.29 26.23 as price2)
select * from t where rowOr(price1>50, price2>50);
```

| sym | price |
| --- | --- |
| AAPL | 8691.408 |
| MS | 1495.3896 |
| IBM | 1485.4464 |
| IBM | 1539.7258 |
| C | 4589.4631 |

相关函数：[prod](../p/prod.md)

