# crossStat

## 语法

`crossStat(X, Y)`

## 参数

**X** 和 **Y** 是长度相同的数值型向量。

## 详情

返回的结果是一个元组，结果中的每个元素依次为 count(X), sum(X), sum(Y), sum2(X), sum2(Y),
sum(X\*Y) 的计算结果。

## 例子

```
x=1 NULL 2 3
y=4 3 NULL 2
crossStat(x,y);
// output
(2,4,6,10,20,10)
```

