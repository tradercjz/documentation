# getTraces

## 语法

`getTraces()`

## 参数

无

## 详情

获取跟踪信息，返回一张表，包含以下几列：

* time：客户端将脚本发送给 server 的时间戳。
* scripts：客户端发送给 server 端执行的脚本。部分脚本（如下例：objs11
  等）是客户端调用的脚本，可以忽略。
* traceId：记录 SQL Trace 信息的 id，配合 [viewTraceInfo](viewTraceInfo.md) 函数可以展示该脚本完整的跟踪信息。
* sessionId：发起 SQL Trace 的会话的 id。

## 例子

```
getTraces();
```

| time | scripts | traceId | sessionId |
| --- | --- | --- | --- |
| 2022.09.26T08:50:48.486114674 | setTraceMode(false) | db80c71c-51e4-4fa5-524c-8230a9e14259 | 2,333,906,441 |
| 2022.09.26T08:50:45.202118926 | [n,db,[0, 0]] | 078cafbc-003c-6495-e248-58f111d973c4 | 2,333,906,441 |
| 2022.09.26T08:50:45.196684636 | objs11 | 50e9d859-2d4d-368d-c641-71f239325926 | 2,333,906,441 |
| 2022.09.26T08:50:45.150871346 | ``` login("admin", "123456") if(existsDatabase("dfs://tedb")){	 	dropDatabase("dfs://tedb") } n=30 ticker = rand(`MSFT`GOOG`FB`ORCL`IBM`PPT`AZHILM`ANZ,n); id = rand(`A`B`C, n) x=rand(1.0, n) t=table(ticker, id, x) select *, x>0.5 as x1 from t db=database(directory="dfs://tedb", partitionType=HASH, partitionScheme=[STRING, 5]) pt = db.createPartitionedTable(t, `pt, `ticker) pt.append!(t) update t set x = 1 where id = `A ``` | 64ae3ac9-3963-6eab-c244-48bd1c0adc80 | 2,333,906,441 |
| 2022.09.26T08:50:37.921672908 | objs11 | a2c39b23-8260-1cb7-ab4b-205429c0c60d | 2,333,906,441 |

