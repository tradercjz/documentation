# setMaxJobParallelism

## 语法

`setMaxJobParallelism(userId, maxParallelism)`

## 参数

**userId** 是一个字符串，表示用户名。

**maxParallelism** 是一个1到64之间的整数，表示该用户的作业的最大并行度，即最多可以有多少个子任务同时并行执行。

## 详情

为给定用户指定其提交的作业最多可以有多少个子任务同时并行执行。该命令必须要用户登录后才能执行。

若未执行该函数，管理员的作业的默认最大并行度为64；非管理员用户的作业的默认最大并行度为2。

注： 该函数可在控制节点、数据节点和计算节点运行。

## 例子

```
login(`admin,`123456)
createUser(`ElonMusk, `superman)
setMaxJobParallelism(`ElonMusk, 64);
```

