# getSupportBundle

## 语法

`getSupportBundle([dir])`

## 参数

**dir** 可选参数，用于指定存储路径。若不指定该参数，单节点环境下默认存储至 <HomeDir>（可通过 [getHomeDir](getHomeDir.html) 查看
<HomeDir>）；集群环境下默认存储至 <HomeDir> 同级目录。

## 详情

生成一个包含所有配置信息的文件，并返回文件路径。该函数只能在数据节点/计算节点调用。

配置文件包含以下信息：

| 模块名 | 含义 | 信息来源 |
| --- | --- | --- |
| VERSION | server 的版本信息。 | version() |
| CONFIGS | 配置信息。单机环境下，返回单节点的配置信息；集群环境下，包含集群、控制节点、 和数据节点/计算节点的配置。 | 单机: dolphindb.cfg 集群: cluster.cfg, cluster.nodes, controller.cfg |
| DB AND TABLE SCHEMA | 所有数据库和表的结构。 | schema |
| LICENSE AND MACHINE INFO | license、机器核数和内存信息。 节点绑定的 CPU 内核绑定和端口信息。 | 许可证: dolphindb.lic |
| OLAP CACHE ENGINE STATUS | OLAP 引擎 cache Engine 的状态信息，包含各节点的内存信息以及当前节点的状态表。 | pnodeRun(getOLAPCacheEngineSize) pnodeRun(getOLAPCacheEngineStat) |
| TSDB META | TSDB 引擎下所有 chunk 的元数据。 | pnodeRun(getTSDBMetaData) |
| REDO LOG GC STATUS | 事务 redo log 回收的状态。 | pnodeRun(getRedoLogGCStat) |
| TRANSACTION STATUS | 事务的状态。 | pnodeRun(getTransactionStatus) |
| TABLETS META | 集群中行数最多的前100个 chunk 的元数据信息。 | select top 100 \* from pnodeRun(getTable tsMeta{“%”,”%”,false,-1}) order by rowNum desc |
| ANOMALOUS CHUNK STATUS (only in cluster mode) | 处于异常状态的 chunk 信息。异常状态包含处于 recovery 状态，版本号不一致， 副本数不一致等。 | getClusterChunksStatus() |

## 例子

```
getSupportBundle()
// output
/home/dolphindb/server/getSupportBundle.1655869793424

getSupportBundle("/home/dolphindb/sup")
// output
/home/dolphindb/sup/getSupportBundle.1655869853178
```

