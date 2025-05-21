# row

## 语法

`row(obj,index)`

## 参数

**obj** 可以是向量、矩阵或表

**index** 是一个整数标量或数据对。

## 详情

返回向量、矩阵或表的一行。参见相关函数：[col](../c/col.html)。

## 例子

```
x=matrix(1 2 3, 4 5 6);
x;
```

| #0 | #1 |
| --- | --- |
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |

```
row(x,1);
// output
[2,5]

row(x,0);
// output
[1,4]

x.row(2);
// output
[3,6]

a=table(1..3 as x,`IBM`C`AAPL as y);
a
```

| x | y |
| --- | --- |
| 1 | IBM |
| 2 | C |
| 3 | AAPL |

```
row(a,1);
// output
y->C
x->2
```

