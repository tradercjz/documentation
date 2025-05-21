# unifiedExpr

## 语法

`unifiedExpr(objs, optrs)`

## 参数

**objs** 是包含两个及以上元素的元组。

**optrs** 是由二元运算符组成的向量，其数量为 size(*objs*)-1。

## 详情

使用 *optrs* 中的二元运算符，将 *objs* 中元素连接，生成一个多元运算表达式的元代码。使用
[eval](../e/eval.md) 函数可以执行 `unifiedExpr`
函数生成的元代码。

## 例子

```
unifiedExpr((1, 2), add)
// output
<1 + 2>

t=table(1..3 as price1, 4..6 as price2, 5..7 as price3)
a=sqlColAlias(unifiedExpr((sqlCol("price1"), sqlCol("price2"), sqlCol("price3")), take(add, 2)))
sql(select=(sqlCol(`price1),sqlCol(`price2),sqlCol(`price3),a), from=t).eval()
```

| price1 | price2 | price3 | price1\_add |
| --- | --- | --- | --- |
| 1 | 4 | 5 | 10 |
| 2 | 5 | 6 | 13 |
| 3 | 6 | 7 | 16 |

相关函数： [binaryExpr](../b/binaryExpr.md)

