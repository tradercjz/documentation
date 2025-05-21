# createDualOwnershipReactiveStateEngine

## 语法

`createDualOwnershipReactiveStateEngine(name, metrics1,
metrics2, dummyTable, outputTable, keyColumn1, keyColumn2, [snapshotDir],
[snapshotIntervalInMsgCount], [keyPurgeFilter1], [keyPurgeFilter2],
[keyPurgeFreqInSecond=0], [raftGroup], [outputHandler=NULL],
[msgAsTable=false])`

## 详情

Dual Ownership Reactive State Engine
是对响应式状态引擎的扩展，支持对同一张流数据表指定两种不同的分组方式分别应用不同的指标进行并行计算。与响应式状态级联实现相比，该函数能极大地提升计算性能。

注： 该引擎输出和输入顺序保持一致，即内部强制使 *keepOrder* = True。

## 参数

`createDualOwnershipReactiveStateEngine` 与 [createReactiveStateEngine](createReactiveStateEngine.html)
参数基本一致，这里仅介绍有区别的参数：

对 *keyColumn1* 分组后的数据按照 *metrics1* 进行计算，分组数据的清条件则由参数
*keyPurgeFilter1* 设置。

对 *keyColumn2* 分组后的数据按照 *metrics2* 进行计算，分组数据的清条件则由参数
*keyPurgeFilter2* 设置。

**outputTable** 结果的输出表，可以是内存表或者分布式表。使用
`createDualOwnershipReactiveStateEngine`
函数之前，需要将输出表预先设立为一个空表，并指定各列列名以及数据类型。

输出表各列的顺序如下：

1. 分组列。输出表的前几列为 *keyColumn1* 和 *keyColumn2*
   的公共列，然后依次为 *keyColumn1* 的非公共列和 *keyColumn2* 的非公共列。
2. 计算结果列。包含 *metrics1* 的计算结果列，*metrics2*的计算结果列。

**outputHandler** 一元函数。设置此参数时，引擎计算结束后，不再将计算结果写到输出表，而是会调用此函数处理计算结果。默认值为
NULL，表示仍将结果写到输出表。

**msgAsTable** 布尔标量，表示在设置了参数 outputHandler 时，将引擎的计算结果以表的结构调用函数。默认值为
false，此时将计算结果的每一列作为元素组成元组。

## 例子

```
share streamTable(1:0, `date`time`sym`market`price`qty, [DATE, TIME, SYMBOL, CHAR, DOUBLE, INT]) as trades
share table(100:0, `date`sym`market`factor1`factor2, [DATE, SYMBOL, CHAR, DOUBLE, DOUBLE]) as outputTable
dors = createDualOwnershipReactiveStateEngine(name="test", metrics1=<mfirst(price, 3)>, metrics2=<mmax(price, 3)>, dummyTable=trades, outputTable=outputTable, keyColumn1=`date`sym, keyColumn2=`date`market)
tmp = table(1:0, `date`time`sym`market`price`qty, [DATE, TIME, SYMBOL, CHAR, DOUBLE, INT])
subscribeTable(tableName=`trades, actionName="test",msgAsTable=true, handler=tableInsert{dors})
insert into tmp values(2012.01.01, 09:00:00.030, `a, 'B', 10.65, 1500)
insert into tmp values(2012.01.01, 09:00:00.030, `a, 'B', 10.59, 2500)
insert into tmp values(2012.01.01, 09:00:00.031, `b, 'A', 10.59, 2500)
insert into tmp values(2012.01.01, 09:00:00.031, `a, 'B', 10.65, 1500)
insert into tmp values(2012.01.01, 09:00:00.031, `a, 'A', 10.59, 2500)
insert into tmp values(2012.01.01, 09:00:00.033, `b, 'B', 10.59, 2500)
insert into tmp values(2012.01.01, 09:00:00.033, `a, 'A', 10.59, 2500)
insert into tmp values(2012.01.01, 09:00:00.034, `b, 'A', 10.59, 2500)
insert into tmp values(2012.01.01, 09:00:00.034, `b, 'A', 10.22, 1200)
insert into tmp values(2012.01.01, 09:00:00.035, `a, 'A', 11.0, 2500)
insert into tmp values(2012.01.02, 09:00:00.031, `b, 'A', 10.22, 1200)
insert into tmp values(2012.01.02, 09:00:00.032, `a, 'B', 11.0, 2500)
insert into tmp values(2012.01.02, 09:00:00.032, `b, 'B', 15.6, 1300)
insert into tmp values(2012.01.02, 09:00:00.040, `c, 'B', 13.2, 2000)
trades.append!(tmp)
select * from outputTable
```

| date | sym | market | factor1 | factor2 |
| --- | --- | --- | --- | --- |
| 2012.01.01 | a | 'B' |  |  |
| 2012.01.01 | a | 'B' |  |  |
| 2012.01.01 | b | 'A' |  |  |
| 2012.01.01 | a | 'B' | 10.65 | 10.65 |
| 2012.01.01 | a | 'A' | 10.59 |  |
| 2012.01.01 | b | 'B' |  | 10.65 |
| 2012.01.01 | a | 'A' | 10.65 | 10.59 |
| 2012.01.01 | b | 'A' | 10.59 | 10.59 |
| 2012.01.01 | b | 'A' | 10.59 | 10.59 |
| 2012.01.01 | a | 'A' | 10.59 | 11 |
| 2012.01.02 | b | 'A' |  |  |
| 2012.01.02 | a | 'B' |  |  |
| 2012.01.02 | b | 'B' |  |  |
| 2012.01.02 | c | 'B' |  | 15.6 |

```
unsubscribeTable(tableName=`trades, actionName="test")
undef(`trades,SHARED)
dropStreamEngine("test")
```

