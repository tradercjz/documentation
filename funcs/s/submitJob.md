# submitJob

## 语法

`submitJob(jobId, jobDesc, jobDef, args...)`

## 参数

**jobId** 是作业的 ID，是字符串类型。

**jobDesc** 是字符串，用于描述作业。

**jobDef** 是用于定义作业的本地函数。请注意，该参数是一个函数对象，而不是表示函数名的字符串，因此不可使用引号。

**args...** 是函数的参数。如果函数没有参数，可以不指定。

## 详情

把批处理作业提交到本地节点并且返回作业的 ID。如果要把批处理作业提交到远程节点，需要结合使用
`rpc` 或 [remoteRun](../r/remoteRun.md)
函数。详情请参考 [BatchJobManagement](../../sys_man/BatchJobManagement.md)。

## 例子

把作业提交到本地节点：

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
// output
jobDemo1

getJobStatus("jobDemo1");
```

| node | userID | jobId | rootJobId | jobDesc | priority | parallelism | clientIp | clientPort | receivedTime | startTime | endTime | errorMsg |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| local8848 | guest | jobDemo1 | d1d76cad-d46f-338c-4179-21cface3ce7c | job demo | 4 | 2 | 127.0.0.1 | 62016 | 2023.12.12T17:52:01.576 | 2023.12.12T17:52:01.585 |  |  |

在作业的状态中，endTime 为空，这意味着作业还在执行中。作业完成后，就能在状态中看到 endTime 的值。

```
getJobStatus("jobDemo1");
```

| node | userID | jobId | rootJobId | jobDesc | priority | parallelism | clientIp | clientPort | receivedTime | startTime | endTime | errorMsg |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| local8848 | guest | jobDemo1 | d1d76cad-d46f-338c-4179-21cface3ce7c | job demo | 4 | 2 | 127.0.0.1 | 62016 | 2023.12.12T17:52:01.576 | 2023.12.12T17:52:01.585 | 2023.12.12T17:53:23.204 |  |

```
getJobMessage("jobDemo1");

// output
2023-12-12 17:52:01.586399 Start the job [jobDemo1]: job demo
2023-12-12 17:52:02.550241 iteration 1 1094.345887943766229
2023-12-12 17:52:03.417464 iteration 2 3167.431462436133642
2023-12-12 17:52:04.463558 iteration 3 5265.929786668073575
...
2023-12-12 17:53:21.609843 iteration 97 25681.096442654183192
2023-12-12 17:53:22.401263 iteration 98 25609.952331757223873
2023-12-12 17:53:23.204495 iteration 99 23660.316042780508723
2023-12-12 17:53:23.204495 The job is done.

getJobReturn("jobDemo1");
// output
924.915703

submitJob("jobDemo2",, jobDemo, 10);
// output
jobDemo2

getRecentJobs();
```

| node | userID | jobId | rootJobId | jobDesc | priority | parallelism | clientIp | clientPort | receivedTime | startTime | endTime | errorMsg |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| local8848 | guest | jobDemo1 | d1d76cad-d46f-338c-4179-21cface3ce7c | job demo | 4 | 2 | 127.0.0.1 | 62016 | 2023.12.12T17:52:01.576 | 2023.12.12T17:52:01.585 | 2023.12.12T17:53:23.204 |  |
| local8848 | guest | jobDemo2 | def84639-5b21-c6b0-47be-986b4563e192 | jobDemo | 4 | 2 | 127.0.0.1 | 62016 | 2023.12.12T17:57:42.325 | 2023.12.12T17:57:42.327 | 2023.12.12T17:57:49.995 |  |

把作业提交到远程节点：

使用 `rpc` 函数（"DFS\_NODE2" 与本地节点在同一集群）：

```
def jobDemo(n){
    s = 0
    for (x in 1 : n) {
        s += sum(sin rand(1.0, 100000000)-0.5)
        print("iteration " + x + " " + s)
    }
    return s
}

rpc("DFS_NODE2", submitJob, "jobDemo3", "job demo", jobDemo, 10);
// output
Output: jobDemo3

rpc("DFS_NODE2", getJobReturn, "jobDemo3");
// output
Output: -3426.577521
```

* 使用 `remoteRun` 函数或
  `remoteRunWithCompression` 函数，这里以
  `remoteRun` 为例：

```
conn = xdb("DFS_NODE2")
conn.remoteRun(submitJob, "jobDemo4", "job demo", jobDemo, 10);
// output
Output: jobDemo4

conn.remoteRun(getJobReturn, "jobDemo4");
// output
Output: 4238.832005
```

