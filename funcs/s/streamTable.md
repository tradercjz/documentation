# streamTable

## 语法

`streamTable(X, [X1], [X2], .....)`

或

`streamTable(capacity:size, colNames, colTypes)`

## 参数

第一种用法中，**X**, **X1**, **X2** ...
可以是向量、数组向量、矩阵或元组。每个向量、元组、数组向量的长度，以及矩阵中每列长度都必须相同。**当 Xk 是元组时：**

* 若 Xk 的元素是等长的向量，**元组的每个元素将作为表的一列。**元组的长度必须等于表的行数。
* 若 Xk 包含不同类型或不等长元素，**则将单独作为表的一列（列类型为 ANY），其每个元素将作为该列每行的元素值。**Xk
  的长度仍然必须和表的行数保持一致。

第二种用法中：

* **capacity** 是正整数，表示建表时系统为该表分配的内存（以记录数为单位）。当记录数超过
  *capacity* 时，系统首先会分配 *capacity*
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
  是一个向量，表示每列的数据类型，支持数组向量类型和元组（ANY）类型。可使用表示数据类型的系统保留字或相应的字符串。

## 详情

创建[流数据表](../../stream/str_table.md)。流数据表可处理并发的读写操作。

## 例子

```
id=`XOM`GS`AAPL
x=102.1 33.4 73.6

rt=streamTable(id, x);

rt=streamTable(`XOM`GS`AAPL as id, 102.1 33.4 73.6 as x);

colName=["Name","Age"]
colType=["string","int"]
rt=streamTable(100:10, colName, colType);
```

