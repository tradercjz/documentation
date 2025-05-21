# createLookupJoinEngine

## 语法

`createLookupJoinEngine(name, leftTable, rightTable,
outputTable, metrics, matchingColumn, [rightTimeColumn], [checkTimes],
[outputElapsedMicroseconds=false], [keepDuplicates=false], [isInnerJoin], [snapshotDir],
[snapshotIntervalInMsgCount])`

## 详情

创建流数据表的 lookup join 引擎，该引擎以 *matchingColumn*作为连接列，将左表（必须为流数据表）与右表进行左连接或内连接。lookup join
引擎常用于右表更新不频繁的场景（如保存了日频指标的维度表）。若右表为非流数据表，则需设置定时刷新该表数据。

### 工作机制

1. 仅当左表有新数据流入时才会触发计算。
2. 当 *keepDuplicates* = false 时，引擎仅保留右表在基于 *matchingColumn*
   分组后每组的最新一条数据。此时：
   * 默认连接方式为左连接，即 *isInnerJoin* =
     false。每次数据注入左表时，无论右表中是否有匹配的记录，都会计算指标并输出（如果右表没有匹配记录，则输出空值）。
   * 用户可以通过将 *isInnerJoin* 设置为 true 来将连接方式改为内连接。

   当 *keepDuplicates* = true 时，引擎保留右表在基于 *matchingColumn*
   分组后每组的所有数据。此时，连接方式只能是内连接，即每次数据注入左表时，系统会在右表中查找与连接列匹配的记录，只有匹配成功才会计算指标并输出，否则不进行计算和输出。
3. 当右表是订阅的流数据表时，数据流入右表的同时会更新数据； 若右表为内存表、维度表或元代码，系统会根据 *checkTimes*
   定时刷新右表数据。

lookup join 引擎与 asof join, semi lookup join, snapshot join 引擎的比较：

|  |  |
| --- | --- |
| asof join 引擎 | * lookup join 引擎输出表的第一列可以不是时间列，而 asof join   引擎输出表第一列必须是时间列。 * lookup join 引擎当左表有新数据流入便会触发连接计算，因此无需考虑数据延迟，也无需缓存左表数据。而   asof join 引擎，当指定 *timeColumn* 时，需要考虑左右表的数据延时。 |
| left semi join 引擎 | lookup join 引擎和 left semi join 引擎都由左表的新记录触发连接计算，当引擎根据连接列匹配上右表中的记录时，引擎将输出结果。  lookup join 引擎对于左表中未在右表中成功匹配的记录，根据参数设置或直接输出、或不输出结果；left semi join 引擎对于左表中未成功匹配的记录将进行缓存，等待与右表中更新的记录匹配后输出。  left semi join 引擎在缓存右表的记录时，对于相同连接列的数据总是只保留第一条或者最新一条，因此对于左表的每一条记录至多只会匹配一条右表记录并输出一条记录。在lookup join engine中，对于相同连接列的数据用户可选择保留全部记录，因此存在左表的每一条记录匹配到右表多条记录、输出多条记录的情况。 |
| snapshot join 引擎 | lookup join 引擎只能由左表的新记录触发连接；而 snapshot join 引擎可以由左表或右表的新记录触发连接。 |

更多流数据引擎的应用场景说明可以参考 [流计算引擎](../themes/streamingEngine.html)。

## 参数

**name** 必选参数，表示流数据 lookup join
引擎的名称，作为其在一个数据节点/计算节点上的唯一标识。可包含字母，数字和下划线，但必须以字母开头。

**leftTable**
*可选参数*, 表对象。可以不包含数据，但结构必须与订阅的流数据表相同。

**rightTable***可选参数*, 表对象，可以是内存表、流数据表、维度表或 SQL 查询元代码（查询语句必须返回表 ）。请注意，如果
*rightTable* 没有被订阅，但 *rightTable* 会定期更新，则必须设置 *checkTimes*
来定时刷新右表数据。

**outputTable** 必选参数，为计算结果的输出表。在使用 `createLookupJoinEngine`
函数之前，需要将输出表预先设立为一个空表，并指定各列列名以及数据类型。

输出表的各列的顺序如下：

