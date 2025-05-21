# getComputeNodeCacheWarmupJobStatus

## 语法

`getComputeNodeCacheWarmupJobStatus([jobId])`

## 参数

**jobId** 可选参数，字符串标量或向量，表示预热任务的 jobId。

## 详情

查询指定 *jobId* 的数据预热任务状态。省略 *jobId* 时返回所有预热任务的状态。

返回一个表，包括以下字段：

* jobId：数据预热任务的 jobId。
* tableName：任务对应的库表信息。
* jobStatus：任务状态，包括 Pending（待执行），Running（正在执行），Finished（已完成），Error（发生错误）。
* parallelism：并行度，其中 -1 代表该任务没有并行度限制。
* elapsed：任务的执行时长，单位为 ms。
* errMsg：错误信息。

## 例子

```
getComputeNodeCacheWarmupJobStatus()
```

