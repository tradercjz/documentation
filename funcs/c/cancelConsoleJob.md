# cancelConsoleJob

## 语法

`cancelConsoleJob(rootJobId)`

## 参数

**rootJobId** 是作业的 ID，是一个字符串标量或者向量。若为向量，表示同时取消多个作业。

## 详情

取消已经提交但是尚未完成的交互式任务。如果要取消批处理作业，请使用 [cancelJob](cancelJob.html)。

`cancelConsoleJob` 在当前正在执行的子任务完成后，才会取消任务。因此，
`cancelConsoleJob` 并不是马上生效。如果 `cancelConsoleJob`
的对象是没有子任务的任务，该命令不生效。

## 例子

在一个节点的某个会话中，执行以下代码：

```
pt = loadTable("dfs://TAQ", `quotes)
select count(*) from pt;
```

在同一个节点的其他会话中，使用 [getConsoleJobs](../g/getConsoleJobs.html) 获取要取消的交互式任务的 ID，然后使用 `cancelConsoleJob`
来取消该任务。

```
cancelConsoleJob("bf768327-776d-40a7-8a8d-00a6cfd054e3");
```

