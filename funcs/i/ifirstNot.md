# ifirstNot

## 语法

`ifirstNot(X)`

## 参数

**X** 可以是一个向量，也可以是由多个等长向量组成的元组，亦可是一个矩阵或表。

## 详情

如果 *X* 是一个向量，返回第一个非空元素的下标。如果 *X* 中的所有元素都为空，返回-1。

如果 *X* 是一个元组，返回第一个所有向量中均不为空的位置的下标。

如果 *X* 是一个矩阵，返回每列中第一个非空元素的下标。返回一个向量。

如果 *X* 是一个表，返回每列中第一个非空元素的下标。返回一个表。

## 例子

```
ifirstNot(NULL NULL 2 4 8 NULL 1);
// output
2

ifirstNot(take(int(),5));
// output
-1

x=NULL NULL 4 7 8 NULL
y=1 NULL NULL 4 NULL NULL
ifirstNot([x,y]);
// output
3

x=NULL NULL 4 7 8 NULL
y=1 2 NULL NULL NULL 6
ifirstNot([x,y]);
// output
-1

m=matrix(0 NULL 1 2 3, NULL 2 NULL 0 3);
m;
```

| #0 | #1 |
| --- | --- |
| 0 |  |
|  | 2 |
| 1 |  |
| 2 | 0 |
| 3 | 3 |

```
ifirstNot(m);
// output
[0,1]
```

相关函数：[ilastNot](ilastNot.md), [firstNot](../f/firstNot.md), [lastNot](../l/lastNot.md)

