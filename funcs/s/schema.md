# schema

## 语法

`schema(table|dbHandle)`

## 详情

显示指定数据表或数据库的结构信息。`schema`返回一个无序字典，包含以下字段（按首字母排序）：

* atomic：写入事务的原子性层级。
* chunkGranularity：分区粒度。
* clusterReplicationEnabled：集群间异步复制的开启状态。若开启，则该值为 true，否则为 false。
* colDefs：数据表各字段的结构信息。

  + name：列名
  + typeString：列的类型
  + typeInt：列类型对应的ID
  + extra：仅在列类型为 DECIMAL 时，显示 DECIMAL 的 scale
  + comment：列字段的注释信息
  + sensitive：该列是否已设置为敏感列，仅当 DFS 表返回此列。
* compressMethods：分布式表各列的压缩算法类型。

  + name：列名
  + compressMethods：压缩算法类型。lz4，delta （即 delta-of-delta encoding 算法）或
    zstd
* databaseDir：数据库的保存目录的路径。
* databaseOwner：数据库创建者名称。
* dbUrl：DFS 表所在分布式数据库的路径。仅当 *table* 为 DFS 表时返回。
* encryptMode：建表时指定的表加密方式。仅当 *table* 为 DFS 表时返回。
* engineType：存储引擎的类型，OLAP 或者 TSDB。
* keepDuplicates：数据保留策略。
* keyColumn：键值列列名。仅当 *table* 包含键值列时返回。
* partitionColumnIndex：分区列在表字段中对应的下标。维度表时，该值为 -1。
* partitionColumnName：分区列的名称。
* partitionColumnType：分区列类型对应的 ID，参照数据类型章节。
* partitionSchema：分区的结构。
* partitionSites：若 `database` 函数配置了 *locations* 参数，则该字段将列出
  locations 指定节点的 ip:port 信息。
* partitionTypeName / partitionType：分区的类型名和对应的 ID。VALUE(1), RANGE(2), LIST(3),
  COMPO(4), HASH(5)。
* sortColumns：数据表的排序列。
* softDelete：创建的表开启了软删除。仅在通过 TSDB 存储引擎创建的库中的表的 schema 返回值中可见。该功能开启时，softDelete
  返回字段中显示为 true；否则显示为 false。
* sortKeyMappingFunction：索引列的映射函数。
* tableComment：表的注释。
* tableName：DFS 表的表名。仅当 *table* 为 DFS 表时返回。
* tableOwner：表创建者名称。
* partitionFunction：处理分区列数据的函数。是一个字符串向量，每个元素是一个函数签名。若某个元素为
  asis，则表示建表时未指定函数对象。例如：`partitionFunction->[myPartitionFunc{, 6,
  8},asis]`。

* latestKeyCache：该分区表是否开启最新值缓存功能。
* compressHashSortKey：该分区表是否开启静态表 sortKey 压缩功能。

## 参数

参数可为一个数据表，亦可为一个数据库句柄 （dbHandle）。

## 例子

应用于 OLAP 引擎下的数据库：

```
n=1000000  // 设置变量n为1000000
ID=rand(10, n)  // 生成一个随机整数数组ID
x=rand(1.0, n)  // 生成一个随机浮点数数组x
t=table(ID, x)  // 创建表t，包含ID和x两列
db=database("dfs://rangedb101", RANGE, 0 5 10)  // 创建分布式数据库dfs://rangedb101，使用RANGE分布方式
pt = db.createPartitionedTable(t, `pt, `ID)  // 创建分区表pt，使用ID作为分区键
pt.append!(t)  // 将表t的数据追加到分区表pt中
pt=loadTable(db,`pt);  // 从数据库db中加载分区表pt
schema(db);  // 显示数据库db的模式信息
```

返回：

```
databaseDir->dfs://rangedb101
partitionSchema->[0,5,10]
partitionSites->
atomic->TRANS
chunkGranularity->TABLE
partitionType->2
partitionTypeName->RANGE
partitionColumnType->4
clusterReplicationEnabled->1
databaseOwner->admin
```

应用于 OLAP 引擎下的数据表时：

```
schema(pt);
```

返回：

```
chunkGranularity->TABLE
tableOwner->admin
compressMethods->
name compressMethods
---- ---------------
ID   lz4
x    lz4

colDefs->
name typeString typeInt comment
---- ---------- ------- -------
ID   INT        4
x    DOUBLE     16

