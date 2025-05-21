# unsubscribeTable

## 语法

`unsubscribeTable([server], tableName, [actionName], [removeOffset=true],
[raftGroup])`

## 参数

**server** 是表示服务器的别名或与流数据表所在服务器创建的 xdb 连接的字符串。

**tableName** 是表示取消订阅的流数据表名称的字符串。

**actionName** 是表示句柄名称的字符串。它可以包含字母、数字和下划线。如果创建订阅时指定了 *actionName*，取消订阅时必须指定
*actionName*。

**removeOffset** 是一个布尔值，表示是否删除持久化保存的最新一条已经处理订阅数据的偏移量（在 [subscribeTable](../s/subscribeTable.html) 函数中通过指定
*persistOffset* 参数为 true 获得）。

**raftGroup** 是在 [subscribeTable](../s/subscribeTable.html) 中设定的 raft 组的 ID，用于取消相应的订阅高端可用。不设置该参数，则订阅信息仍然保留在 raft
中，再次切换 leader 会重新订阅。

注： `unsubscribeTable` 函数如果指定了
*raftGroup* ，则只能在 leader 上执行。

## 详情

在信息订阅端的节点执行，以停止向信息发布者订阅数据。在调用该命令时，会删除流计算执行线程的队列中未处理的消息。

## 例子

在发布节点发布一张表 trades。

```
t=streamTable(100:0,`date`time`sym`qty`price`exch,[DATE,TIME,SYMBOL,INT,DOUBLE,SYMBOL])
share t as trades
t=NULL
```

在订阅节点上创建表 trades2 来保存发布节点中的表 trades 的数据。

```
t=streamTable(100:0,`date`time`sym`qty`price`exch,[DATE,TIME,SYMBOL,INT,DOUBLE,SYMBOL])
share t as trades2
t=NULL
h=xdb("localhost",8902)
subscribeTable(server=h, tableName="trades", actionName="sub1", handler=trades2);
// output
localhost:8902:node1/trades/sub1
```

取消订阅表 trades 的数据：

```
unsubscribeTable(h, "trades","sub1");
```

