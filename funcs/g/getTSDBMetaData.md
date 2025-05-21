# getTSDBMetaData

## 语法

`getTSDBMetaData()`

## 参数

无

## 详情

获取 TSDB 引擎下所有 chunk 的元数据。该函数只能在数据节点上执行。

返回一个表，包含以下列:

* chunkId：chunk 的唯一标识
* chunkPath：分区的物理路径
* level：数据文件所在的 level 级别
* table：数据表名称
* files：数据文件名称，即 level file 名称

**首发版本**：2.00.4

## 例子

```
getTSDBMetaData()
```

| chunkId | chunkPath | level | table | files |
| --- | --- | --- | --- | --- |
| 7e0c65ca-5e4a-4594-2948-fa0b5... | /hdd/hdd7/test/v... | 0 | pt\_2 | 0\_00211490,0\_002115580 |
| 7e0c65ca-5e4a-4594-2948-fa0b5... | /hdd/hdd7/test/v... | 1 | pt\_2 | 1\_00013041 |

