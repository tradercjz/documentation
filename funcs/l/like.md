# like

## 语法

like(X, pattern)

## 参数

**X** 可以是字符串类型的标量/向量。

**pattern** 是一个字符串，通常包含通配符（例如 "%"）。

## 详情

确定 *X* 是否与 *Pattern* 指定的模式相匹配。比较操作是区分大小写的。

## 例子

```
like(`ABCDEFG, `DE);
// output
false

like(`ABCDEFG, "%DE%");
// output
true

a=`IBM`ibm`MSFT`Goog`YHOO`ORCL;
like(a, "%OO%");
// output
[false,false,false,false,true,false]
a[like(a, "%OO%")];
// output
["YHOO"]
```

`like` 可以搭配 `select`
使用，用于筛选字符串类型的列的范围：

```
t = table(`abb`aac`aaa as sym, 1.8 2.3 3.7 as price);
select * from t where sym like "%aa%";
```

| sym | price |
| --- | --- |
| aac | 2.3 |
| aaa | 3.7 |

相关函数：[ilike](../i/ilike.html)

