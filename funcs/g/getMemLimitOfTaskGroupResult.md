# getMemLimitOfTaskGroupResult

## 语法

`getMemLimitOfTaskGroupResult()`

## 参数

无

## 详情

获取当前节点发送的批量子查询占用的内存上限（单位为字节），返回一个 DOUBLE 类型数据。

## 例子

```
setMemLimitOfTaskGroupResult(10)
getMemLimitOfTaskGroupResult() / 1024 / 1024 / 1024
// output: 10
```

相关函数：[setMemLimitOfTaskGroupResult](../s/setMemLimitOfTaskGroupResult.html)

