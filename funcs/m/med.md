# med

## 语法

`med(X)`

## 参数

**X** 可以是标量、向量或矩阵。

## 详情

如果 *X* 是向量，返回 *X* 中所有元素的中值。

若 *X* 为矩阵，计算每列的中值，返回一个向量。

与所有其它聚合函数一致，计算时忽略 NULL 值。

无论 *X* 为何种数据类型，结果的数据类型为 DOUBLE。

## 例子

```
x=3 6 1 5 9;
med x;
// output
5

m=matrix(1 2 10, 4 5 NULL);
m;
```

| #0 | #1 |
| --- | --- |
| 1 | 4 |
| 2 | 5 |
| 10 |  |

```
med m;
// output
[2,4.5]
```

相关的中心趋势函数：[mean](mean.md) 和 [mode](mode.md)

