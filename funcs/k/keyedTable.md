# keyedTable

## 语法

`keyedTable(keyColumns, X, [X1], [X2], .....)`

或

`keyedTable(keyColumns, capacity:size, colNames, colTypes)`

或

`keyedTable(keyColumns, table)`

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

第三种用法中，`table` 是一个表。注意，*table* 中的
*keyColumns* 不能包含重复值。

## 详情

创建键值内存表。一个键值内存表有一个主键。主键可由一个或多个字段组成。键值内存表基于哈希表实现，将主键字段的组合值存成一个键值，每个键值对应表中的一行数据。在查询时，指定主键的所有字段，便可通过键值定位数据，而无需进行全表扫描。

向表中添加新记录时，系统会自动检查新记录的主键值，如果新记录的主键值与已有记录的主键值重复时，系统会更新表中对应的记录，否则向表中添加记录。

键值表对单行的更新和查询效率很高，是数据缓存的理想选择。键值表也可作为时间序列聚合引擎的输出表，用于实时更新输出表的结果。

关于对键值内存表和[索引内存表](../i/indexedTable.html)使用怎样的查询语句以及如何进行查询优化，详见下表：

|  | keyedTable | indexedTable |
| --- | --- | --- |
| 查询优化 | * 查询语句必须包含 *keyColumns* 所有列。 * 过滤条件中只能使用 =, in 或 and，且对不同列使用 in 的次数不超过2次； * 建议调用 [sliceByKey](../s/sliceByKey.html)   以提高性能。 | * 查询语句必须包含 *keyColumns* 的第 1 列，且该列过滤条件中只能使用 =, in 或   and； * 除 keyColumns 的第 1 列外，其它列可以通过   between、比较运算符等进行范围查询，且查询效率高于使用 in 谓词。 * 所有过滤条件中，对不同列使用的 in 的次数不超过2次； * 建议调用 [sliceByKey](../s/sliceByKey.html)   以提高性能。 |
| 查询语句特点 | 包含 keyColumns 的所有列。此时查询性能优于 indexedTable。 | 只需要包含 *keyColumns* 的第 1 列，而无需包含所有列。 |

## 例子

例1. 创建键值表

第一种写法：

```
sym=`A`B`C`D`E
id=5 4 3 2 1
val=52 64 25 48 71
t=keyedTable(`sym`id,sym,id,val)
t;
```

| sym | id | val |
| --- | --- | --- |
| A | 5 | 52 |
| B | 4 | 64 |
| C | 3 | 25 |
| D | 2 | 48 |
| E | 1 | 71 |

第二种写法：

```
t=keyedTable(`sym`id,1:0,`sym`id`val,[SYMBOL,INT,INT])
insert into t values(`A`B`C`D`E,5 4 3 2 1,52 64 25 48 71);
```

第三种写法：

```
tmp=table(sym, id, val)
t=keyedTable(`sym`id, tmp);
```

创建键值内存分区表：

```
sym=`A`B`C`D`E
id=5 4 3 2 1
val=52 64 25 48 71
t=keyedTable(`sym`id,sym,id,val)
db=database("",VALUE,sym)
pt=db.createPartitionedTable(t,`pt,`sym).append!(t);
```

例2. 更新键值表

