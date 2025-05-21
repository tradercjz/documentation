# nullCompare

## 语法

`nullCompare(func, X, Y)`

## 详情

返回一个布尔值，是表达式 “func(X,Y)” 的结果。涉及 NULL 值的计算结果均为 NULL。该函数不受配置项
nullAsMinValueForComparison 影响。

## 参数

* **func** 是<, >, >=, <=运算符，或函数 between,
  in。
* **X** 和 **Y** 可以是标量、数据对、向量、矩阵或集合。当 *X* 和
  *Y* 都是向量或矩阵时，它们的长度或维度必须相同。

注： *X* 和 *Y* 暂不支持以下数据类型：STRING, SYMBOL, IPADDR, UUID,
BLOB 和I NT128。

## 例子

配置项 *nullAsMinValueForComparison* = true 时，在比较运算中，NULL
元素取相应数据类型的最小值。若使用 nullCompare，则不受该配置影响，依然取 NULL 值。

```
NULL < 3
// output
true
nullCompare(<, NULL, 3)
// output
NULL
m1=matrix(1 2 NULL, NULL 8 4, 4 7 2 )
m2 = 1..9$3:3
m1>m2
```

| col1 | col2 | col3 |
| --- | --- | --- |
| false | false | false |
| false | true | false |
| false | false | false |

```
nullCompare(>,m1,m2)
```

| col1 | col2 | col3 |
| --- | --- | --- |
| false |  | false |
| false | true | false |
|  | false | false |

```
nullCompare(between, 4 5 NULL, 4:9)
// output
[1,1,]
```

