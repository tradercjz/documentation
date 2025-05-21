# cols

## 语法

`cols(X)`

## 参数

**X** 可以是向量、矩阵或表。

## 详情

返回 *X* 中列的数目。参见相关函数：[rows](../r/rows.md)。

## 例子

```
x=1..6$2:3;
x;
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 1 | 3 | 5 |
| 2 | 4 | 6 |

```
cols x;
// output
3

a=table(1..3 as x,`IBM`C`AAPL as y);
a;
```

| x | y |
| --- | --- |
| 1 | IBM |
| 2 | C |
| 3 | AAPL |

```
cols a;
// output
2

y=1 2 3;
cols(y);
// output
1
// 向量可以被视为一个 n*1 的矩阵
```

