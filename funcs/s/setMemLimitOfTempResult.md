# setMemLimitOfTempResult

## 语法

`setMemLimitOfTempResult(X)`

## 参数

**X** 一个数值型标量，必须大于0且不能大于 *maxMemSize* 的设置值。

## 详情

在线修改表连接过程中产生的临时数据表（单个）的大小，单位为 GB。该命令只能由管理员在数据节点/计算节点上执行。

注： 此命令修改的配置值在系统重启后将失效。若需要配置值永久生效，请更改配置文件中的
*memLimitOfTempResult*。

