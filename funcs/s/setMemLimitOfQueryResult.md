# setMemLimitOfQueryResult

## 语法

`setMemLimitOfQueryResult(memLimit)`

## 参数

**memLimit** 数值类型标量，表示内存上限，单位为 GB。该值必须小于 80% \* maxMemSize。

## 详情

在线修改单次查询结果占用的最大内存上限。该命令只能由管理员在数据节点/计算节点执行。

相关函数： [getMemLimitOfQueryResult](../g/getMemLimitOfQueryResult.md)

