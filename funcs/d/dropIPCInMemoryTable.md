# dropIPCInMemoryTable

## 语法

`dropIPCInMemoryTable(tableName)`

## 参数

**tableName** 字符串，表示跨进程共享内存表的名称。

## 详情

删除跨进程共享内存表。

注：

* 此函数仅适用于 Linux 系统。
* server 关机并不能删除跨进程共享内存表，仍然需要通过 `dropIPCInMemoryTable`
  进行删除。

## 例子

删除函数 `createIPCInMemoryTable` 例子中创建的表 ipc\_table。

```
dropIPCInMemoryTable(`ipc_table)
// output
ipc_table
```

