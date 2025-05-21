# sliceByKey

## 语法

`sliceByKey(table, rowKeys, [colNames])`

## 参数

**table** 是键值表或索引内存表。

**rowKeys** 是标量或向量，表示索引列的指定值。

**colNames** 是字符串标量或向量，表示要选择的列的列名。

## 详情

从键值表或索引内存表中获取含有索引列指定值（由参数 *rowKeys* 指定）的行以及指定列（由
*colNames* 参数指定）的数据。耗时约为相应的 SQL 语句的50%。

如果是键值表，*rowKeys* 参数必须含有所有 *keyColumns* 的值。

如果是索引内存表，可指定前 n 个 *keyColumns*
的值，若其中有一列指定值为向量，所有指定列的指定值均需为同等长度的向量。

若不指定 *colNames* 参数，则会输出所有列。

结果的数据结构取决于 *colNames*。若 *colNames* 为标量，返回一个向量；若 *colNames*
为向量，返回一个内存表。

## 例子

```
t = indexedTable(`sym`side, 10000:0, `sym`side`price`qty, [SYMBOL,CHAR,DOUBLE,INT])
insert into t values(`IBM`MSFT`IBM, ['B','S','S'], 125.27 208.9 125.29, 1000 800 200)
a=sliceByKey(t,"IBM", 'price');

a;
// output
[125.27,125.29]

typestr(a);
// output
FAST DOUBLE VECTOR

a=sliceByKey(t,("IBM",'S'));
a;
```

| sym | side | price | qty |
| --- | --- | --- | --- |
| IBM | S | 125.29 | 200 |

```
typestr(a);
// output
IN-MEMORY TABLE

t1 = keyedTable(`sym`side, 10000:0, `sym`side`price`qty, [SYMBOL,CHAR,DOUBLE,INT])
insert into t1 values(`IBM`MSFT`IBM, ['B','S','S'], 125.27 208.9 125.29, 1000 800 200)
sliceByKey(t1, [["IBM", "MSFT"], ['B', 'S']]);
```

| sym | side | price | qty |
| --- | --- | --- | --- |
| IBM | B | 125.27 | 1000 |
| MSFT | S | 208.9 | 800 |

