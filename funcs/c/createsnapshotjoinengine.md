# createSnapshotJoinEngine

## 语法

`createSnapshotJoinEngine(name, leftTable, rightTable, outputTable, metrics,
matchingColumn, [timeColumn], [outputElapsedMicroseconds=false],
[keepLeftDuplicates=false], [keepRightDuplicates=false], [isInnerJoin=true], [snapshotDir],
[snapshotIntervalInMsgCount])`

## 详情

创建流数据表的快照连接引擎。该引擎以*matchingColumn*作为连接列，将两个流数据表进行实时的内连接（等值连接）或外连接（左/右连接）。

**返回值：**返回一个左、右两表连接后的表对象。

**连接行为**

由 *isInnerJoin* 参数决定连接方式：

* 当 *isInnerJoin*=true
  时，进行内连接，即每次数据注入引擎左表时，会在右表中查找与连接列字段相匹配的记录，匹配成功才会将两表匹配的记录进行连接，并计算
  *metrics* 后输出。每次数据注入引擎右表时，亦会做同样操作。
* 当 *isInnerJoin*=false 时，进行外连接，即每次数据注入引擎左表时，与右表进行左连接。无论在右表中是否找到匹配的记录，都会计算
  *metrics* 并输出（右表未匹配的记录输出空值）。每次数据注入引擎右表时，亦会做同样操作。
* 当 keepLeftDuplicates=false 时，仅与左表中根据 *matchingColumn* 分组后的最新一条数据进行匹配连接。当
  keepLeftDuplicates=true 时，与左表所有数据进行匹配连接。
* 当 keepRightDuplicates=false 时，仅与右表中根据 *matchingColumn*
  分组后的最新一条数据进行匹配连接。当 keepRightDuplicates=true 时，与右表所有数据进行匹配连接。

snapshot join 引擎与 lookup join、equi join 引擎很相似，主要区别如下：

* lookup join 引擎只能由左表的新记录触发连接；而 snapshot join
  引擎可以由左表或右表的新记录触发连接。

* equi join 引擎仅匹配最新记录，且没有缓存；而 snapshot join 引擎可以选择与右表/左表所有记录或最新记录进行匹配，且有缓存。

## 参数

**name**：字符串标量，表示 Snapshot join
引擎的名称，作为其在一个数据节点/计算节点上的唯一标识。可包含字母，数字和下划线，但必须以字母开头。

**leftTable**：表对象，表示左表，其结构必须与订阅的流数据表相同。

**rightTable**：表对象，表示右表，其结构必须与订阅的流数据表相同。

**outputTable**：计算结果的输出表。在使用 `createSnapshotJoinEngine`
函数之前，需要将输出表预先设立为一个空表，并指定各列列名以及数据类型。

输出表的各列的顺序如下：

1. 连接列。与 *matchingColumn* 中的列以及其顺序一致，可为多列。
2. 时间列（两列）。如果指定了 *timeColumn*，则分别为左表和右表的时间列，类型与 *timeColumn* 列一致；如果未指定
   *timeColumn*，则两列分别是 leftTable 和 rightTable 的数据到达时间，类型为
   TIMESTAMP。
3. 计算结果列。可为多列。
4. 耗时列。如果指定 *outputElapsedMicroseconds* = true，则指定一个 LONG
   类型的列用于记录单次响应计算耗时（单位：微秒）。
5. batchSize 列。如果指定 *outputElapsedMicroseconds* = true,
   则指定一个INT类型的列，记录单次响应的数据条数。

**metrics**：以元代码的格式表示计算指标，支持输入元组。有关元代码的更多信息可参考 [Metaprogramming](../../progr/objs/meta_progr.html)。

* 计算指标可以是一个或多个表达式、系统内置或用户自定义函数，但不能是聚合函数。
* *metrics* 内支持调用具有多个返回值的函数，且必须指定列名，例如 <func(price) as
  `col1`col2>。
* 若在 *metrics* 指定了 *leftTable* 和 *rightTable*
  中具有相同名称的列，默认取左表的列，可以通过 "tableName.colName" 指定该列来自哪个表。

  **注：**
  *metrics* 中使用的列名大小写不敏感，不需要与输入表的列名大小写保持一致。

