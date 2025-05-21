# createIPCInMemoryTable

## 语法

`createIPCInMemoryTable(size, tableName, columnNames,
columnTypes)`

## 参数

**size** 整数，表示 table 能缓存的记录数。该值必须大于 1,000,000，否则系统自动取 1,000,000。

**tableName** 字符串，表示跨进程共享内存表的名称。

**columnNames** 字符串向量，用于指定表的列名。

**columnTypes** 向量，表示每列的数据类型。可使用表示数据类型的系统保留字或相应的字符串。

## 详情

创建一个跨进程共享内存表的句柄。跨进程共享内存表通常作为流计算的输出表。在对时延要求极高的场景下，用户进程通过插件直接访问共享内存获取数据，极大减小了 TCP
等网络传输的时延。

跨进程共享内存表通过共享内存（由操作系统管理）进行跨进程通信。共享内存表仅支持在同一物理机内共享，不支持在集群不同物理节点间进行共享。

跨进程共享内存表支持读写，但不支持对跨进程共享内存表的表结构进行修改。向跨进程共享内存表写数据的方法，与普通内存表一致。若一次性插入的数据量大于共享内存，系统会抛出异常。

* 读写机制：将写入共享内存的进程作为生产者，从共享内存中读取数据的进程作为消费者。一次写入的数据将作为一个整体，供一次读取消费，且读进程依次按顺序对写入的数据进行消费。例如：第一写入
  100 条数据，第二次写入 200 条数据，则第一次会读到 100 条数据，第二次会读到第二批写入的 200
  条数据，以此类推。读取数据时，共享内存表中的所有数据均已被消费，则读进程会被阻塞，直到有新写入的可消费数据时，才能将数据读出。

DolphinDB
支持多进程并发写入共享内存表，以及在写入的同时进行读操作。但注意，只能同时存在一个读进程。参考上述读写机制，读取是一次性的，若不同进程并发读取，将会得到不同阶段写入的数据。

注： 此函数仅适用于 Linux 系统。

## 例子

创建一个跨进程共享内存表，并作为流数据订阅的输出表。

```
share streamTable(10000:0,`timestamp`temperature, [TIMESTAMP,DOUBLE]) as pubTable
ipc_t = createIPCInMemoryTable(1000000, "ipc_table", `timestamp`temperature, [TIMESTAMP, DOUBLE])
def shm_append(mutable table, msg) {
   table.append!(msg)
}
subscribeTable(tableName="pubTable", actionName="act3", offset=0, handler=shm_append{ipc_t}, msgAsTable=true)
// 写入数据

n = 200
timestamp = 2022.01.01T09:00:00.000 + 1..n
temp = 30 + rand(5.0,n)

tableInsert(pubTable,timestamp,temp)
```

**相关信息**

* [dropIPCInMemoryTable](../d/dropIPCInMemoryTable.html "dropIPCInMemoryTable")
* [loadIPCInMemoryTable](../l/loadIPCInMemoryTable.html "loadIPCInMemoryTable")

