# rowMax

## 语法

`rowMax(args...)`

row 系列函数通用参数说明和计算规则请参考：[rowFunctions](../themes/rowFunctions.html)

## 详情

逐行进行取最大值的操作，返回一个长度与输入参数行数相同的向量。

## 例子

```
m=matrix([4.5 2.6 1.5, 1.5 4.8 5.9, 4.9 2.0 NULL])
rowMax(m);
```

返回：[4.9,4.8,5.9]

```
t1=table(1..5 as x, 6..10 as y)
t2=table(5..1 as a, 10..6 as b);

rowMax(t1);
```

返回：[6,7,8,9,10]

```
rowMax(t1[`y], t2, take(8, 5));
```

返回：[10,9,8,9,10]

```
t=table(`AAPL`MS`IBM`IBM`C as sym, 49.6 29.46 29.52 30.02 174.97 as price1, 175.23 50.76 50.32 51.29 26.23 as price2);
select sym,rowMax(price1,price2) as max from t;
```

返回：

| sym | max |
| --- | --- |
| AAPL | 175.23 |
| MS | 50.76 |
| IBM | 50.32 |
| IBM | 51.29 |
| C | 174.97 |

**相关信息**

* [max](../m/max.html "max")

