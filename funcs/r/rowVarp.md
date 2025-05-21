# rowVarp

## 语法

`rowVarp(args...)`

row 系列函数通用参数说明和计算规则请参考：[rowFunctions](../themes/rowFunctions.html)

## 详情

逐行进行元素求总体方差操作，返回一个长度与输入参数行数相同的向量。

## 例子

```
m=matrix([4.5 2.6 1.5, 1.5 4.8 5.9, 4.9 2.0 NULL]);
rowVarp(m);
// output
[2.302222222222225,1.448888888888887,4.84]

t1=table(1..5 as x, 10..6 as y, take(3, 5) as z);
t2=table(5..1 as a, 6..10 as b, take(8, 5) as c);
rowVarp(t1);
// output
[14.888888888888891,9.555555555555557,5.555555555555558,2.888888888888891,1.555555555555557]

rowVarp(t1[`x], t2, 1 1 2 2 2);
// output
[7.76,7.440000000000001,6.96,8.8,11.760000000000001]

t=table(`AAPL`MS`IBM`IBM`C as sym, 49.6 29.46 29.52 30.02 174.97 as price1, 175.23 50.76 50.32 51.29 26.23 as price2);
select sym,rowVarp(price1,price2) as varp from t;
```

| sym | varp |
| --- | --- |
| AAPL | 3945.7242 |
| MS | 113.4225 |
| IBM | 108.16 |
| IBM | 113.1032 |
| C | 5530.8969 |

相关函数：[rowVar](rowVar.html), [varp](../v/varp.html)

