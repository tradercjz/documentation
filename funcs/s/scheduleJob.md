# scheduleJob

## 语法

`scheduleJob(jobId, jobDesc, jobFunc, scheduleTime, startDate, endDate,
frequency, [days], [onComplete], [priority], [parallelism])`

## 参数

**jobId** 是一个字符串。

**jobDesc** 是关于任务描述的字符串。

**jobFunc** 是一个没有参数的函数。它通常是一个部分应用。注意：若该函数是一个自定义函数，则它只能接收标量、数据对或常规数组作为默认参数。

**scheduleTime** 是一个 MINUTE 类型的标量/向量。任务之间的时间间隔最小为5分钟。

**startDate** 是一个日期标量。

**endDate** 是一个日期标量。

**frequency** 是一个字符。它可以是下列3个值之一：'D' 表示每日，'W' 表示每周，'M' 表示每月。

**days** 是一个整型标量/向量，表示执行定时任务的日期。如果 *frequency* 为 'W' 或 'M' 时，它是必需的。如果
*frequency* 为W，*days* 可以取以下值：0（周日），1（周一），...，5（周五），6（周六）。

**onComplete**
是一个有4个参数的回调函数，细节请见以下最后一个例子。当定时作业执行完毕（包括有异常的情况）后，会执行该函数。可通过该函数向外部消息系统如邮件系统或微信与钉钉发送消息。

**priority** 属于 0 到 8 的整数，表示任务的优先级。默认值为 4。

**parallelism** 属于 0 到 8 的整数，表示任务的并行度。默认值为 2。

注：用户设置的优先级和并行度，还分别受到 [setMaxJobPriority](setMaxJobPriority.md) 的参数 *maxPriority* 和 [setMaxJobParallelism](setMaxJobParallelism.md) 的参数
*maxParallelism* 限制。最终的优先级和并行度分别为 min(*priority*, *maxPriority*),
min(*parallelism*, *maxParallelism*)。

## 详情

返回定时任务的任务 ID。如果 *jobId* 与已有的定时任务的 ID 不一致，系统返回 *jobId*。否则在 *jobId*
后面添加当前日期，"000", "001" 等作为后缀，直到产生唯一的任务 ID。 我们可以使用 [getRecentJobs](../g/getRecentJobs.md) 来查看最近完成的定时任务。

执行定时任务生成的信息保存在 jodId.msg 文件中；如果定时任务会返回值，它会保存在 jobId.object 文件中。
jobId.msg 和 jobId.object 保存在 batchIobs 文件夹中。我们可以分别使用 [getJobMessage](../g/getJobMessage.md) 和 [getJobReturn](../g/getJobReturn.md) 来查看这两个文件。

## 例子

定时执行一个函数：

```
def f():1+2;
scheduleJob(jobId=`daily, jobDesc="Daily Job 1", jobFunc=f, scheduleTime=17:23m, startDate=2018.01.01, endDate=2018.12.31, frequency='D');
scheduleJob(jobId=`weekly, jobDesc="Weekly Job", jobFunc=f, scheduleTime=17:30m, startDate=2018.01.01, endDate=2018.12.31, frequency='W', days=2);
```

定时执行一个脚本：

```
scheduleJob(jobId=`monthly, jobDesc="Monthly Job 1", jobFunc=run{"monthlyJob.dos"}, scheduleTime=17:23m, startDate=2018.01.01, endDate=2018.12.31, frequency='M', days=1);
```

这里使用部分应用 run{<script>}，因为 *jobFunc* 必须是没有参数的函数。

```
getJobMessage(`daily);
// output
018-02-08 17:23:27.166296 Start the job [daily]: Daily Job 1
018-02-08 17:23:27.167303 The job is done.

getJobReturn(`daily);
// output
3
```

可以在一天中多次定时执行相同的任务：

```
scheduleJob(jobId=`Trading, jobDesc="Generate Trading Tickets", jobFunc=run{"TradingTickets.dos"}, scheduleTime=[09:25m, 12:00m, 02:00m, 15:50m], startDate=2018.01.01, endDate=2018.12.31, frequency='D');
```

在这种情况下，每次执行定时任务时，任务 ID 是不一样的。

可以在每周的工作日中多次执行相同的定时任务：

```
scheduleJob(jobId=`PnL, jobDesc="Calculate Profit & Loss", jobFunc=run{"PnL.dos"}, scheduleTime=[12:00m, 02:00m, 14:50m], startDate=2018.01.01, endDate=2018.12.31, frequency='W', days=[1,2,3,4,5]);
```

定时任务执行结束后可发送邮件通知。以下脚本运行前需安装 HttpClient 插件。

```
def sendEmail(jobId, jobDesc, success, result){
  desc = "jobId=" + jobId + " jobDesc=" + jobDesc
  if(success){
  desc += " successful " + result
    res = httpClient::sendEmail('patrick.mahomes@dolphindb.com','password','andy.reid@dolphindb.com','This is a subject',desc)
  }
  else{
  desc += " with error: " + result
    res = httpClient::sendEmail('patrick.mahomes@dolphindb.com','password','andy.reid@dolphindb.com','This is a subject',desc)
  }
}
scheduleJob(jobId=`PnL, jobDesc="Calculate Profit & Loss", jobFunc=run{"PnL.dos"}, scheduleTime=[12:00m, 02:00m, 14:50m], startDate=2018.01.01, endDate=2018.12.31, frequency='W', days=[1,2,3,4,5], onComplete=sendEmail);
```

