# cacheDSNow

## 语法

`cacheDSNow(ds)`

## 参数

**ds** 是数据源或数据源列表。

## 详情

函数 `cacheDSNow` 立即执行并缓存数据源和缓存行的总数。

## 例子

```
PTNDB_DIR = "/home/db_testing"
dbName = database(PTNDB_DIR + "/NYSETAQByName")
Trades = dbName.loadTable(`Trades)

ds=sqlDS(<select Time,Exchange,Symbol,Trade_Volume as Vol, Trade_Price as Price from Trades>)
ds.cacheDSNow()        # cache the data immediately
ds.clearDSCacheNow()  # clear the cache immediately
```

