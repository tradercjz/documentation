# setTSDBCacheEngineSize

## 语法

`setTSDBCacheEngineSize(memSize)`

## 参数

**memSize** 一个数值型标量（单位为GB），必须大于0且小于 *maxMemSize* \* 0.75。

## 详情

用于在线修改 TSDB 引擎的 Cache Engine 容量。集群环境下，该命令只能由管理员在数据节点/计算节点上执行。执行前需要确保开启了 Cache Enigne
(配置参数 *TSDBCacheEngineSize* )。可以通过 `getTSDBCacheEngineSize`
查看设置是否生效。

注：

此命令修改的配置值在集群重启后将失效。若需要配置值永久生效，请更改配置文件中的
*TSDBCacheEngineSize*。

自 2.00.16/3.00.3 起，当 Cache Engine 内存占用达到
*TSDBCacheEngineSize*设定值时，系统将阻塞写入线程。此前版本中，内存占用允许升至设定值的两倍后才会触发阻塞。详情请见[配置项 *TSDBCacheEngineSize* 说明](../../db_distr_comp/cfg/function_configuration.html#topic_jgf_glk_gcc)。

相关函数： [getTSDBCacheEngineSize](../g/getTSDBCacheEngineSize.md)

