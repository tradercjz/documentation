# getJobStat

## 语法

`getJobStat()`

## 参数

无

## 详情

监控正在执行或者队列中的作业和任务的数量。返回一个字典，其 key 的含义为：

| 参数 | 含义 |
| --- | --- |
| queuedLocalTasks | 等待执行的本地任务数。 |
| runningLocalTasks | 正在执行的本地任务数。 |
| queuedJobs | 队列中的作业数。 |
| runningJobs | 正在执行的作业数。 |
| queuedRemoteTasks | 发送到远程执行的任务数。 |

## 例子

```
getJobStat();
```

返回：

```
queuedLocalTasks->0
runnningJobs->0
queuedRemoteTasks->0
queuedJobs->0
runningLocalTasks->0
```

