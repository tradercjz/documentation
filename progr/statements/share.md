# share

## 语法

`share <table> as <shared name>`

或

`share <obj> as <db>.<table name> on <column
name>`

或

`share <engine> as <engine name>`

## 详情

* 第一种用法：节点内的会话共享

将一个表共享到当前节点的所有会话中。包括表在内的局部对象在其他会话中是不可见的，需要通过共享才能在其他会话中可见。

共享表名必须与所有其他会话中的普通表名不同。DolphinDB 服务器可以最多定义 65535 张共享表。

* 第二种用法：节点间的分布式表共享

在分布式系统中表的共享。分布式表通过指定的列实现共享。在多个节点使用 share 命令保存一张共享表。

请注意，不可以将同一个流数据表通过修改共享变量名称的方式共享2次及以上。

* 第三种用法：为引擎添加写入锁

通过 share
语句，可以为引擎添加写入锁，从而允许当前节点的所有会话并发地向引擎写入数据（要求引擎共享后的名称和引擎名称相同）。注意：在其它会话中，需要通过函数
`getStreamEngine` 来获取引擎的句柄。

## 例子

* 第一种用法

```
t1= table(1 2 3 as id, 4 5 6 as value);
share t1 as table1;
```

* 第二种用法

首先配置两个节点。在一个节点的命令行窗口输入以下命令 (node 8500)：

```
dolphindb -logFile dolphindb.log0 -maxMemSize 50 -localSite localhost:8500:local8500 -sites localhost:8500:local8500,localhost:8501:local8501
```

在另一个节点的命令行窗口输入以下命令 (node 8501)：

```
dolphindb -logFile dolphindb.log1 -maxMemSize 50 -localSite localhost:8501:local8501 -sites localhost:8500:local8500,localhost:8501:local8501
```

然后在 node 8500 上执行以下脚本：

```
TickDB = database("C:/DolphinDB/Data/shareEx", RANGE, `A`M`ZZZZ, `local8500`local8501)
t=table(rand(`AAPL`IBM`C`F,100) as sym, rand(1..10, 100) as qty, rand(10.25 10.5 10.75, 100) as price)
share t as TickDB.Trades on sym;
```

在 node 8501 上执行以下脚本：

```
TickDB = database("C:/DolphinDB/Data/shareEx", RANGE, `A`M`ZZZZ, `local8500`local8501)
t=table(rand(`WMI`PG`TSLA,100) as sym, rand(1..10, 100) as qty, rand(10.25 10.5 10.75, 100) as price)
share t as TickDB.Trades on sym;
```

接下来就可以使用 Trades 或 TickDB.Trades 来访问表格。在两个节点上我们都可以运行以下脚本。

```
select count(*) from Trades;
```

| count |
| --- |
| 200 |

* 第三种用法

在一个会话中定义一个引擎，且通过 share 语句进行共享。

```
trades = streamTable(1:0, `time`sym`price, [TIMESTAMP, SYMBOL, DOUBLE])
share table(100:0, `sym`time`factor1, [SYMBOL, TIMESTAMP, DOUBLE]) as outputTable
engine = createReactiveStateEngine(name="test", metrics=[<time>, <mavg(price, 3)>], dummyTable=trades, outputTable=outputTable, keyColumn=`sym)
//通过 share 语句，将引擎 test 共享后，便可以对引擎进行并发写入
share engine as "test"
```

当前节点所连接的任意一个会话中执行以下脚本：

```
//第一个自定义函数，向 engine 写入数据
def write1(mutable engine) {
	N = 10
	for (i in 1..500) {
		data = table(take(now(), N) as time, take(`A`B, N) as sym, rand(10.0, N) as price)
		getStreamEngine(engine).append!(data)
	}
}
//第二个自定义函数，向 engine 写入数据
def write2(mutable engine) {
	N = 10
	for (i in 1..500) {
		data = table(take(now(), N) as time, take(`C`D, N) as sym, rand(10.0, N) as price)
		getStreamEngine(engine).append!(data)
	}
}
//提交作业，使 write1 和 write2 同时向引擎写入数据
submitJob("j1", "j1", write1, "test")
submitJob("j2", "j2", write2, "test")
//查看输出表中数据行数为 10000，正好是 write1 和 write2 写入的数据量之和。
select count(*) from outputTable
//output
10000
```

相关文档：[取消变量](../objs/undef_var.md), [undef](../../funcs/u/undef.md)

