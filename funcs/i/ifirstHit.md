# ifirstHit

## 语法

`ifirstHit(func, X, target)`

## 参数

**func** 关系运算符 >, >=, <, <=, !=, <>, ==。

**X** 向量，矩阵或表。

**target** 和 *X* 类型相同的标量，表示与 *X* 比较的对象。

## 详情

返回 *X* 中第一个满足 *X*
*func*
*target* （例如 *X*>5) 条件的元素的下标。

若 *X* 中无元素满足条件，则返回-1。

通过 `ifirstHit` 查找时，NULL 值会被忽略：

* 如需查找第一个非 NULL 的下标， 可以通过函数 [ifirstNot](ifirstNot.md)；
* 如需查找第一个空值的下标，可以通过函数 [find](../f/find.md)。

## 例子

```
X = NULL 3.2 4.5 1.2 NULL 7.8 0.6 9.1
ifirstHit(<, X, 2.5)
// output
3

// 若无元素满足查找条件，返回 -1
ifirstHit(>, X, 10.0)
// output
-1

```

相关函数：[firstHit](../f/firstHit.md)