**matchingColumn：**表示连接列的字符串标量/向量或字符串向量组成的 tuple，支持 Integral,
Temporal 或 Literal(UUID 除外)类型。*matchingColumn* 指定规则：

1. 只有一个连接列。当左表和右表的连接列名相同时，*matchingColumn* 是一个字符串标量，否则是一个长度为 2 的
   tuple。例如：左表连接列名为 sym，右表连接列名为 sym1，则 *matchingColumn* =
   [[`sym],[`sym1]]。
2. 有多个连接列。当左表和右表的连接列名相同时，*matchingColumn* 是一个字符串向量，否则是一个长度为 2 的
   tuple。例如：左表连接列名为 timestamp, sym，右表连接列名为 timestamp, sym1，则
   *matchingColumn* = [[`timestamp, `sym],
   [`timestamp,`sym1]]。

**timeColumn:** 字符串标量或向量，可选参数。用于指定 leftTable 和 rightTable
中时间列的名称。两表的时间列名称可以不同，但数据类型需保持一致。当 leftTable 和 rightTable 时间列名称相同时，timeColumn
是字符串标量，否则，timeColumn 是长度为2的字符串向量。

**outputElapsedMicroseconds**：布尔值，可选参数，表示是否输出单次响应计算的耗时（从触发计算的数据注入引擎到计算完成的耗时），默认为
false。指定参数 *outputElapsedMicroseconds* 后，在定义 outputTable 时需要在计算结果列后增加一个 LONG
类型的列和 INT 类型的列，详见 *outputTable* 参数说明。

**keepLeftDuplicates**：布尔值，可选参数，表示在进行右连接时，是否匹配左表各分组内的所有数据。

* 若设置为 false（默认值）：仅匹配左表各分组内的最新一条数据。
* 若设置为 true：匹配左表各分组内的所有数据。

**keepRightDuplicates**：布尔值，可选参数，表示在进行左连接时，是否保留右表各分组内的所有数据。

* 若设置为 false（默认值）：仅匹配右表各分组内的最新一条数据。
* 若设置为 true：匹配右表各分组内的所有数据。

**isInnerJoin：**布尔值，可选参数，表示是否进行内连接。

* 若设置为 true（默认值）：进行内连接，只有左右两表匹配的记录被计算输出。
* 若设置为 false：进行左连接或右连接，保留两个表中的所有记录。对于左右两表中匹配的记录进行计算，而未匹配的记录输出空值。

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

例1. 不指定 *outputElapsedMicroseconds，*指定 *isInnerJoin*=true，同时指定
*keepLeftDuplicates*=true，*keepRightDuplicates*=true。此时，引擎进行内连接，且匹配左/右表各分组内的所有数据。

```
//定义输入、输出表
share streamTable(1:0, `timestamp`sym1`id`price`val, [TIMESTAMP, SYMBOL, INT, DOUBLE, DOUBLE]) as leftTable
share streamTable(1:0, `timestamp`sym2`id`price`qty, [TIMESTAMP, SYMBOL, INT, DOUBLE, DOUBLE]) as rightTable
output=table(100:0, ["id","sym", "timestamp1", "timestamp2", "factor1", "factor2"],
[INT, SYMBOL, TIMESTAMP, TIMESTAMP, DOUBLE, DOUBLE])

test_metrics = [<val*10>, <qty>]
// 创建引擎
test_engine = createSnapshotJoinEngine(name = "test_SJE", leftTable=leftTable, rightTable=rightTable,
outputTable=output, metrics=test_metrics, matchingColumn = [["id","sym1"],["id","sym2"]],
timeColumn = `timestamp, isInnerJoin=true, keepLeftDuplicates=true,keepRightDuplicates=true)

//将左表数据注入引擎
timestamp = 2024.10.10T15:12:01.507+1..10
sym = take(["a","b","c","d"],10)
id = [1,1,2,1,5,2,4,4,1,4]
price = [2.53,7.61,8.07,7.87,7.29,9.39,5.98,9.49,9.20,9.17]
val = [101,108,101,109,104,100,108,100,107,104]
left_data = table(timestamp as timestamp,sym as sym1,id as id,price as price,val as val)
appendForJoin(test_engine,true, left_data)

