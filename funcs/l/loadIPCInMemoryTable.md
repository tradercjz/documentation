# loadIPCInMemoryTable

## 语法

`loadIPCInMemoryTable(tableName)`

## 参数

**tableName** 字符串，表示跨进程共享内存表的名称。

## 详情

加载跨进程共享内存表，并返回该表的句柄。

注意：此函数仅适用于 Linux 系统。

## 例子

加载函数 `createIPCInMemoryTable` 例子中创建的表 ipc\_table。

```
ipc_t = loadIPCInMemoryTable("ipc_table")
ipc_t
// output
timestamp temperature
```

