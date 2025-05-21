# rowOr

## 语法

`rowOr(args...)`

row 系列函数通用参数说明和计算规则请参考：[rowFunctions](../themes/rowFunctions.html)

## 详情

逐行进行逻辑或操作，返回一个长度与输入参数行数相同的向量。

## 例子

```
m=matrix([true false false, true true true, true true true])
rowOr(m);
// output
[1,1,1]

t1=table(false true true true false as x, false true false true true as y)
rowOr(t1);

0,1,1,1,1]]

t=table(`AAPL`MS`IBM`IBM`C as sym, 49.6 29.46 29.52 30.02 174.97 as price1, 175.23 50.76 50.32 51.29 26.23 as price2)
select *  from t where rowOr(price1>30, price2>100);
```

| sym | price1 | price2 |
| --- | --- | --- |
| AAPL | 49.6 | 175.23 |
| IBM | 30.02 | 51.29 |
| C | 174.97 | 26.23 |

相关函数：[or](../o/or.html)

