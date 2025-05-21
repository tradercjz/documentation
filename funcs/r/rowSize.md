# rowSize

## 语法

`rowSize(args...)`

row 系列函数通用参数说明和计算规则请参考：[rowFunctions](../themes/rowFunctions.md)

## 详情

逐行进行元素统计（包含空值）操作，返回一个长度与输入参数行数相同的向量。

## 例子

```
m=matrix([4.5 2.6 1.5, 1.5 4.8 5.9, 4.9 2.0 NULL]);
rowSize(m);
// output
[3,3,3]

t1=table(1 NULL 3 NULL 5 as x, 6..10 as y);
t2=table(5 NULL 3 NULL 1 as a, 10..6 as b);
rowSize(t1);
// output
[2,2,2,2,2]

rowCount(t1[`x], t2, 1 NULL 2 NULL NULL);
// output
[4,1,4,1,3]
rowSize(t1[`x], t2, 1 NULL 2 NULL NULL);
// output
[4,4,4,4,4]

t=table(`AAPL`MS`IBM`IBM`C as sym, [49.6, NULL, 29.52, NULL, 174.97] as price1, [175.23, NULL, 50.32, 51.29, 26.23] as price2);
select sym,rowSize(price1,price2) as size from t;
```

输出返回：

| sym | size |
| --- | --- |
| AAPL | 2 |
| MS | 2 |
| IBM | 2 |
| IBM | 2 |
| C | 2 |

相关函数：[rowCount](rowCount.md), [size](../s/size.md)

