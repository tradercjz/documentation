# renameSchema

## 语法

`renameSchema(catalog, oldSchema, newSchema)`

## 参数

**catalog** 字符串标量，表示 catalog 的名称。

**oldSchema** 字符串标量，表示要修改的 schema 的原名称。

**newSchema** 字符串标量，表示要修改的 schema 的新名称。

## 详情

重命名 schema。

## 例子

```
renameSchema("catalog1", "schema1", "schema2")
```