1. 连接列。与 *matchingColumn* 中的列以及其顺序一致，可为多列。
2. 计算结果列。可为多列。
3. 耗时列。如果指定 *outputElapsedMicroseconds* = true，则指定一个 LONG
   类型的列用于记录单次响应计算耗时（单位：微秒）。
4. batchSize 列。如果指定 *outputElapsedMicroseconds* = true,
   则指定一个INT类型的列，记录单次响应的数据条数。

**metrics**
*可选参数*, 以元代码的格式表示计算指标，支持输入元组。有关元代码的更多信息可参考 [Metaprogramming](../../progr/objs/meta_progr.html)。

* 计算指标可以是一个或多个表达式、系统内置或用户自定义函数、一个常量标量/向量，但不能是聚合函数。当指定为常量向量时，对应的输出列必须设置为数组向量类型，例子参见
  [createReactiveStateEngine](createReactiveStateEngine.html) 中的例4。
* *metrics* 内支持调用具有多个返回值的函数，且必须指定列名，例如 <func(price) as
  `col1`col2>。
* 若在 *metrics* 指定了 *leftTable* 和 *rightTable*
  中具有相同名称的列，默认取左表的列，可以通过 "tableName.colName" 指定该列来自哪个表。

  注： *metrics* 中使用的列名大小写不敏感，不需要与输入表的列名大小写保持一致。

**matchingColumn**
*可选参数*, 表示连接列的字符串标量/向量或字符串向量组成的 tuple，支持 Integral, Temporal 或 Literal(UUID
除外)类型。*matchingColumn* 指定规则：

1. 只有一个连接列。当左表和右表的连接列名相同时，*matchingColumn* 是一个字符串标量，否则是一个长度为 2 的
   tuple。例如：左表连接列名为 sym，右表连接列名为 sym1，则 *matchingColumn* =
   [[`sym],[`sym1]]。
2. 有多个连接列。当左表和右表的连接列名相同时，*matchingColumn* 是一个字符串向量，否则是一个长度为 2 的
   tuple。例如：左表连接列名为 timestamp, sym，右表连接列名为 timestamp, sym1，则
   *matchingColumn* = [[`timestamp, `sym], [`timestamp,`sym1]]。

**rightTimeColumn**
*可选参数*,
是字符串标量，表示右表的时间列名称。若设置该参数，右表会根据指定的时间列的时间戳保留最新的数据（若有多行，则取其中最后一行）。若不指定该参数，则根据数据注入系统的时间保留最新数据。

**checkTimes**
*可选参数*, 是一个时间类型向量或 DURATION 的标量。设置后，系统会定时更新 *rightTable* 的数据（只保留
*rightTable* 的最新数据），并将更新后的数据追加到引擎中。当无需更新 *rightTable*
时，则不用设置该参数，但需要在引擎创建后，手动将 *rightTable* 注入到引擎中。

* *checkTimes* 是时间类型向量时，只能为SECOND、TIME 或 NANOTIME 类型。 lookup join
  引擎每天根据向量内各元素指定的时间定时更新右表。
* *checkTimes* 是 DURATION 标量时，表示更新右表的时间间隔。

**outputElapsedMicroseconds**
*可选参数*, 布尔值，表示是否输出单次响应计算的耗时（从触发计算的数据注入引擎到计算完成的耗时），默认为 false。指定参数
*outputElapsedMicroseconds* 后，在定义 outputTable 时需要在计算结果列后增加一个 LONG 类型的列和 INT
类型的列，详见 *outputTable* 参数说明。

**keepDuplicates**
*可选参数*, 布尔值，表示是否保留右表各分组内的所有数据。默认值为 false，即在关联时只取右表各分组内的最新一条数据。当设置为 true
时，在关联时则使用右表各分组内的所有数据，此时的连接类型为内连接，即只有左右两表匹配的记录被计算输出。

**isInnerJoin：**布尔值，可选参数，表示是否进行内连接。该参数只在 *keepDuplicates* 为 false
时可进行配置。该参数默认值为 false，即进行左连接，无论在右表中是否找到匹配的记录，都会输出结果（右表未匹配的记录输出空值）。设置为 true
时左右两表进行内连接。

