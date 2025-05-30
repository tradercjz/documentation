# prod

## 语法

`prod(X)`

## 参数

**X** 可以是标量、向量、矩阵或表。

## 详情

* 若 *X* 为向量，返回 *X* 中所有元素的乘积。
* 若 *X* 为矩阵，计算每列中所有元素的乘积，返回一个向量。
* 若 *X* 为表，计算每列中所有元素的乘积，返回一个表。

与所有其它聚合函数一致，计算时忽略 NULL 值。

## 例子

```
prod(1 2 NULL 3);
// output
6
```

```
m=matrix(1 2 3, 4 5 6);
m;
```

| #0 | #1 |
| --- | --- |
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |

```
prod(m);
// output
[6,120]
```

