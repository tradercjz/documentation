# getChunksMeta

## 语法

`getChunksMeta([chunkPath], [top = 1024])`

## 参数

**chunkPath** 是一个或多个 chunk 的 DFS 路径，支持使用通配符 %，\* 以及？。

**top** 是一个正整数，表示结果中返回的 chunk 的最多个数。默认值为1024。若设置 *top*= -1，则不限制返回的
chunk的数量。

## 详情

返回本地节点上指定数据库 chunk 的元数据。若不指定 *chunkPath*，返回本地节点上所有数据库 chunk
的元数据。

返回一个表，包含以下列

* site：节点别名
* chunkId：chunk 的唯一标识
* path：分区的物理路径
* dfsPath：分区 DFS 路径
* type：分区类型。0表示 file chunk；1表示 tablet chunk。
* flag：删除标志。若 flag=0，表示此 chunk 数据可以正常被查询和访问。若 flag=1，表示此
  chunk 数据已在逻辑上被标记为删除，不可被查询，但仍然占用磁盘空间。
* size：表示 file chunk 占用磁盘空间，单位为字节。对于 tablet chunk，返回0，需要使用
  [getTabletsMeta](getTabletsMeta.html)
  函数来查看其占用的磁盘空间。
* version：版本号
* state：chunk 的状态。
  + 0：表示 chunk 的最终状态，即所涉及的事务最终正确完成，或者 rollback。
  + 1：before commit，提交事务之前，即 chunk 上正在执行事务。比如正在写数据或者删除数据。
  + 2： after commit，已经 commit 事务。
  + 3： waiting for recovery，等待恢复的状态，比如发生版本不一致或者数据损坏时，数据节点向控制节点发起 recovery
    请求后，等待控制节点发起 recovery 时，则会处于这种状态。
  + 4： in recovery 状态，在 recovery 状态中，接收到控制节点的 recovery 请求，开始启动
    recovery，则处于这个状态。recovery 完成后变为最终状态（0）。
* versionList：版本链
* resolved：表示 chunk 的事务是否处于决议（commit）状态。true 表示决议状态，false
  表示决议后的最终状态。

## 例子

```
if(existsDatabase("dfs://testDB")){
  dropDatabase("dfs://testDB")
}

db=database("dfs://testDB", VALUE, 1..10)
n=1000000
t=table(rand(1..10, n) as id, rand(100.0, n) as x)
n=2000000
t=table(rand(1..10, n) as id, rand(100.0, n) as x, rand(100, n) as y)
db.createPartitionedTable(t, `pt2, `id).append!(t)
getChunksMeta("/testDB%");
```

| site | chunkId | path | dfsPath | type | flag | size | version | state | versionList | resolved |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P2-node1 | 092d5e12-e595-6f9e-b049-83cba1716997 | /ssd/ssd5/jzVol... | /testDB/pt2.tbl | 0 | 0 | 49 | 1 | 0 | 2052:49; | false |
| P2-node1 | d31e6b47-18f0-37a6-0146-45bf6e266c56 | /ssd/ssd6/jzVol... | /testDB/7 | 1 | 0 | 0 | 2 | 0 | cid : 2053,pt1... | false |
| P2-node1 | cd99d9ef-d864-f3bc-4945-f97017d43bf1 | /ssd/ssd5/jzVol... | /testDB/2 | 1 | 0 | 0 | 2 | 0 | cid : 2053,pt1... | false |
| P2-node1 | 8da4bea8-31d0-31b5-784f-67aa6339633d | /ssd/ssd5/jzVol... | /testDB/pt1.tbl | 0 | 0 | 41 | 1 | 0 | 2050:41; | false |
| P2-node1 | dd5fc885-f6a6-bfae-8543-254f9fb92484 | /ssd/ssd6/jzVol... | /testDB/10 | 1 | 0 | 0 | 2 | 0 | cid : 2053,pt1... | false |
| P2-node1 | 4b8aaed1-2dd6-acb7-5148-4add878c3b33 | /ssd/ssd6/jzVol... | /testDB/domain | 0 | 0 | 88 | 1 | 0 | 2049:88; | false |
| P2-node1 | 28cb59ec-185a-0ebf-a849-267e769936af | /ssd/ssd6/jzVol... | /testDB/8 | 1 | 0 | 0 | 2 | 0 | cid : 2053,pt1... | false |
| P2-node1 | b2facbd2-e301-428f-f94f-8579023f78af | /ssd/ssd6/jzVol... | /testDB/3 | 1 | 0 | 0 | 2 | 0 | cid : 2053,pt1... | false |
| P2-node1 | 8bec6445-bc6d-3693-7f46-d1bcdd350182 | /ssd/ssd6/jzVol... | /testDB/5 | 1 | 0 | 0 | 2 | 0 | cid : 2053,pt1... | false |

