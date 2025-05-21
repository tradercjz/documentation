# setDatanodeRestartInterval

## 语法

`setDatanodeRestartInterval(interval)`

## 参数

**interval** 非负整数，表示时间，单位为秒。

## 详情

在线设置控制节点自动重启计算节点/数据节点的功能。该命令只能由管理员在控制节点上调用。

* 若 *interval*=0，则控制节点不会自动重启数据节点/计算节点。
* 若 *interval*>0，则当节点离线时长超过 interval 时，控制节点会自动启动该节点。

注：

* 该命令并不会改变配置文件中的 datanodeRestartInterval 值。因此，一旦控制节点重启，通过该命令设置的 interval
  将失效。
* 高可用环境下，Leader 节点通过该命令设置的 interval 并不会同步到其它 Follower 节点。

相关函数：[getDatanodeRestartInterval](../g/getDatanodeRestartInterval.html)

