# appendMsg

## 语法

`appendMsg(engine, msgBody, msgId)`

## 参数

**engine** 是内置流数据引擎，即 [createReactiveStateEngine](../c/createReactiveStateEngine.html) 等函数返回的抽象表对象。

**msgBody** 是将要写入流数据引擎的消息。

**msgId** 是写入数据之前，流数据引擎已接收到的最后一条消息的 ID。ID 从订阅发布的第一条消息开始计数。

## 详情

当流数据引擎启用快照机制（snapshot）且未开启 RaftGroup 时，订阅函数 [subscribeTable](../s/subscribeTable.html) 的handler参数必须为
`appendMsg` 函数，将数据写入流数据引擎。

## 例子

```
share streamTable(10000:0,`time`sym`price, [TIMESTAMP,SYMBOL,DOUBLE]) as trades
output1 =table(10000:0, `time`sym`avgPrice, [TIMESTAMP,SYMBOL,DOUBLE]);

engine1 = createTimeSeriesEngine(name=`engine1, windowSize=100, step=50, metrics=<avg(price)>, dummyTable=trades, outputTable=output1, timeColumn=`time, keyColumn=`sym, snapshotDir="C:/DolphinDB/Data/snapshotDir", snapshotIntervalInMsgCount=100)
subscribeTable(tableName="trades", actionName="engine1", offset=0, handler=appendMsg{engine1}, msgAsTable=true, handlerNeedMsgId=true)

n=500
timev=2021.03.12T15:00:00.000 + (1..n join 1..n)
symv = take(`A, n) join take(`B, n)
pricev = (100+cumsum(rand(1.0,n)-0.5)) join (200+cumsum(rand(1.0,n)-0.5))
t=table(timev as time, symv as sym, pricev as price).sortBy!(`time)
trades.append!(t)

select * from output1
```

