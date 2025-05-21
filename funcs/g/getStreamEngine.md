# getStreamEngine

## 语法

`getStreamEngine(name)`

## 参数

**name** 是一个字符串，表示流数据引擎的名称。它可以包含字母，数字和下划线，但必须以字母开头。

## 详情

返回流数据引擎的句柄，可以作为 [subscribeTable](../s/subscribeTable.html) 函数的 *handler* 参数。

## 例子

```
share streamTable(1000:0, `time`sym`qty, [TIMESTAMP, SYMBOL, INT]) as trades
outputTable = table(10000:0, `time`sym`sumQty, [TIMESTAMP, SYMBOL, INT])
tradesAggregator = createTimeSeriesEngine("StreamAggregatorDemo",3, 3, <[sum(qty)]>, trades, outputTable, `time, false,`sym, 50)
subscribeTable(, "trades", "tradesAggregator", 0, append!{tradesAggregator}, true)

def writeData(n){
   timev = 2018.10.08T01:01:01.001 + timestamp(1..n)
   symv =take(`A`B, n)
   qtyv = take(1, n)
   insert into trades values(timev, symv, qtyv)
}

writeData(6);
h = getStreamEngine("StreamAggregatorDemo")
```

