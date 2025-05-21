# getTableSchemaByCluster

## 语法

`getTableSchemaByCluster(clusterName, dbUrl, table)`

## 参数

**clusterName** 字符串标量，表示要查询的集群名称。

**dburl** 字符串标量，表示要查询的数据库路径。

**table** 字符串标量，表示要查询的表名。

## 详情

获取指定表的 schema。只能由管理员在 MoM（Master of Master，管理集群）上执行该函数。

**返回值**：一个字典，与 `schema(table)` 的结果相同。

## 例子

```
getTableSchemaByCluster("MoMSender", "dfs://db1", "dt")

/* Output:
  colDefs->name      typeString typeInt extra comment
  --------- ---------- ------- ----- -------
timestamp SECOND     10
  sym       STRING     18
  qty       INT        4
  price     DOUBLE     16
  chunkPath->
  partitionColumnIndex->-1

*/
```

相关函数：[schema](../s/schema.md)

