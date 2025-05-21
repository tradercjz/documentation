# rowImax

## 语法

`rowImax(args...)`

row 系列函数通用参数说明和计算规则请参考：[rowFunctions](../themes/rowFunctions.html)

## 详情

返回每行元素中最大元素的索引。如果有多个相同的最大值，返回左起第一个最大值的索引。结果为一个长度与输入参数行数相同的向量。

## 例子

```
m=matrix([4.5 2.6 1.5 3.2, 1.5 4.8 5.9 1.7, 4.9 2.0 NULL 5.5])
print rowImax(m)
```

返回：[2,1,1,2]

```
trades = table(10:0,`time`sym`p1`p2`p3`p4`p5`vol1`vol2`vol3`vol4`vol5,[TIMESTAMP,SYMBOL,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,INT,INT,INT,INT,INT])
insert into trades values(2022.01.01T09:00:00, `A, 33.2, 33.8, 33.6, 33.3, 33.1, 200, 180, 180, 220, 200)
insert into trades values(2022.01.01T09:00:00, `A, 33.1, 32.8, 33.2, 34.3, 32.3, 150, 280, 190, 100, 220)
insert into trades values(2022.01.01T09:00:00, `A, 31.2, 32.6, 33.6, 35.3, 34.5, 220, 160, 130, 100, 110)
insert into trades values(2022.01.01T09:00:00, `A, 30.2, 32.5, 33.6, 35.3, 34.1, 200, 180, 150, 140, 120)
insert into trades values(2022.01.01T09:00:00, `A, 33.2, 33.8, 33.6, 33.3, 33.1, 180, 160, 160, 180, 200)
select rowAt(matrix(p1, p2, p3, p4, p5), rowImax(vol1, vol2, vol3, vol4, vol5)) as price from trades
```

返回：

| price |
| --- |
| 33.3 |
| 32.8 |
| 31.2 |
| 30.2 |
| 33.1 |

当 args 是数组向量时，返回每行元素中的最大元素的索引，结果为一个向量：

```
a = 1 8 3 8 1
b = 5 8 1 3 6
c =  9 5 4 7 6
x = fixedLengthArrayVector(a, b, c)
rowImax(x)
```

返回：[2,0,2,0,1]

**相关信息**

* [imax](../i/imax.html "imax")
* [rowImaxLast](rowimaxlast.html "rowImaxLast")
* [rowFunctions](../themes/rowFunctions.html "rowFunctions")

