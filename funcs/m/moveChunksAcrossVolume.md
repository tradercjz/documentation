# moveChunksAcrossVolume

注： 此函数将于近期版本中废弃，推荐使用函数 [moveReplicas](moveReplicas.md) 实现相关功能。

## 语法

`moveChunksAcrossVolume(srcPath, destPath, chunkIds,
[isDelSrc=true])`

## 参数

**srcPath**
是一个字符串，格式如："volumeA/CHUNKS"。表示源 chunks 的路径。

**destPath**
是一个字符串，格式如："volumeB/CHUNKS"。表示要转移到的目的 chunks 的路径。

**chunkIds** 是一个字符串或者字符串向量。表示需要移动的 chunks 的 id 值。

**isDelSrc** 布尔值，默认为 true。表示拷贝后是否删除源 chunks。

注： *srcPath*、 *destPath* 和 *chunkIds* 可以通过
[getChunksMeta](../g/getChunksMeta.md) 获取。

## 详情

将一个磁盘卷 chunks 文件转移至指定的路径。 *isDelSrc* = true 时，源路径下的 chunks
被成功转移后，将被删除；否则，仍被保留。如果转移失败，保留源路径下的所有 chunks，清空目标路径下已经拷贝完成的文件。

注意：

* 只能在同一个节点下进行 chunks 文件的转移。
* 进行该操作前，需要停止写入，保证所有事务都已完成，并将所有缓冲区的数据刷入磁盘。
* 配置项 *volumes* 必须包含 *srcPath* 和 *destPath*
  指定路径所在的磁盘卷，且该配置已经生效（修改配置项后重启使其生效）。
* *destPath* 指定的 chunks 目录必须为空目录。

**首发版本**：2.00.4

