# avg

## 语法

`avg(X)`

## 参数

**X** 可以是标量、数据对、向量、矩阵或表。

## 详情

* 若 *X* 为向量，计算 *X* 的平均值。
* 若 *X* 为矩阵，计算每列的平均值，返回一个向量。
* 若 *X* 为表，计算每列的平均值，返回一个表。

该函数与 [mean](../m/mean.md) 函数完全相同。

与所有其它聚合函数一致，计算时忽略 NULL 值。

## 例子

```
avg(1 2 3 NULL)
// output
2

m=matrix(1 2 3, 4 5 6)
m
```

| 0 | 1 |
| --- | --- |
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |

```
avg(m)
// output
[2,5]
```

