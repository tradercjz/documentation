# existsSubscriptionTopic

## 语法

`existsSubscriptionTopic([server], tableName, [actionName])`

别名：`existSubscriptionTopic`

## 参数

**server** 是一个字符串，表示订阅的流数据表所在节点的别名或远程连接的句柄。如果未指定或者为空字符串，表示流数据所在的服务器是本地实例。

**tableName** 是一个字符串，表示一个共享流数据表的名称。

**actionName** 是一个字符串，表示订阅任务的名称。它可以包含字母，数字和下划线。如果创建订阅时指定了
*actionName*，查询订阅时必须指定 *actionName*。

## 详情

查询共享流数据表的订阅主题是否存在。存在返回 true，不存在则返回 false。

## 例子

```
t=streamTable(1000000:0,`date`time`sym`qty`price`exch,[DATE,TIME,SYMBOL,INT,DOUBLE,SYMBOL])
share t as trades
trades_1=streamTable(1000000:0,`date`time`sym`qty`price`exch,[DATE,TIME,SYMBOL,INT,DOUBLE,SYMBOL])
subscribeTable(tableName=`trades, actionName=`vwap, offset=-1, handler=append!{trades_1})
existsSubscriptionTopic(,`trades,`vwap)
// output
true
```

