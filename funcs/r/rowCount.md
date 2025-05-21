# rowCount

## 语法

`rowCount(args...)`

row 系列函数通用参数说明和计算规则请参考：[rowFunctions](../themes/rowFunctions.html)

## 详情

逐行进行非空值的统计操作，返回一个长度与输入参数行数相同的向量。

## 例子

```
m=matrix([4.5 2.6 1.5, 1.5 4.8 5.9, 4.9 2.0 NULL]);
rowCount(m);
// output
[3,3,2]

t1=table(1 NULL 3 NULL 5 as x, 6..10 as y);
t2=table(5 NULL 3 NULL 1 as a, 10..6 as b);
rowCount(t1);
// output
[2,1,2,1,2]

rowCount(t1[`x], t2, 1 NULL 2 NULL NULL);
// output
[4,1,4,1,3]

t=table(`AAPL`MS`IBM`IBM`C as sym, [49.6, NULL, 29.52, NULL, 174.97] as price1, [175.23, NULL, 50.32, 51.29, 26.23] as price2);
select sym,rowCount(price1,price2) as count from t;
```

| sym | count |
| --- | --- |
| AAPL | 2 |
| MS | 0 |
| IBM | 2 |
| IBM | 1 |
| C | 2 |

相关函数：[rowSize](rowSize.html), [count](../c/count.html)

