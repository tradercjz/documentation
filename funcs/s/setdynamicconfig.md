# setDynamicConfig

## 语法

`setDynamicConfig(configName, configValue)`

## 参数

**configName** 字符串标量，表示待修改的配置项名。

**configValue** 标量，表示待修改的配置项的值。

## 详情

在线修改指定的配置项。无返回值。

注： 此命令修改的配置值在系统重启后将失效。若需永久生效，请更新对应的配置文件。

如下为支持修改的配置项（详情请参考文档 [DolphinDB-功能配置](../../db_distr_comp/cfg/function_configuration.md)）：

*enableMultiThreadMerge*, enableNullSafeJoin, *logLevel*,
*maxBlockSizeForReservedMemory*, *maxConnections*,
*memLimitOfQueryResult*, *memLimitOfTaskGroupResult*,
*maxMemSize*, *maxPartitionNumPerQuery*, *memLimitOfTempResult*,
*OLAPCacheEngineSize*, *recoveryWorkers*, *reservedMemSize*,*dfsChunkNodeHeartBeatTimeout*, *TSDBCacheEngineSize*,
*TSDBVectorIndexCacheSize*, *memLimitOfAllTempResults*.

## 例子

```
setDynamicConfig("maxMemSize", 8);
setDynamicConfig("maxConnections", 4096);
```

**相关信息**

* [getDynamicConfig](../g/getdynamicconfig.html "getDynamicConfig")