```
t=keyedTable(`sym,1:0,`sym`datetime`price`qty,[SYMBOL,DATETIME,DOUBLE,DOUBLE])
insert into t values(`APPL`IBM`GOOG,2018.06.08T12:30:00 2018.06.08T12:30:00 2018.06.08T12:30:00,50.3 45.6 58.0,5200 4800 7800)
t;
```

| sym | datetime | price | qty |
| --- | --- | --- | --- |
| APPL | 2018.06.08T12:30:00 | 50.3 | 5200 |
| IBM | 2018.06.08T12:30:00 | 45.6 | 4800 |
| GOOG | 2018.06.08T12:30:00 | 58 | 7800 |

插入新记录，并且新记录中的主键值与表中主键值重复：

```
insert into t values(`APPL`IBM`GOOG,2018.06.08T12:30:01 2018.06.08T12:30:01 2018.06.08T12:30:01,65.8 45.2 78.6,5800 8700 4600)
t;
```

| sym | datetime | price | qty |
| --- | --- | --- | --- |
| APPL | 2018.06.08T12:30:01 | 65.8 | 5800 |
| IBM | 2018.06.08T12:30:01 | 45.2 | 8700 |
| GOOG | 2018.06.08T12:30:01 | 78.6 | 4600 |

插入新记录，并且新记录中的主键值重复：

```
insert into t values(`MSFT`MSFT,2018.06.08T12:30:01 2018.06.08T12:30:01,45.7 56.9,3600 4500)
t;
```

| sym | datetime | price | qty |
| --- | --- | --- | --- |
| APPL | 2018.06.08T12:30:01 | 65.8 | 5800 |
| IBM | 2018.06.08T12:30:01 | 45.2 | 8700 |
| GOOG | 2018.06.08T12:30:01 | 78.6 | 4600 |
| MSFT | 2018.06.08T12:30:01 | 56.9 | 4500 |

主键不允许更新：

```
update t set sym="C_"+sym;
// output: Can't update a key column.
```

例3. 查询键值内存表

当过滤条件不使用 or，包含所有 *keyColumns*，并且每个条件都使用了等值谓词(=)或 in 谓词，且 in
谓词数量不超过两个时，键值内存表的查询性能优于普通内存表。

以下例子将比较键值内存表和普通内存表的查询性能。首先，分别创建包含100万条记录的普通内存表 t 和键值内存表 kt。

```
id=shuffle(1..1000000)
date=take(2012.06.01..2012.06.10, 1000000)
type=rand(9, 1000000)
val=rand(100.0, 1000000)
t=table(id, date, type, val)
kt=keyedTable(`id`date`type, id, date, type, val);
```

例3.1

```
timer(100) select * from t where id=500000, date=2012.06.01, type=0;
// output: Time elapsed: 161.574 ms

timer(100) select * from kt where id=500000, date=2012.06.01, type=0;
// output: Time elapsed: 1.483 ms

timer(100) sliceByKey(t1, (500000, 2012.06.01, 0))
// output: Time elapsed: 0.705 ms
```

例3.2

```
timer(100) select * from t where id in [1, 500000], date in 2012.06.01..2012.06.05, type=5;
// output: Time elapsed: 894.241 ms

timer(100) select * from kt where id in [1, 500000], date in 2012.06.01..2012.06.05, type=5;
// output: Time elapsed: 2.322 ms
```

in 谓词数量超过两个时，键值内存表不会进行查询优化：

例3.3

```
timer(100) select * from t where id in [1, 500000], date in 2012.06.01..2012.06.05, type in 1..5;
// output: Time elapsed: 801.347 ms

timer(100) select * from kt where id in [1, 500000], date in 2012.06.01..2012.06.05, type in 1..5;
// output: Time elapsed: 834.184 ms
```

若过滤条件没有包括所有 *keyColumns*，键值内存表亦不会进行查询优化：

例3.4

```
timer(100) select * from t where id=500000, date in 2012.06.01..2012.06.05;
// output: Time elapsed: 177.113 ms

timer(100) select * from kt where id=500000, date in 2012.06.01..2012.06.05;
// output: Time elapsed: 163.265 ms
```

例4. 使用 `keyedTable` 保留每只股票卖方委托的最新五档报价。

```
sym=["a","b","c "]
time=22:58:52.827 22:58:53.627 22:58:53.827
volume=array(INT[]).append!([[100,110,120,115,125],[200,230,220,225,230],[320,300,310,315,310]])
price=array(DOUBLE[]).append!([[10.5,10.6,10.7,10.77,10.85],[8.6,8.7,8.76,8.83,8.9],[6.3,6.37,6.42,6.48,6.52]])
t=keyedTable(`sym,sym,time,volume,price)
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
newVolume=array(INT[]).append!([[130,110,110,120]])
newPrice= array(DOUBLE[]).append!([[10.55,10.57,10.62,10.5]])

update t set volume=newVolume, price=newPrice where sym="a"
// error: Failed to update column: volume
```

相关函数：[indexedTable](../i/indexedTable.html)