//将右表数据注入引擎，此时会触发两表进行右连接
timestamp = 2024.10.10T15:12:01.507+1..10
sym = take(["a","b","c","d"],10)
id = [1,2,4,3,5,5,4,2,5,5]
price =  [1.08,9.08,9.97,7.60,1.91,6.77,7.81,8.81,0.61,5.92]
qty =  [208,200,203,202,204,201,206,207,205,205]
right_data = table(timestamp as timestamp,sym as sym2,id as id,price as price,qty as qty)
appendForJoin(test_engine,false, right_data)

select * from output
```

结果表中将保留左表所有匹配记录。

| id | sym | timestamp1 | timestamp2 | factor1 | factor2 |
| --- | --- | --- | --- | --- | --- |
| 1 | a | 2024.10.10T15:12:01.508 | 2024.10.10T15:12:01.508 | 1,010 | 208 |
| 1 | a | 2024.10.10T15:12:01.516 | 2024.10.10T15:12:01.508 | 1,070 | 208 |
| 2 | b | 2024.10.10T15:12:01.513 | 2024.10.10T15:12:01.509 | 1,000 | 200 |
| 4 | c | 2024.10.10T15:12:01.514 | 2024.10.10T15:12:01.510 | 1,080 | 203 |
| 5 | a | 2024.10.10T15:12:01.512 | 2024.10.10T15:12:01.512 | 1,040 | 204 |
| 4 | c | 2024.10.10T15:12:01.514 | 2024.10.10T15:12:01.514 | 1,080 | 206 |
| 5 | a | 2024.10.10T15:12:01.512 | 2024.10.10T15:12:01.516 | 1,040 | 205 |

例2. 不指定 *outputElapsedMicroseconds*，指定
*isInnerJoin*=true，*keepLeftDuplicate*s=false，*keepRightDuplicates*=true。此时，引擎进行内连接，且匹配左表各分组内的最新一条数据。

```
//首先取消上例中定义的引擎
dropStreamEngine("test_SJE")

//定义输入、输出表
share streamTable(1:0, `timestamp`sym1`id`price`val, [TIMESTAMP, SYMBOL, INT, DOUBLE, DOUBLE]) as leftTable
share streamTable(1:0, `timestamp`sym2`id`price`qty, [TIMESTAMP, SYMBOL, INT, DOUBLE, DOUBLE]) as rightTable
output=table(100:0, ["id","sym", "timestamp1", "timestamp2", "factor1", "factor2"],
[INT, SYMBOL, TIMESTAMP, TIMESTAMP, DOUBLE, DOUBLE])

