# getTables

## 语法

`getTables(dbHandle)`

## 参数

**dbHandle** 是数据库句柄。

## 详情

返回指定数据库中的所有表。

## 例子

```
n=1000000
ID=rand(10, n)
dates=2017.08.07..2017.08.11
date=rand(dates, n)
x=rand(10.0, n)
y=rand(10, n)
t1=table(ID, date, x)
t2=table(ID, date, y)
db = database("dfs://valueDB", VALUE, 2017.08.07..2017.08.11)
pt1 = db.createPartitionedTable(t1, `pt1, `date)
pt1.append!(t1)
pt2 = db.createPartitionedTable(t2, `pt2, `date)
pt2.append!(t2);
getTables(db);
```

输出返回：["pt1","pt2"]

