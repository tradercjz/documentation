# iif

## 语法

`iif(cond, trueResult, falseResult)`

## 参数

**cond** 是布尔标量、向量或矩阵。可为产生布尔标量、向量或矩阵的表达式。

**trueResult** 和 **falseResult** 可以是标量、与 *cond* 等长的向量/元组、或元素个数与
*cond* 相同的矩阵。

## 详情

`iif` 是元素级的条件运算符。它逐元素判断给定的条件，并根据每个元素的条件结果从
*trueResult* 或 *falseResult* 中返回相应位置的元素。具体来说，如果 cond[i] 为 true，它返回
*trueResult* 的第 i 个元素；否则返回 *falseResult* 的第 i 个元素。 当 cond[i]
为空值时，则返回空值。

注： 此函数会首先执行其中的三个参数，然后根据 *cond* 的结果决定返回
*trueResult* 或 *falseResult*。

## 例子

```
iif(true true true false false false, 1..6, 6..1);
// output: [1,2,3,3,2,1]

iif(1..6==3, 1, 2);
// output: [2,2,1,2,2,2]

x=9 6 8;
iif(x<=8, 10*x, 20*x-80);
// output: [100,60,80]

a = 1..10
iif(isNull(a.prev()), a.cut(1), a.prev().cut(1))
// output: (1,1,2,3,4,5,6,7,8,9)

t=table(1..5 as id, 11..15 as x);
t1=table(take(12,5) as a, take(14,5) as b);
t;
```

| id | x |
| --- | --- |
| 1 | 11 |
| 2 | 12 |
| 3 | 13 |
| 4 | 14 |
| 5 | 15 |

```
t1;
```

| a | b |
| --- | --- |
| 12 | 14 |
| 12 | 14 |
| 12 | 14 |
| 12 | 14 |
| 12 | 14 |

```
update t set x=iif(x<t1.a, t1.a, iif(x>t1.b,t1.b, x));
t;
```

| id | x |
| --- | --- |
| 1 | 12 |
| 2 | 12 |
| 3 | 13 |
| 4 | 14 |
| 5 | 14 |

当配置了 *nullAsMinValueForComparison*=true时，在比较运算中，NULL
元素取相应数据类型的最小值。使用 [nullCompare](../ho_funcs/nullCompare.md) 可以保持
`iif` 条件语句里的 NULL 值。

```
a = NULL 1 -3 5
iif(a > 0, a, 0)
// output: [0, 1, 0, 5]
iif(nullCompare(>,a,0), a, 0)
// output: [ , 1, 0, 5]
```

```
m1=1..6$3:2
m2=6..1$3:2
iif(m1>m2, m1, m2);
```

| col1 | col2 |
| --- | --- |
| 6 | 4 |
| 5 | 5 |
| 4 | 6 |