test_metrics = [<val*10>, <qty>]
// 创建引擎
test_engine = createSnapshotJoinEngine(name = "test_SJE", leftTable=leftTable, rightTable=rightTable,
outputTable=output, metrics=test_metrics, matchingColumn = [["id","sym1"],["id","sym2"]],
timeColumn = `timestamp, isInnerJoin=true, keepLeftDuplicates=false,keepRightDuplicates=true)

//将左表数据注入引擎
timestamp = 2024.10.10T15:12:01.507+1..10
sym = take(["a","b","c","d"],10)
id = [1,1,2,1,5,2,4,4,1,4]
price = [2.53,7.61,8.07,7.87,7.29,9.39,5.98,9.49,9.20,9.17]
val = [101,108,101,109,104,100,108,100,107,104]
left_data = table(timestamp as timestamp,sym as sym1,id as id,price as price,val as val)
appendForJoin(test_engine,true, left_data)

//将右表数据注入引擎，此时会触发两表进行右连接
timestamp = 2024.10.10T15:12:01.507+1..10
sym = take(["a","b","c","d"],10)
id = [1,2,4,3,5,5,4,2,5,5]
price =  [1.08,9.08,9.97,7.60,1.91,6.77,7.81,8.81,0.61,5.92]
qty =  [208,200,203,202,204,201,206,207,205,205]
right_data = table(timestamp as timestamp,sym as sym2,id as id,price as price,qty as qty)
appendForJoin(test_engine,false, right_data)

select * from output
```

结果表中仅保留左表每个分组中的最新记录，因此比例1中的结果少了一行记录。

| id | sym | timestamp1 | timestamp2 | factor1 | factor2 |
| --- | --- | --- | --- | --- | --- |
| 1 | a | 2024.10.10T15:12:01.516 | 2024.10.10T15:12:01.508 | 1,070 | 208 |
| 2 | b | 2024.10.10T15:12:01.513 | 2024.10.10T15:12:01.509 | 1,000 | 200 |
| 4 | c | 2024.10.10T15:12:01.514 | 2024.10.10T15:12:01.510 | 1,080 | 203 |
| 5 | a | 2024.10.10T15:12:01.512 | 2024.10.10T15:12:01.512 | 1,040 | 204 |
| 4 | c | 2024.10.10T15:12:01.514 | 2024.10.10T15:12:01.514 | 1,080 | 206 |
| 5 | a | 2024.10.10T15:12:01.512 | 2024.10.10T15:12:01.516 | 1,040 | 205 |

例3. 不指定 *outputElapsedMicroseconds*，指定
*isInnerJoin*=false，*keepLeftDuplicates*=false，*keepRightDuplicates*=true。此时，引擎进行左连接或右连接。在左连接时，匹配右表各分组内的所有数据；在进行右连接时，仅匹配左表各分组内的最新一条数据。

```
//首先取消上例中定义的引擎
dropStreamEngine("test_SJE")

//定义输入、输出表
share streamTable(1:0, `timestamp`sym1`id`price`val, [TIMESTAMP, SYMBOL, INT, DOUBLE, DOUBLE]) as leftTable
share streamTable(1:0, `timestamp`sym2`id`price`qty, [TIMESTAMP, SYMBOL, INT, DOUBLE, DOUBLE]) as rightTable
output=table(100:0, ["id","sym", "timestamp1", "timestamp2", "factor1", "factor2"],
[INT, SYMBOL, TIMESTAMP, TIMESTAMP, DOUBLE, DOUBLE])

test_metrics = [<val*10>, <qty>]
// 创建引擎
test_engine = createSnapshotJoinEngine(name = "test_SJE", leftTable=leftTable, rightTable=rightTable,
outputTable=output, metrics=test_metrics, matchingColumn = [["id","sym1"],["id","sym2"]],
timeColumn = `timestamp, isInnerJoin=false, keepLeftDuplicates=false,keepRightDuplicates=true)

//将左表数据注入引擎
timestamp = 2024.10.10T15:12:01.507+1..10
sym = take(["a","b","c","d"],10)
id = [1,1,2,1,5,2,4,4,1,4]
price = [2.53,7.61,8.07,7.87,7.29,9.39,5.98,9.49,9.20,9.17]
val = [101,108,101,109,104,100,108,100,107,104]
left_data = table(timestamp as timestamp,sym as sym1,id as id,price as price,val as val)
appendForJoin(test_engine,true, left_data)

//将右表数据注入引擎，此时会触发两表进行右连接
timestamp = 2024.10.10T15:12:01.507+1..10
sym = take(["a","b","c","d"],10)
id = [1,2,4,3,5,5,4,2,5,5]
price =  [1.08,9.08,9.97,7.60,1.91,6.77,7.81,8.81,0.61,5.92]
qty =  [208,200,203,202,204,201,206,207,205,205]
right_data = table(timestamp as timestamp,sym as sym2,id as id,price as price,qty as qty)
appendForJoin(test_engine,false, right_data)

