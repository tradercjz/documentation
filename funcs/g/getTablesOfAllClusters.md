# getTablesOfAllClusters

## 语法

`getTablesOfAllClusters()`

## 参数

无

## 详情

与 `getClusterDFSTables` 函数类似，但此函数能够获取当前用户在多个集群中拥有访问权限的所有表。

**返回值**：字符串向量。

## 例子

```
getTablesOfAllClusters()
// Output:   ["dfs://testDB/pt1", "trading.schema.pt@cluster3"]
```

