# getQueryStatus

## 语法

`getQueryStatus()`

## 参数

无

## 详情

获取由当前节点发起且正在执行的查询任务状态，返回一个表对象，包含以下几列：

* id：表示到该查询任务为止，系统已执行的查询任务总数。
* sessionId：任务发起会话的 id。请注意，无法获取通过 `submitJob`
  提交的查询任务的 sessionId。
* userId：任务发起会话的用户名。
* query：原始查询语句中主要的查询信息。
* startTime：查询任务开始的时间戳。
* elapsedTimeInMs：查询任务已经经过的时间，单位为毫秒。
* memoryUsage：查询过程中变量和结果所占用的内存空间，单位为字节。
* totalTaskCount：查询子任务总数。
* completedTaskCount：已完成的查询子任务数。
* percentComplete：已完成的查询子任务占比。

该函数只能在任务发起节点上调用。

## 例子

```
getQueryStatus();
```

| id | sessionId | userId | query | startTime | elapsedTimeInMs | memoryUsage | totalTaskCount | completedTaskCount | percentComplete |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 1166953221 | admin | select ticker, id, x from pt | 2022.06.14 08:15:00.606 | 1052 | 184550000 | 4 | 1 | 0.25 |

