# addNode

## 语法

`addNode(host, port, alias, [saveConfig=true],
[nodeType='datanode'], [computeGroup])`

## 参数

**host** 是字符串标量或向量，表示新增节点的 IP 地址。

**port** 是正整数标量或向量，表示新增节点的端口号。

**alias** 是字符串标量或向量，表示新增节点的别名。

**saveConfig** 是一个布尔值，表示是否在增加节点的同时，将节点信息保存到 cluster.nodes 配置文件。默认值为 true。

**nodeType** 是字符串标量或向量，表示新增节点类型。支持 'datanode' 和 'computenode' 两个选项。

**computeGroup** 可选参数，字符串标量，用于指定计算节点所属的计算组名称。若未设置此参数，则表示该计算节点未加入任何计算组，不会缓存数据。

注： 参数 *host*, *port*, *alias*,
*nodeType* 的长度须保持一致。

## 详情

增加数据节点或计算节点。仅限 admin 用户调用。

新增加的节点为关闭状态，需要通过 Web 集群管理器或命令行启动它。

注：

在新服务器上增加节点前需要先部署代理节点。详情参考教程： [多服务器集群部署](../../tutorials/multi_machine_cluster_deployment.md)。

## 例子

增加一个别名为 “node1” 的数据节点。

```
addNode("192.168.1.103",8900,"node1");
```

增加一个别名为 “orca4” 的计算节点到计算组 "orca"。

```
addNode("192.168.1.243", 23796, "orca4", true, 'computenode', "orca");
```