若要开启快照机制 (snapshot)，必须指定 *snapshotDir* 与
*snapshotIntervalInMsgCount*。

**snapshotDir** 可选参数，字符串，表示保存引擎快照的文件目录。

* 指定的目录必须存在，否则系统会提示异常。
* 创建流数据引擎时，如果指定了 *snapshotDir*，会检查该目录下是否存在快照。如果存在，会加载该快照，恢复引擎的状态。
* 多个引擎可以指定同一个目录存储快照，用引擎的名称来区分快照文件。
* 一个引擎的快照可能会使用三个文件名：
* 临时存储快照信息：文件名为 <engineName>.tmp；
* 快照生成并刷到磁盘：文件保存为 <engineName>.snapshot；
* 存在同名快照：旧快照自动重命名为 <engineName>.old。

**snapshotIntervalInMsgCount**
可选参数，为整数类型，表示每隔多少条数据保存一次流数据引擎快照。

## 例子

例1.

```
login(`admin, `123456)
share streamTable(1000:0, `timestamps`sym`price, [TIMESTAMP, SYMBOL, DOUBLE]) as trades
share streamTable(1000:0, `timestamps`sym`val`id, [TIMESTAMP, SYMBOL, DOUBLE, INT]) as prices
share table(100:0, `sym`factor1`factor2`factor3, [SYMBOL, DOUBLE, DOUBLE, DOUBLE]) as output

