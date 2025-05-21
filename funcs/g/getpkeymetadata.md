# getPKEYMetaData

## 语法

`getPKEYMetaData()`

## 参数

无

## 详情

获取 PKEY 引擎下所有 chunk 的元数据。该函数只能在数据节点上执行。

返回一个表，包含以下列:

* chunkId：chunk 的唯一标识
* chunkPath：分区的物理路径
* level：数据文件所在的 level 级别
* table：数据表名称
* files：数据文件名称，即 level file 名称

## 例子

```
getPKEYMetaData()
```

| chunkId | chunkPath | level | table | files |
| --- | --- | --- | --- | --- |
| a0a7b031-15b8-32be-664b-21b156dc94c0 | /home/dolphindb/server/local8848/storage/CHUNKS/test\_pkey/20200102/Key94/1B8 | 0 | pt1\_2 | 0-000000006-000 |
| b3307046-77cb-bbb4-2244-dc4dcdd4c4e2 | /home/dolphindb/server/local8848/storage/CHUNKS/test\_pkey/20200104/Key39/1B8 | 0 | pt1\_2 | 0-000000009-000 |
| 1b47193f-39a4-8b93-3f44-d1b32b892126 | /home/dolphindb/server/local8848/storage/CHUNKS/test\_pkey/20200105/Key94/1B8 | 0 | pt1\_2 | 0-000000007-000 |
| 65ac20af-e1ea-21a6-254a-0c7a1f4a1bcf | /home/dolphindb/server/local8848/storage/CHUNKS/test\_pkey/20200102/Key39/1B8 | 0 | pt1\_2 | 0-000000003-000 |
| 600e024e-e280-62bb-084d-b440f7ccc349 | /home/dolphindb/server/local8848/storage/CHUNKS/test\_pkey/20200101/Key94/1B8 | 0 | pt1\_2 | 0-000000002-000 |
| 4f33838b-1b90-3f84-6943-e0da5fda3e10 | /home/dolphindb/server/local8848/storage/CHUNKS/test\_pkey/20200104/Key94/1B8 | 0 | pt1\_2 | 0-000000005-000 |
| e625607d-03ce-00bc-ab47-a419ae5af3f3 | /home/dolphindb/server/local8848/storage/CHUNKS/test\_pkey/20200103/Key94/1B8 | 0 | pt1\_2 | 0-000000004-000 |
| 9e0004ea-33b5-b2b4-d947-065c9333709f | /home/dolphindb/server/local8848/storage/CHUNKS/test\_pkey/20200101/Key39/1B8 | 0 | pt1\_2 | 0-000000001-000 |
| 595d1703-88b4-4397-4b46-281eb8014251 | /home/dolphindb/server/local8848/storage/CHUNKS/test\_pkey/20200103/Key39/1B8 | 0 | pt1\_2 | 0-000000008-000 |
| 280b3b44-8006-52a8-694e-1133e8740c07 | /home/dolphindb/server/local8848/storage/CHUNKS/test\_pkey/20200105/Key39/1B8 | 0 | pt1\_2 | 0-000000010-000 |

