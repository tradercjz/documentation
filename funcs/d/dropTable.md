# dropTable

## 语法

`dropTable(dbHandle, tableName)`

## 详情

删除指定的表。该命令只能在数据节点/计算节点上执行，不能在控制节点和代理节点上执行。

## 参数

**dbHandle** 是数据库句柄。

**tableName** 是一个字符串，表示表名。

## 例子

```
n=1000000
ID=rand(10, n)
x=rand(1.0, n)
t=table(ID, x)
db=database("dfs://rangedb", RANGE,  0 5 10)
pt = db.createPartitionedTable(t, `pt, `ID)
pt.append!(t)

dropTable(db,`pt);
```

**相关信息**

* [truncate](../t/truncate.html "truncate")

