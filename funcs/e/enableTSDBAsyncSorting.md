# enableTSDBAsyncSorting

## 语法

`enableTSDBAsyncSorting()`

## 参数

无

## 详情

TSDB 写入 Cache Engine 中的数据会根据 *sortColumns*
排序。写入任务和排序任务可以同步或异步进行，该命令用于开启异步进行数据排序的功能。异步线程数量由配置参数
*TSDBAsyncSortingWorkerNum* 指定。 只能由管理员在数据节点上执行。请注意，执行该命令前请确认
*TSDBAsyncSortingWorkerNum* 配置值大于0。

因异步数据排序能提高数据写入性能，若 TSDB 引擎所在服务器 CPU 核数较多，建议在进行数据写入前，执行该命令开启异步数据排序功能。

相关函数：[disableTSDBAsyncSorting](../d/disableTSDBAsyncSorting.md)

