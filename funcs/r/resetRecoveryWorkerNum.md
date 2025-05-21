# resetRecoveryWorkerNum

## 语法

`resetRecoveryWorkerNum(newWorkerNum)`

## 参数

**newWorkerNum** 正整数，指定用于 chunk 恢复的工作线程数。

## 详情

在线修改当前节点用于 chunk 恢复的工作线程数。该命令只能由管理员在数据节点执行。

请注意，此命令修改的配置值在系统重启后将失效。若需要配置值永久生效，请更改配置文件中的 *recoveryWorkers* （默认值是 1）。

## 例子

```
resetRecoveryWorkerNum(2)
```

相关函数：[getRecoveryWorkerNum](../g/getRecoveryWorkerNum.md)

