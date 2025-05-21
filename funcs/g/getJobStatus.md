# getJobStatus

## 语法

`getJobStatus(jobId)`

## 参数

**jobId** 是批处理作业的 ID，是一个字符串。

## 详情

取得批处理作业返回的对象。

返回一个表，包含以下字段：

| 参数 | 含义 |
| --- | --- |
| node | 本地节点的别名。 |
| userID | 提交作业任务的用户 ID。 |
| jobId | 在提交批作业时指定的作业名。 |
| rootJobId | 系统中作业的唯一标识。 |
| jobDesc | 用于描述作业的字符串。 |
| priority | 作业的优先级，为 0-9 之间的整数。 |
| parallelism | 作业的并行度，即分配给该作业的线程数上限。 |
| clientIp | 发起作业任务的客户端 IP。 |
| clientPort | 发起作业任务的客户端端口号。 |
| receivedTime | 作业接收的时间，为 TIMESTAMP 类型。 |
| startTime | 作业开始时间，为 TIMESTAMP 类型。 |
| endTime | 作业结束时间，为 TIMESTAMP 类型。 |
| errorMsg | 报错信息。 |

详情请参考 [BatchJobManagement](../../sys_man/BatchJobManagement.md)。

## 例子

```
def job1(n){
   s = 0
   for (x in 1 : n) {
       s += sum(sin rand(1.0, 100000000)-0.5)
       print("iteration " + x + " " + s)
   }
   return s
}

job1_ID=submitJob("job1_ID","", job1, 100);
getJobStatus(job1_ID);
```

返回：

| node | userID | jobId | rootJobId | jobDesc | priority | parallelism | clientIP | clientPort | receivedTime | startTime | endTime | errorMsg |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| controller2 | guest | job1\_ID20210428... | b9263bfd-50b8-70b3-9845-e595f9b0c506 | job1 | 4 | 1 | 115.204.199.28 | 61537 | 2023.12.12T02:50:32.598 |  |  |  |

在作业的状态中，*EndTime* 是空的。这意味着作业还在执行中。作业完成后，就能在状态中看到 EndTime。

```
getJobStatus(job1_ID);
```

| node | userID | jobId | rootJobId | jobDesc | priority | parallelism | clientIP | clientPort | receivedTime | startTime | endTime | errorMsg |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| controller2 | guest | job1\_ID20210428... | b9263bfd-50b8-70b3-9845-e595f9b0c506 | job1 | 4 | 1 | 115.204.199.28 | 61537 | 2023.12.12T02:50:32.598 | 2023.12.12T02:50:32.599 | 2023.12.12T02:52:32.477 |  |

