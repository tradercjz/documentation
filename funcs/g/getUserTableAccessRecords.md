# getUserTableAccessRecords

## 语法

`getUserTableAccessRecords([from=0], [to])`

## 参数

**from** 整型或时间类型，表示查询的起始时间点。默认值为0，表示查询从1970.01.01零点开始的记录。

**to** 整型或时间类型，表示查询的结束时间点。默认为空，表示查询到目前时间点为止的记录。

*from* 必须小于等于 *to*。

## 详情

从已保存记录了分布式表查询信息的日志中，提取指定时间段内的查询日志。返回一个表。含以下字段：

* timestamp：NANOTIMESTAMP 类型的时间戳。如果 type 是 sql，则这里记录开始执行 SQL 的时间戳；如果 type 是
  rowCount 或 memUsage，则这里记录的是读出数据的时间戳。
* rootQueryId：SQL 查询任务的 ID，是分布式 SQL 查询任务的唯一标识符。一个分布式查询会按分区拆分为多个 SQL 子查询。该 ID
  为分布式查询及其拆分出的子查询的根 ID。
* userid：用户名。
* database：数据库名。
* table：表名。
* type：记录的信息类型，包括3类：sql, rowCount, memUsage。
* value：

  + 当类型为 sql 时，为 SQL 查询任务的执行次数。该值总是为1。
  + 当类型为 rowCount 时，为 SQL 执行时存储引擎返回的表的行数。
  + 当类型为 memUsage 时，为查询结果占用的内存大小。单位是字节。
* script：当类型为 sql 时，记录 SQL 脚本，其他类型则为空字符串。

该函数仅限管理员在数据节点上调用。

## 例子

```
getUserTableAccessRecords(2023.12.30T09:18:35.894150296,2023.12.30T09:18:35.894538439)
// output
timestamp	                    rootQueryId	                         userId       database	    table     type	value    script
2023.12.30T09:18:35.894150296	e892855b-7843-1492-0140-a85810662006	admin	dfs://rangedb	pt	sql	1	select count(x) as count_x from pt
2023.12.30T09:18:35.894497304	e892855b-7843-1492-0140-a85810662006	admin	dfs://rangedb	pt	rowCount   43
2023.12.30T09:18:35.894501600	e892855b-7843-1492-0140-a85810662006	admin	dfs://rangedb	pt	memUsage   516
```

