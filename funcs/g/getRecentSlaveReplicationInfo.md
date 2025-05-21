# getRecentSlaveReplicationInfo

## 语法

`getRecentSlaveReplicationInfo()`

## 参数

无

## 详情

查看跨集群异步复制进程中，连接到主集群的各从集群最近一次的任务状态。该函数只能由管理员在主集群的控制节点调用。

返回一个表对象，包含以下字段：

* connectedController：从集群的 controller 的 ip:port。
* allControllersInRaft：若从集群为高可用集群，则将显示 raft 组所有控制节点的 ip:port。
* lastFinishedTaskId：最近一次执行完成的异步复制任务 id。
* lastPullTime：从集群最近一次连接到主集群拉取异步复制任务的时间。

## 例子

```
getRecentSlaveReplicationInfo()
```

输出返回：

| connectedController | allControllersInRaft | lastFinishedTaskId | lastPullTime |
| --- | --- | --- | --- |
| 192.168.2.2:1111 | 192.168.2.2:1111,192.168.2.2:1112,192.168.2.2:1113 | 233 | 2022.11.11T11:11:11 |

