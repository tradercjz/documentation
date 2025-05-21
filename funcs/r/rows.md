# rows

## 语法

`rows(X)`

## 参数

**X** 可以是向量、矩阵或表。

## 详情

返回 *X* 中的行数。参见相关函数： [cols](../c/cols.md)。

## 例子

```
y=1 2 3;
rows(y);
// output
3
// 一个向量可以被视为一个 n* 1 的矩阵

x=1..6$2:3;
X
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 1 | 3 | 5 |
| 2 | 4 | 6 |

```
rows X
// output
2

a=table(1..3 as x,`IBM`C`AAPL as y);
a
```

| x | y |
| --- | --- |
| 1 | IBM |
| 2 | C |
| 3 | AAPL |

```
rows a;
// output
3
```

