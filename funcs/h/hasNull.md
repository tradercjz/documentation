# hasNull

## 语法

`hasNull(X)`

## 参数

**X** 可以是标量、向量、矩阵或表。

## 详情

判断 *X* 中是否包含 NULL 值。

* 如果 *X* 是标量，当 *X* 为 NULL 值时，该函数返回 true。
* 如果 *X* 是向量，当 *X* 中至少有一个元素为 NULL 时，该函数返回
  true。
* 如果 *X* 是矩阵或表，当 *X* 中至少有一列包含 NULL 值时，该函数返回
  true。

## 例子

```
hasNull NULL;
// output
true

x=00f;
hasNull x;
// output
true

hasNull 5;
// output
false

hasNull(1 2 NULL 4 NULL 6);
// output
true

x=((NULL,1),2);
hasNull x;
// output
false

m=(1 NULL 3 4 5 6)$2:3;
hasNull m;
// output
true

t=table(`AAPL`IBM`MSFT as sym, 2200 NULL 4500 as qty);
hasNull(t);
// output
true
```

相关函数：[isNull](../i/isNull.html), [nullFill](../n/nullFill.html)

