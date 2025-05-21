# addValuePartitions

## 语法

`addValuePartitions(dbHandle, newValues, [level=0],
[locations])`

## 参数

**dbHandle** 是数据库句柄。

**newValues** 是标量或向量，表示新的分区。

**level** 是整数。当分区类型为 COMPO，并且每层分区为 VALUE 时，需要使用 *level*
参数指定 VALUE 分区所在的层。它是可选参数。默认值为0

**locations** 是字符串标量或向量。如果目标数据库创建时，指定了 *locations*
参数，增加新的分区时可以使用 *locations* 参数指定新增分区的位置。它是可选参数。

## 详情

给数据库增加新的分区。目标数据库必须是 VALUE 分区类型或 COMPO 分区类型并且至少其中一层分区为 VALUE
类型。

如果配置参数 *newValuePartitionPolicy*=add，系统会自动为新的数据增加分区。

## 例子

下面的例子是给分区类型为 COMPO 的数据库新增2017.08.12到2017.08.20分区。

```
n=1000000
ID=rand(100, n)
dates=2017.08.07..2017.08.11
date=rand(dates, n)
x=rand(10.0, n)
t=table(ID, date, x)

dbID=database(, RANGE, 0 50 100);
dbDate = database(, VALUE, 2017.08.07..2017.08.11)
db = database("dfs://compoDB", COMPO, [dbID, dbDate]);
pt = db.createPartitionedTable(t, `pt, `ID`date)
pt.append!(t)

addValuePartitions(db,2017.08.12..2017.08.20,1)
// output
9
```

添加新的分区后，需要重新加载数据库。

```
db=database("dfs://compoDB")
pt=loadTable(db,"pt")

t1=table(0..99 as ID,take(2017.08.12,100) as date,rand(10.0,100) as x)
pt.append!(t1)

select count(*) from loadTable("dfs://compoDB","pt")
// output
1000100
```