chunkPath->
partitionColumnIndex->0
partitionColumnName->ID
partitionColumnType->4
partitionType->2
partitionTypeName->RANGE
partitionSchema->[0,5,10]
partitionSites->
```

应用于 TSDB 引擎下的数据库：

```
n = 10000 // 设置变量n为10000
SecurityID = rand(`st0001`st0002`st0003`st0004`st0005, n) // 从指定的证券ID中随机选择n个值赋给SecurityID
sym = rand(`A`B, n)  // 从符号A和B中随机选择n个值赋给sym
TradeDate = 2022.01.01 + rand(100,n) // 从2022年1月1日至100天后的日期中随机选择n个日期赋给TradeDate
TotalVolumeTrade = rand(1000..3000, n)  // 生成n个介于1000和3000之间的随机整数赋给TotalVolumeTrade
TotalValueTrade = rand(100.0, n)  // 生成n个小数赋给TotalValueTrade
schemaTable_snap = table(SecurityID, TradeDate, TotalVolumeTrade, TotalValueTrade).sortBy!(`SecurityID`TradeDate)
// 创建表schemaTable_snap，并按SecurityID和TradeDate排序

dbPath = "dfs://TSDB_STOCK"  // 设置数据库路径为dfs://TSDB_STOCK
if (existsDatabase(dbPath)){dropDatabase(dbPath)}  // 如果数据库路径存在，则删除该数据库
db_snap = database(dbPath, VALUE, 2022.01.01..2022.01.05, engine='TSDB')  // 创建名为db_snap的数据库，时间范围为2022年1月1日至2022年1月5日，引擎为TSDB

schema(db_snap)  // 显示db_snap的模式信息
```

返回：

```
databaseDir->dfs://TSDB_STOCK
partitionSchema->[2022.01.01,2022.01.02,2022.01.03,2022.01.04,2022.01.05]
partitionSites->
engineType->TSDB
atomic->TRANS
chunkGranularity->TABLE
partitionType->1
partitionTypeName->VALUE
partitionColumnType->6
clusterReplicationEnabled->1
databaseOwner->admin
```

应用于 TSDB 引擎下的数据表：

```
// 定义名为myHashFunc的函数，该函数接受一个参数x，并返回x的哈希桶编号，桶数为10
def myHashFunc(x){
  return hashBucket(x, 10)
}

// 使用db_snap中的schemaTable_snap创建一个分区表snap，表名为"snap"
// 以TradeDate分区，以SecurityID和TradeDate排序
// 保留重复值，排序键映射函数为myHashFunc
snap = createPartitionedTable(dbHandle=db_snap, table=schemaTable_snap, tableName="snap", partitionColumns=`TradeDate, sortColumns=`SecurityID`TradeDate, keepDuplicates=ALL, sortKeyMappingFunction=[myHashFunc])

// 显示snap表的模式信息
schema(snap)
```

返回：

```
engineType->TSDB
keepDuplicates->ALL
chunkGranularity->TABLE
sortColumns->["SecurityID","TradeDate"]
sortKeyMappingFunction->["def myHashFunc(x){
  return hashBucket(x, 10)
}"]
softDelete->0
tableOwner->admin
compressMethods->
name             compressMethods
---------------- ---------------
SecurityID       lz4
TradeDate        lz4
TotalVolumeTrade lz4
TotalValueTrade  lz4

colDefs->
name             typeString typeInt extra comment
---------------- ---------- ------- ----- -------
SecurityID       SYMBOL     17
TradeDate        DATE       6
TotalVolumeTrade INT        4
TotalValueTrade  DOUBLE     16

chunkPath->
partitionColumnIndex->1
partitionColumnName->TradeDate
partitionColumnType->6
partitionType->1
partitionTypeName->VALUE
partitionSchema->[2022.01.01,2022.01.02,2022.01.03,2022.01.04,2022.01.05]
partitionSites->
```

建立一个点位管理表，复合分区方案按 id 和 ts 分区，创建了一个名为 pt 的点位管理表。该表使用 ticket 和 id2
作为唯一识别一个点位的两列；启用最新值缓存，且 value 为 IOTANY 类型，可存储不同类型的测点数据；启用了 hashSortKey
压缩。

```
dbName = "pt"
if(existsDatabase(dbName)){
        dropDatabase(dbName)
}
db1 = database(, partitionType=HASH, partitionScheme=[INT, 10])
db2 = database(, partitionType=VALUE, partitionScheme=2017.08.07..2017.08.11)
db = database(dbName, COMPO, [db1, db2], engine='IOTDB')

create table "dfs://db"."pt" (
        id INT,
        ticket SYMBOL,
        id2 LONG,
        ts TIMESTAMP,
        id3 IOTANY
)
partitioned by id, ts,
sortColumns = [`ticket, `id2, `ts],
sortKeyMappingFunction = [hashBucket{, 50}, hashBucket{, 50}],
latestKeyCache = true,
compressHashSortKey = true
print schema(loadTable(dbName, `pt))
```

返回：

```
/*
engineType->IOTDB
keepDuplicates->ALL
chunkGranularity->TABLE
sortColumns->["deviceId","location","timestamp"]
sortKeyMappingFunction->["hashBucket{, 50}","hashBucket{, 50}"]
softDelete->0
tableOwner->admin
compressMethods->name      compressMethods
--------- ---------------
deviceId  lz4
location  lz4
timestamp lz4
value     lz4

tableComment->
latestKeyCache->1
compressHashSortKey->0
colDefs->name      typeString typeInt extra comment
--------- ---------- ------- ----- -------
deviceId  INT        4
location  SYMBOL     17
timestamp TIMESTAMP  12
value     IOTANY     41

chunkPath->
partitionColumnIndex->[0,2]
partitionColumnName->["deviceId","timestamp"]
partitionColumnType->[4,6]
partitionType->[5,1]
partitionTypeName->["HASH","VALUE"]
partitionSchema->(20,[2017.08.07,2017.08.08,2017.08.09,2017.08.10,2017.08.11,2024.10.12])
partitionSites->
*/
```

**相关信息**

* [database](../d/database.html "database")
* [createTable](../c/createTable.html "createTable")
* [createPartitionedTable](../c/createPartitionedTable.html "createPartitionedTable")

