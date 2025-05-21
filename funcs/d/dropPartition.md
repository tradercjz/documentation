# dropPartition

## 语法

`dropPartition(dbHandle, partitionPaths, [tableName],
[forceDelete=false],
[deleteSchema=false])`

## 详情

删除数据库中指定分区的数据。

如果指定了 *tableName* ：删除指定表中符合指定条件的分区数据。

如果没有指定 *tableName*：删除指定数据库所有表中符合指定条件的分区数据。

## 参数

**dbHandle** 分布式数据库的句柄。

**partitionPaths** 有两种指定模式：

* 指定路径：以 "/" 开头的字符串或字符串向量，表示数据库目录下单个或多个分区的路径。请注意对组合分区，路径必须包括所有层次分区。
* 指定条件：以分区列的一个或多个值组成的标量或向量作为过滤条件，系统会找到并删除这些值所在的分区。对于组合分区，partitionPaths
  是由每层分区的过滤条件组成的元组，如果某层分区不需要过滤，那么相应的过滤条件需置为空。

**tableName** 字符串，表示表名。若分区粒度为数据库级（[database](database.md): *chunkGranularity* = 'DATABASE'），可以不指定
*tableName*，否则必须指定该参数。

**forceDelete** 布尔值，默认值为 false，表示不开启强制删除。如果 *forceDelete*
=true，即使指定的分区正在恢复，系统也会将其强制删除。

**deleteSchema** 布尔值，默认值为
false，表示仅删除分区数据，分区方案（partitionSchema）中仍保留其对应的分区方案信息。

如果
*deleteSchema*=true，在满足以下条件时，删除分区数据及其对应的分区方案信息（可通过 [schema](../s/schema.md).partitionSchema 函数查看）：

1. 数据库只包含一个表；
2. 单级分区时采用 VALUE 分区，或多级分区的第一级为 VALUE 分区；
3. `dropPartition` 仅删除第一级分区的数据。

## 例子

下面例子中的脚本需要在集群中的数据节点/计算节点执行。

```
n=1000000
ID=rand(150, n)
dates=2017.08.07..2017.08.11
date=rand(dates, n)
x=rand(10.0, n)
t=table(ID, date, x)
dbDate = database(, VALUE, 2017.08.07..2017.08.11)
dbID = database(, RANGE, 0 50 100 150)
db = database("dfs://compoDB", COMPO, [dbDate, dbID])
pt = db.createPartitionedTable(t, `pt, `date`ID)
pt.append!(t);
```

上面的代码创建了组合分区的数据库，第一层分区为基于日期的值分区，第二层分区为基于值的范围分区。

例 1. 删除某个分区的数据

例如，删除表 pt "/20170807/0\_50" 分区，有以下两种方法：

(1) 指定路径：

```
dropPartition(dbHandle=database("dfs://compoDB"), partitionPaths="/20170807/0_50", tableName=`pt);
```

注： 这里使用 `database("dfs://compoDB")` 获取数据库
dfs://compoDB 的句柄，参数 *dbHandle* 也可指定为创建数据库时返回的句柄`db`。

(2) 指定条件：

```
dropPartition(dbHandle=database("dfs://compoDB"), partitionPaths=[2017.08.07, 0], tableName=`pt);
```

注意："/20170807/0\_50" 分区中的 ID 的可取值范围是从 0 到 49，不包括 50。以上脚本中，可以使用 0 到 49 的任一数字来代表此分区。

例 2. 删除一级分区的数据

例如，删除表 pt 的一级分区 2017.08.08，有以下两种方法：

(1) 使用向量指定该一级分区之下所有分区的路径：

```
partitions=["/20170808/0_50","/20170808/50_100","/20170808/100_150"]
dropPartition(dbHandle=database("dfs://compoDB"), partitionPaths=partitions, tableName=`pt);
```

(2) 指定条件：

```
dropPartition(dbHandle=database("dfs://compoDB"), partitionPaths=2017.08.08, tableName=`pt);
```

删除分区数据后，我们使用 [schema](../s/schema.md)
函数查看数据库的分区方案：

```
schema(database("dfs://compoDB"));
/*
databaseDir->dfs://compoDB
partitionSchema->([2017.08.07,2017.08.08,2017.08.09,2017.08.10,2017.08.11],[0,50,100,150])
partitionSites->
engineType->OLAP
atomic->TRANS
chunkGranularity->TABLE
partitionType->[1,2]
partitionTypeName->["VALUE","RANGE"]
partitionColumnType->[6,4]
clusterReplicationEnabled->1
databaseOwner->admin
*/
```

可以发现，2017.08.08 仍然在分区方案中，这是因为 `dropPartition` 只删除了
2017.08.08 这个分区中的数据，并不会将 2017.08.08 从数据库的分区方案中移除。由于该例删除的是一级 VALUE 分区，通过指定
*deleteSchema* = true，来同步删除分区方案中的对应分区信息。

```
dropPartition(dbHandle=database("dfs://compoDB"), partitionPaths=2017.08.08, tableName=`pt, deleteSchema = true);
```

使用 `schema` 函数查看数据库的分区方案：

```
schema(database("dfs://compoDB"));
// output
partitionSchema->([2017.08.11,2017.08.10,2017.08.09,2017.08.07],[0,50,100,150])
...
```

例 3. 删除二级分区的数据

例如，删除表 pt 的二级分区 [0,50)，有以下两种方法：

(1) 使用向量指定含有该二级分区的所有分区的路径：

```
partitions=["/20170807/0_50","/20170808/0_50","/20170809/0_50","/20170810/0_50","/20170811/0_50"]
dropPartition(dbHandle=database("dfs://compoDB"), partitionPaths=partitions, tableName=`pt);
```

(2) 指定条件：

```
dropPartition(dbHandle=database("dfs://compoDB"), partitionPaths=[,[0]], tableName=`pt);
```

例 4. 删除多个二级分区的数据

例如，删除表 pt 的二级分区 [0,50) 和 [100,150)：

```
dropPartition(dbHandle=database("dfs://compoDB"), partitionPaths=[,[0,100]], tableName=`pt);
```

例 5. 修改分布式数据库中的数据

在 DolphinDB 中，如果要修改分布式数据库中的数据，需要先把相关分区的数据加载到内存中进行修改，然后使用
`dropPartition` 将数据库中的相关分区删除，最后将内存中修改好的分区数据重新追加到数据库中。

例如，将分布式表 pt 中 date=2017.08.10, ID=88 的记录 x+10。

首先，将包含 date=2017.08.10, ID=88 的所有相关分区数据加载到内存中，这些数据位于 "20170810/50\_100" 分区中：

```
tmp=select * from loadTable("dfs://compoDB","pt") where date=2017.08.10 and 50<=ID<100 ;
```

接着，将内存表 tmp 中 date=2017.08.10, ID=88 的记录 x+10。：

```
update tmp set x=x+10 where date=2017.08.10 and ID=88;
```

然后，删除表 pt 中 "20170810/50\_100" 分区中的数据：

```
dropPartition(dbHandle=database("dfs://compoDB"), partitionPaths="/20170810/50_100", tableName=`pt);
```

最后，将内存中修改好的记录追加到表 pt 中：

```
pt.append!(tmp);
```

