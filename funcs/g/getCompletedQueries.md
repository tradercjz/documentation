# getCompletedQueries

## 语法

`getCompletedQueries([top])`

## 参数

**top** 是一个正整数。可选参数，默认值为 10。

## 详情

返回本地节点上最近完成的 *top* 条查询分布式数据库的 SQL 语句的描述信息表，包含以下字段：

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

本函数只可由系统管理员执行。在使用该函数之前，必须设定配置参数 *perfMonitoring* = 1 以启动性能监控。

## 例子

```
n=1000000
ID=rand(10, n)
x=rand(1.0, n)
t=table(ID, x)
db=database("dfs://rangedb16", RANGE,  0 5 10)
pt = db.createPartitionedTable(t, `pt, `ID)
pt.append!(t)
t1 = select count(x) from pt;
t2 = select * from pt where ID=1;
t3 = select * from pt where ID=5;

getCompletedQueries()
```

| userID | sessionID | jobID | rootID | level | startTime | endTime | jobDesc | errorMsg | remoteIP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| admin | 1166953221 | 4be0f403-a62d-7bae-4ded-43938cc2b4e9 | 4be0f403-a62d-7bae-4ded-43938cc2b4e9 | 0 | 2021.06.28T18:05:34.366483000 | 2021.06.28T18:05:34.372467000 | select ID,x from pt where ID == 1 |  | 127.0.0.1 |
| admin | 1166953221 | 9e9132c5-60c2-b3ab-41da-039ad2dcb6ff | 4be0f403-a62d-7bae-4ded-43938cc2b4e9 | 0 | 2021.06.28T18:05:34.366483000 | 2021.06.28T18:05:34.372467000 | select ID,x from pt where ID == 5 |  | 127.0.0.1 |
| admin | 1166953221 | 98275891-9c9b-948e-425c-6c3083713d84 | 98275891-9c9b-948e-425c-6c3083713d84 | 0 | 2021.06.28T18:05:34.344272000 | 2021.06.28T18:05:34.359201000 | select count(x) as count\_x from pt |  | 127.0.0.1 |

```
getCompletedQueries().keys()
```

返回：["userID","sessionID","jobID","rootID","level","startTime","endTime","jobDesc","errorMsg","remoteIP"]

```
getCompletedQueries().ErrorMsg
```

返回：[,,]

```
getCompletedQueries().jobDesc
```

返回：["select ID,x from pt where ID == 5","select ID,x from pt where ID == 1","select
count(x) as count\_x from pt"]

**相关信息**

* [getRunningQueries](getRunningQueries.html "getRunningQueries")

