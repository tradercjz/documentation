# getDFSDatabasesByOwner

## 语法

`getDFSDatabasesByOwner(user)`

## 参数

**user** STRING 类型标量，表示用户名。

## 详情

该函数仅限管理员用户执行，查询当前集群中所有由用户 *user* 创建的数据库。

## 例子

```
getDFSDatabasesByOwner(user="user1")
// output:["dfs://tsdb1","dfs://tsdb2"]
```

