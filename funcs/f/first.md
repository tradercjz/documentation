# first

## 语法

`first(X)`

或

`first X`

## 参数

**X** 可以是标量、数据对、向量、矩阵或表。

## 详情

返回向量的第一个元素，或矩阵、表的第一行。

注： 若向量的第一个元素为 NULL，则返回 NULL。若要返回第一个非 NULL 的元素，请使用 [firstNot](firstNot.md) 函数。

## 例子

```
first(`hello `world);
```

输出返回：hello

```
first(1..10);
```

输出返回：1

```
m = matrix(1 2 3, 4 5 6);
m;
```

输出返回：

| #0 | #1 |
| --- | --- |
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |

```
first(m);
```

输出返回：[1,4]

相关函数：[last](../l/last.md)

