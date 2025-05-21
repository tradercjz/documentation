# existsDatabase

## 语法

`existsDatabase(dbUrl)`

## 参数

**dbUrl** 是一个字符串，表示数据库的路径。

## 详情

检查指定数据库是否存在。

## 例子

检查分布式数据库是否存在：

```
n=1000000
ID=rand(10, n)
dates=2017.08.07..2017.08.11
date=rand(dates, n)
x=rand(10.0, n)
t=table(ID, date, x)

db = database("dfs://valueDB", VALUE, 2017.08.07..2017.08.11)
pt = db.createPartitionedTable(t, `pt, `date);
pt.append!(t);

existsDatabase("dfs://valueDB");
```

输出返回：true

```
existsDatabase("dfs://valueDB/20170807");
```

输出返回：false

