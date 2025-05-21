# unionAll

## 语法

`unionAll(tableA, tableB, [byColName=false])`

或

`unionAll(tables, [partition=true], [byColName=false])`

或

`unionAll(tables, tableB)`

## 参数

* 用法一：

  + **tableA** 和 **tableB** 是列数相同的内存表。
* 用法二：

  + **tables** 是一个元组，其中每个元素都是一个表，并且它们具有相同的列数。
  + **partition** 是布尔值，表示是否进行顺序分区（SEQ），默认值是
    true。
  + **byColName** 是一个布尔值。若设为
    true，表示表合并时，依照列名进行，各表中相同列名的列进行合并，缺失的列用空值填充。若设为
    false，表示表合并时仅基于列顺序，不管列名是否一致。
* 用法三：

  + **tables**
    是一个元组，其中每个元素都是一个内存表，并且它们具有相同的列数。**tableB** 是一个和 *tables*
    中表列数相同的内存表。

注：

*tableA*, *tableB*, *tables* 支持以下内存表：table,
keyedTable, indexedTable, latestKeyedTable, latestIndexedTable。此外，用法三的
*tableB* 还可以是一个分区内存表。

## 详情

第一种用法只能将两个表合并成一个表，返回的结果是未分区的内存表。

第二种用法可以多个表合并成一个表。如果 *partition* 为 false，返回的结果是未分区的内存表；如果
*partition* 为 true，返回的结果是一个顺序分区的内存表。默认值为 true。

当 *byColName* =true 时，各表可有不同数量的列。若某列在某些表中不存在，结果中会以空值填充。

当 *byColName* =false 时，各表必须有相同数量的列。

第三种用法是将多个表追加到指定的表，并返回该表。常用于 `mr` 函数的 finalFunc。

## 例子

用法一：合并两个内存表

```
t1=table(1 2 3 as id, 11 12 13 as x)
t2=table(4 5 6 as id, 14 15 16 as x)
re=unionAll(t1,t2)
re;
```

| id | x |
| --- | --- |
| 1 | 11 |
| 2 | 12 |
| 3 | 13 |
| 4 | 14 |
| 5 | 15 |
| 6 | 16 |

```
typestr(re);
// output
IN-MEMORY TABLE
```

用法二：合并多个内存表

```
t1=table(1 2 3 as id, 11 12 13 as x)
t2=table(4 5 6 as id, 14 15 16 as x)
t3=table(7 8 as id, 17 18 as x)
re=unionAll([t1,t2,t3])
select * from re;
```

| id | x |
| --- | --- |
| 1 | 11 |
| 2 | 12 |
| 3 | 13 |
| 4 | 14 |
| 5 | 15 |
| 6 | 16 |
| 7 | 17 |
| 8 | 18 |

```
typestr(re);
// output
SEGMENTED IN-MEMORY TABLE
```

指定 byColName：

```
t1=table(1 2 3 as id, 11 12 13 as x)
t2=table(14 15 16 as x, 4 5 6 as id)
unionAll(t1,t2,true);
```

| id | x |
| --- | --- |
| 1 | 11 |
| 2 | 12 |
| 3 | 13 |
| 4 | 14 |
| 5 | 15 |
| 6 | 16 |

```
t1=table(1 2 3 as id, 11 12 13 as x)
t2=table(14 15 16 as x, 4 5 6 as id)
unionAll(t1,t2);
```

| id | x |
| --- | --- |
| 1 | 11 |
| 2 | 12 |
| 3 | 13 |
| 14 | 4 |
| 15 | 5 |
| 16 | 6 |

上例中可见，若不指定 *byColName* （即 *byColName* =false），请务必确认各表中列名顺序一致，否则会产生错误结果。

```
t1=table(1 2 3 as id, 11 12 13 as x, 21 22 23 as y)
t2=table(4 5 6 as id, 14 15 16 as x)
unionAll(t1,t2,true);
```

| id | x | y |
| --- | --- | --- |
| 1 | 11 | 21 |
| 2 | 12 | 22 |
| 3 | 13 | 23 |
| 4 | 14 |  |
| 5 | 15 |  |
| 6 | 16 |  |

```
t1=table(1 2 3 as id, 11 12 13 as x, 21 22 23 as y)
t2=table(4 5 6 as id, 14 15 16 as x)
unionAll(t1, t2) => The number of columns of the table to insert must be the same as that of the original table.
```

上例中可见，若各表中列数不一致，必须将 *byColName* 设为 true。

用法三：将多个内存表合并到分区内存表

```
def testFunc(data, off){
    return select *, price * (1-off) as `discountPrice from data
}
n = 100
dates = 2021.01.01..2021.12.31
t = table(take(dates, 365 * n).sort() as `date, `sym + take(1..n, 365 * n).sort()$STRING as `sym, round(10 + norm(0, 2, 365 * n), 2) as `price)

db = database("", VALUE, 2021.01.01..2021.12.31)
trade = db.createPartitionedTable(table=t, tableName="trade", partitionColumns=`date).append!(t)
db = database("", RANGE, date(month(dates.first()) .. (month(dates.last()) + 1)))
outputT=table(1:0, `date`sym`price`discountPrice, [DATE,SYMBOL,DOUBLE,DOUBLE])
ports = db.createPartitionedTable(outputT, "ports", `date)
//map reduce
mr(sqlDS(<select * from trade>), testFunc{,0.3},,unionAll{,ports})

select * from ports
```

