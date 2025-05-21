# appendForJoin

## 语法

`appendForJoin(engine, isLeftTable, data)`

## 参数

**engine** 是流数据 join 引擎，即 [createAsofJoinEngine](../c/createAsofJoinEngine.html) 等函数返回的抽象表对象。目前支持以下 join 引擎:

* createAsofJoinEngine
* createEquiJoinEngine
* createLookupJoinEngine
* createWindowJoinEngine
* createLeftSemiJoinEngine

**isLeftTable** 布尔类型，插入左表还是右表。

**data** 将要插入表中的数据。

## 详情

将数据插入流数据 join 引擎中。

注： 使用订阅函数 [subscribeTable](../s/subscribeTable.html) 为流数据 join
引擎订阅数据时，*handler* 参数需要为 `appendForJoin`、[getLeftStream](../g/getLeftStream.html) 或 [getRightStream](../g/getRightStream.html) 函数。

## 例子

```
leftTable=table(1:0, `timestamp`sym`price, [TIMESTAMP, SYMBOL, DOUBLE])
rightTable=table(1:0, `timestamp`sym`val, [TIMESTAMP, SYMBOL, DOUBLE])
output=table(100:0, `timestamp`sym`price`val`total, [TIMESTAMP, SYMBOL, DOUBLE, DOUBLE, DOUBLE])
ajEngine=createAsofJoinEngine("test1", leftTable, rightTable, output, <[price, val, price*val]>, `sym, `timestamp, false, 7)

tmp1=table(take(2012.01.01T00:00:00.000+[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 20) as timestamp, take(`AAPL, 10) join take(`IBM, 10) as sym, double(1..20) as price)
tmp2=table(take(2012.01.01T00:00:00.000+[1, 2, 3, 4, 4, 4, 4, 4, 4, 4], 20) as timestamp, take(`AAPL, 10) join take(`IBM, 10) as sym, double(1..20) as val)

appendForJoin(ajEngine, true, (select * from tmp1 where timestamp=2012.01.01T00:00:00.001))
appendForJoin(ajEngine, false, (select * from tmp2 where timestamp=2012.01.01T00:00:00.001))
appendForJoin(ajEngine, true, (select * from tmp1 where timestamp=2012.01.01T00:00:00.002))
appendForJoin(ajEngine, false, (select * from tmp2 where timestamp=2012.01.01T00:00:00.002))
appendForJoin(ajEngine, true, (select * from tmp1 where timestamp=2012.01.01T00:00:00.003))
appendForJoin(ajEngine, false, (select * from tmp2 where timestamp=2012.01.01T00:00:00.003))
appendForJoin(ajEngine, true, (select * from tmp1 where timestamp=2012.01.01T00:00:00.004))
appendForJoin(ajEngine, false, (select * from tmp2 where timestamp=2012.01.01T00:00:00.004))
appendForJoin(ajEngine, true, (select * from tmp1 where timestamp=2012.01.01T00:00:00.005))
appendForJoin(ajEngine, true, (select * from tmp1 where timestamp=2012.01.01T00:00:00.006))
appendForJoin(ajEngine, true, (select * from tmp1 where timestamp=2012.01.01T00:00:00.007))
appendForJoin(ajEngine, true, (select * from tmp1 where timestamp=2012.01.01T00:00:00.008))
appendForJoin(ajEngine, true, (select * from tmp1 where timestamp=2012.01.01T00:00:00.009))
appendForJoin(ajEngine, true, (select * from tmp1 where timestamp=2012.01.01T00:00:00.010))

sleep(5000)
```

