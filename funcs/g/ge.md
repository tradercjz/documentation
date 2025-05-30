# ge

## 语法

`ge(X, Y)` 或 `X>=Y`

## 参数

**X** 和 **Y** 可以是标量、数据对、向量、矩阵或集合。如果 *X* 或 *Y*
的其中一个是数据对、向量或矩阵，另一个必须是标量，或具有相同长度或维度的数据对、向量或矩阵。

## 详情

如果 *X* 和 *Y* 都不是集合，返回逐个元素比较 *X*>=*Y*
的结果。

如果 *X* 和 *Y* 都是集合，则检查 *Y* 是否为 *X* 的子集。

## 例子

*X* 是向量：

```
1 2 3 >= 2;
// output
[0,1,1]

1 2 3 >= 0 2 4;
// output
[1,1,0]

2:3>=1:6;
// output
1 : 0

m1=1..6$2:3;
m1;
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 1 | 3 | 5 |
| 2 | 4 | 6 |

```
m1 ge 4;
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 0 | 0 | 1 |
| 0 | 1 | 1 |

```
m2=6..1$2:3;
m2;
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 6 | 4 | 2 |
| 5 | 3 | 1 |

```
m1>=m2;
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 0 | 0 | 1 |
| 0 | 1 | 1 |

集合操作：如果 *X*>=*Y*，则 *Y* 是 *X* 的子集。

```
x=set(4 6);
x;
// output
set(6,4)
y=set(8 9 4 6);
y;
// output
set(6,4,9,8)

y>=x;
// output
1

x>=y;
// output
0

x>=x;
// output
1
// x 是 x 的子集
```

