# createSchema

## 语法

`createSchema(catalog, dbUrl, schema)`

## 参数

**catalog** 字符串标量，表示 catalog 的名称。

**dbUrl** 字符串标量，表示数据库的路径。

**schema** 字符串标量，表示数据库对应的 schema 名称。

## 详情

把指定数据库添加到指定的 catalog 中。

由于数据库的 dbUrl 是全局唯一的，但不同 catalog 中的 schema 可以重名。因此需要先将数据库和 dbUrl 进行解耦。然后在将指定数据库添加到指定
catalog 时，需要为该数据库指定一个 schema 名称（类似该数据库的别名）。在后续 catalog 的相关操作中，都将使用该数据库的 schema 名称而非
dbUrl。

注意：不支持将数据库同时加到两个 catalog 中。

## 例子

```
createSchema("catalog1", "dfs://db1", "schema1")
```

