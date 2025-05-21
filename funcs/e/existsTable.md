# existsTable

## 语法

`existsTable(dbUrl, tableName)`

## 参数

**dbUrl** 是一个字符串，表示数据库的路径。

**tableName** 是表的名称。它需要用反引号(`)或双引号。

## 详情

检查指定表是否存在于指定数据库中。

## 例子

检查分区是否在分布式文件系统中（以下脚本需要在集群的数据节点/计算节点中执行）：

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

existsTable("dfs://valueDB", `pt);
// output
true

existsTable("dfs://valueDB/20170807", `pt);
// output
true
```

