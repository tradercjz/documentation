# loadTable

## 语法

`loadTable(database, tableName, [partitions], [memoryMode=false])`

## 参数

**database** 字符串，表示数据库的路径，也可以是数据库句柄。可以是分布式数据库或本地磁盘数据库。

**tableName** 字符串，表示表的名称，它需要使用反引号(`)或双引号。

**partitions** 标量或向量，表示要加载的分区。注意，只有本地磁盘数据库支持该参数，分布式数据库不支持该参数。

**memoryMode** 布尔值，表示是否把数据加载到内存。如果 *memoryMode* =false，表示只加载元数据到内存；如果
*memoryMode* =true，
表示将实际数据加载到内存。注意，只有本地磁盘数据库支持该参数，分布式数据库不支持该参数。对于分布式数据库，只将元数据加载到内存中。

## 详情

将数据加载到内存中。

* 对于分布式数据库，返回包含元数据的表对象。
* 对于本地磁盘数据库，如果 *memoryMode* =false，返回包含元数据的表对象；如果 *memoryMode*
  =true，返回包含实际数据的内存分区表。

## 例子

### 例1. 分布式数据库

```
n=1000000
ID=rand(100, n)
dates=2017.08.07..2017.08.11
date=rand(dates, n)
x=rand(10.0, n)
t1=table(ID, date, x);

dbDate = database(, VALUE, 2017.08.07..2017.08.11)
dbID=database(, RANGE, 0 50 100);
db = database("dfs://compoDB", COMPO, [dbDate, dbID]);
pt = db.createPartitionedTable(t1, `pt, `date`ID).append!(t1)

t2=table(0..100 as ID,take(2017.08.07..2017.08.11,101) as date)
dt = db.createTable(t2, `dt).append!(t2)
```

* 加载维度表：

```
tmp = loadTable("dfs://compoDB", `dt)
select count(*) from tmp
```

| count |
| --- |
| 101 |

* 加载分区表：

```
tmp = loadTable("dfs://compoDB", `pt)
select count(*) from tmp
```

| count |
| --- |
| 1000000 |

* 对于分布式数据库，`loadTable`
  函数不支持加载指定分区的数据。如果需要将某些分区的数据加载到内存中，可以在 SQL 语句中指定过滤条件。

```
tmp = loadTable("dfs://compoDB", `pt)
select * from tmp where date=2017.08.07
```

对于内存的分区表，我们可以执行一些函数，如 [update!](../u/update_.md), [drop!](../d/dropColumns_.md), [rename!](../r/rename_.md), [sortBy!](../s/sortBy_.md)。

