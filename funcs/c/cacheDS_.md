# cacheDS!

## 语法

`cacheDS!(ds)`

## 参数

**ds** 是数据源或数据源列表。

## 详情

函数 `cacheDS!` 会在下次执行，并缓存数据。它返回 true 或 false
表示此操作成功或失败。

## 例子

```
PTNDB_DIR = "/home/db_testing"
dbName = database(PTNDB_DIR + "/NYSETAQByName")
Trades = dbName.loadTable(`Trades)

ds=sqlDS(<select Time,Exchange,Symbol,Trade_Volume as Vol, Trade_Price as Price from Trades>)
ds.cacheDS!()        // cache the data
ds.clearDSCache!()  // clear the cache
```

