# getLocalIOTDBStaticTable

## 语法

`getLocalIOTDBStaticTable(dbUrl, tableName, [dfsPath])`

## 参数

**dbUrl** STRING 类型标量，表示分布式数据库的路径。

**tableName** STRING 类型标量，表示表名。

**dfsPath** STRING 类型标量，表示 chunk 的 DFS 路径。该参数可由 `getChunksMeta`
的返回值 dfsPath 列，去掉时间维度及之后内容获得，例如某 chunk 的 dfsPath 为
`/db/Key1/20250428/gP`，则该参数应设置为 `/db/Key1`
。默认返回当前节点该表的所有静态表。

## 详情

该函数仅支持对该表有 TABLE\_READ 权限或对该数据库有 DB\_READ 权限的用户在数据节点调用。

返回当前节点上点位管理引擎的静态表，包含以下字段：

* innerId: 测点对应的内部 ID。
* 测点列：列数和列名取决于 sort key，即建表时 sortColumns 中除时间列以外的其他列。如果这些列中存在名为 innerId 或
  valueType 的列，返回表中将自动重命名为 \_innerId\_ 和 \_valueType\_。
* valueType: 测点对应的 IOTANY 列的类型。

## 例子

```
getLocalIOTDBStaticTable(dbUrl="dfs://db", tableName="pt", dfsPath="/db/Key1")
```

| innerId | deviceId | location | valueType |
| --- | --- | --- | --- |
| 1 | 1 | loc2 | DOUBLE |
| 0 | 1 | loc1 | INT |

