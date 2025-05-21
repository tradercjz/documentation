# getTablesByCluster

## 语法

`getTablesByCluster(clusterName, dbUrl)`

## 参数

**clusterName** 字符串标量，表示要查询的集群名称。

**dbUrl** 字符串标量，表示要查询的数据库路径。

## 详情

获取集群指定数据库下的所有表。只能由管理员在 MoM（Master of Master，管理集群）上执行该函数。

**返回值**：字符串向量。

## 例子

```
// MoMSender 集群数据节点:
db = database(directory="dfs://db1", partitionType=RANGE, partitionScheme=0 5 10)
timestamp = [09:34:07,09:36:42,09:36:51,09:36:59,09:32:47,09:35:26,09:34:16,09:34:26,09:38:12]
sym = `C`MS`MS`MS`IBM`IBM`C`C`C
price= 49.6 29.46 29.52 30.02 174.97 175.23 50.76 50.32 51.29
qty = 2200 1900 2100 3200 6800 5400 1300 2500 8800
t = table(timestamp, sym, qty, price);
dt=db.createDimensionTable(t,`dt).append!(t);

// MoM 集群:
getTablesByCluster("MoMSender", "dfs://db1")
// Output:  ["dt"]
```

