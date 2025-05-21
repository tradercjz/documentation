# firstNot

## 语法

`firstNot(X, [k])`

## 参数

**X** 可以是标量、数据对、向量、矩阵或表。

**k** 是一个标量，它是可选参数。

## 详情

若 *X* 是向量：

* 如果没有指定 *k*，返回 *X* 中第一个不为 NULL 的元素。
* 如果指定 *k*，返回 *X* 中第一个不为 *k* 或 NULL 的元素。

若 *X* 是矩阵或表，在每列内进行上述计算，返回一个向量。

`firstNot` 函数也支持查询分布式表和分区表。

## 例子

*X* 是向量：

```
firstNot(0 0 0 6 1, 0);
// output
6

firstNot(NULL 0 3 2 1, 0);
// output
3

firstNot(NULL 0 1 6);
// output
0

t=table(1 1 1 1 1 2 2 2 2 2 as id, 0 0 0 2 1 NULL NULL 0 0 3 as x);
t;
```

| id | x |
| --- | --- |
| 1 | 0 |
| 1 | 0 |
| 1 | 0 |
| 1 | 2 |
| 1 | 1 |
| 2 |  |
| 2 |  |
| 2 | 0 |
| 2 | 0 |
| 2 | 3 |

```
select firstNot(x, 0) from t group by id;
```

| id | firstNot\_x |
| --- | --- |
| 1 | 2 |
| 2 | 3 |

```
m=matrix(0 NULL 1 2 3, NULL 2 NULL 0 3);
m;
```

| #0 | #1 |
| --- | --- |
| 0 | 2 |
| 1 |  |
| 2 | 0 |
| 3 | 3 |

```
firstNot(m, 0);
// output
[1,2]
```

