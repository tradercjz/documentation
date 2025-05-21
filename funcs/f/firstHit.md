# firstHit

## 语法

`firstHit(func, X, target)`

## 参数

**func** 关系运算符 >, >=, <, <=, !=, <>, ==。

**X** 向量，矩阵或表。

**target** 和 *X* 类型相同的标量，表示比较的对象。

## 详情

返回 *X* 中第一个满足 *X*
*func*
*target* （例如 *X*>5) 条件的元素。

若 *X* 中无元素满足条件，则返回空值。

通过 `firstHit` 查找时，NULL 值会被忽略。如需查找第一个非 NULL 值， 可以调用函数 [firstNot](firstNot.html)。

## 例子

```
X = NULL 3.2 4.5 1.2 NULL 7.8 0.6 9.1
firstHit(<, X, 2.5)
```

输出返回：1.2

若无元素满足查找条件，返回空值，如下面这个例子：

```
firstHit(>, X, 10.0)
```

输出返回：NULL

相关函数：[ifirstHit](../i/ifirstHit.html)

