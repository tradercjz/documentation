# createLeftSemiJoinEngine

## 语法

`createLeftSemiJoinEngine(name, leftTable, rightTable,
outputTable, metrics, matchingColumn, [garbageSize=5000],
[updateRightTable=false], [snapshotDir],
[snapshotIntervalInMsgCount])`

## 详情

创建流数据左半等值连接引擎，返回一个左、右表关联后的表对象。对于左表每一条数据，都去匹配右表相同
*matchingColumn* 的数据，若无匹配的右表记录，则不输出。若匹配多条右表记录，则由 *updateRightTable*
参数决定连接右表的第一条记录还是最新一条记录。

注： 右表根据 *updateRightTable* 指定的策略，同一 *matchingColumn*
只保留第一条或者最新一条数据，历史数据不再进行垃圾回收，因此用户需要控制 *matchingColumn*
的唯一值数量，否则可能会导致内存溢出。

## 参数

**name** 表示流数据 left semi join
引擎的名称，作为其在一个数据节点/计算节点上的唯一标识。可包含字母，数字和下划线，但必须以字母开头。

**leftTable** 表对象。可以不包含数据，但结构必须与订阅的流数据表相同。自 2.00.11
版本开始，该参数支持 array vector。

**rightTable** 表对象。可以不包含数据，但结构必须与订阅的流数据表相同。自 2.00.11
版本开始，该参数支持 array vector。

**outputTable** 为计算结果的输出表。在使用 `createLeftSemiJoinEngine`
函数之前，需要将输出表预先设立为一个空表，并指定各列列名以及数据类型。自 2.00.11
版本开始，引擎支持通过自定义聚合函数，将多个计算结果以 array vector 的形式输出，此时必须在该参数中指定对应列类型为 array
vector。

输出表的各列的顺序如下：

1. 连接列。与 *matchingColumn* 中的列以及其顺序一致，可为多列。
2. 计算结果列。可为多列。

**metrics** 以元代码的格式表示计算指标，支持输入元组。有关元代码的更多信息可参考 [Metaprogramming](../../progr/objs/meta_progr.html)。

* 计算指标可以是一个或多个表达式、系统内置或用户自定义函数、一个常量标量/向量。当指定为常量向量时，对应的输出列必须设置为数组向量类型，例子参见
  [createReactiveStateEngine](createReactiveStateEngine.html) 中的例4。
* **metrics** 内支持调用具有多个返回值的函数，且必须指定列名，例如 <func(price) as
  `col1`col2>。

  若在 *metrics* 指定了 *leftTable* 和
  *rightTable* 中具有相同名称的列，默认取左表的列，可以通过 "tableName.colName"
  指定该列来自哪个表。

  注： *metrics*
  中使用的列名大小写不敏感，不需要与输入表的列名大小写保持一致。

**matchingColumn** 表示连接列的字符串标量/向量或字符串向量组成的 tuple，支持 Integral,
Temporal 或 Literal(UUID 除外)类型。

*matchingColumn* 指定规则：

1. 只有一个连接列。当左表和右表的连接列名相同时，*matchingColumn* 是一个字符串标量，否则是一个长度为 2 的
   tuple。例如：左表连接列名为 sym，右表连接列名为 sym1，则 *matchingColumn* =
   [[`sym],[`sym1]]。
2. 有多个连接列。当左表和右表的连接列名相同时，*matchingColumn* 是一个字符串向量，否则是一个长度为 2 的
   tuple。例如：左表连接列名为 timestamp, sym，右表连接列名为 timestamp, sym1，则
   *matchingColumn* = [[`timestamp, `sym], [`timestamp,`sym1]]。

**garbageSize** 可选参数，正整数，默认值是 5,000（单位为行）。和其他连接引擎不同，该函数的
*garbageSize* 参数只用于清理左表的历史数据。当左表发生过 join 的记录数超过 *garbageSize*
时，系统会触发清理。

**updateRightTable** 可选参数，布尔值，默认为 false，表示右表存在多条相同
*matchingColumn* 的记录时，是保留第一条（false）还是最新一条记录（true）。

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

```
share streamTable(1:0, `time`sym`price, [TIMESTAMP, SYMBOL, DOUBLE]) as leftTable
share streamTable(1:0, `time`sym1`vol, [TIMESTAMP, SYMBOL, INT]) as rightTable

share table(100:0, `time`sym`price`vol`total, [TIMESTAMP, SYMBOL, DOUBLE, INT, DOUBLE]) as output
lsjEngine=createLeftSemiJoinEngine(name="test1", leftTable=leftTable, rightTable=rightTable, outputTable=output,  metrics=<[price, vol,price*vol]>, matchingColumn=[[`time,`sym], [`time,`sym1]], updateRightTable=true)

subscribeTable(tableName="leftTable", actionName="joinLeft", offset=0, handler=appendForJoin{lsjEngine, true}, msgAsTable=true)
subscribeTable(tableName="rightTable", actionName="joinRight", offset=0, handler=appendForJoin{lsjEngine, false}, msgAsTable=true)

v = [1, 5, 10, 15]
tp1=table(2012.01.01T00:00:00.000+v as time, take(`AAPL, 4) as sym, rand(100,4) as price)
leftTable.append!(tp1)

v = [1, 1, 3, 4, 5, 5, 5, 15]
tp2=table(2012.01.01T00:00:00.000+v as time, take(`AAPL, 8) as sym, rand(100,8) as vol)
rightTable.append!(tp2)

select * from output
```

| time | sym | price | vol | total |
| --- | --- | --- | --- | --- |
| 2012.01.01T00:00:00.001 | AAPL | 44 | 76 | 3344 |
| 2012.01.01T00:00:00.005 | AAPL | 15 | 64 | 960 |
| 2012.01.01T00:00:00.015 | AAPL | 24 | 75 | 1800 |

若要再次执行以上脚本，需要先删除引擎并取消订阅：

```
dropStreamEngine("test1")
lsjEngine=NULL
unsubscribeTable(tableName="leftTable", actionName="joinLeft")
unsubscribeTable(tableName="rightTable", actionName="joinRight")
```

**相关信息**

* [流计算引擎](../themes/streamingEngine.html "流计算引擎")

