# conditionalFilter

## 语法

`conditionalFilter(X, condition, filterMap)`

## 参数

**X** 是标量或者向量。

**condition** 是标量，或与 *X* 等长的向量。

**filterMap** 是字典，表示过滤条件。

## 详情

根据给定的字典参数 *filterMap*，若向量 *condition* 中某元素为该字典的 key，而且向量
*X* 中相应位置元素为字典中该 key 值对应的 value 表示的向量中一个元素，或在该 value 表示的数据对的范围中时，返回
true，否则返回 false。

如果 *X* 和 *condition* 都是向量，返回的结果是与它们等长的向量。

## 例子

例1：

```
conditionalFilter(1 2 3,`a`b`c, dict(`a`b,1 2));
// output
[1,1,0]

conditionalFilter(1 2 3,`a`b`b, dict(`a`b,[1 2,3 4]))
// output
[1,0,1]
```

例2：

从数据表 t 中，提取如下天内指定股票的数据：

2012.06.01: C, MS 2012.06.02: IBM, MS 2012.06.03: MS 2012.06.04: IBM

```
sym = `C`MS`MS`MS`IBM`IBM`C`C`C$SYMBOL
date = 2012.06.01 2012.06.01 2012.06.02 2012.06.03 2012.06.01 2012.06.02 2012.06.02 2012.06.03 2012.06.04
price = 49.6 29.46 29.52 30.02 174.97 175.23 50.76 50.32 51.29
qty = 2200 1900 2100 3200 6800 5400 1300 2500 8800
t = table(sym, date, price, qty)
t;
```

| sym | date | price | qty |
| --- | --- | --- | --- |
| C | 2012.06.01 | 49.60 | 2200 |
| MS | 2012.06.01 | 29.46 | 1900 |
| MS | 2012.06.02 | 29.52 | 2100 |
| MS | 2012.06.03 | 30.02 | 3200 |
| IBM | 2012.06.01 | 174.97 | 6800 |
| IBM | 2012.06.02 | 175.23 | 5400 |
| C | 2012.06.02 | 50.76 | 1300 |
| C | 2012.06.03 | 50.32 | 2500 |
| C | 2012.06.04 | 51.29 | 8800 |

```
filter = dict(2012.06.01..2012.06.04, [`C`MS, `IBM`MS, `MS, `IBM])
select * from t where conditionalFilter(sym, date, filter) order by date, sym;
```

| sym | date | price | qty |
| --- | --- | --- | --- |
| C | 2012.06.01 | 49.6 | 2200 |
| MS | 2012.06.01 | 29.46 | 1900 |
| IBM | 2012.06.02 | 175.23 | 5400 |
| MS | 2012.06.02 | 29.52 | 2100 |
| MS | 2012.06.03 | 30.02 | 3200 |

例3：

*filterMap* 的 value 亦可采用数据对的形式。

```
t=table(`aaa`aaa`bbb`bbb as id, 2020.09.03 2020.09.10 2020.09.06 2020.09.09 as date)
t
```

| id | date |
| --- | --- |
| aaa | 2020.09.03 |
| aaa | 2020.09.10 |
| bbb | 2020.09.06 |
| bbb | 2020.09.09 |

```
mydict = dict(`aaa`bbb, [2020.09.01 : 2020.09.09,  2020.09.05 : 2020.09.09])
select * from t where conditionalFilter(date, id, mydict);
```

| id | date |
| --- | --- |
| aaa | 2020.09.03 |
| bbb | 2020.09.06 |
| bbb | 2020.09.09 |

