# createEquiJoinEngine

## 语法

`createEquiJoinEngine(name, leftTable, rightTable,
outputTable, metrics, matchingColumn, timeColumn, [garbageSize=5000],
[maxDelayedTime], [snapshotDir],
[snapshotIntervalInMsgCount])`

别名：createEqualJoinEngine

## 详情

创建流数据等值连接引擎。返回一个左、右两表 equi join 后的表对象。注入等值连接引擎的左、右两表将以
*matchingColumn* + *timeColumn* 作为连接列，返回两表中连接字段相等的行。

更多流数据引擎的应用场景说明可以参考 [内置多数据源流式关联引擎](../../stream/str_join_engine.html)。

## 计算规则

* 每次数据注入引擎左表时，会在右表中查找与连接列字段相匹配的记录，若找到，则将两表匹配的记录 join 后，根据
  *metrics* 给出的因子进行计算并输出。
* 每次数据注入引擎右表时，亦会做同样操作。

## 参数

equi join 引擎的部分参数和 asof join 引擎相同，请参照 [createAsofJoinEngine](createAsofJoinEngine.html) 中参数介绍。下面介绍不同的参数：

**name** 字符串标量，表示 equi join 引擎的名称，作为其在一个数据节点/计算节点上的唯一标识。可包含字母，数字和下划线，但必须以字母开头。

**timeColumn** 字符串标量或向量。用于指定 *leftTable* 和
*rightTable* 中时间列的名称。两表的时间列名称可以不同，但数据类型需保持一致。当 *leftTable* 和
*rightTable* 时间列名称相同时，*timeColumn* 是字符串标量，否则，*timeColumn*
是长度为2的字符串向量。

**garbageSize** 可选参数，正整数，默认值是 5,000（单位为行）。当内存中历史数据行数超过
*garbageSize* 时，会清理本次计算不需要的历史数据。

满足以下条件的数据才会被清理：

1. 历史数据中已经 join 并输出的数据；
2. 历史数据未发生 join 的数据，但其时间戳与 *leftTable* 或 *rightTable* 收到的最新数据的时间戳的差值大于
   *maxDelayedTime*。

**maxDelayedTime** 可选参数，正整数，单位同 *timeColumn* 精度一致，默认值为 3
秒。该参数仅在达到 *garbageSize* 清理条件时才会起效，表示引擎内能够保留最新多长时间的数据。详情参考上述清理条件 2。不建议设置
*maxDelayedTime* 值设置过小，否则可能导致一些需关联却没及时关联的数据被清理。

## 例子

```
share streamTable(1:0, `time`sym`price, [SECOND, SYMBOL, DOUBLE]) as leftTable
share streamTable(1:0, `time`sym`val, [SECOND, SYMBOL, DOUBLE]) as rightTable
share table(100:0, `time`sym`price`val`total, [SECOND, SYMBOL, DOUBLE, DOUBLE, DOUBLE]) as output
ejEngine=createEquiJoinEngine("test1", leftTable, rightTable, output, [<price>, <val>, <price*val>], `sym, `time)
subscribeTable(tableName="leftTable", actionName="joinLeft", offset=0, handler=appendForJoin{ejEngine, true}, msgAsTable=true)
subscribeTable(tableName="rightTable", actionName="joinRight", offset=0, handler=appendForJoin{ejEngine, false}, msgAsTable=true)

tmp1=table(13:30:10+1..20 as time, take(`AAPL, 10) join take(`IBM, 10) as sym, double(1..20) as price)
leftTable.append!(tmp1)
tmp2=table(13:30:10+1..20 as time, take(`AAPL, 10) join take(`IBM, 10) as sym, double(50..31) as val)
rightTable.append!(tmp2)
```

下例中时间列类型为 TIMESTAMP，若不设置 *maxDelayedTime*，取默认值3000ms(3s)。

```
share streamTable(5000000:0, `timestamp`sym`price, [TIMESTAMP, SYMBOL, DOUBLE]) as leftTable
share streamTable(5000000:0, `timestamp`sym`val, [TIMESTAMP, SYMBOL, DOUBLE]) as rightTable
share table(5000000:0, `timestamp`sym`price`val`total`diff`ratio, [TIMESTAMP, SYMBOL, DOUBLE, DOUBLE, DOUBLE, DOUBLE, DOUBLE]) as output
ejEngine=createEquiJoinEngine("test1", leftTable, rightTable, output, <[price, val, price+val, price-val, price/val]>, `sym, `timestamp, 5000)
topic1=subscribeTable(tableName="leftTable", actionName="writeLeft", offset=0, handler=appendForJoin{ejEngine, true}, batchSize=10000, throttle=1)
topic2=subscribeTable(tableName="rightTable", actionName="writeRight", offset=0, handler=appendForJoin{ejEngine, false}, batchSize=10000, throttle=1)
def writeLeftTable(mutable tb){
   batch = 1000
   for(i in 1..300){
           tmp = table(batch:batch, `timestamp`sym`price, [TIMESTAMP, SYMBOL, DOUBLE])
           tmp[`timestamp]=take(2012.01.01T00:00:00.000+i, batch)
           tmp[`sym]=shuffle("A"+string(1..batch))
           tmp[`price]=rand(100.0, batch)
           tb.append!(tmp)
   }
}

def writeRightTable(mutable tb){
   batch = 500
   for(i in 1..200){
           tmp = table(batch:batch, `timestamp`sym`val, [TIMESTAMP, SYMBOL, DOUBLE])
           tmp[`timestamp]=take(2012.01.01T00:00:00.000+i, batch)
           tmp[`sym]=shuffle("A"+string(1..batch))
           tmp[`val]=rand(100.0, batch)
           tb.append!(tmp)
   }
}

job1 = submitJob("writeLeft", "", writeLeftTable, leftTable)
job2 = submitJob("writeRight", "", writeRightTable, rightTable)

select count(*) from output order by sym, timestamp
// output: 100000
```