select * from output
```

由于引擎进行了右连接，仅保留左表每个分组中的最新记录。

| id | sym | timestamp1 | timestamp2 | factor1 | factor2 |
| --- | --- | --- | --- | --- | --- |
| 1 | a | 2024.10.10T15:12:01.508 | 1,010 |  |  |
| 1 | b | 2024.10.10T15:12:01.509 | 1,080 |  |  |
| 2 | c | 2024.10.10T15:12:01.510 | 1,010 |  |  |
| 1 | d | 2024.10.10T15:12:01.511 | 1,090 |  |  |
| 5 | a | 2024.10.10T15:12:01.512 | 1,040 |  |  |
| 2 | b | 2024.10.10T15:12:01.513 | 1,000 |  |  |
| 4 | c | 2024.10.10T15:12:01.514 | 1,080 |  |  |
| 4 | d | 2024.10.10T15:12:01.515 | 1,000 |  |  |
| 1 | a | 2024.10.10T15:12:01.516 | 1,070 |  |  |
| 4 | b | 2024.10.10T15:12:01.517 | 1,040 |  |  |
| 1 | a | 2024.10.10T15:12:01.516 | 2024.10.10T15:12:01.508 | 1,070 | 208 |
| 2 | b | 2024.10.10T15:12:01.513 | 2024.10.10T15:12:01.509 | 1,000 | 200 |
| 4 | c | 2024.10.10T15:12:01.514 | 2024.10.10T15:12:01.510 | 1,080 | 203 |
| 3 | d | 2024.10.10T15:12:01.511 | 202 |  |  |
| 5 | a | 2024.10.10T15:12:01.512 | 2024.10.10T15:12:01.512 | 1,040 | 204 |
| 5 | b | 2024.10.10T15:12:01.513 | 201 |  |  |
| 4 | c | 2024.10.10T15:12:01.514 | 2024.10.10T15:12:01.514 | 1,080 | 206 |
| 2 | d | 2024.10.10T15:12:01.515 | 207 |  |  |
| 5 | a | 2024.10.10T15:12:01.512 | 2024.10.10T15:12:01.516 | 1,040 | 205 |
| 5 | b | 2024.10.10T15:12:01.517 | 205 |  |  |

例4. 指定 *outputElapsedMicroseconds* = true，输出耗时列和 batchSize 列。

```
//首先取消上例中定义的引擎
dropStreamEngine("test_SJE")

//定义输入、输出表
share streamTable(1:0, `timestamp`sym1`id`price`val, [TIMESTAMP, SYMBOL, INT, DOUBLE, DOUBLE]) as leftTable
share streamTable(1:0, `timestamp`sym2`id`price`qty, [TIMESTAMP, SYMBOL, INT, DOUBLE, DOUBLE]) as rightTable
output=table(100:0, ["id","sym", "timestamp1", "timestamp2", "factor1", "factor2", "timecost","batchsize"],
[INT, SYMBOL, TIMESTAMP, TIMESTAMP, DOUBLE, DOUBLE, LONG, INT])

