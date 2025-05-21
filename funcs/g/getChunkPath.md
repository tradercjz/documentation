# getChunkPath

## 语法

`getChunkPath(ds)`

## 参数

**ds** 是一个或多个数据源。

## 详情

返回指定数据源代表数据块的路径。

## 例子

```
if(existsDatabase("dfs://valuedb")){
  dropDatabase("dfs://valuedb")
}

db=database("dfs://valuedb", VALUE, 1..10)
n=1000000
t=table(rand(1..10, n) as id, rand(100.0, n) as val)
pt=db.createPartitionedTable(t, `pt, `id).append!(t);
ds=sqlDS(<select * from pt where id in 1..3>)
getChunkPath(ds);

// output
["/valuedb/1/p","/valuedb/2/p","/valuedb/3/p"]
```

