# rowSum2

## 语法

`rowSum2(args...)`

row 系列函数通用参数说明和计算规则请参考：[rowFunctions](../themes/rowFunctions.md)

## 详情

逐行进行元素求平方和操作，返回一个长度与输入参数行数相同的向量。

## 例子

```
m=matrix([4.5 2.6 1.5, 1.5 4.8 5.9, 4.9 2.0 NULL]);
rowSum2(m);
// output
[46.51,33.8,37.06]

t1=table(1..5 as x, 6..10 as y);
t2=table(5..1 as a, 10..6 as b);

rowSum2(t1);
// output
[37,53,73,97,125]

rowSum2(t1[`x], t2, 1 1 2 2 2);
// output
[127,102,86,73,66]

t=table(`AAPL`MS`IBM`IBM`C as sym, 49.6 29.46 29.52 30.02 174.97 as price1, 175.23 50.76 50.32 51.29 26.23 as price2);
select sym,rowSum2(price1,price2) as price2Sum from t;
```

| sym | priceSum |
| --- | --- |
| AAPL | 224.83 |
| MS | 80.22 |
| IBM | 79.84 |
| IBM | 81.31 |
| C | 201.2 |

相关函数：[sum2](../s/sum2.md)

