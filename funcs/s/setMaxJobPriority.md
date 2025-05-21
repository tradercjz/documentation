# setMaxJobPriority

## 语法

`setMaxJobPriority(userId, maxPriority)`

## 参数

**userId** 是一个字符串，表示用户名。

**maxPriority** 是一个0到8之间的整数，表示给定用户提交作业的最高优先级。

## 详情

为给定用户指定其提交作业的最高优先级。该函数必须要用户登录后才能执行。

注： 该函数可在控制节点、数据节点和计算节点运行。

## 例子

```
login(`admin,`123456)
createUser(`KyleMurray, `Cardinals2020QB)
setMaxJobPriority(`KyleMurray, 7);
```

