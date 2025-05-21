# rowSum

## 语法

`rowSum(args...)`

row 系列函数通用参数说明和计算规则请参考：[rowFunctions](../themes/rowFunctions.html)

## 详情

逐行进行元素求和操作，返回一个长度与输入参数行数相同的向量。

## 例子

```
m=matrix([4.5 2.6 1.5, 1.5 4.8 5.9, 4.9 2.0 NULL])
rowSum(m);
// output
[10.9,9.4,7.4]

t1=table(1..5 as x, 6..10 as y)
t2=table(5..1 as a, 10..6 as b);

rowSum(t1);
// output
[7,9,11,13,15]

rowSum(t1[`x], t2, 1 1 2 2 2);
// output
[17,16,16,15,14]

t=table(`AAPL`MS`IBM`IBM`C as sym, 49.6 29.46 29.52 30.02 174.97 as price1, 175.23 50.76 50.32 51.29 26.23 as price2)
select sym,rowSum(price1,price2) as priceSum from t;
```

| sym | priceSum |
| --- | --- |
| AAPL | 224.83 |
| MS | 80.22 |
| IBM | 79.84 |
| IBM | 81.31 |
| C | 201.2 |

相关函数：[sum](../s/sum.html)

