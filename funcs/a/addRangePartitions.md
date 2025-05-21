# addRangePartitions

## 语法

`addRangePartitions(dbHandle, newRanges, [level=0],
[locations])`

## 参数

**dbHandle** 是数据库句柄。

**newRanges** 是向量，表示新的分区。它必须按升序排序，并且第一个元素必须与数据库的原分区方案的最后一个元素相同。

**level** 是整数。当分区类型为 COMPO，并且每层分区为 RANGE 时，需要使用 *level*
参数指定 RANGE 分区所在的层。它是可选参数。默认值为0。

**locations** 是字符串标量或向量。如果目标数据库创建时，指定了 *locations*
参数，增加新的分区时可以使用 *locations* 参数指定新增分区的位置。它是可选参数。

## 详情

给数据库增加新的分区。目标数据库必须是 RANGE 分区类型或 COMPO 分区类型并且至少其中一层分区为 RANGE
类型。返回的结果是一个整数，表示新增的分区数量。注意，只能在最后一个现有数据分区后面添加分区，不能在第一个现有数据分区前面添加分区。

## 例子

下面的例子是给分区类型为 COMPO 的数据库新增[101, 150), [150,200)和[200,250)分区，但无法新增
[50,100) 分区。

```
n=1000000
ID=rand(100, n)
dates=2017.08.07..2017.08.11
date=rand(dates, n)
x=rand(10.0, n)
t=table(date, ID, x);
dbDate = database(, VALUE, 2017.08.07..2017.08.11)
dbID=database(, RANGE, 0 50 101);
db = database("dfs://compoDB", COMPO, [dbDate,dbID]);
pt = db.createPartitionedTable(t, `pt, `date`ID)
pt.append!(t);

addRangePartitions(db,101 150 200 250,1)
// output
3
```

添加新的分区后，需要重新加载数据库。

```
db=database("dfs://compoDB")
pt=loadTable(db,"pt")

t1=table(rand(2017.08.07..2017.08.11,n) as date, rand(101..249,n) as ID, rand(10.0,n) as x)
pt.append!(t1);

select count(*) from loadTable("dfs://compoDB","pt");
// output
2000000
```

