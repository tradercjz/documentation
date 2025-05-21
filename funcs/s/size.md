# size

## 语法

`size(X)`

## 参数

**X** 可以是标量、向量、矩阵或表。

## 详情

对于向量或矩阵，`size` 返回元素的个数，而 [count](../c/count.html) 返回的是非 NULL 元素个数。

对于内存表，`size` 返回行数。

## 例子

```
size(3 NULL 5 6);
// output
4
count(3 NULL 5 6);
// output
3

m=1 2 3 NULL 4 5$2:3;
m;
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 1 | 3 | 4 |
| 2 |  | 5 |

```
size(m);
// output
6

count(m);
// output
5

t = table(1 NULL 3 as id, 3 NULL 9 as qty);
t;
```

| id | qty |
| --- | --- |
| 1 | 3 |
|  |  |
| 3 | 9 |

```
size(t);
// output
3

count(t);
// output
3
```

