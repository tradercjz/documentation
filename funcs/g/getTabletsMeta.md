# getTabletsMeta

## 语法

`getTabletsMeta([chunkPath], [tableName], [diskUsage=false],
[top=1024])`

## 参数

**chunkPath** 是一个或多个 chunk 的 DFS 路径，支持使用通配符 %，\* 以及？。

**tableName** 是字符串，表示数据表名。

**diskUsage** 是一个 Boolean 值，表示结果是否输出磁盘占用。

**top** 是一个正整数，表示结果中返回的 chunk 的个数上限。默认值为1024。若不设上限，需将 *top* 参数设为-1。

## 详情

返回当前节点上指定数据表 chunk 的元数据信息。若结合 [pnodeRun](../p/pnodeRun.md) 函数使用，可返回所有节点上指定数据表的元数据信息。

返回一个表，包含以下列：

* chunkId：chunk的唯一标识
* path：分区的物理路径
* dfsPath：分区DFS路径
* tableName：表名
* version：版本号
* rowNum：分区的记录条数
* createCids：update/delete表时创建的版本号
* latestPhysicalDir：最新版本号（cid）对应的存储数据的临时物理路径
* diskUsage：分区占用的磁盘空间，单位为字节。

## 例子

```
if(existsDatabase("dfs://testDB")){
   dropDatabase("dfs://testDB")
}
db=database("dfs://testDB", VALUE, 1..10)
n=1000000
t=table(rand(1..10, n) as id, rand(100.0, n) as x)
db.createPartitionedTable(t, `pt1, `id).append!(t)
n=2000000
t=table(rand(1..10, n) as id, rand(100.0, n) as x, rand(100, n) as y)
db.createPartitionedTable(t, `pt2, `id).append!(t)
getTabletsMeta("/testDB/%", `pt1, true);
```

| chunkId | path | dfsPath | tableName | version | rowNum | createCids | latestPhysicalDir | diskUsage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| dbfd1767-f9ca-689e-4d5e-643b8506e82d | C:\Users\Downl... | /testDB/10/8 | pt1 | 2 | 100155 | [2059] | pt1\_2\_2059 | 696295 |
| d221b457-fa7b-5990-4caa-13c99f56f716 | C:\Users\Downl... | /testDB/9/8 | pt1 | 2 | 99703 | [2059] | pt1\_2\_2059 | 693026 |
| 92904d3b-0147-9bb8-4a28-f99525b250e7 | C:\Users\Downl... | /testDB/8/8 | pt1 | 2 | 99791 | [2059] | pt1\_2\_2059 | 693848 |
| 7478c15a-0629-c8ab-47ee-a1d12c3c1cd6 | C:\Users\Downl... | /testDB/1/8 | pt1 | 2 | 100215 | [2059] | pt1\_2\_2059 | 696932 |
| 8bc48c11-86ca-97ac-4ee4-8f829de92cc8 | C:\Users\Downl... | /testDB/5/8 | pt1 | 2 | 100156 | [2059] | pt1\_2\_2059 | 696584 |
| 6b3a0a09-bc64-3bab-4535-344b7316d244 | C:\Users\Downl... | /testDB/2/8 | pt1 | 2 | 100121 | [2059] | pt1\_2\_2059 | 696303 |
| a7452c44-5d2b-6f82-4150-7bc48e941d64 | C:\Users\Downl... | /testDB/4/8 | pt1 | 2 | 99858 | [2059] | pt1\_2\_2059 | 696572 |
| a1a375cc-b6c0-29b2-485a-330af7447564 | C:\Users\Downl... | /testDB/6/8 | pt1 | 2 | 100280 | [2059] | pt1\_2\_2059 | 697596 |
| b04b4c04-6d43-0d8d-4000-6ae88e349eda | C:\Users\Downl... | /testDB/3/8 | pt1 | 2 | 99858 | [2059] | pt1\_2\_2059 | 694400 |
| b20df3a7-678b-1cbe-400d-d8e566706682 | C:\Users\Downl... | /testDB/7/8 | pt1 | 2 | 99865 | [2059] | pt1\_2\_2059 | 6942755 |

