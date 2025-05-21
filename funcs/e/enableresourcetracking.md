# enableResourceTracking

## 语法

`enableResourceTracking()`

## 参数

无

## 详情

在线开启资源跟踪。仅当 *resourceSamplingInterval* 设置为正整数时才能调用该函数。该函数仅限管理员在数据节点上调用。

成功启动资源跟踪后，各个数据节点会根据 *resourceSamplingInterval*
设置的时间间隔获取以下资源：CPU、内存和数据使用量、查询分布式表的信息。

* CPU、内存和数据使用量写入一个 CSV 日志文件，路径是
  `<HomeDir>/resource/hardware.log`。日志记录了以下信息：

  + timestamp：NANOTIMESTAMP 类型的时间戳。
  + userId：登录用户名。
  + cpu：当前用户占用的工作线程数量。
  + memory：内存使用量，当前用户使用的所有变量的内存占用大小。单位是字节。
  + send：单次采集间隔内发送的数据量。单位是字节。
  + recv：单次采集间隔内接收的数据量。单位是字节。需要注意的是，统计的接收数据量可能会有一定误差，最大误差范围在 2KB 以内。
* 查询分布式表的信息写入另一个 CSV
  日志文件，路径是`<HomeDir>/resource/access.log`。目前仅支持 SQL SELECT
  语句，并且在跟踪过程中不会记录非标准 SQL-92 嵌套表连接中的表信息，例如在 ej(ej(t1, t2, `id), t3, `id) 查询中，t1
  和 t2 的信息将不会被记录。日志记录了以下内容：

  + timestamp：NANOTIMESTAMP 类型的时间戳。如果 type 是 sql，则这里记录开始执行 SQL 的时间戳；如果
    type 是 rowCount 或 memUsage，则这里记录的是读出数据的时间戳。
  + rootQueryId：SQL 查询任务的 ID，是分布式 SQL 查询任务的唯一标识符。一个分布式查询会按分区拆分为多个 SQL
    子查询。该 ID 为分布式查询及其拆分出的子查询的根 ID。
  + userId：用户名。
  + database：数据库名。
  + table：表名。
  + type：记录的信息类型，包括3类：sql, rowCount, memUsage。
  + value：

    - 当类型为 sql 时，为 SQL 查询任务的执行次数。该值总是为1。
    - 当类型为 rowCount 时，为读出的行数。
    - 当类型为 memUsage 时，为读出的表的数据量。单位是字节。

注意：这里只记录每次访问表的行数和数据量。例如维度表读入内存后，会记录每次访问该表的行数和数据量，而非第一次读入内存的数据量。

* script：当类型为 sql 时，记录 SQL 脚本，其他类型则为空字符串。

为防止文件大小持续增长，DolphinDB
对这两个文件都采用日志滚动策略，一旦文件大小达到阈值就会生成滚动日志文件。文件名以时间戳作为前缀。例如20231101162302\_access.log，表示
2023.11.01T16:23:02 拆分出来的滚动日志。

系统会根据 *resourceSamplingLogRetentionTime*
的配置值自动清理资源跟踪日志。此自动清理机制不受资源跟踪功能的开启或关闭影响。

相关函数：[disableResourceTracking](../d/disableresourcetracking.md)

