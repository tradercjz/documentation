# clearDSCache!

## 语法

`clearDSCache!(ds)`

## 参数

**ds** 是数据源或数据源列表。

## 详情

`clearDSCache!` 函数指示系统在下次执行数据源之后清除缓存。

## 例子

```
PTNDB_DIR = "/home/db_testing"
dbName = database(PTNDB_DIR + "/NYSETAQByName")
Trades = dbName.loadTable(`Trades)

ds=sqlDS(<select Time,Exchange,Symbol,Trade_Volume as Vol, Trade_Price as Price from Trades>)
ds.cacheDS!()        // cache the data
ds.clearDSCache!()  // clear the cache
```

