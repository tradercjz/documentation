# rowGroupby

## 语法

`rowGroupby(func, funcArgs, groupingCol, [mode='tuple'],
[ascending=true])`

## 参数

**func** 一个聚合函数。

**funcArgs** 是函数 *func* 的参数。如果有多个参数，则用元组表示，且每个元素的维度必须和 *groupingCol*
保持一致。

**groupingCol** 非空矩阵或数组向量，用于分组。

**mode** 可选参数，指定 `rowGroupby` 返回值的数据形式，默认为 "tuple"。可取值为：

* "tuple"：返回一个长度为2的 tuple，其第1个元素是一个数组向量，存储分组变量，第2个元素是一个数组向量，存储各分组中
  *funcArgs* 应用 *func* 后的结果。
* "dict"：返回一个字典。包含两个元素：'key' 和 'value'，分别存储分组变量和各分组中 *funcArgs* 应用*func* 后的结果。
* "table"：返回一个包含两列的表。字段为 "key" 和 "value"，分别存储分组变量及各分组中 *funcArgs* 应用
  *func* 后的结果。

**ascending** 布尔值，表示输出结果按 *groupingCol* 升序还是降序排序。默认值为 true（升序）。

## 详情

对 *groupingCol* 的每一行分组后，在每个分组中计算 *func(funcArgs)*，每组的计算结果是一个标量。该函数将根据
*mode* 指定的形式输出结果。

## 例子

下例对表 t 中的 price 列按升序排序后分组，对每个分组内对应的 qty 进行求和。

```
sym=`A`B
price = array(DOUBLE[], 0).append!([12.5 12.6 12.5 12.5 12.6, 15.5 15.5 15.5 15.3 15.3])
qty = array(INT[], 0).append!([201 212 220 215 214, 210 213 223 219 211])
t=table(sym,price,qty)
//指定 mode='dict' 时，以字典形式输出结果，其中 key 存储 price 排序后分组的结果，value 存储对 qty 分组求和的结果
rowGroupby(func=sum,funcArgs=t.qty,groupingCol=t.price,mode='dict')

/* output:
value->[[636,426],[430,646]]
key->[[12.5,12.6],[15.3,15.5]]
*/

//指定 ascending=false，按照 price 降序输出结果。
rowGroupby(func=sum,funcArgs=t.qty,groupingCol=t.price,mode='dict', ascending=false)
/* output:
value->[[426,636],[646,430]]
key->[[12.6000,12.5000],[15.5000,15.3000]]
*/

//指定 mode='table' 时，以表的形式输出结果，其中 key 存储 price 排序后分组的结果，value 存储对 qty 分组求和的结果
rowGroupby(func=sum,funcArgs=t.qty,groupingCol=t.price,mode='table')
```

| key | value |
| --- | --- |
| [12.5,12.6] | [636,426] |
| [15.3,15.5] | [430,646] |

```
//指定 mode='tuple'，输出结果为 tuple，将 tuple 的两个元素重命名后作为表的一列输出。
select rowGroupby(sum, qty, price, 'tuple') as `a`b from t
```

| a | b |
| --- | --- |
| [12.5,12.6] | [636,426] |
| [15.3,15.5] | [430,646] |

接下来通过一个例子来展示如何在矩阵上使用 `rowGroupby` 函数：

```
m=matrix([32.5 12.6 22.5 42.5 32.6, 17.5 25.5 35.5 17.3 19.3, 17 20.1 30 13 19])
g=matrix([1 2 2 5 4, 2 2 3 2 1, 1 3 2 3 5])
//对 g 的每行排序后分组，对 m 的每行在每个组内进行求和
rowGroupby(func=sum, funcArgs=m, groupingCol=g, mode='table')
```

| key | value |
| --- | --- |
| [1,2] | [49.5,17.5] |
| [2,3] | [38.1,20.1] |
| [2,3] | [52.5,35.5] |
| [2,3,5] | [17.3,13,42.5] |
| [1,4,5] | [19.3,32.6,19] |

