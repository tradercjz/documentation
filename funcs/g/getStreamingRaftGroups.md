# getStreamingRaftGroups

## 语法

`getStreamingRaftGroups()`

## 参数

无

## 详情

获取当前节点所在的流数据 Raft 组的信息。返回的结果是一个表，第一列表示 Raft 组的 id，第二列表示 Raft
组包含的数据节点/计算节点信息。

## 例子

```
getStreamingRaftGroups();
```

| id | sites |
| --- | --- |
| 12 | 192.168.1.135:18102:NODE1,192.168.1.135:18103:NODE2,192.168.1.135:18104:NODE3 |
| 11 | 192.168.1.135:18102:NODE1,192.168.1.135:18103:NODE2,192.168.1.135:18105:NODE4 |

使用以下脚本可以获取当前集群所有流数据 Raft 组的信息。

```
select id,sites from pnodeRun(getStreamingRaftGroups) where isDuplicated([id,sites],FIRST)=false;
```

