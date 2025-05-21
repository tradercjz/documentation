# getRecentJobs

## 语法

`getRecentJobs([n])`

## 参数

**n** 是一个可选参数，为正整数。 无参数时返回所有 Jobs。

## 详情

取得本地节点上最近 *n* 个批处理作业的状态。

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

详情参考：[BatchJobManagement](../../sys_man/BatchJobManagement.html)。

## 例子

```
def jobDemo(n){
   s = 0
   for (x in 1 : n) {
       s += sum(sin rand(1.0, 100000000)-0.5)
       print("iteration " + x + " " + s)
   }
   return s
};

submitJob("jobDemo1","job demo", jobDemo, 100);
submitJob("jobDemo2",, jobDemo, 10);
getRecentJobs(10);
```

| node | userID | jobId | rootJobId | jobDesc | priority | parallelism | clientIp | clientPort | receivedTime | startTime | endTime | errorMsg |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| local8848 | admin | jobDemo1 | 859c3c53-c9ad-1abc-41f5-6dbaaf8003e9 | job demo | 0 | 1 | 127.0.0.1 | 61,436 | 2024.02.29 10:18:07.160 |  |  |  |
| local8848 | admin | jobDemo2 | 5515626b-0dd9-e7ac-466c-d8b4d1fff2d1 | jobDemo | 0 | 1 | 127.0.0.1 | 61,436 | 2024.02.29 10:18:07.164 |  |  |  |

