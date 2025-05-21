# createDistributedInMemoryTable

## 语法

`createDistributedInMemoryTable(tableName, colNames,
colTypes, globalPartitionType, globalPartitionScheme, globalPartitionColumn,
[localPartitionType], [localPartitionScheme], [localPartitionColumn])`

## 详情

创建一个分布式共享内存表，按指定分区方案，将数据存储在不同在节点上。该函数只能在数据节点/计算节点执行。

按全局分区方案将分布式共享内存表的数据分散地存储在不同节点（数据节点/计算节点）的内存中。每个节点最多只能存放一个分区的数据。分布式共享内存表支持并行读写，因此，它适用于需要对内存表进行分布式计算的场景。

分布式共享内存表的分区分为两级：

* 第一级为全局分区。全局分区可以将内存表的数据按照分区存放在不同的节点上。
* 第二级为局部分区（可选配置）。局部分区对存储在单个节点内的分区数据进行再分区。

若同时配置了全局分区和局部分区，等同于对分布式共享内存表进行了组合分区。

注：

* 仅支持在集群模式下创建分布式共享内存表。
* 全局分区的数量必须不小于2，且不能超过数据节点和计算节点总数。
* 其它节点访问分布式共享内存表前，需要执行 [loadDistributedInMemoryTable](../l/loadDistributedInMemoryTable.md) 函数加载表。
* 通过命令 [dropDistributedInMemoryTable](../d/dropDistributedInMemoryTable.md) 删除分布式共享内存表。
* 分布式共享内存表的操作暂不支持事务。

## 参数

**tableName** 字符串标量，表示分布式共享内存表的名称。

**colNames** 字符串向量，用于指定表的列名。

**colTypes** 由数据类型组成的向量，用于指定 *colNames* 各列的类型。

**globalPartitionType**
必选参数，表示集群全局的分区类型，仅支持范围分区（RANGE），哈希分区（HASH），数值分区（VALUE），列表分区（LIST）。

**globalPartitionScheme** 必选参数，表示集群全局的分区方案。

分区类型及对应的分区方案见下表：

| 分区类型 | 分区符号 | 分区方案 |
| --- | --- | --- |
| 范围分区 | RANGE | 向量。向量的任意两个相邻元素定义分区的范围。 |
| 哈希分区 | HASH | 元组。第一个元素是分区列的数据类型，第二个元素是分区的数量。 |
| 值分区 | VALUE | 向量。向量的每个元素定义了一个分区。 |
| 列表分区 | LIST | 向量。向量的每个元素定义了一个分区。 |

**globalPartitionColumn** 必选参数，字符串标量，表示集群全局的分区列。

以上参数对应整个集群的分区配置，分布式共享内存表将按照上述分区方案将数据分区后存储到各个节点。各个节点的数据可以通过以下参数，进行节点内部的二次分区。

**localPartitionType**
可选参数，表示节点内部的分区类型，仅支持范围分区（RANGE），哈希分区（HASH），数值分区（VALUE），列表分区（LIST）。

**localPartitionScheme** 可选参数，表示节点内部的分区方案。

**localPartitionColumn** 可选参数，字符串标量，表示节点内部的分区列。

## 例子

* 创建分布式共享内存表

  本例的集群拥有两个数据节点 node1 和 node2，在 node1
  上创建一个分布式共享内存表。因为分区的数量不能超过数据节点和计算节点数总和，建议进行 HASH 分区。

  ```
  pt = createDistributedInMemoryTable(`dt, `time`id`value, `DATETIME`INT`LONG, HASH, [INT, 2],`id)
  ```
* 加载分布式共享内存表

  在 node2 上加载分布式共享内存表，并插入数据。

  ```
  time = take(2021.08.20 00:00:00..2021.08.30 00:00:00, 40);
  id = 0..39;
  value = rand(100, 40);
  tmp = table(time, id, value);

  pt = loadDistributedInMemoryTable(`dt)
  pt.append!(tmp);

  select * from pt;
  ```
* 查看分布式共享内存表是否存在。

  ```
  objs(true)
  ```
* 删除分布式共享内存表

  ```
  dropDistributedInMemoryTable(`dt)
  ```

