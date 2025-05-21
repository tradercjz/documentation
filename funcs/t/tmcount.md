# tmcount

## 语法

`tmcount(T, X, window)`

参数说明和窗口计算规则请参考：[tmFunctions](../themes/tmFunctions.html)

## 详情

在给定长度（以时间 *T* 衡量）的滑动窗口内统计 *X* 中的非 NULL 元素个数。

## 例子

```
T = 1 1 1 2 5 6
X = 1 4 NULL -1 NULL 4
m = table(T as t,X as x)
select *, tmcount(t, x, 3) from m
```

| t | x | tmcount\_t |
| --- | --- | --- |
| 1 | 1 | 1 |
| 1 | 4 | 2 |
| 1 |  | 2 |
| 2 | -1 | 3 |
| 5 |  | 0 |
| 6 | 4 | 1 |

```
T = 2021.01.02 2021.01.02  2021.01.04  2021.01.05 2021.01.07 2021.01.09
X = NULL 4 NULL -1 2 4
m = table(T as t,X as x)
select *, tmcount(t, x, 3d) from m
```

| t | x | tmcount\_t |
| --- | --- | --- |
| 2021.01.02 |  | 0 |
| 2021.01.02 | 4 | 1 |
| 2021.01.04 |  | 1 |
| 2021.01.05 | -1 | 1 |
| 2021.01.07 | 2 | 2 |
| 2021.01.09 | 4 | 2 |

```
select *, tmcount(t, x, 1w) from m
```

| t | x | tmcount\_t |
| --- | --- | --- |
| 2021.01.02 |  | 0 |
| 2021.01.02 | 4 | 1 |
| 2021.01.04 |  | 1 |
| 2021.01.05 | -1 | 2 |
| 2021.01.07 | 2 | 3 |
| 2021.01.09 | 4 | 3 |

相关函数：[mcount](../m/mcount.html), [count](../c/count.html)

