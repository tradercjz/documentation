# getConnections

## 语法

`getConnections()`

## 参数

无

## 详情

获取当前节点的所有网络连接信息，可以在所有节点上执行。返回结果有三列，第一列（server）为当前节点自己的 IP 和端口信息，第二列（client）为网络连接对端的
IP 和端口信息，第三列（startTime）为连接建立时间。

## 例子

```
getConnections()
```

| server | client | startTimem |
| --- | --- | --- |
| localhost:8848 | 127.0.0.1:62546 | 2021.09.02T16:50:57.814 |
| localhost:8848 | 127.0.0.1:63081 | 2021.09.02T10:50:16.350 |
| localhost:8848 | 127.0.0.1:57559 | 2021.09.02T16:50:57.736 |

