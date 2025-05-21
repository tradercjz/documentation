# contextby

## 语法

`contextby(func, funcArgs, groupingCol, [sortingCol],
[semanticFilter=1])`

或

`funcArg func:X groupingCol`

或

`func:X(funcArgs, groupingCol, [sortingCol],
[semanticFilter=1])`

## 参数

**func** 是一个函数。**注意**：对于第二种用法，func表示的函数只能有一个参数。

**funcArgs** 是函数func的参数。如果有多个参数，则用元组表示。

**groupingCol** 是分组变量，可为一组或多组。

**sortingCol** 是可选参数，表示在应用函数func前，依此列进行组内排序。

**semanticFilter** 可选参数，当 *funcArgs* 指定为表时，用于指定表中参与计算的字段。它是一个正整数，可取以下值：

* 0：所有列。
* 1（默认值）：数值列（FLOATING/INTEGRAL/DECIMAL 分类，COMPRESSED 除外）。
* 2：时间列（TEMPORAL 类型）。
* 3：字符串列（LITERAL 类型，BLOB 除外）。
* 4：数值列和时间列。

*funcArgs*, *groupingCol* 和 *sortingCol*
中包含的向量长度相等。

## 详情

根据 groupingCol 分组，并在组内进行指定计算。返回一个与输入参数长度相同的向量。

如果func是聚合函数，每组内的所有结果相同。若指定了sortingCol，在计算前，依此列进行组内排序。

注： 当 func 为聚合函数时，用于定义该聚合函数的关键词为 defg。

## 例子

```
sym=`IBM`IBM`IBM`MS`MS`MS
price=172.12 170.32 175.25 26.46 31.45 29.43
qty=5800 700 9000 6300 2100 5300
trade_date=2013.05.08 2013.05.06 2013.05.07 2013.05.08 2013.05.06 2013.05.07;
contextby(avg, price, sym);
```

输出返回：[172.563,172.563,172.563,29.113,29.113,29.113]

```
price avg :X sym;
```

输出返回：[172.563,172.563,172.563,29.113,29.113,29.113]

```
price at price>contextby(avg, price,sym);
```

输出返回：[175.25,31.45,29.43]

```
price at price>price avg :X sym;
```

输出返回：[175.25,31.45,29.43]

```
sym at price>contextby(avg, price,sym);
```

输出返回：["IBM","MS","MS"]

```
contextby(wavg, [price, qty], sym);
```

输出返回：[173.856,173.856,173.856,28.374,28.374,28.374]

```
// 计算数量加权的平均值
contextby(ratios, price, sym, trade_date) - 1;
```

输出返回：[-0.01786,,0.028946,-0.100917,,-0.064229]

groupingCol 可包含多个向量：

```
sym=`IBM`IBM`IBM`IBM`IBM`IBM`MS`MS`MS`MS`MS`MS
date=2020.12.01 + 0 0 0 1 1 1 0 0 0 1 1 1
qty=5800 700 9000 1000 3500 3900 6300 2100 5300 7800 1200 4300
contextby(cumsum, qty, [sym,date]);
```

输出返回：[5800,6500,15500,1000,4500,8400,6300,8400,13700,7800,9000,13300]

*contextby* 高阶函数可在 SQL 查询中使用：

```
t1=table(trade_date,sym,qty,price);
t1;
```

输出返回：

| trade\_date | sym | qty | price |
| --- | --- | --- | --- |
| 2013.05.08 | IBM | 5800 | 172.12 |
| 2013.05.06 | IBM | 700 | 170.32 |
| 2013.05.07 | IBM | 9000 | 175.25 |
| 2013.05.08 | MS | 6300 | 26.46 |
| 2013.05.06 | MS | 2100 | 31.45 |
| 2013.05.07 | MS | 5300 | 29.43 |

```
// 选出价格高于组内平均价的交易记录
select trade_date, sym, qty, price from t1 where price > contextby(avg, price,sym);
```

输出返回：

| trade\_date | sym | qty | price |
| --- | --- | --- | --- |
| 2013.05.07 | IBM | 9000 | 175.25 |
| 2013.05.06 | MS | 2100 | 31.45 |
| 2013.05.07 | MS | 5300 | 29.43 |

```
// t1 的所有交易日期都增加一天
contextby(temporalAdd{,1d}, t1, t1.sym,,2)
```

| trade\_date | sym | qty | price |
| --- | --- | --- | --- |
| 2013.05.09 | IBM | 5,800 | 172.12 |
| 2013.05.07 | IBM | 700 | 170.32 |
| 2013.05.08 | IBM | 9,000 | 175.25 |
| 2013.05.09 | MS | 6,300 | 26.46 |
| 2013.05.07 | MS | 2,100 | 31.45 |
| 2013.05.08 | MS | 5,300 | 29.43 |

