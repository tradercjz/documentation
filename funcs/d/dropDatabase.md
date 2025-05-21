# dropDatabase

## 语法

`dropDatabase(dbDir)`

## 参数

**dbDir** 是数据库所在的目录。对于分布式文件系统中的数据库，目录要以 `"dfs://"` 开始。

## 详情

删除指定数据库的所有物理文件。

自 3.00.0 版本起，支持删除 catalog 中的数据库，其引用关系也会同时被删掉。

## 例子

删除分布式数据库：

```
n=1000000
ID=rand(10, n)
dates=2017.08.07..2017.08.11
date=rand(dates, n)
x=rand(10.0, n)
t=table(ID, date, x);
saveText(t, "C:/DolphinDB/Data/t.txt");

db = database("dfs://valueDB", VALUE, 2017.08.07..2017.08.11)
pt = loadTextEx(db, `pt1, `date, "C:/DolphinDB/Data/t.txt");

dropDatabase("dfs://valueDB")
```

删除本地磁盘数据库：

```
n=1000000
ID=rand(10, n)
dates=2017.08.07..2017.08.11
date=rand(dates, n)
x=rand(10.0, n)
t=table(ID, date, x)
saveText(t, "C:/DolphinDB/Data/t.txt");

db = database("C:/DolphinDB/Data/rangedb", RANGE, 0 5 10)
pt = loadTextEx(db, `pt, `ID, "C:/DolphinDB/Data/t.txt");

dropDatabase("C:/DolphinDB/Data/rangedb");
```

