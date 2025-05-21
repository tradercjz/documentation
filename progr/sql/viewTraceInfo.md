# viewTraceInfo

## 语法

`viewTraceInfo(traceId, [isTreeView=true])`

## 参数

* **traceId** 字符串，表示记录 SQL Trace 信息的 id。通过函数 [getTraces](getTraces.html) 获取。
* **isTreeView** 布尔值，表示是否以树状结构显示跟踪信息，默认为 true。

## 详情

展示 traceId 对应脚本的跟踪信息。返回一个表，包含以下几列：

* tree (*isTreeView* = true)：以树状结构显示执行流程，每个节点可视为一个操作的 [span](https://opentracing.io/docs/overview/spans/)。| name (*isTreeView* = false)：直接显示每个
  span 的操作名。
* script：每个 span 所执行的由用户编写的脚本字符串。
* startTime：脚本开始执行的时间戳，单位为纳秒。
* timeElapsed：脚本执行总耗时，单位为微秒。
* reference：该列显示了子 span 和父 span 的关系。有三种类型：

  + Root：根节点，为首次接收请求的阶段。
  + ChildOf：父 span 依赖于子 span 返回的结果。表示该 span 是被同步调用的。
  + FollowsFrom：父 span 并不依赖子 span 的的返回结果。表示是该 span
    是被异步调用的（如：进入队列或网络请求等操作）。
* node：该 span 所在执行节点的别名。
* thread：该 span 对应的线程号。

name/tree 中各 span 的操作及其含义：

| 操作名 | 含义 |
| --- | --- |
| Worker::run | 服务器获取请求后将请求送入队列，由 worker 线程进行计算工作。其中x是正整数，取值范围[0, 6]。 |
| Tokenizer::tokenize | 对请求内的脚本做词法分析，得到词素流便于后续语法解析。 |
| Parser::parse | 对请求内的脚本做语法解析，得到可执行的语句。 |
| Statement::execute | 执行语句，指代一行脚本。 |
| SQLQueryImp::getReference | 对 SQL 查询求值，即执行 SQL 查询。 |
| SQLQueryImp::partitionedCall | 进行一次分区查询，该查询任务会分解并发送给其他 datanode 来执行查询。常见于分布式查询。 |
| SQLQueryImp::simpleCall | 简单的查询语句，一般不包含 group by, context by, cgroup by 等操作。常见于内存表查询。 |
| SQLQueryImp::basicCall | 从存储引擎中读取数据。 |
| StaticStageExecutor::execute[probing] | 指分布式查询执行前的探测过程（probing）。系统会将客户端发起的查询任务拆分成多个子任务，部分在本地执行，部分发送到远端节点。当发送给远端的子任务过多时，系统会分批进行发送。[probing]阶段，系统会先发送一个子任务，根据其返回结果占用的内存大小估算所有子任务结果占用的内存大小，若超出 memLimitOfQueryResult，则抛出异常。若小于 memLimitOfQueryResult，则根据 memLimitOfTaskGroupResult 和单个子任务返回结果的大小计算每批包含的子任务数，再根据子任务总数算出拆分的批次。 |
| StaticStageExecutor::execute[remote] | 执行远程任务的过程，包括了网络调用和远端执行。 |
| StaticStageExecutor::execute[local] | 在本地工作线程执行任务的过程。 |
| GOContainer::addRemoteTask | 发送一个远程任务。注意这里只包含发送任务过程，不包括远端执行和响应过程。 |
| TableJoiner::getReference | 进行一次表连接。 |
| GroupByEngine::getReference | 对一次 group by 操作进行求值。 |
| ContextByEngine::getReference | 对一次 context by 操作进行求值。 |
| PivotByEngine::getReference | 对一次 pivot by 操作进行求值。 |
| PartitionedPersistentTable::spillToDisk | 对分区持久化表执行一次磁盘溢写 |
| PipelinedJoinTask::getReference | 执行一次 pipeline join任务 |
| StaticStageExecutor::execute[batch] | 批量执行任务 |
| UniversalTableJoinImp::executeJoinPipeline | 对多表查询执行一次 pipeline join |
| UniversalTableJoinImp::getReference | 执行一次多表查询 |

## 例子

```
viewTraceInfo("c87ffe02-0c93-1db0-8e4f-b5416cce0207", true);
```

| tree | script | startTime | timeElapsed | reference | node | thread |
| --- | --- | --- | --- | --- | --- | --- |
| receiving request |  | 2023.11.27 07:53:37.564128355 | 50 | Root | local7270 | 41,472 |
| └── Worker<0>::run |  | 2023.11.27 07:53:37.565859643 | 109,969 | FollowsFrom | local7270 | 41,457 |
| ├── Tokenizer::tokenize |  | 2023.11.27 07:53:37.566078288 | 61 | ChildOf | local7270 | 41,457 |
| ├── Parser::parse |  | 2023.11.27 07:53:37.566161146 | 429 | ChildOf | local7270 | 41,457 |
| └── Statement::execute | t1 = select ID,col1,col2,ratio1,ratio2,col1 \* ratio1 as col1\_mul,col2 \* ratio2 as col2\_mul from ej(loadTable("dfs://TSDBdemo", "data"),temp,"ID","securityId") where ID in "tag" + string(1 .. 19) | 2023.11.27 07:53:37.566651394 | 109,110 | ChildOf | local7270 | 41,457 |
| └── SQLQueryImp::getReference | select ID,col1,col2,ratio1,ratio2,col1 \* ratio1 as col1\_mul,col2 \* ratio2 as col2\_mul from ej(loadTable("dfs://TSDBdemo", "data"),temp,"ID","securityId") where ID in "tag" + string(1 .. 19) | 2023.11.27 07:53:37.566691562 | 109,031 | ChildOf | local7270 | 41,457 |
| └── SQLQueryImp::getReference | select ID,col1,col2,ratio1,ratio2,col1 \* ratio1 as col1\_mul,col2 \* ratio2 as col2\_mul from ej(data,tempb035e530587f0000,"ID","securityId") where ID in "tag" + string(1 .. 19) | 2023.11.27 07:53:37.567047904 | 108,611 | ChildOf | local7270 | 41,457 |
| └── SQLQueryImp::partitionedCall |  | 2023.11.27 07:53:37.568467496 | 107,166 | ChildOf | local7270 | 41,457 |
| └── SQLQueryImp::executeDistributedTasks |  | 2023.11.27 07:53:37.569360522 | 105,751 | ChildOf | local7270 | 41,457 |
| ├── StaticStageExecutor::execute |  | 2023.11.27 07:53:37.569425993 | 103,402 | ChildOf | local7270 | 41,457 |
| │ ├── StaticStageExecutor::execute[probing] |  | 2023.11.27 07:53:37.569446501 | 5 | ChildOf | local7270 | 41,457 |
| │ ├── StaticStageExecutor::execute[localWorker] |  | 2023.11.27 07:53:37.569472069 | 16,530 | ChildOf | local7270 | 41,457 |
| │ ├── StaticStageExecutor::execute[remote] |  | 2023.11.27 07:53:37.569491542 | 16,503 | ChildOf | local7270 | 41,457 |
| │ └── StaticStageExecutor::execute[local] |  | 2023.11.27 07:53:37.569512416 | 102,990 | ChildOf | local7270 | 41,457 |
| │ ├── SQLQueryImp::getReference | select [147467] ID,col1,col2,ratio1,ratio2,col1 \* ratio1 as col1\_mul,col2 \* ratio2 as col2\_mul from ej(data,tempb035e530587f0000,"ID","securityId") where ID in "tag" + string(1 .. 19) [partition = /TSDBdemo/20231112/Key0/x5] | 2023.11.27 07:53:37.586062823 | 10,658 | ChildOf | local7270 | 41,457 |
| │ │ └── SQLQueryImp::basicCall |  | 2023.11.27 07:53:37.586079488 | 10,611 | ChildOf | local7270 | 41,457 |
| │ │ └── TableJoiner::getReference | ej(data,tempb035e530587f0000,"ID","securityId") | 2023.11.27 07:53:37.586099380 | 10,465 | ChildOf | local7270 | 41,457 |
| │ │ └── TableJoinerImp::getReference | ej(data,tempb035e530587f0000,"ID","securityId") | 2023.11.27 07:53:37.586123907 | 10,374 | ChildOf | local7270 | 41,457 |
| │ ├── SQLQueryImp::getReference |  | 2023.11.27 07:53:37.596826822 | 16,607 | ChildOf | local7270 | 41,457 |
| │ │ └── SQLQueryImp::basicCall |  | 2023.11.27 07:53:37.596858895 | 16,529 | ChildOf | local7270 | 41,457 |
| │ │ └── TableJoiner::getReference |  | 2023.11.27 07:53:37.596885332 | 16,342 | ChildOf | local7270 | 41,457 |
| │ │ └── TableJoinerImp::getReference |  | 2023.11.27 07:53:37.596920858 | 14,428 | ChildOf | local7270 | 41,457 |
| │ ├── SQLQueryImp::getReference |  | 2023.11.27 07:53:37.613520106 | 5,338 | ChildOf | local7270 | 41,457 |
| │ │ └── SQLQueryImp::basicCall |  | 2023.11.27 07:53:37.613543452 | 5,251 | ChildOf | local7270 | 41,457 |
| │ │ └── TableJoiner::getReference |  | 2023.11.27 07:53:37.613565397 | 5,127 | ChildOf | local7270 | 41,457 |
| │ │ └── TableJoinerImp::getReference |  | 2023.11.27 07:53:37.613591427 | 5,067 | ChildOf | local7270 | 41,457 |
| │ ├── SQLQueryImp::getReference |  | 2023.11.27 07:53:37.618933658 | 13,263 | ChildOf | local7270 | 41,457 |
| │ │ └── SQLQueryImp::basicCall |  | 2023.11.27 07:53:37.618955493 | 13,198 | ChildOf | local7270 | 41,457 |
| │ │ └── TableJoiner::getReference |  | 2023.11.27 07:53:37.618973938 | 10,390 | ChildOf | local7270 | 41,457 |
| │ │ └── TableJoinerImp::getReference |  | 2023.11.27 07:53:37.618998447 | 10,167 | ChildOf | local7270 | 41,457 |
| │ ├── SQLQueryImp::getReference |  | 2023.11.27 07:53:37.632284783 | 11,046 | ChildOf | local7270 | 41,457 |
| │ │ └── SQLQueryImp::basicCall |  | 2023.11.27 07:53:37.632305236 | 11,022 | ChildOf | local7270 | 41,457 |
| │ │ └── TableJoiner::getReference |  | 2023.11.27 07:53:37.632330014 | 10,864 | ChildOf | local7270 | 41,457 |
| │ │ └── TableJoinerImp::getReference |  | 2023.11.27 07:53:37.632352650 | 7,955 | ChildOf | local7270 | 41,457 |
| │ ├── SQLQueryImp::getReference |  | 2023.11.27 07:53:37.643674730 | 11,336 | ChildOf | local7270 | 41,457 |
| │ │ └── SQLQueryImp::basicCall |  | 2023.11.27 07:53:37.643693926 | 11,313 | ChildOf | local7270 | 41,457 |
| │ │ └── TableJoiner::getReference |  | 2023.11.27 07:53:37.643714493 | 11,168 | ChildOf | local7270 | 41,457 |
| │ │ └── TableJoinerImp::getReference |  | 2023.11.27 07:53:37.643737539 | 8,961 | ChildOf | local7270 | 41,457 |
| │ ├── SQLQueryImp::getReference | select [147467] ID,col1,col2,ratio1,ratio2,col1 \* ratio1 as col1\_mul,col2 \* ratio2 as col2\_mul from ej(data,tempb035e530587f0000,"ID","securityId") where ID in "tag" + string(1 .. 19) [partition = /TSDBdemo/20231120/Key0/x5] | 2023.11.27 07:53:37.655067979 | 10,913 | ChildOf | local7270 | 41,457 |
| │ │ └── SQLQueryImp::basicCall |  | 2023.11.27 07:53:37.655087126 | 10,874 | ChildOf | local7270 | 41,457 |
| │ │ └── TableJoiner::getReference |  | 2023.11.27 07:53:37.655294579 | 10,551 | ChildOf | local7270 | 41,457 |
| │ │ └── TableJoinerImp::getReference |  | 2023.11.27 07:53:37.655322871 | 10,413 | ChildOf | local7270 | 41,457 |
| │ └── SQLQueryImp::getReference |  | 2023.11.27 07:53:37.666074996 | 6,352 | ChildOf | local7270 | 41,457 |
| │ └── SQLQueryImp::basicCall |  | 2023.11.27 07:53:37.666094885 | 6,317 | ChildOf | local7270 | 41,457 |
| │ └── TableJoiner::getReference |  | 2023.11.27 07:53:37.666112965 | 6,188 | ChildOf | local7270 | 41,457 |
| │ └── TableJoinerImp::getReference |  | 2023.11.27 07:53:37.666133582 | 6,111 | ChildOf | local7270 | 41,457 |
| ├── SQLQueryImp::executeDistributedTasks[firstNonEmptyTask.getValue] |  | 2023.11.27 07:53:37.672891073 | 102 | ChildOf | local7270 | 41,457 |
| ├── SQLQueryImp::executeDistributedTasks[collectFinalColumns] |  | 2023.11.27 07:53:37.673014087 | 72 | ChildOf | local7270 | 41,457 |
| └── SQLQueryImp::executeDistributedTasks[concatenateColumns] |  | 2023.11.27 07:53:37.673112499 | 1,621 | ChildOf | local7270 | 41,457 |

