# mvccTable

## 语法

`mvccTable(X, [X1], [X2], .....)`

或

`mvccTable(capacity:size, colNames, colTypes, [path],
[tableName], [defaultValues],
[allowNull])`

## 参数

对于第一种用法，**X**, **X1**, **X2** ...是向量。

对于第二种用法：

**capacity** 是正整数，表示表的容量，即建表时系统为该表分配的内存（以记录数为单位）。当记录数超过 *capacity*
时，系统会自动扩充容量。系统首先会分配当前容量1.2~2倍的内存，然后复制数据到新的内存空间，最后释放原来的内存。对于规模较大的表，扩容时的内存占用会很高。因此，建议创建内存表时预先分配一个合理的容量。

**size** 是正整数，表示该表新建时的行数。若 *size*=0，创建一个空表；若 *size*>0，则新建表中记录的初始值由
*defaultValues* 决定。

**colNames** 是字符串向量，表示列名。

**colTypes** 是向量，表示列的数据类型。

**path** 是一个字符串，表示保存表的路径。只能指定磁盘路径，不支持指定为分布式数据库路径。

**tableName** 是一个字符串，表示保存到磁盘上的表名。

**defaultValues** 是与 *colNames*
等长的元组，表示建表时各列的默认值。若不指定，则：

* BOOL 类型默认值为 false；
* 数值类型、时间类型、IPADDR、COMPLEX、POINT 的默认值为 0；
* Literal, INT128 类型的默认为 NULL。

**allowNull** 是与 *colNames* 等长的布尔类型向量，表示是否允许各列包含空值。默认值为
true，允许包含空值。

## 详情

创建一个多版本并发控制的表（MVCC
表）。我们可以对该表进行并发读写。多版本并发控制的表适用于频繁读写但很少更新和删除记录的场景。

如果指定了 *path* 和 *tableName* 参数，会把表持久化到硬盘上。通过 [loadMvccTable](../l/loadMvccTable.html) 函数，可以把磁盘上的表加载到内存中。

注：

* 不支持对 MVCC
  表进行以下操作：addColumn、reorderColumns!、upsert!、drop、erase!。
* 当 *size*=0 时，即使对某列设置
  *allowNull*=false，也可以成功创建空表，但不能向该列追加空值。

## 例子

例1：介绍两种创建 MVCC 表的方法

第一种用法：

```
id=`XOM`GS`AAPL
x=102.1 33.4 73.6
mvccTable(id, x);
```

| id | x |
| --- | --- |
| XOM | 102.1 |
| GS | 33.4 |
| AAPL | 73.6 |

第二种用法：

```
mvccTable(200:10, `name`id`value, [STRING,INT,DOUBLE],"/home/DolphinDB/Data","t1");
```

| name | id | value |
| --- | --- | --- |
|  | 0 | 0 |
|  | 0 | 0 |
|  | 0 | 0 |
|  | 0 | 0 |
|  | 0 | 0 |
|  | 0 | 0 |
|  | 0 | 0 |
|  | 0 | 0 |
|  | 0 | 0 |
|  | 0 | 0 |

"/home/DolphinDB/Data" 目录下会有一个名为 "t1"
文件夹、t1.tbl 文件和 t1.sym 文件。如果需要删除磁盘上的表，需要把这三个文件都删除。

例2：创建分区 MVCC
内存表：

```
n=200000
colNames = `time`sym`qty`price
colTypes = [TIME,SYMBOL,INT,DOUBLE]
trades_mvcc1 = mvccTable(n:0, colNames, colTypes)
trades_mvcc2 = mvccTable(n:0, colNames, colTypes)
db=database(, VALUE, `A`D)
trades = createPartitionedTable(db,table=[trades_mvcc1, trades_mvcc2], tableName="", partitionColumns=`sym)
```

在 2.00.10.4 版本之前，只支持对分区 MVCC
内存表的子表进行更新、插入和删除操作：

```
insert into trades_mvcc1 values(09:30:00.001,`A,100,56.5)
insert into trades_mvcc2 values(09:30:01.001,`D,100,15.5)

insert into trades values(09:30:00.001,`D,100,26.5)
// 报错：Can't append data to a segmented table that contains external partitions.

select * from trades;
```

表 1.

| time | sym | qty | price |
| --- | --- | --- | --- |
| 09:30:00.001 | A | 100 | 56.5 |
| 09:30:01.001 | D | 100 | 15.5 |

2.00.10.4 版本开始支持直接对分区 MVCC
内存表进行更新、插入和删除操作：

```
insert into trades values(09:30:00.001,`D,100,26.5)
select * from trades;
```

表 2.

| time | sym | qty | price |
| --- | --- | --- | --- |
| 09:30:00.001 | A | 100 | 56.5 |
| 09:30:01.001 | D | 100 | 15.5 |
| 09:30:01.001 | D | 100 | 26.5 |

```
delete from trades where sym=`A
select * from trades;
```

表 3.

| time | sym | qty | price |
| --- | --- | --- | --- |
| 09:30:01.001 | D | 100 | 15.5 |
| 09:30:01.001 | D | 100 | 26.5 |

```
update trades set price=price*10 where sym=`D
select * from trades;
```

表 4.

| time | sym | qty | price |
| --- | --- | --- | --- |
| 09:30:01.001 | D | 100 | 155 |
| 09:30:01.001 | D | 100 | 265 |

需要注意的是，直接向子表插入数据时，系统不会校验向子表插入的数据是否与该表匹配。如果插入了不匹配的数据，会导致分区 MVCC
内存表的数据混乱。 因此，为了确保数据的准确性，建议用户直接对分区 MVCC 内存表进行操作，而不要操作子表。

