# rowMin

## 语法

`rowMin(args...)`

row 系列函数通用参数说明和计算规则请参考：[rowFunctions](../themes/rowFunctions.md)

## 详情

逐行进行取最小值的操作，返回一个长度与输入参数行数相同的向量。

## 例子

```
m=matrix([4.5 2.6 1.5, 1.5 4.8 5.9, 4.9 2.0 NULL])
rowMin(m);
// output
[1.5,2,1.5]

t1=table(1..5 as x, 6..10 as y)
t2=table(5..1 as a, 10..6 as b);

rowMin(t1);
// output
[1,2,3,4,5]

rowMin(t1[`x], t2, take(2, 5));
// output
[1,2,2,2,1]

t=table(`AAPL`MS`IBM`IBM`C as sym, 49.6 29.46 29.52 30.02 174.97 as price1, 175.23 50.76 50.32 51.29 26.23 as price2);
select sym,rowMin(price1,price2) as min from t;
```

| sym | min |
| --- | --- |
| AAPL | 49.6 |
| MS | 29.46 |
| IBM | 29.52 |
| IBM | 30.02 |
| C | 26.23 |

相关函数：[min](../m/min.md)

