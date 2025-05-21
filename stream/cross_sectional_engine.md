# 横截面引擎

横截面引擎适用于对截面数据（如每只股票代码最新时间戳下的数据）进行实时计算。如：金融场景下，使用某个指数的所有成分股的最新价格计算该指数的内在价值；工业物联网场景下，对某批设备最新温度求最值等等。

横截面引擎包含两个部分：

* 横截面数据表（键值表）：保存所有分组的最新记录
* 计算引擎：包含一组聚合计算表达式以及触发器，系统会根据指定规则触发对横截面数据表的计算，计算结果将保存到指定的数据表中。

横截面引擎由 `createCrossSectionalEngine` 函数创建。语法如下：

`createCrossSectionalEngine(name, [metrics], dummyTable,
[outputTable], keyColumn, [triggeringPattern='perBatch'],
[triggeringInterval=1000], [useSystemTime=true], [timeColumn],
[lastBatchOnly=false], [contextByColumn], [snapshotDir],
[snapshotIntervalInMsgCount], [raftGroup], [outputElapsedMicroseconds=false],
[roundTime=true], [keyFilter], [updatedContextGroupsOnly=false])`

其参数的详细含义可以参考：[createCrossSectionalEngine](../funcs/c/createCrossSectionalEngine.md)

## 应用示例

触发横截面引擎的计算方式非常灵活，只需在创建引擎时指定相应参数即可。本节将重点介绍横截面引擎在不同触发模式下的示例。

注：

每次执行示例之前，建议先清理环境（取消订阅、取消横截面引擎，并删除数据表）。清理环境的代码示例如下：

