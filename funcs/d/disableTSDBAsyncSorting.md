# disableTSDBAsyncSorting

## 语法

`disableTSDBAsyncSorting()`

## 参数

无

## 详情

TSDB 写入 Cache Engine 中的数据会根据 *sortColumns*
排序。写入任务和排序任务可以同步或异步进行，该命令用于关闭异步进行数据排序的功能。只能由管理员在数据节点上执行。

**相关信息**

* [enableTSDBAsyncSorting](../e/enableTSDBAsyncSorting.html "enableTSDBAsyncSorting")

