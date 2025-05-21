# getRunningQueries

## 语法

`getRunningQueries()`

## 参数

无

## 详情

获取本地节点上正在执行的查询任务的描述信息。

返回一张表，包含以下字段：

| 参数 | 含义 |
| --- | --- |
| userID | 用户 ID 。 |
| sessionID | 发起查询的会话 ID。 |
| jobID | 系统中查询任务的唯一标识。 |
| rootID | 当前任务所属根任务的 jobID。 |
| level | 任务的级别。根任务的 level 为 0，其分解的子任务 level 为 1，该子任务分解的子任务 level 为 2，以此类推。 |
| startTime | 查询任务开始时间，为 NANOTIMESTAMP 类型。 |
| endTime | 查询任务结束时间，为 NANOTIMESTAMP 类型。 |
| jobDesc | 查询语句描述。 |
| errorMsg | 报错信息。 |
| remoteIP | 发起查询的客户端 IP。 |

使用该函数之前，必须设定参数 *perfMonitoring* = 1 来启用性能监控。

## 例子

```
getRunningQueries();
```

| userID | sessionID | jobID | rootID | level | startTime | endTime | jobDesc | errorMsg | remoteIP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| admin | 738481026 | 88e738a8-a749-4dcb-9cfe-740df2d9ce7d | 88e738a8-a749-4dcb-9cfe-740df2d9ce7d | 0 | 2019.02.07T19:02:26.809905612 |  | select count(\*) as count from pt |  | 192.168.1.106 |

**相关信息**

* [getCompletedQueries](getCompletedQueries.html "getCompletedQueries")

