# indexedTable

## 语法

`indexedTable(keyColumns, X, [X1], [X2], .....)`

或

`indexedTable(keyColumns, capacity:size, colNames, colTypes)`

或

`indexedTable(keyColumns, table)`

## 参数

**keyColumns** 是一个字符串标量或向量，表示主键。主键的数据类型必须属于以下类别： INTEGRAL,
TEMPORAL 或 LITERAL。

第一种用法中，**X**, **X1**, **X2** ...
可以是向量、数组向量、矩阵或元组。每个向量、元组、数组向量的长度，以及矩阵中每列长度都必须相同。**当 Xk 是元组时：**

* 若 Xk 的元素是等长的向量，**元组的每个元素将作为表的一列。**元组的长度必须等于表的行数。
* 若 Xk 包含不同类型或不等长元素，**则将单独作为表的一列（列类型为 ANY），其每个元素将作为该列每行的元素值。**Xk
  的长度仍然必须和表的行数保持一致。

第二种用法中：

* **capacity** 是正整数，表示建表时系统为该表分配的内存（以记录数为单位）。当记录数超过 *capacity*
  时，系统首先会分配 *capacity*
  1.2~2倍的新的内存空间，然后复制数据到新的内存空间，最后释放原来的内存。对于规模较大的表，此类操作的内存占用会很高。因此，建议建表时预先分配一个合理的
  *capacity*。
* **size** 是整数，表示该表新建时的行数。若 *size* =0，创建一个空表。 若
  *size*>0，则建立一个只包含 size 条记录的表，记录初始值如下：

  + BOOL 类型默认值为 false；
  + 数值类型、时间类型、IPADDR、COMPLEX、POINT 的默认值为 0；
  + Literal, INT128 类型的默认值为 NULL。

  注： 如果
  *colTypes* 指定为数组向量， *size* 必须为0。
* **colNames** 是一个向量，表示列名。
* **colTypes**
  是一个向量，表示每列的数据类型，允许主键外的其它列指定为数组向量类型或元组（ANY）类型。可使用表示数据类型的系统保留字或相应的字符串。

第三种用法中，**table** 是一个表。注意，*table* 中的 *keyColumns*
不能包含重复值。

## 详情

创建索引内存表（indexed
table）。一个索引内存表有一个主键。主键可由一个或多个字段组成。索引内存表使用红黑树存储主键索引。在查询时，只要查询条件中包含主键的第1个列字段，便可通过索引定位数据，而无需进行全表扫描。

向表中添加新记录时，系统会检查新记录的主键值。如果新记录的主键值与已有记录的主键值重复，系统会更新表中对应的记录；否则，系统会将新记录添加到表中。

键值内存表在指定所有键值字段时才能达到最佳的查询性能。然而，在实际应用中，并不总是需要查询所有键值字段的信息。对于那些只需查询部分键值字段的情况，可以考虑使用索引内存表。

关于对索引内存表和[键值内存表](../k/keyedTable.md)使用怎样的查询语句以及如何进行查询优化，详见下表：

|  | indexedTable | keyedTable |
| --- | --- | --- |
| 查询优化 | * 查询语句必须包含 *keyColumns* 的第 1 列，且该列过滤条件中只能使用 =, in 或   and； * 除 keyColumns 的第 1 列外，其它列可以通过   between、比较运算符等进行范围查询，且查询效率高于使用 in 谓词。 * 所有过滤条件中，对不同列使用的 in 的次数不超过2次； * 建议调用 [sliceByKey](../s/sliceByKey.md)   以提高性能。 | * 查询语句必须包含 *keyColumns* 所有列。 * 过滤条件中只能使用 =, in 或 and，且对不同列使用 in 的次数不超过2次； * 建议调用 [sliceByKey](../s/sliceByKey.md)   以提高性能。 |
| 查询语句特点 | 只需要包含 *keyColumns* 的第 1 列，而无需包含所有列。 | 包含 keyColumns 的所有列。此时查询性能优于 indexedTable。 |

