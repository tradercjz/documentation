# rowStdp

## 语法

`rowStdp(args...)`

row 系列函数通用参数说明和计算规则请参考：[rowFunctions](../themes/rowFunctions.html)

## 详情

逐行进行元素求总体标准差操作，返回一个长度与输入参数行数相同的向量。

## 例子

```
m=matrix([4.5 2.6 1.5, 1.5 4.8 5.9, 4.9 2.0 NULL])
rowStdp(m);
// output
[1.517307556898806,1.203698005684518,2.2]

t1=table(1..5 as x, 10..6 as y, take(3, 5) as z)
t2=table(5..1 as a, 6..10 as b, take(8, 5) as c);
rowStdp(t1);
// output
[3.858612300930075,3.091206165165235,2.357022603955159,1.699673171197595,1.247219128924648]

rowStdp(t1[`x], t2, 1 1 2 2 2);
// output
[2.785677655436824,2.727636339397171,2.638181191654584,2.966479394838265,3.42928563989645]

t=table(`AAPL`MS`IBM`IBM`C as sym, 49.6 29.46 29.52 30.02 174.97 as price1, 175.23 50.76 50.32 51.29 26.23 as price2)
select sym,rowStdp(price1,price2) as stdp from t;
```

| sym | stdp |
| --- | --- |
| AAPL | 62.815 |
| MS | 10.65 |
| IBM | 10.4 |
| IBM | 10.635 |
| C | 74.37 |

相关函数：[rowStd](rowStd.html), [std](../s/std.html)

