# setMaxMemSize

## 语法

`setMaxMemSize(memSizeGB, [emergencyMemSizeGB])`

## 参数

**memSizeGB** 一个数值型标量（单位为 GB），必须大于0且不能大于 DolphinDB 的许可证文件配置的
*maxMemoryPerNode* （通过函数 `license` 查看），否则系统会报错。

**emergencyMemSizeGB** 可选参数，一个数值型标量（单位为 GB），用于在线修改紧急内存区的大小，必须大于 0 且小于
*memSizeGB*的 50%。最小不低于
256 M，最大不能超过5G。若不指定，默认保持配置项 *[emergencyMemSize](../../db_distr_comp/cfg/function_configuration.html#topic_btq_p3k_gcc)* 的值不变。

## 详情

在线修改可以分配给 DolphinDB 的最大内存空间和紧急内存区大小。该命令只能由管理员执行。可通过
getClusterPerf().maxMemSize 查看修改后的设置是否生效。

当动态设置最大内存空间 （即配置项
*maxMemSize*）后，若用户不进行其他修改，系统会自动调整小内存分配区（reservedMemSize）和紧急内存区（emergencyMemSize）大小：

* 小内存分配区将调整为传入的 *memSizeGB* 的5%，最小不低于64M、最大不超过 1G。
* 紧急内存区（如果没有指定）调整为 *memSizeGB* 的5%，最小不低于 256M，最大不超过 5G。

关于 DolphinDB 内存管理相关配置参数及策略，参见[功能配置-内存](../../db_distr_comp/cfg/function_configuration.html#topic_btq_p3k_gcc)。

注：

此命令修改的配置值在系统重启后将失效。若需要配置值永久生效，请更改配置文件中的 *maxMemSize* 和
*emergencyMemSize*。

