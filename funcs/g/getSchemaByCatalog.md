# getSchemaByCatalog

## 语法

`getSchemaByCatalog(catalog)`

## 参数

**catalog** 字符串标量，表示 catalog 的名称。

## 详情

检索指定 catalog 中的所有 schema。返回一个 Table，包含 schema 的名称（schema）和对应路径（dbUrl）。

## 例子

```
getSchemaByCatalog("catalog1")
```

返回：

| schema | dbUrl |
| --- | --- |
| schema1 | dfs://db1 |
| schema2 | dfs://db2 |

