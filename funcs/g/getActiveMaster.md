# getActiveMaster

## 语法

`getActiveMaster()`

## 参数

无

## 详情

对于普通集群，`getActiveMaster` 函数返回控制节点的别名。

对于包含多个控制节点的集群，`getActiveMaster` 函数返回 Leader
控制节点的别名。

注： 该函数只能在控制节点上执行。

## 例子

```
getActiveMaster();
// output
controller1
```

