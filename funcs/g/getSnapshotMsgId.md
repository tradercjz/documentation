# getSnapshotMsgId

## 语法

`getSnapshotMsgId(engine)`

## 参数

**engine** 是流数据引擎，即 [createReactiveStateEngine](../c/createReactiveStateEngine.html) 等函数返回的抽象表对象。

## 详情

用于订阅断开后重新订阅时，获取指定流数据引擎的最近一个快照（snapshot）的 msgId。启用 snapshot
后，重订阅时，`subscribeTable` 函数的 *offset* 参数设置为
getSnapshotMsgId(engine)+1，引擎会加载 snapshot，并从 getSnapshotMsgId(engine)
之后一条消息开始重新订阅。

