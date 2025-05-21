# rowStd

## 语法

`rowStd(args...)`

row 系列函数通用参数说明和计算规则请参考：[rowFunctions](../themes/rowFunctions.html)

## 详情

逐行进行元素求样本标准差操作，返回一个长度与输入参数行数相同的向量。

## 例子

```
m=matrix([4.5 2.6 1.5, 1.5 4.8 5.9, 4.9 2.0 NULL])
rowStd(m);
// output
[1.858315,1.474223,3.11127]

t1=table(1..5 as x, 10..6 as y, take(3, 5) as z)
t2=table(5..1 as a, 6..10 as b, take(8, 5) as c);

rowStd(t1);
// output
[4.725816,3.785939,2.886751,2.081666,1.527525]

rowStd(t1[`x], t2, 1 1 2 2 2);
// output
[3.114482,3.04959,2.949576,3.316625,3.834058]

t=table(`AAPL`MS`IBM`IBM`C as sym, 49.6 29.46 29.52 30.02 174.97 as price1, 175.23 50.76 50.32 51.29 26.23 as price2)
select sym,rowStd(price1,price2) as std from t;
```

| sym | std |
| --- | --- |
| AAPL | 88.833825 |
| MS | 15.061374 |
| IBM | 14.707821 |
| IBM | 15.040161 |
| C | 105.175063 |

相关函数：[rowStdp](rowStdp.html), [std](../s/std.html)