LjEngine = createLookupJoinEngine(name="test1", leftTable=trades, rightTable=prices, outputTable=output, metrics=<[price,val,price*val]>, matchingColumn=`sym)
subscribeTable(tableName="trades", actionName="append_leftTable", offset=0, handler=appendForJoin{LjEngine, true}, msgAsTable=true)
subscribeTable(tableName="prices", actionName="append_rightTable", offset=0, handler=appendForJoin{LjEngine, false}, msgAsTable=true)

n = 15
tem1 = table( (2018.10.08T01:01:01.001 + 1..12) join (2018.10.08T01:01:01.001 + 1..3)as timestamps,take(`A`B`C, n) as sym,take(1..15,n) as val,1..15 as id)
prices.append!(tem1)
sleep(2000)
n  = 10
tem2 = table( 2019.10.08T01:01:01.001 + 1..n as timestamps,take(`A`B`C, n) as sym,take(0.1+10..20,n) as price)
trades.append!(tem2)
sleep(100)
select * from output
```

| sym | factor1 | factor2 | factor3 |
| --- | --- | --- | --- |
| A | 10.1 | 13 | 131.3 |
| B | 11.1 | 14 | 155.4 |
| C | 12.1 | 15 | 181.5 |
| A | 13.1 | 13 | 170.3 |
| B | 14.1 | 14 | 197.4 |
| C | 15.1 | 15 | 226.5 |
| A | 16.1 | 13 | 209.3 |
| B | 17.1 | 14 | 239.4 |
| C | 8.1 | 15 | 271.5 |
| A | 19.1 | 13 | 248.3 |

例2.

```
share streamTable(1000:0, `timestamps`sym`price, [TIMESTAMP, SYMBOL, DOUBLE]) as trades
share streamTable(1000:0, `timestamps`sym`val`id, [TIMESTAMP, SYMBOL, DOUBLE, INT]) as prices
share table(100:0, `sym`factor1`factor2`factor3, [SYMBOL, DOUBLE, DOUBLE, DOUBLE]) as output
LjEngine = createLookupJoinEngine(name="test1", leftTable=trades, rightTable=prices, outputTable=output, metrics=<[price,val,price*val]>, matchingColumn=`sym, rightTimeColumn=`timestamps)
subscribeTable(tableName="trades", actionName="append_leftTable", offset=0, handler=appendForJoin{LjEngine, true}, msgAsTable=true)
subscribeTable(tableName="prices", actionName="append_rightTable", offset=0, handler=appendForJoin{LjEngine, false}, msgAsTable=true)

n = 15
tem1 = table( (2018.10.08T01:01:01.001 + 1..12) join (2018.10.08T01:01:01.001 + 1..3)as timestamps,take(`A`B`C, n) as sym,take(1..15,n) as val,1..15 as id)
prices.append!(tem1)
sleep(2000)
n  = 10
tem2 = table( 2019.10.08T01:01:01.001 + 1..n as timestamps,take(`A`B`C, n) as sym,take(0.1+10..20,n) as price)
trades.append!(tem2)
sleep(100)
select * from output
```

| sym | factor1 | factor2 | factor3 |
| --- | --- | --- | --- |
| A | 10.1 | 10 | 101 |
| B | 11.1 | 11 | 122.1 |
| C | 12.1 | 12 | 145.2 |
| A | 13.1 | 10 | 131 |
| B | 14.1 | 11 | 155.1 |
| C | 15.1 | 12 | 181.2 |
| A | 16.1 | 10 | 161 |
| B | 17.1 | 11 | 188.1 |
| C | 18.1 | 12 | 217.2 |
| A | 19.1 | 10 | 191 |

例3. 右表是内存表，需设置 *checkTimes*

```
share streamTable(1000:0, `timestamps`sym`price, [TIMESTAMP, SYMBOL, DOUBLE]) as trades
share table(100:0, `sym`factor1`factor2`factor3, [SYMBOL, DOUBLE, DOUBLE, DOUBLE]) as output
share table(1000:0, `timestamps`sym`val`id, [TIMESTAMP, SYMBOL, DOUBLE, INT]) as prices
LjEngine = createLookupJoinEngine(name="test1", leftTable=trades, rightTable=prices, outputTable=output, metrics=<[price,val,price*val]>, matchingColumn=`sym, rightTimeColumn=`timestamps, checkTimes=1s)
subscribeTable(tableName="trades", actionName="append_leftTable", offset=0, handler=appendForJoin{LjEngine, true}, msgAsTable=true)

n = 15
tem1 = table( (2018.10.08T01:01:01.001 + 1..12) join (2018.10.08T01:01:01.001 + 1..3)as timestamps,take(`A`B`C, n) as sym,take(1..15,n) as val,1..15 as id)
prices.append!(tem1)
sleep(2000)
n  = 10
tem2 = table( 2019.10.08T01:01:01.001 + 1..n as timestamps,take(`A`B`C, n) as sym,take(0.1+10..20,n) as price)
trades.append!(tem2)
sleep(100)
select * from output
```

| sym | factor1 | factor2 | factor3 |
| --- | --- | --- | --- |
| A | 10.1 | 10 | 101 |
| B | 11.1 | 11 | 122.1 |
| C | 12.1 | 12 | 145.2 |
| A | 13.1 | 10 | 131 |
| B | 14.1 | 11 | 155.1 |
| C | 15.1 | 12 | 181.2 |
| A | 16.1 | 10 | 161 |
| B | 17.1 | 11 | 188.1 |
| C | 18.1 | 12 | 217.2 |
| A | 19.1 | 10 | 191 |

例4. 左表为一个实时的交易表与右表（相对稳定的维度表）做连接。

```
share streamTable(1000:0, `time`volume`id, [TIMESTAMP, INT,INT]) as trades
dbPath="dfs://testlj"
if(existsDatabase(dbPath)){
   dropDatabase(dbPath)
}
rt=table(1000:0, `time`price`id, [TIMESTAMP, DOUBLE, INT])
db=database(dbPath, VALUE, `A`B`C)
prices=db.createTable(rt,`rightTable)
share table(10000:0, `id`volume`price`prod, [INT,INT,DOUBLE,DOUBLE]) as outputTable

tradesLookupJoin = createLookupJoinEngine(name="streamLookup1", leftTable=trades, rightTable=prices, outputTable=outputTable, metrics=<[volume,price,volume*price]>, matchingColumn=`id, rightTimeColumn=`time,checkTimes=1s)
subscribeTable(tableName="trades", actionName="append_trades", offset=0, handler=appendForJoin{tradesLookupJoin, true}, msgAsTable=true)

def writeData(t,n){
    timev = 2021.10.08T01:01:01.001 + timestamp(1..n)
    volumev = take(1..n, n)
    id = take(1 2 3, n)
    insert into t values(timev, volumev, id)
}
writeData(rt, 10)
prices.append!(rt)
sleep(2000)
writeData(trades, 6)
sleep(2)

select * from outputTable
```

| id | volume | price | prod |
| --- | --- | --- | --- |
| 1 | 1 | 10 | 10 |
| 2 | 2 | 8 | 16 |
| 3 | 3 | 9 | 27 |
| 1 | 4 | 10 | 40 |
| 2 | 5 | 8 | 40 |
| 3 | 6 | 9 | 54 |

例5. 通过 *rightTable* 可以对分布式分区表中的字段进行关联，此时 *rightTable* 是一个 SQL 查询元代码：

```
share streamTable(1000:0, `time`volume`id, [TIMESTAMP, INT,INT]) as trades
dbPath="dfs://lookupjoinDB"
if(existsDatabase(dbPath)){
   dropDatabase(dbPath)
}
rt=table(1000:0, `time`price`id, [TIMESTAMP, DOUBLE, INT])
db=database(dbPath, HASH, [INT,5])
prices=db.createPartitionedTable(rt,`rightTable, `id)
share table(10000:0, `id`volume`price`prod, [INT,INT,DOUBLE,DOUBLE]) as outputTable

tradesLookupJoin = createLookupJoinEngine(name="streamLookup1", leftTable=trades, rightTable=<select * from loadTable(dbPath, `rightTable)>, outputTable=outputTable, metrics=<[volume,price,volume*price]>, matchingColumn=`id, rightTimeColumn=`time,checkTimes=1s)
subscribeTable(tableName="trades", actionName="append_trades", offset=0, handler=appendForJoin{tradesLookupJoin, true}, msgAsTable=true)

