# drop

## 语法

`drop(X, n)`

## 参数

**X** 可以是向量、矩阵或表。

**n** 是一个整数。

## 详情

从向量中删除前 *n* 个或后 *n* 个（如果 *n* 为负数）个元素，或从矩阵中删除前/后
*n* 列，或从表中删除前/后 *n* 行。

## 例子

```
x=1..10;
x.drop(2);
// output
[3,4,5,6,7,8,9,10]
x.drop(-2);
// output
[1,2,3,4,5,6,7,8]

x=1..10$2:5;
x;
```

| #0 | #1 | #2 | #3 | #4 |
| --- | --- | --- | --- | --- |
| 1 | 3 | 5 | 7 | 9 |
| 2 | 4 | 6 | 8 | 10 |

```
drop(x,2);
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 5 | 7 | 9 |
| 6 | 8 | 10 |

```
x drop -2;
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 1 | 3 | 5 |
| 2 | 4 | 6 |

```
t=table(1 2 3 4 as x, 11..14 as y);
t;
```

| x | y |
| --- | --- |
| 1 | 11 |
| 2 | 12 |
| 3 | 13 |
| 4 | 14 |

```
t.drop(2);
```

| x | y |
| --- | --- |
| 3 | 13 |
| 4 | 14 |

