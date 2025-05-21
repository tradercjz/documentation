# getRedoLogGCStat

## 语法

`getRedoLogGCStat()`

## 参数

无

## 详情

获取 redo log 垃圾回收的状态。返回一个表对象，包含以下几列：

* physicalName：物理表名，格式为 "/数据库名/物理表名"
* txnCount：redo log 尚未回收的事务数
* numOfTxnPendingGC：等待回收的事务数
* minTidPendingGC：等待回收的事务的最小 tid
* numOfTxnPendingFlush：等待刷盘的事务数
* minTidPendingFlush：等待刷盘的事务的最小 tid

## 例子

```
getRedoLogGCStat();
```

| physicalName | txnCount | numOfTxnPendingGC | minTidPendingGC | numOfTxnPendingFlush | minTidPendingFlush |
| --- | --- | --- | --- | --- | --- |
| /test/pt\_2 | 2 | 0 |  | 2 | 1031 |
| /listdb/pt\_2 | 1 | 1 | 1033 | 0 |  |

