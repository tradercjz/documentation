# reciprocal

## 语法

`reciprocal(X)`

## 参数

**X** 可以是数值型标量、向量或矩阵。

## 详情

返回 *X* 的倒数。返回结果为 DOUBLE 类型。

## 例子

```
reciprocal(10);
// output
0.1

reciprocal(1 2 4 8);
// output
[1,0.5,0.25,0.125]

reciprocal(1 2 4 8$2:2);
```

| #0 | #1 |
| --- | --- |
| 1 | 0.25 |
| 0.5 | 0.125 |