```
unsubscribeTable(,`trades, "tradesCrossAggregator")
dropStreamEngine("CrossSectionalDemo")
undef(`trades, SHARED)
```

**例1. 每行触发计算的方式**

股市的交易数据会实时以流数据的形式写入数据表 *trades*。该表通常具有这些列：股票代码(sym)、
时间（time）、成交价（price）、成交数（qty）。以下步骤将使用横截面引擎结合流数据订阅，实时计算如下指标：所有股票的最新成交量之最大值、最新成交金额之最大值，以及最新交易金额之和。

定义流数据表，以写入模拟交易数据。

```
share streamTable(10:0,`time`sym`price`qty,[TIMESTAMP,SYMBOL,DOUBLE,INT]) as trades
```

定义结果表，以保存横截面引擎计算的结果。

```
outputTable = table(10:0, `time`maxQty`maxDollarVolume`sumDollarVolume, [TIMESTAMP,INT,DOUBLE,DOUBLE])
```

创建横截面引擎，指定表达式、输入表、结果表、分组列、计算频率。返回的对象 tradesCrossAggregator 为保存横截面数据的表。

```
tradesCrossAggregator=createCrossSectionalEngine(name="CrossSectionalDemo", metrics=<[max(qty), max(price*qty), sum(price*qty)]>, dummyTable=trades, outputTable=outputTable, keyColumn=`sym, triggeringPattern=`perRow, useSystemTime=false, timeColumn=`time)
```

订阅流数据表，将新写入的流数据追加到横截面引擎中。

```
subscribeTable(tableName="trades", actionName="tradesCrossAggregator", offset=-1, handler=append!{tradesCrossAggregator}, msgAsTable=true)
```

模拟生成实时交易流数据。

```
def writeData(n){
   timev  = 2000.10.08T01:01:01.001 + timestamp(1..n)
   symv   = take(`A`B, n)
   pricev = take(102.1 33.4 73.6 223,n)
   qtyv   = take(60 74 82 59, n)
   insert into trades values(timev, symv, pricev, qtyv)
}
writeData(4)
```

查询流数据表，共有 A 与 B 两只股票的 4 笔交易数据：

```
select * from trades
```

| time | sym | price | qty |
| --- | --- | --- | --- |
| 2000.10.08T01:01:01.002 | A | 102.1 | 60 |
| 2000.10.08T01:01:01.003 | B | 33.4 | 74 |
| 2000.10.08T01:01:01.004 | A | 73.6 | 82 |
| 2000.10.08T01:01:01.005 | B | 223 | 59 |

截面数据表保存了 A 与 B 两只股票最新的交易数据：

```
select * from tradesCrossAggregator
```

| time | sym | price | qty |
| --- | --- | --- | --- |
| 2000.10.08T01:01:01.004 | A | 73.6 | 82 |
| 2000.10.08T01:01:01.005 | B | 223 | 59 |

横截面引擎采用了每行触发计算的方式（*triggeringPattern*="perRow"
），因此每向横截面表写入一行数据，横截面引擎都会进行一次计算，并向结果表插入一条结果数据：

```
select * from outputTable
```

| time | maxQty | maxDollarVolume | sumDollarVolume |
| --- | --- | --- | --- |
| 2019.04.08T04:26:01.634 | 60 | 6126 | 6126 |
| 2019.04.08T04:26:01.634 | 74 | 6126 | 8597.6 |
| 2019.04.08T04:26:01.634 | 82 | 6035.2 | 8506.8 |
| 2019.04.08T04:26:01.634 | 82 | 13157 | 19192.2 |

**例2. 每写入一批数据触发一次计算**

*riggeringPattern* 取值为 "perBatch" 时，表示每追加一批数据触发一次写入。本例在创建引擎时指定
*triggeringPattern*="perBatch"。以下脚本共生成 6 条记录，分两批写入，预期产生 2 次输出：

```
share streamTable(10:0,`time`sym`price`qty,[TIMESTAMP,SYMBOL,DOUBLE,INT]) as trades
outputTable = table(1:0, `time`maxQty`maxDollarVolume`sumDollarVolume, [TIMESTAMP,INT,DOUBLE,DOUBLE])
tradesCrossAggregator=createCrossSectionalEngine("CrossSectionalDemo", <[max(qty), max(price*qty), sum(price*qty)]>, trades, outputTable, `sym, `perBatch, useSystemTime=false, timeColumn=`time)
subscribeTable(,"trades","tradesCrossAggregator",-1,append!{tradesCrossAggregator},true)
def writeData1(){
  timev  = 2000.10.08T01:01:01.001 + timestamp(1..4)
  symv   = take(`A`B, 4)
  pricev = 102.1 33.4 102.3 33.2
  qtyv   = 10 20 40 30
  insert into trades values(timev, symv, pricev,qtyv)
}
def writeData2(){
  timev  = 2000.10.08T01:01:01.005 + timestamp(1..2)
  symv   = `A`B
  pricev = 102.4 33.1
  qtyv   = 120 60
  insert into trades values(timev, symv, pricev,qtyv)
}
//写入2批数据，预期会触发2次计算，输出2次聚合结果。
writeData1();
sleep(100)
writeData2();
dropStreamEngine(`CrossSectionalDemo)
unsubscribeTable(, `trades, `tradesCrossAggregator)
```

trades 表中共写入了 6 条记录：

```
select * from trades
```

| time | sym | price | qty |
| --- | --- | --- | --- |
| 2000.10.08T01:01:01.002 | A | 102.1 | 10 |
| 2000.10.08T01:01:01.003 | B | 33.4 | 20 |
| 2000.10.08T01:01:01.004 | A | 102.3 | 40 |
| 2000.10.08T01:01:01.005 | B | 33.2 | 30 |
| 2000.10.08T01:01:01.006 | A | 102.4 | 120 |
| 2000.10.08T01:01:01.007 | B | 33.1 | 60 |

横截面表包含每组最新记录：

```
select * from tradesCrossAggregator
```

| time | sym | price | qty |
| --- | --- | --- | --- |
| 2000.10.08T01:01:01.006 | A | 102.4 | 120 |
| 2000.10.08T01:01:01.007 | B | 33.1 | 60 |

由于分 2 次写入，在 perBatch 模式下，横截面引擎输出了 2 条记录：

```
select * from outputTable
```

| time | maxQty | maxDollarVolume | sumDollarVolume |
| --- | --- | --- | --- |
| 2019.04.08T04:52:50.255 | 40 | 4092 | 5088 |
| 2019.04.08T04:52:50.355 | 120 | 12288 | 14274 |

**例3. 基于系统时间间隔触发计算**

*triggeringPattern* 取值 "interval" 时，必须与 *triggeringInterval* 参数配合使用，表示每隔
*triggeringInterval* 毫秒基于系统时间触发一次计算。本例中，数据分 6 次写入，每 500 毫秒触发一次计算，每次写入 1
条数据，间隔为 500 或 1000 毫秒。

```
share streamTable(10:0,`time`sym`price`qty,[TIMESTAMP,SYMBOL,DOUBLE,INT]) as trades
outputTable = table(1:0, `time`avgPrice`volume`dollarVolume`count, [TIMESTAMP,DOUBLE,INT,DOUBLE,INT])
tradesCrossAggregator=createCrossSectionalEngine(name="tradesCrossAggregator", metrics=<[avg(price), sum(qty), sum(price*qty), count(price)]>, dummyTable=trades, outputTable=outputTable, keyColumn=`sym, triggeringPattern="interval", triggeringInterval=500)
subscribeTable(tableName="trades", actionName="tradesStats", offset=-1, handler=append!{tradesCrossAggregator}, msgAsTable=true)

