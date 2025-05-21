# col

## 语法

`col(obj, index)` 或 `column(obj,
index)`

## 参数

**obj** 可以是向量、矩阵或表。

**index** 是一个整数标量或数据对。

## 详情

返回向量、矩阵或表的一列。参见相关函数：[row](../r/row.md)。

## 例子

```
x=1..6$3:2;
x;
```

| #0 | #1 |
| --- | --- |
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |

```
col(x,0);
// output
[1,2,3]

x.col(1);
// output
[4,5,6]

a=table(1..3 as x,`IBM`C`AAPL as y);
a;
```

| x | y |
| --- | --- |
| 1 | IBM |
| 2 | C |
| 3 | AAPL |

```
a col 1;
// output
["IBM","C","AAPL"]
```

