# getScheduledJobs

## 语法

`getScheduledJobs([jobIdPattern])`

## 参数

**jobIdPattern** 是表示任务 ID 或任务 ID 模式的字符串。它支持通配符“%”和“?”。

## 详情

以表格的形式返回定时任务。如果 *jobIdPattern* 没有指定，返回所有已有的定时作业。

包含以下字段：

| 参数 | 含义 |
| --- | --- |
| userId | 用户 ID。 |
| jobId | 在提交定时作业时指定的作业名。 |
| jobDesc | 作业描述。 |
| startDate | 定时作业的开始日期，为 DATE 类型。 |
| endDate | 定时作业的结束日期，为 DATE 类型。 |
| frequency | 定时作业的执行频率。 |
| scheduledTime | 定时作业的执行间隔，为 MINUTE 类型。 |
| days | frequency 为 'W' 或 'M' 时，执行定时任务的日期。 |

## 例子

```
getScheduledJobs();
```

| userId | jobId | jobDesc | startDate | endDate | frequency | scheduleTime | days |
| --- | --- | --- | --- | --- | --- | --- | --- |
| root | monthly | Monthly Job | 2018.01.01 | 2018.12.31 | M | 17:00m | 1 |
| root | weekly | Weekly Job | 2018.01.01 | 2018.12.31 | W | 17:30m | 2 |
| root | daily | Daily Job | 2018.01.01 | 2018.12.31 | D | 18:00m |  |

