# getBackupStatus

## 语法

`getBackupStatus([userName])`

## 参数

**userName** 表示用户名的字符串。

## 详情

查看指定用户的 backup/restore 任务。返回一个表，每一行为一个任务的信息。包含以下字段：

* userName：用户名。
* type：备份或恢复的类型。

  + BACKUP\_BY\_SQL/RESTORE\_BY\_SQL： 表示使用 SQL
    元代码方式的备份/恢复。
  + BACKUP\_BY\_COPY\_FILE/RESTORE\_BY\_COPY\_FILE：表示使用拷贝文件方式的备份/恢复。
* startTime：任务开始的时间。
* dbName：数据库的路径。
* tableName：表的名称。
* totalPartitions：待备份/恢复的分区数量。
* completedPartitions：完成备份/恢复的分区数量。
* percentComplete：任务完成百分比。
* endTime：若任务已完成，则返回任务完成的时间，否则返回预估完成时间。
* completed ：任务完成状态。若全部完成，则为1，否则为0。

注：

* 一次 backup 执行过程产生的任务数与其备份的分区的个数相同。
* 管理员调用该函数时，若指定了 *userName*，则返回指定用户的
  backup/restore 任务；否则返回所有用户的 backup/restore 任务。
* 非管理员调用该函数时，只能返回当前用户的 backup/restore 任务。

## 例子

```
getBackupStatus()
```

| userName | type | startTime | dbName | tableName | totalPartitions | completedPartitions | percentComplete | endTime | completed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| u1 | BACKUP\_BY\_COPY\_FILE | 2022.09.21T17:18:04.264 | dfs://valuedb | pt | 1 | 1 | 100 | 2022.09.21T17:18:04.269 | 1 |
| u1 | BACKUP\_BY\_SQL | 2022.09.21T17:13:04.344 | dfs://valuedb | pt | 4 | 4 | 100 | 2022.09.21T17:13:04.413 | 1 |
| u1 | BACKUP\_BY\_COPY\_FILE | 2022.09.21T17:18:04.264 | dfs://valuedb | pt1 | 1 | 1 | 100 | 2022.09.21T17:18:04.265 | 1 |
| admin | BACKUP\_BY\_COPY\_FILE | 2022.09.21T16:47:42.798 | dfs://valuedb | pt | 4 | 4 | 100 | 2022.09.21T16:47:42.859 | 1 |
| admin | BACKUP\_BY\_COPY\_FILE | 2022.09.21T16:37:33.725 | dfs://valuedb | pt | 4 | 4 | 100 | 2022.09.21T16:37:33.790 | 1 |
| admin | BACKUP\_BY\_SQL | 2022.09.21T15:10:05.016 | dfs://compoDB | pt2 | 10 | 10 | 100 | 2022.09.21T15:10:05.075 | 1 |