insert into trades values(2020.08.12T09:30:00.000, `A, 10, 20)
sleep(500)
insert into trades values(2020.08.12T09:30:00.000 + 500, `B, 20, 10)
sleep(500)
insert into trades values(2020.08.12T09:30:00.000 + 1000, `A, 10.1, 20)
sleep(1000)
insert into trades values(2020.08.12T09:30:00.000 + 2000, `B, 20.1, 30)
sleep(500)
insert into trades values(2020.08.12T09:30:00.000 + 2500, `B, 20.2, 40)
sleep(500)
insert into trades values(2020.08.12T09:30:00.000 + 3000, `A, 10.2, 20)

select * from outputTable;
```

| time | avgPrice | volume | dollarVolume | count |
| --- | --- | --- | --- | --- |
| 2021.07.27T10:54:00.303 | 10 | 20 | 200 | 1 |
| 2021.07.27T10:54:00.818 | 15 | 30 | 400 | 2 |
| 2021.07.27T10:54:01.331 | 15.05 | 30 | 402 | 2 |
| 2021.07.27T10:54:02.358 | 15.1 | 50 | 805 | 2 |
| 2021.07.27T10:54:02.871 | 15.15 | 60 | 1010 | 2 |
| 2021.07.27T10:54:03.386 | 15.2 | 60 | 1012 | 2 |

**例4. 保留并计算最新时间戳的截面数据。**

设置 *triggeringPattern*="keyCount"，同时设置 *lastBatchOnly* =
true，横截面引擎将仅保留最新时间戳上的数据并进行计算。这里设置 *triggeringInterval*=4，所以只有收到的具有相同时间戳的记录数达到 4
条或者收到更新时间戳的数据时，才会触发截面数据进行计算输出。

```
// 定义输入表与输出表
share streamTable(10:0,`time`sym`price`qty,[TIMESTAMP,SYMBOL,DOUBLE,INT]) as tick
share table(1:0, `time`amount, [TIMESTAMP,INT]) as opt

// 创建引擎
csEngine=createCrossSectionalEngine(name="csEngineDemo", metrics=<[sum(qty)]>, dummyTable=tick, outputTable=opt, keyColumn=`sym, triggeringPattern="keyCount", triggeringInterval=4, timeColumn=`time, useSystemTime=false,lastBatchOnly=true)

subscribeTable(tableName=`tick, actionName="csEngineDemo", msgAsTable=true, handler=append!{csEngine})

def writeData1(){
    time = array(timestamp)
    time=take(2020.10.08T10:01:01.000,7)
    sym=take("A"+string(1..7),7)
    price=1..7
    qty=1..7
    insert into tick values(time, sym, price, qty)
}

// 第一次写入数据
writeData1();

def writeData2(){
    time = array(timestamp)
    time=take(2020.10.08T10:30:01.000,5)
    sym=take("A"+string(1..5),5)
    price=1..5
    qty=1..5
    insert into tick values(time, sym, price, qty)
}

// 第二次写入数据
writeData2();

select * from opt
```

| time | amount |
| --- | --- |
| 2020.10.08 10:01:01.000 | 28 |
| 2020.10.08 10:30:01.000 | 15 |

以上结果表中，第一行的结果由引擎收到的 2020.10.08T10:01:01.000 时刻的数据触发。此时横截面数据表中的
2020.10.08T10:01:01.000 时刻 A1~A7 每个分组中的最后一个记录进行求和，结果是28。第二行的结果由于收到的 2020.10.08
10:30:01.000 时刻的数据条数达到 4 条，触发计算输出。

由于设置了 *lastBatchOnly* = true，横截面数据表将只保留最新时间戳的各分组数据。查看截面数据表：

```
select * from csEngine
```

| time | sym | price | qty |
| --- | --- | --- | --- |
| 2020.10.08 10:30:01.000 | A1 | 1 | 1 |
| 2020.10.08 10:30:01.000 | A2 | 2 | 2 |
| 2020.10.08 10:30:01.000 | A3 | 3 | 3 |
| 2020.10.08 10:30:01.000 | A4 | 4 | 4 |
| 2020.10.08 10:30:01.000 | A5 | 5 | 5 |

**横截面表作为最终结果**

在以上的例子中，`createCrossSectionalEngine`
的返回结果（以下称为横截面表）是为聚合计算提供的一个中间结果，但横截面表亦可为最终结果。例如若需要定时刷新某只股票的最新交易价格，按照常规思路是从实时交易表中按代码筛选股票并取出最后一条记录，而交易表的数据量是随着时间快速增长的，如果频繁做这样的查询，无论从系统的资源消耗还是从查询的效能来看都不是最优的做法。而横截面表永远只保存所有股票的最近一次交易数据，数据量是稳定的，对于这种定时轮询的场景非常合适。

要将横截面表作为最终结果，需要在创建横截面时，对 *metrics* 与 *outputTable* 这两个参数置空。

```
tradesCrossAggregator=createCrossSectionalEngine("CrossSectionalDemo", , trades, , `sym, `perRow)
```

Copyright

**©2025 浙江智臾科技有限公司 浙ICP备18048711号-3**
