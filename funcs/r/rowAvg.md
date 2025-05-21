# rowAvg

## 语法

`rowAvg(args...)`

row 系列函数通用参数说明和计算规则请参考：[rowFunctions](../themes/rowFunctions.md)

## 详情

逐行进行元素求平均操作，返回一个长度与输入参数行数相同的向量。

## 例子

```
m=matrix([4.5 2.6 1.5, 1.5 4.8 5.9, 4.9 2.0 NULL])
rowAvg(m);
// output
[3.633333,3.133333,3.7]

t1=table(1..5 as x, 6..10 as y)
t2=table(5..1 as a, 10..6 as b);
rowAvg(t1);
// output
[3.5,4.5,5.5,6.5,7.5]

rowAvg(t1[`x], t2, take(1, 5));
// output
[4.25,4,3.75,3.5,3.25]

t=table(`AAPL`MS`IBM`IBM`C as sym, 49.6 29.46 29.52 30.02 174.97 as price1, 175.23 50.76 50.32 51.29 26.23 as price2)
select sym,rowAvg(price1,price2) as avg from t;
```

| sym | price1 |
| --- | --- |
| AAPL | 112.415 |
| MS | 40.11 |
| IBM | 39.92 |
| IBM | 40.655 |
| C | 100.6 |

相关函数：[avg](../a/avg.md)

