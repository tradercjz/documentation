# tableInsert

## 语法

`tableInsert(table, args...)`

## 详情

将 *args...* 插入到 *table* 中，并返回插入的行数。

如果  *args...* 是一个表，它的结构必须与 *table* 的结构相同。若 *table*
是分区表， *args...* 只能是一个表。

如果  *args...* 是一个元组，那么它的元素个数必须与 *table*
的列数相同，并且每个元素的数据类型必须与 *table* 中与之对应的每列的数据类型相同。

如果  *args...* 是多个向量或元组，那么向量与元组的个数必须与 *table*
中列数一致，且每个向量或元组的数据类型必须与 *table* 中与之对应的每列的数据类型相同。

如果  *args...* 是一个字典，那么它的 keys 对应 *table* 的列名，values 对应
*table* 中每列的值，且 values 必须为元组。这种用法只适用于 *table* 为内存表的情况。

注： 若数据库为 VALUE 分区，且分区列为字符串类型，则追加的分区列数据不能包含空格，“/n”, “/r”,
“/t”。

## 参数

**table** 是表对象或表名。该表可为内存表或 DFS 表。在远程调用中，由于得不到远程表对象的引用，因此必须使用表名。

**args...** 可以是一个表、元组或字典，或多个向量或元组。

## 例子

```
colName=["Name","Age"]
colType=["string","int"]
t1=table(100:0,colName, colType);

name=`Tom`Jerry`John
age=24 25 26
t2=table(name, age)

tableInsert(t1, t2);
// output
3

t1;
```

| Name | Age |
| --- | --- |
| Tom | 24 |
| Jerry | 25 |
| John | 26 |

```
tableInsert(t1, (`George, 29));
// output
1

t1;
```

| Name | Age |
| --- | --- |
| Tom | 24 |
| Jerry | 25 |
| John | 26 |
| George | 29 |

```
tableInsert(t1, (`Frank`Henry, 31 32));
// output
2

tableInsert(t1, `Nicole`Nancy, 28 29);
// output
2

t1.tableInsert(dict(`Name`Age, [`Patrick, 22]));
// output
1
```

使用 `tableInsert` 函数向分布式表中插入批量数据：

```
db=database("dfs://db1",RANGE,0 20 50 101)
n=100000
id=rand(100,n)
val=rand(100.0,n)
t=table(id,val)
pt=db.createPartitionedTable(t,`pt,`id).append!(t);

tmp=table(rand(100,10000) as id,take(200.0,10000) as val);

tableInsert(pt,tmp);
// output
10000
```