test_metrics = [<val*10>, <qty>]
// 创建引擎
test_engine = createSnapshotJoinEngine(name = "test_SJE", leftTable=leftTable, rightTable=rightTable,
outputTable=output, metrics=test_metrics, matchingColumn = [["id","sym1"],["id","sym2"]],
timeColumn = `timestamp, outputElapsedMicroseconds=true, isInnerJoin=true,
keepLeftDuplicates=false,keepRightDuplicates=true)

//将左表数据注入引擎
timestamp = 2024.10.10T15:12:01.507+1..10
sym = take(["a","b","c","d"],10)
id = [1,1,2,1,5,2,4,4,1,4]
price = [2.53,7.61,8.07,7.87,7.29,9.39,5.98,9.49,9.20,9.17]
val = [101,108,101,109,104,100,108,100,107,104]
left_data = table(timestamp as timestamp,sym as sym1,id as id,price as price,val as val)
appendForJoin(test_engine,true, left_data)

//将右表数据注入引擎，此时会触发两表进行右连接
timestamp = 2024.10.10T15:12:01.507+1..10
sym = take(["a","b","c","d"],10)
id = [1,2,4,3,5,5,4,2,5,5]
price =  [1.08,9.08,9.97,7.60,1.91,6.77,7.81,8.81,0.61,5.92]
qty =  [208,200,203,202,204,201,206,207,205,205]
right_data = table(timestamp as timestamp,sym as sym2,id as id,price as price,qty as qty)
appendForJoin(test_engine,false, right_data)

select * from output
```

| id | sym | timestamp1 | timestamp2 | factor1 | factor2 | timecost | batchsize |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | a | 2024.10.10T15:12:01.516 | 2024.10.10T15:12:01.508 | 1,070 | 208 | 109 | 10 |
| 2 | b | 2024.10.10T15:12:01.513 | 2024.10.10T15:12:01.509 | 1,000 | 200 | 109 | 10 |
| 4 | c | 2024.10.10T15:12:01.514 | 2024.10.10T15:12:01.510 | 1,080 | 203 | 109 | 10 |
| 5 | a | 2024.10.10T15:12:01.512 | 2024.10.10T15:12:01.512 | 1,040 | 204 | 109 | 10 |
| 4 | c | 2024.10.10T15:12:01.514 | 2024.10.10T15:12:01.514 | 1,080 | 206 | 109 | 10 |
| 5 | a | 2024.10.10T15:12:01.512 | 2024.10.10T15:12:01.516 | 1,040 | 205 | 109 | 10 |

例5. *keepRightDuplicates*、*keepLeftDuplicates* 为 false，不指定时间列
*timeColumn*，此时输出表中的两个时间列为左表、右表数据到达的时间。

```
//首先取消上例中定义的引擎
dropStreamEngine("test_SJE")

//定义输入、输出表
share streamTable(1:0, `timestamp`sym1`id`price`val, [TIMESTAMP, SYMBOL, INT, DOUBLE, DOUBLE]) as leftTable
share streamTable(1:0, `timestamp`sym2`id`price`qty, [TIMESTAMP, SYMBOL, INT, DOUBLE, DOUBLE]) as rightTable
output=table(100:0, ["id","sym", "timestamp1", "timestamp2", "factor1", "factor2"],
[INT, SYMBOL, TIMESTAMP, TIMESTAMP, DOUBLE, DOUBLE])

test_metrics = [<val*10>, <qty>]
// 创建引擎
test_engine = createSnapshotJoinEngine(name = "test_SJE", leftTable=leftTable, rightTable=rightTable,
outputTable=output, metrics=test_metrics, matchingColumn = [["id","sym1"],["id","sym2"]], isInnerJoin=true)

//将左表数据注入引擎
timestamp = 2024.10.10T15:12:01.507+1..10
sym = take(["a","b","c","d"],10)
id = [1,1,2,1,5,2,4,4,1,4]
price = [2.53,7.61,8.07,7.87,7.29,9.39,5.98,9.49,9.20,9.17]
val = [101,108,101,109,104,100,108,100,107,104]
left_data = table(timestamp as timestamp,sym as sym1,id as id,price as price,val as val)
appendForJoin(test_engine,true, left_data)

//将右表数据注入引擎，此时会触发两表进行右连接
timestamp = 2024.10.10T15:12:01.507+1..10
sym = take(["a","b","c","d"],10)
id = [1,2,4,3,5,5,4,2,5,5]
price =  [1.08,9.08,9.97,7.60,1.91,6.77,7.81,8.81,0.61,5.92]
qty =  [208,200,203,202,204,201,206,207,205,205]
right_data = table(timestamp as timestamp,sym as sym2,id as id,price as price,qty as qty)
appendForJoin(test_engine,false, right_data)

select * from output
```

| id | sym | timestamp1 | timestamp2 | factor1 | factor2 |
| --- | --- | --- | --- | --- | --- |
| 1 | a | 2024.12.20T15:05:49.603 | 2024.12.20T15:05:49.603 | 1,070 | 208 |
| 2 | b | 2024.12.20T15:05:49.603 | 2024.12.20T15:05:49.603 | 1,000 | 200 |
| 4 | c | 2024.12.20T15:05:49.603 | 2024.12.20T15:05:49.603 | 1,080 | 203 |
| 5 | a | 2024.12.20T15:05:49.603 | 2024.12.20T15:05:49.603 | 1,040 | 204 |
| 4 | c | 2024.12.20T15:05:49.603 | 2024.12.20T15:05:49.603 | 1,080 | 206 |
| 5 | a | 2024.12.20T15:05:49.603 | 2024.12.20T15:05:49.603 | 1,040 | 205 |

