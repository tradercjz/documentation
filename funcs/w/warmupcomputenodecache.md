# warmupComputeNodeCache

## 语法

`warmupComputeNodeCache(sqlObj, [parallelism])`

## 参数

**sqlObj** SQL 元代码，表示预热的数据。

**parallelism** 可选参数，正整数，表示分配给该任务的线程数上限。

## 详情

创建数据预热任务，将指定数据缓存至计算组。

返回该任务的 jobId。

## 例子

```
warmupComputeNodeCache(sqlObj=<select * from loadTable("dfs://test","pt") where date>=2025.04.01>, parallelism=3)
```

