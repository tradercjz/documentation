# bfill

## 语法

`bfill(obj, [limit])`

## 参数

**obj** 可以是向量、数组向量、矩阵或表。

**limit** 是正整数，表示最大可填充的连续空值个数。*obj* 为数组向量时不支持该参数。

## 详情

* 如果 *obj* 是向量，则使用空值后的第一个非空元素来填充空值。
* 如果 *obj* 是数组向量：
  + 对于每一行，如果该行为空，则用该行后的第一个非空行填充。
  + 对于某一列中的空值，使用该列中空值后的第一个非空元素填充。
* 如果 *obj* 是矩阵或表，则对每一列按照上述规则进行填充。

该函数会返回一个新的对象，不会改变输入的对象。函数 [bfill!](bfill_.md)
会改变输入的对象。

## 例子

```
x=1 2 3 NULL NULL NULL 4 5 6
x.bfill();
// output
[1,2,3,4,4,4,4,5,6]

x=1 2 3 NULL NULL NULL 4 5 6
x.bfill(1);
// output
[1,2,3,,,4,4,5,6]

x.bfill!(2);
x;
// output
[1,2,3,,4,4,4,5,6]

date=[2012.06.12,2012.06.12,2012.06.13,2012.06.14,2012.06.15]
sym=["IBM","MSFT","IBM","MSFT","MSFT"]
price=[,,26.56,,50.76]
qty=[,,4500,5600,6800]
timestamp=[09:34:07,09:35:26,09:36:42,09:36:51,09:36:59]
t=table(date,timestamp,sym,price,qty)
t;
```

| date | timestamp | sym | price | qty |
| --- | --- | --- | --- | --- |
| 2012.06.12 | 09:34:07 | IBM |  |  |
| 2012.06.12 | 09:35:26 | MSFT |  |  |
| 2012.06.13 | 09:36:42 | IBM | 26.56 | 4500 |
| 2012.06.14 | 09:36:51 | MSFT |  | 5600 |
| 2012.06.15 | 09:36:59 | MSFT | 50.76 | 6800 |

```
t.bfill()
```

| date | timestamp | sym | price | qty |
| --- | --- | --- | --- | --- |
| 2012.06.12 | 09:34:07 | IBM | 26.56 | 4500 |
| 2012.06.12 | 09:35:26 | MSFT | 26.56 | 4500 |
| 2012.06.13 | 09:36:42 | IBM | 26.56 | 4500 |
| 2012.06.14 | 09:36:51 | MSFT | 50.76 | 5600 |
| 2012.06.15 | 09:36:59 | MSFT | 50.76 | 6800 |

```
select date, timestamp, sym, price.bfill() as price, qty.bfill() as qty from t context by sym;
```

| date | timestamp | sym | price | qty |
| --- | --- | --- | --- | --- |
| 2012.06.12 | 09:34:07 | IBM | 26.56 | 4500 |
| 2012.06.13 | 09:36:42 | IBM | 26.56 | 4500 |
| 2012.06.12 | 09:35:26 | MSFT | 50.76 | 5600 |
| 2012.06.14 | 09:36:51 | MSFT | 50.76 | 5600 |
| 2012.06.15 | 09:36:59 | MSFT | 50.76 | 6800 |

下例中，数组向量 x 的第三行为空，因此使用第四行 [8, 9, 10] 对其进行填充；第三列的第一个元素为空，故用该列中其后的第一个非空元素（10） 进行填充。

```
x = array(INT[], 0).append!([1 2 NULL, 4 5, NULL, 8 9 10])
x
// output:[[1,2,NULL],[4,5],[NULL],[8,9,10]]
bfill(x)
// output:[[1,2,10],[4,5],[8,9,10],[8,9,10]]
```

