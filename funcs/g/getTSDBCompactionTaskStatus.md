# getTSDBCompactionTaskStatus

## 语法

`getTSDBCompactionTaskStatus([count])`

## 参数

**count** 非负整数。设置后，将返回最近的 *count* 条合并任务的记录。默认值为 0，返回每个
volume 中最新的 256 个已完成的合并任务以及所有未完成的合并任务。

## 详情

返回一个表，显示 TSDB 引擎 level file 合并操作任务的状态。该函数只能在数据节点调用。

状态表包含以下几列：

| 列名 | 含义 |
| --- | --- |
| volume | 发生合并的文件所在的磁盘卷路径。由配置项 *volumes* 进行配置。 |
| level | 当前合并的 level file 层级。 |
| chunkId | 发生合并操作的 chunk 的 ID。 |
| tableName | 发生合并操作的数据表的物理表名。 |
| files | 参与当前合并任务的 level file。 |
| force | 是否由 `triggerTSDBCompaction` 强制触发。 |
| receivedTime | 当前合并任务进入任务队列的时间戳。 |
| startTime | 当前合并任务开始执行的时间戳。 |
| endTime | 当前合并任务执行结束的时间戳。 |
| errorMessage | 报错信息。如果失败，则显示失败的原因；否则显示空。 |

## 例子

```
getTSDBCompactionTaskStatus()
```

| volume | level | chunkId | tableName | files | force | receivedTime | startTime | endTime | errorMessage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /home/DolphinDB/DolphinDB\_Linux64\_V2.00.9/server/clusterDemo/data/node1/storage | 0 | e0e00bc2-b81e-6eb9-4d01-7bb17fb39595 | pt\_2 | 0\_00000006,0\_00000011, | true | 2023.06.22T12:47:32.009 | 2023.06.22T12:47:32.010 | 2023.06.22T12:47:32.182 |  |
| /home/DolphinDB/DolphinDB\_Linux64\_V2.00.9/server/clusterDemo/data/node1/storage | 1 | a9dfccad-cec1-0786-480a-9ae809481a8b | pt\_2 | 0\_00000003,0\_00000007, | true | 2023.06.22T12:47:32.010 | 2023.06.22T12:47:32.182 | 2023.06.22T12:47:32.326 |  |
| /home/DolphinDB/DolphinDB\_Linux64\_V2.00.9/server/clusterDemo/data/node1/storage | 1 | 331324ce-b49f-94ac-4da8-a4bcf6c34e1c | pt\_2 | 0\_00000004,0\_00000010, | true | 2023.06.22T12:47:32.010 | 2023.06.22T12:47:32.326 | 2023.06.22T12:47:32.451 |  |
| /home/DolphinDB/DolphinDB\_Linux64\_V2.00.9/server/clusterDemo/data/node1/storage | 2 | f3597e0f-6ad9-6eb6-45c8-d42adc5c50f7 | pt\_2 | 0\_00000002,0\_00000008, | true | 2023.06.22T12:47:32.010 | 2023.06.22T12:47:32.451 | 2023.06.22T12:47:32.527 |  |
| /home/DolphinDB/DolphinDB\_Linux64\_V2.00.9/server/clusterDemo/data/node1/storage | 2 | d36ac640-3428-069b-4382-0b9608b94d17 | pt\_2 | 0\_00000005,0\_00000009, | true | 2023.06.22T12:47:32.010 | 2023.06.22T12:47:32.527 | 2023.06.22T12:47:32.616 |  |
| /home/DolphinDB/DolphinDB\_Linux64\_V2.00.9/server/clusterDemo/data/node1/storage | 2 | e0e00bc2-b81e-6eb9-4d01-7bb17fb39595 | pt\_2 | 0\_00000016,0\_00000021, | true | 2023.06.22T12:47:33.058 | 2023.06.22T12:47:33.058 | 2023.06.22T12:47:33.151 |  |

相关函数：[triggerTSDBCompaction](../t/triggerTSDBCompaction.html)

