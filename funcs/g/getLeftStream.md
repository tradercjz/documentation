# getLeftStream

## 语法

`getLeftStream(joinEngine)`

## 参数

**joinEngine** 创建连接引擎返回的对象。目前 DolphinDB 支持的连接引擎有：

* createAsofJoinEngine
* createEquiJoinEngine
* createLookupJoinEngine
* createWindowJoinEngine
* createLeftSemiJoinEngine

## 详情

返回连接引擎左表的表结构对象。向该对象注入的数据，会注入到 *joinEngine* 中。

通过该函数，可以将一个引擎的计算结果直接注入到连接引擎中，实现引擎间的级联。

## 例子

```
share streamTable(1000:0, `time`sym`price, [TIMESTAMP, SYMBOL, DOUBLE]) as trades

output=table(100:0, `timestamp`sym`price1`price2, [TIMESTAMP, SYMBOL, DOUBLE, DOUBLE])

leftTable=table(1:0, `sym`timestamp`price, [SYMBOL, TIMESTAMP, DOUBLE])
rightTable=table(1:0, `sym`timestamp`price, [SYMBOL, TIMESTAMP, DOUBLE])

ajEngine = createAsofJoinEngine("asofjoin_engine", leftTable, rightTable, output, <[leftTable.price, rightTable.price]>, `sym, `timestamp)

leftEngine = createReactiveStateEngine(name=`left_reactive_engine, metrics=<[time,msum(price,3)]>, dummyTable=trades, outputTable=getLeftStream(ajEngine), keyColumn="sym")
rightEngine = createReactiveStateEngine(name=`right_reactive_engine, metrics=<[time,mfirst(price,3)]>, dummyTable=trades, outputTable=getRightStream(ajEngine), keyColumn="sym")

subscribeTable(, "trades", "left_reactive_engine", 0, append!{leftEngine}, true)
subscribeTable(, "trades", "right_reactive_engine", 0, append!{rightEngine}, true)

t = table(2022.01.01 + 1..20 as time, take(`AMZN`IBM`APPL, 20) as sym, rand(100.0, 20) as price)
trades.append!(t)
select * from output order by timestamp,sym
```

| timestamp | sym | price1 | price2 |
| --- | --- | --- | --- |
| 2022.01.02T00:00:00.000 | AMZN |  |  |
| 2022.01.03T00:00:00.000 | IBM |  |  |
| 2022.01.04T00:00:00.000 | APPL |  |  |
| 2022.01.05T00:00:00.000 | AMZN |  |  |
| 2022.01.06T00:00:00.000 | IBM |  |  |
| 2022.01.07T00:00:00.000 | APPL |  |  |
| 2022.01.08T00:00:00.000 | AMZN | 102.192 | 26.2273 |
| 2022.01.09T00:00:00.000 | IBM | 152.2704 | 43.6296 |
| 2022.01.10T00:00:00.000 | APPL | 126.1056 | 74.929 |
| 2022.01.11T00:00:00.000 | AMZN | 137.4656 | 57.6015 |
| 2022.01.12T00:00:00.000 | IBM | 116.7775 | 54.2854 |
| 2022.01.13T00:00:00.000 | APPL | 58.8909 | 49.3149 |
| 2022.01.14T00:00:00.000 | AMZN | 148.5405 | 18.3633 |
| 2022.01.15T00:00:00.000 | IBM | 141.0848 | 54.3554 |
| 2022.01.16T00:00:00.000 | APPL | 93.9003 | 1.8618 |
| 2022.01.17T00:00:00.000 | AMZN | 210.4329 | 61.5008 |
| 2022.01.18T00:00:00.000 | IBM | 88.7772 | 8.1367 |

相关函数：[getRightStream](getRightStream.html)。

