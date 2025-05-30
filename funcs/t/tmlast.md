# tmlast

## 语法

`tmlast(T, X, window)`

参数说明和窗口计算规则请参考：[tmFunctions](../themes/tmFunctions.md)

## 详情

在给定长度（以时间 *T* 衡量）的滑动窗口内计算 *X* 的最后一个元素。

## 例子

```
T = 1 1 1 2 5 6
X = 1 4 NULL -1 NULL 4
m = table(T as t,X as x)
select *, tmlast(t, x, 3) from m
```

| t | x | tmlast\_t |
| --- | --- | --- |
| 1 | 1 | 1 |
| 1 | 4 | 4 |
| 1 |  |  |
| 2 | -1 | -1 |
| 5 |  |  |
| 6 | 4 | 4 |

```
T = 2021.01.02 2021.01.02  2021.01.04  2021.01.05 2021.01.07 2021.01.08
X = NULL 4 NULL -1 2 4
m = table(T as t,X as x)
select *, tmlast(t, x, 3d) from m
```

| t | x | tmlast\_t |
| --- | --- | --- |
| 2021.01.02 |  |  |
| 2021.01.02 | 4 | 4 |
| 2021.01.04 |  |  |
| 2021.01.05 | -1 | -1 |
| 2021.01.07 | 2 | 2 |
| 2021.01.08 | 4 | 4 |

```
select *, tmlast(t, x, 1w) from m
```

| t | x | tmlast\_t |
| --- | --- | --- |
| 2021.01.02 |  |  |
| 2021.01.02 | 4 | 4 |
| 2021.01.04 |  |  |
| 2021.01.05 | -1 | -1 |
| 2021.01.07 | 2 | 2 |
| 2021.01.08 | 4 | 4 |

相关函数：[mlast](../m/mlast.md), [last](../l/last.md)

