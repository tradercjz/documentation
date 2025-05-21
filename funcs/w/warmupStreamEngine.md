# warmupStreamEngine

## 语法

`warmupStreamEngine(engine, msgs)`

## 参数

**engine** 是创建流数据引擎时返回的表对象。

**msgs** 是一个数据表。

## 详情

把数据写入流数据引擎，但是不输出结果。下一批次数据写入此流数据引擎，可以利用已计算的结果来加速计算。

目前仅支持响应式状态引擎，时间序列聚合引擎和日级时间序列引擎。

## 例子

```
trade=table(1000:0, `date`sym`price`volume, [DATE, SYMBOL, DOUBLE, INT])
n=3000*100
date=take(2021.03.08, n)
sym=take("A"+string(1..3000), n)
price=round(rand(100.0, n), 2)
volume=rand(100, n)
table1 = table(date, sym, price, volume)
outputTable = table(n:0, `sym`factor1, [STRING,DOUBLE])
engine = createReactiveStateEngine("test", <ema(volume, 40)>, table1, outputTable, "sym")
warmupStreamEngine(engine, table1)
date=take(2021.03.09, n)
sym=take("A"+string(1..3000), n)
price=round(rand(100.0, n), 2)
volume=rand(100, n)
table2 = table(date, sym, price, volume)
engine.append!(table2)
```

