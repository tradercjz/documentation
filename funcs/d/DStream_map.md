# DStream::map

## 语法

`DStream::map(func)`

## 参数

**func** 一元函数，入参为流数据消息组成的表。函数返回一个表，后续引擎根据返回的表结构推导处理逻辑。该函数必须是纯函数，不能包含写入外部表等副作用。

## 详情

对流中的数据做映射，将指定函数应用到流数据中的每条消息。

**返回值**：DStream 对象。

## 例子

定义 `map` 合成 AAPL 标的 K 线：

```
use catalog test

g = createStreamGraph("graph")
g.source("trade", 1024:0, `symbol`datetime`price`volume, [SYMBOL,TIMESTAMP,DOUBLE,INT])
    .map(msg -> select * from msg where symbol == "AAPL")
    .timeSeriesEngine(60, 60, <[first(price) as open, max(price) as high, min(price) as low, last(price) as close, sum(volume) as volume]>, "datetime", false, "symbol")
    .sink("output")
```