def writeData(t,n){
    timev = 2021.10.08T01:01:01.001 + timestamp(1..n)
    volumev = take(1..n, n)
    id = take(1 2 3, n)
    insert into t values(timev, volumev, id)
}
writeData(rt, 10)
prices.append!(rt)
sleep(2000)
writeData(trades, 6)
sleep(2)

select * from outputTable
```

| id | volume | price | prod |
| --- | --- | --- | --- |
| 1 | 1 | 10 | 10 |
| 2 | 2 | 8 | 16 |
| 3 | 3 | 9 | 27 |
| 1 | 4 | 10 | 40 |
| 2 | 5 | 8 | 40 |
| 3 | 6 | 9 | 54 |

例6. 设置 *isInnerJoin* 为 true，当在右表中没有匹配的记录时不输出结果。

```
login(`admin, `123456)
share streamTable(1000:0, `timestamps`sym`price, [TIMESTAMP, SYMBOL, DOUBLE]) as trades
share streamTable(1000:0, `timestamps`sym`val`id, [TIMESTAMP, SYMBOL, DOUBLE, INT]) as prices
share table(100:0, `sym`factor1`factor2`factor3, [SYMBOL, DOUBLE, DOUBLE, DOUBLE]) as output

LjEngine = createLookupJoinEngine(name="test1", leftTable=trades, rightTable=prices, outputTable=output, metrics=<[price,val,price*val]>, matchingColumn=`sym, isInnerJoin=true)

n = 15
tem1 = table( (2018.10.08T01:01:01.001 + 1..12) join (2018.10.08T01:01:01.001 + 1..3)as timestamps,take(`A`B`C, n) as sym,take(1..15,n) as val,1..15 as id)
appendForJoin(LjEngine, false,tem1)
sleep(2000)

// 左表中存在 2 条右表中无匹配的记录
n  = 10
tem2 = table( 2019.10.08T01:01:01.001 + 1..n as timestamps,take(`A`B`C`d, n) as sym,take(0.1+10..20,n) as price)
appendForJoin(LjEngine, true,tem2)
sleep(100)
select count(*) from output // 8
```

| sym | factor1 | factor2 | factor3 |
| --- | --- | --- | --- |
| A | 10.1 | 13 | 131.3 |
| B | 11.1 | 14 | 155.4 |
| C | 12.1 | 15 | 181.5 |
| A | 14.1 | 13 | 183.3 |
| B | 15.1 | 14 | 211.4 |
| C | 16.1 | 15 | 241.5 |
| A | 18.1 | 13 | 235.3 |
| B | 19.1 | 14 | 267.4 |

