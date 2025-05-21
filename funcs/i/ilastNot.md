# ilastNot

## 语法

`ilastNot(X)`

## 参数

**X** 可以是一个向量，也可以是由多个等长向量组成的元组，亦可是一个矩阵或表。

## 详情

如果 *X* 是一个向量，返回最后一个非空元素的下标。如果 *X* 中的所有元素都为空，返回-1。

如果 *X* 是一个元组，返回最后一个所有向量中均不为空的位置的下标。

如果 *X* 是一个矩阵，返回每列中最后一个非空元素的下标。返回一个向量。

如果 *X* 是一个表，返回每列中最后一个非空元素的下标。返回一个表。

## 例子

```
ilastNot(NULL NULL 2 4 8 1 NULL);
// output
5

ilastNot(take(int(),5));
// output
-1

x=NULL NULL 4 7 8 NULL
y=1 NULL NULL 4 NULL NULL
ilastNot([x,y]);
// output
3

x=NULL NULL 4 7 8 NULL
y=1 2 NULL NULL NULL 6
ilastNot([x,y]);
// output
-1

m=matrix(2 NULL 1 0 NULL, NULL 2 NULL 6 0);
m;
```

| #0 | #1 |
| --- | --- |
| 2 |  |
|  | 2 |
| 1 |  |
| 0 | 6 |
|  | 0 |

```
ilastNot(m);
// output
[3,4]
```

相关函数：[ifirstNot](ifirstNot.md), [lastNot](../l/lastNot.md), [firstNot](../f/firstNot.md)

