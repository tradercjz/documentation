# getDatabasesByCluster

## 语法

`getDatabasesByCluster(clusterName)`

## 参数

**clusterName** 字符串标量，表示要查询的集群名称。

## 详情

获取集群下所有数据库。只能由管理员在 MoM（Master of Master，管理集群）上执行该函数。

**返回值**：字符串向量

## 例子

```
getDatabasesByCluster("MoMSender")

// Output:   ["dfs://db2","dfs://db1"]
```