## 例子

例1. 创建索引表

第一种写法：

```
sym=`A`B`C`D`E
id=5 4 3 2 1
val=52 64 25 48 71
t=indexedTable(`sym`id,sym,id,val)
t;
```

| sym | id | col1 |
| --- | --- | --- |
| A | 5 | 52 |
| B | 4 | 64 |
| C | 3 | 25 |
| D | 2 | 48 |
| E | 1 | 71 |

第二种写法：

```
t=indexedTable(`sym`id,1:0,`sym`id`val,[SYMBOL,INT,INT])
insert into t values(`A`B`C`D`E,5 4 3 2 1,52 64 25 48 71);
```

第三种写法：

```
tmp=table(sym, id, val)
t=indexedTable(`sym`id, tmp);
```

创建索引内存分区表：

```
t=indexedTable(`sym`id,sym,id,val)
db=database("",VALUE, sym)
pt=db.createPartitionedTable(t,`pt,`sym).append!(t);
```

例2. 更新索引表

```
t=indexedTable(`sym,1:0,`sym`datetime`price`qty,[SYMBOL,DATETIME,DOUBLE,DOUBLE])
insert into t values(`APPL`IBM`GOOG,2018.06.08T12:30:00 2018.06.08T12:30:00 2018.06.08T12:30:00,50.3 45.6 58.0,5200 4800 7800)
t;
```

| sym | datetime | price | qty |
| --- | --- | --- | --- |
| APPL | 2018.06.08T12:30:00 | 50.3 | 5200 |
| IBM | 2018.06.08T12:30:00 | 45.6 | 4800 |
| GOOG | 2018.06.08T12:30:00 | 58 | 7800 |

插入新记录，并且新记录中的 *keyColumns* 的值与表中 *keyColumns* 的值重复：

```
insert into t values(`APPL`IBM`GOOG,2018.06.08T12:30:01 2018.06.08T12:30:01 2018.06.08T12:30:01,65.8 45.2 78.6,5800 8700 4600)
t;
```

| sym | datetime | price | qty |
| --- | --- | --- | --- |
| APPL | 2018.06.08T12:30:01 | 65.8 | 5800 |
| IBM | 2018.06.08T12:30:01 | 45.2 | 8700 |
| GOOG | 2018.06.08T12:30:01 | 78.6 | 4600 |

*keyColumns* 的值不允许更新：

```
update t set sym="C_"+sym;
// output: Can't update a key column.
```

例3. 查询索引内存表

SQL 语句中若不使用 or，且某个过滤条件包含 *keyColumns* 的第1列，且该过滤条件使用 = 或 in
谓词，且 in 谓词使用不超过两次，则查询索引内存表的性能优于查询普通内存表。与之对比，若希望查询键值表的性能优于普通内存表，过滤条件必须包含全部
*keyColumns*。

首先，分别创建包含100万条记录的普通内存表 t 和索引内存表 t1。

```
id=shuffle(1..1000000)
date=take(2012.06.01..2012.06.10, 1000000)
type=take(0..9, 1000000)
val=rand(100.0, 1000000)
t=table(id, date, type, val)
t1=indexedTable(`id`date`type, id, date, type, val);
```

使用 *keyColumns* 的第一列进行过滤：

```
timer(100) select * from t where id=500000;
// output: Time elapsed: 177.286 ms

timer(100) select * from t1 where id=500000;
// output: Time elapsed: 1.245 ms

timer(100) sliceByKey(t1, 500000)
// output: Time elapsed: 0.742 ms

timer(100) select * from t where id in [500000, 600000, 700000];
// output: Time elapsed: 1134.429 ms

timer(100) select * from t1 where id in [500000, 600000, 700000];
// output: Time elapsed: 1.377 ms
```

若 *keyColumns* 第一列的过滤条件不使用 = 或 in ，则查询索引内存表的性能不会优化：

```
timer(100) select * from t where id between 500000:500010;
// output: Time elapsed: 641.544 ms

