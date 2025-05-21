# setMaxConnections

## 语法

`setMaxConnections(newValue)`

## 参数

**newValue** 一个小于 2^16（65536）的正整数。

## 详情

在线修改当前节点的最大连接数。该命令只能由管理员执行。

可以在控制节点调用函数 [getClusterPerf](../g/getClusterPerf.html) 返回的 maxConnections 字段查看是否成功修改。

注：

* *newValue* 指定的值必须大于当前的最大连接数，否则无法生效。
* 此命令修改的配置值在系统重启后将失效。若需要配置值永久生效，请更改配置文件中的
  *maxConnections*。
* `getClusterPerf`
  函数获取节点信息存在延迟，获取的可能不是最新的连接数。

