# getConsoleJobs

## 语法

`getConsoleJobs()`

## 参数

无

## 详情

返回本地节点上正在执行的交互式任务的描述信息。

包含以下字段：

| 参数 | 含义 |
| --- | --- |
| node | 本地节点的别名。 |
| userID | 用户 ID。 |
| rootJobId | 系统中作业的唯一标识。 |
| jobType | 作业类型。 |
| desc | 作业描述。 |
| priority | 作业的优先级，为 0-9 之间的整数。 |
| parallelism | 作业的并行度，即分配给该作业的线程数上限。 |
| receiveTime | 作业被节点接收的时间。 |
| sessionId | 发起作业的会话 ID。 |
| remoteIP | 发起作业的客户端 IP。 |
| remotePort | 发起作业的客户端的端口号。 |
| totalTasks | 作业分解出的总任务数。 |
| finishedTasks | 作业分解出的任务中已经完成的任务数。 |
| runningTask | 作业分解出的任务中正在执行的任务数。 |
| firstTaskStartTime | 第一个任务的开始时间。 |
| latestTaskStartTime | 最近一个任务的开始时间。 |
| queue | 任务队列类型： normal queue（0级 worker 队列），web queue（web 端 worker 队列），local task queue（1~5级 worker 队列），batchJob queue（批作业队列）。 |

## 例子

```
getConsoleJobs()
```

| node | userID | rootJobId | jobType | desc | priority | parallelism | receiveTime | sessionId | remoteIP | remotePort | totalTasks | finishedTasks | runningTask | firstTaskStartTime | latestTaskStartTime | queue |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P2-node1 | admin | 26681f9c-f914-81ae-47dd-8b8e6e106c48 | script | getConsoleJobs() | 4 | 2 | 2022.01.05T11:05:06.778 | 1823289176 | 127.0.0.1 | 50595 | 1 | 0 | 1 | 2022.01.05T11:05:06.778 | 2022.01.05T11:05:06.778 | normal queue |

