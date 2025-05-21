# resetDBDirMeta

## 语法

`resetDBDirMeta(dbDir)`

## 参数

**dbDir** 是一个字符串，格式如："volumeB/DATABASE"。表示 DATABASE 将要转移到的目的路径。

## 详情

跨磁盘卷转移元数据时, 由于元数据中包含了 DATABASE 存储路径相关的信息，所以转移元数据前，必须调用
`resetDBDirMeta` 修改元数据中 DATABASE 存储的路径为目的路径。该命令只能在数据节点上执行。

请注意：

1. 只能在同一个数据节点上进行跨磁盘卷转移元数据的操作。
2. 进行该操作前，需要停止写入，保证所有事务都已完成，并将所有缓冲区的数据刷入磁盘。

假设将 metalog 目录 从 volumeA 转移至 volumeB，完整过程如下：

1. 执行命令 resetDBDirMeta('volumeB/DATABASE') 后关闭 server。
2. 手动拷贝 volumeA 下的目录 CHUNK\_METADATA, DATABASE, IOTRAN\_TYPE 和 LOG 到 volumeB。
3. 删除 volumeA 下的目录 CHUNK\_METADATA，DATABASE，IOTRAN\_TYPE 和 LOG。
4. 修改配置 *chunkMetaDir* = volumeB/CHUNK\_METADATA 后启动 server。

**首发版本**：2.00.4

