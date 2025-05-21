# groupby

## 语法

`groupby(func, funcArgs, groupingCol)`

或

`funcArg func:G groupingCol`

或

`func:G(funcArgs, groupingCol)`

## 详情

对 *groupingCol* 排序后分组，然后在每个分组中计算
func(funcArgs)。每组的计算结果可以是标量，向量或字典。该函数的输出结果是一个表，它的行数与分组数相等。

## 参数

* **func** 是一个函数。
* **funcArgs** 是函数 func 的参数。如果有多个参数，则用元组表示。
* **groupingCol** 表示分组变量。可以是向量，表示一个分组列；也可以是等长向量组成的元组，表示多个分组列。

*groupingCol* 和 *funcArgs* 中的每个参数都是相同长度的向量。

注： 对于第二种情况，*func* 表示的函数只能有一个参数。

## 例子

```
sym=`IBM`IBM`IBM`MS`MS`MS$symbol;
price=172.12 170.32 175.25 26.46 31.45 29.43;
qty=5800 700 9000 6300 2100 5300;
trade_date=2013.05.08 2013.05.06 2013.05.07 2013.05.08 2013.05.06 2013.05.07;
groupby(avg, price, sym);
```

| sym | avg\_price |
| --- | --- |
| IBM | 172.563333 |
| MS | 29.113333 |

```
price avg :G sym;
```

| sym | avg\_price |
| --- | --- |
| IBM | 172.563333 |
| MS | 29.113333 |

```
groupby(wavg, [price, qty], sym);
// 计算每个股票标记数量加权后的平均价格
```

| sym | avg\_price |
| --- | --- |
| IBM | 173.856129 |
| MS | 28.373869 |

```
sym = `C`MS`MS`MS`IBM`IBM`C`C`C$SYMBOL
price= 49.6 29.46 29.52 30.02 174.97 175.23 50.76 50.32 51.29
qty = 2200 1900 2100 3200 6800 5400 1300 2500 8800
timestamp = [09:34:07,09:36:42,09:36:51,09:36:59,09:32:47,09:35:26,09:34:16,09:34:26,09:38:12]

groupby(max, price, [sym,minute(timestamp)])
```

| sym | groupingKey | max\_price |
| --- | --- | --- |
| C | 09:34m | 50.76 |
| C | 09:38m | 51.29 |
| IBM | 09:32m | 174.97 |
| IBM | 09:35m | 175.23 |
| MS | 09:36m | 30.02 |

