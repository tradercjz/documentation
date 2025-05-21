# getUnresolvedTxn

## 语法

`getUnresolvedTxn()`

## 参数

无

## 详情

获取两阶段提交协议中处于决议状态的节点及其事务。只能由管理员在控制节点执行。返回一个表，包含以下字段：

* tid：事务 id。
* cid：提交的版本号。
* chunkId：chunk 的唯一标识。
* initiatingNode：事务决议的发起节点。
* firstResolutionAt：事务开始决议的时间。
* lastResolutionAt：若事务发生多次决议，则会显示最后一次决议的时间。

