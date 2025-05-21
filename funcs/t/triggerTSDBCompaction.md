# triggerTSDBCompaction

## 语法

`triggerTSDBCompaction(chunkId, [level=0])`

## 参数

**chunkId** 是字符串标量，表示 chunk 的 ID。

**level** 可选参数，表示需要合并的层级。可以是 [-1,3] 的整数。

* 当 *level*为 [0,3] 区间内的整数时，触发对应层级的 Level File 合并。默认值为 0。
* 当 *level* =-1 时，所有 Level File 会合并为一个 Level File。

## 详情

在 TSDB 存储引擎中，强制触发指定 chunk 内指定层级所有 Level File 的合并操作，以提升读取效率。

**注**：只有在配置参数 *allowTSDBLevel3Compaction* 设置为 true 且表中指定
*keepDuplicates*=FIRST/LAST 时，才会执行 Level 3 文件的合并。

## 例子

一个分区内包含两种文件类型，一种是记录数据库和数据表结构信息的文件（file chunk），另一种是数据文件（tablet chunk）。
因为只能对数据文件进行合并操作，在查询 chunk ID 时，需通过 type=1（代表数据文件）来进行过滤。

```
chunkIds = exec chunkId from getChunksMeta() where type=1
for (x in chunkIds) {
    triggerTSDBCompaction(x)
}
```

