# getUserHardwareUsage

## 语法

`getUserHardwareUsage([from=0], [to])`

## 参数

**from** 整型或时间类型，表示查询的起始时间点。默认值为0，表示查询从1970.01.01零点开始的记录。

**to** 整型或时间类型，表示查询的结束时间点。默认为空，表示查询到目前时间点为止的记录。

*from* 必须小于等于 *to*。

## 详情

从资源使用日志（*<HomeDir>/resource/hardware.log*）获取特定时间段内用户的硬件资源使用情况。该函数仅在资源跟踪功能开启时（配置
*resourceSamplingInterval*）调用，且仅限管理员在数据节点上调用。

**返回值**

返回一个表，包含以下字段：

* timestamp：NANOTIMESTAMP 类型的时间戳。
* userId：用户名。
* cpu：当前用户占用的工作线程数量。
* memory：内存使用量，当前用户使用的所有变量的内存占用大小。单位是字节。
* send：单次采集间隔内发送的数据量。单位是字节。
* recv：单次采集间隔内接收的数据量。单位是字节。需要注意的是，统计的接收数据量可能会有一定误差，最大误差范围在 2KB 以内。

## 例子

```
login("admin", "123456")
select sum(send), sum(recv) from pnodeRun(getUserHardwareUsage) group by userId, node
```

返回：

| userId | node | sum\_send | sum\_recv |
| --- | --- | --- | --- |
| admin | datanode8902 | 197,783 | 464 |
| admin | datanode8903 | 375,911 | 438 |
| admin | datanode8904 | 1,080,171 | 735,817 |
| guest | datanode8902 | 2,144 | 216 |
| guest | datanode8903 | 120 | 0 |
| guest | datanode8904 | 399 | 0 |
| user1 | datanode8902 | 80,222 | 0 |
| user1 | datanode8903 | 120 | 0 |
| user1 | datanode8904 | 83,361 | 328 |
| user2 | datanode8902 | 80,100 | 0 |

