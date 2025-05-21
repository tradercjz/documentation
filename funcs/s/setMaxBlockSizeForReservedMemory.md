# setMaxBlockSizeForReservedMemory

## 语法

`setMaxBlockSizeForReservedMemory(blockSizeKB)`

## 参数

**blockSizeKB** 一个数值型标量（单位为KB），必须大于0。

## 详情

在线修改系统预留内存可以分配的最大内存块大小。该命令只能由管理员在数据节点/计算节点上执行。

请注意，此命令修改的配置值只对当前节点有效，且在系统重启后将失效。若需要配置值永久生效，请更改配置文件中的
*maxBlockSizeForReservedMemory*。

