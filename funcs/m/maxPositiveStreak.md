# maxPositiveStreak

## 语法

`maxPositiveStreak(X)`

## 参数

**X** 可以是标量、向量或矩阵。

## 详情

如果 *X* 是向量，返回 *X* 中连续的正数之和的最大值。

如果 *X* 是矩阵，返回 *X* 中每列连续的正数之和的最大值。

maxPositiveStreak(X) = max(cumPositiveStreak(X))

## 例子

```
x=1 0 -1 1 2 2 2 1 0 -1 0 2;
cumPositiveStreak x;
// output
[1,0,0,1,3,5,7,8,0,0,0,2]
maxPositiveStreak x;
// output
8

y=x$6:2;
y;
```

| #0 | #1 |
| --- | --- |
| 1 | 2 |
| 0 | 1 |
| -1 | 0 |
| 1 | -1 |
| 2 | 0 |
| 2 | 2 |

```
cumPositiveStreak(y);
```

| #0 | #1 |
| --- | --- |
| 1 | 2 |
| 0 | 3 |
| 0 | 0 |
| 1 | 0 |
| 3 | 0 |
| 5 | 2 |

```
maxPositiveStreak(y);
// output
[5,3]
```

相关函数：[cumPositiveStreak](../c/cumPositiveStreak.html)