timer(100) select * from t1 where id between 500000:500010;
// output: Time elapsed: 599.752 ms
```

使用 *keyColumns* 的第一列与第三列进行过滤：

```
timer(100) select * from t where id=500000, type in [3,6];
// output: Time elapsed: 172.808 ms

timer(100) select * from t1 where id=500000, type in [3,6];
// output: Time elapsed: 1.664 ms
```

若不使用第一列 *keyColumns* 进行过滤，则查询索引内存表的性能不会优化：

```
timer(100) select * from t where date in [2012.06.03, 2012.06.06];
// output: Time elapsed: 490.182 ms

timer(100) select * from t1 where date in [2012.06.03, 2012.06.06];
// output: Time elapsed: 544.015 ms

timer(100) select * from t where date=2012.06.03, type=8;
// output: Time elapsed: 205.443 ms

timer(100) select * from t1 where date=2012.06.03, type=8;
// output: Time elapsed: 204.532 ms
```

若过滤条件使用超过两个 in 谓词，则查询索引内存表的性能不会优化：

```
timer(100) select * from t where id in [100,200], date in [2012.06.03, 2012.06.06], type in [3,6];
// output: Time elapsed: 208.714 ms

timer(100) select * from t1 where id in [100,200], date in [2012.06.03, 2012.06.06], type in [3,6];
// output: Time elapsed: 198.674 ms
```

例4. 使用 `indexedTable` 保留每只股票卖方委托的最新五档报价。

```
sym=["a","b","c "]
time=22:58:52.827 22:58:53.627 22:58:53.827
volume=array(INT[]).append!([[100,110,120,115,125],[200,230,220,225,230],[320,300,310,315,310]])
price=array(DOUBLE[]).append!([[10.5,10.6,10.7,10.77,10.85],[8.6,8.7,8.76,8.83,8.9],[6.3,6.37,6.42,6.48,6.52]])
t=indexedTable(`sym,sym,time,volume,price)
t
```

| sym | time | volume | price |
| --- | --- | --- | --- |
| a | 22:58:52.827 | [100, 110, 120, 115, 125] | [10.5, 10.6, 10.7, 10.77, 10.85] |
| b | 22:58:53.627 | [200, 230, 220, 225, 230] | [8.6, 8.7, 8.76, 8.83, 8.9] |
| c | 22:58:53.827 | [320, 300, 310, 315, 310] | [6.3, 6.37, 6.42, 6.48, 6.52] |

```
//最新的报价数量和价格
newVolume=array(INT[]).append!([[130,110,110,115,120]])
newPrice= array(DOUBLE[]).append!([[10.55,10.57,10.62,10.68,10.5]])
//更新名为 a 的股票的最新报价
update t set volume=newVolume, price=newPrice where sym="a"
t
```

| sym | time | volume | price |
| --- | --- | --- | --- |
| a | 22:58:52.827 | [130, 110, 110, 115, 120] | [10.55, 10.57, 10.62, 10.68, 10.5] |
| b | 22:58:53.627 | [200, 230, 220, 225, 230] | [8.6, 8.7, 8.76, 8.83, 8.9] |
| c | 22:58:53.827 | [320, 300, 310, 315, 310] | [6.3, 6.37, 6.42, 6.48, 6.52] |

需要注意的是，更新 array vector
列的数据时，新记录中各行向量的元素个数必须和原记录中对应行向量的元素个数相同，否则会出现报错。如下例，新记录向量中有4个元素，而已有记录对应行的向量中有5个元素，数量不相同，出现报错：

```
newPrice= array(DOUBLE[]).append!([[10.55,10.57,10.62,10.5]])
update t set volume=newVolume, price=newPrice where sym="a"
// error: Failed to update column: price
```

相关函数：[keyedTable](../k/keyedTable.md)

