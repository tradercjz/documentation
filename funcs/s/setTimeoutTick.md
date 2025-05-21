# setTimeoutTick

## 语法

`setTimeoutTick(tick)`

别名： setDfsChunkNodeHeartBeatTimeoutTick

## 参数

**tick** 一个正整数，表示超时时间，单位为秒。

## 详情

动态设置控制节点判断数据节点是否在线的超时时间。该命令只能由管理员在控制节点上执行。若为高可用集群，则需要在 raft 组的每个控制节点上执行该命令。

注： 此命令修改的配置值在集群重启后将失效。若需要配置值永久生效，请更改配置文件中的
*dfsChunkNodeHeartBeatTimeout* 。

