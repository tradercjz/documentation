# rowIminLast

## 语法

`rowIminLast(args…)`

## 参数

row 系列函数通用参数说明和计算规则请参考：[行计算系列（row
系列）](../themes/rowFunctions.md)

## 详情

返回每行元素中最小元素的索引。如果有多个相同的最小值，返回右起第一个最小值的索引。结果为一个长度与输入参数行数相同的向量。

## 例子

```
m=matrix([4.5 2.6 1.5 3.2, 1.5 4.8 5.9 1.7, 4.9 2.0 NULL 5.5])
rowIminLast(m)
// output
[1,2,0,1]

trades = table(10:0,`time`sym`p1`p2`p3`p4`p5`vol1`vol2`vol3`vol4`vol5,[TIMESTAMP,SYMBOL,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,INT,INT,INT,INT,INT])
insert into trades values(2022.01.01T09:00:00, `A, 33.2, 33.8, 33.6, 33.3, 33.1, 200, 180, 180, 220, 200)
insert into trades values(2022.01.01T09:00:00, `A, 33.1, 32.8, 33.2, 34.3, 32.3, 150, 280, 190, 100, 220)
insert into trades values(2022.01.01T09:00:00, `A, 31.2, 32.6, 33.6, 35.3, 34.5, 220, 160, 130, 100, 110)
insert into trades values(2022.01.01T09:00:00, `A, 30.2, 32.5, 33.6, 35.3, 34.1, 200, 180, 150, 140, 120)
insert into trades values(2022.01.01T09:00:00, `A, 33.2, 33.8, 33.6, 33.3, 33.1, 180, 160, 160, 180, 200)

select rowAt(matrix(p1, p2, p3, p4, p5), rowIminLast(vol1, vol2, vol3, vol4, vol5)) as price from trades
// output
price
33.6
34.3
35.3
34.1
33.6

```

相关函数：[rowImin](rowImin.md)

