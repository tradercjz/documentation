# rowVar

## 语法

`rowVar(args...)`

row 系列函数通用参数说明和计算规则请参考：[rowFunctions](../themes/rowFunctions.md)

## 详情

逐行进行元素求样本方差操作，返回一个长度与输入参数行数相同的向量。

## 例子

```
m=matrix([4.5 2.6 1.5, 1.5 4.8 5.9, 4.9 2.0 NULL]);
rowVar(m);
// output
[3.453333,2.173333,9.68]

t1=table(1..5 as x, 10..6 as y, take(3, 5) as z);
t2=table(5..1 as a, 6..10 as b, take(8, 5) as c);

rowVar(t1);
// output
[22.333333,14.333333,8.333333,4.333333,2.333333]

rowVar(t1[`x], t2, 1 1 2 2 2);
// output
[9.7,9.3,8.7,11,14.7]

t=table(`AAPL`MS`IBM`IBM`C as sym, 49.6 29.46 29.52 30.02 174.97 as price1, 175.23 50.76 50.32 51.29 26.23 as price2);
select sym,rowVar(price1,price2) as var from t;
```

| sym | var |
| --- | --- |
| AAPL | 7891.44845 |
| MS | 226.845 |
| IBM | 216.32 |
| IBM | 226.20645 |
| C | 11061.7938 |

相关函数：[rowVarp](rowVarp.md), [varp](../v/varp.md)

