# setDatabaseForClusterReplication

## 语法

`setDatabaseForClusterReplication(dbHandle, option)`

## 参数

`dbHandle`：一个分布式数据库句柄。

`option`：布尔值，表示开启（true）/关闭（false）指定数据库的异步复制，默认为 false。

## 详情

开启/关闭分布式数据库的集群间的异步复制。该函数只能由管理员在主集群的数据节点调用。

相关函数：[getDatabaseClusterReplicationStatus](../g/getDatabaseClusterReplicationStatus.html)

