# createDimensionTable

## 语法

`createDimensionTable(dbHandle, table, tableName, [compressMethods],
[sortColumns|primaryKey],
[keepDuplicates=ALL], [softDelete=false],
[indexes], [encryptMode='plaintext'])`

别名：createTable

## 详情

在分布式数据库中创建一个维度表。维度表是分布式数据库中没有进行分区的表，查询时会将表中所有数据加载到内存，适用于存储不频繁更新的小数据集。

系统会定期检查内存的使用情况，当内存使用超过系统配置参数 *warningMemSize*
设定的阈值时，系统会尝试释放部分缓存。维度表如果长时间未被使用，其占用的内存根据 LRU（Least Recently Used）策略将被释放。用户也可以调用
*clearCachedDatabase* 手动释放维度表的缓存。

维度表与分区表都是根据设置参数 *dfsReplicationFactor*
决定副本的数量。维度表的读写操作也支持事务。

通过在配置项配置 *enableConcurrentDimensionalTableWrite* =
true，可以支持对维度表进行并发的写入、修改或删除操作。

## 参数

**dbHandle** 是 [database](../d/database.md)
函数返回的分布式数据库句柄。

**table** 是一个表，系统将根据该表的结构在数据库中创建一个空的维度表。

**tableName** 是一个字符串，表示维度表的名称。

**compressMethods** 一个字典，指定某些列使用 lz4, delta, zstd 或 chimp
压缩算法存储。key 为字段名，value 为压缩算法（"lz4", "delta", "zstd" 或 "chimp"）。若未指定，默认采用 lz4 压缩算法。有关
Delta 压缩算法，亦称为 delta-of-delta encoding，参考：[Delta Compression Techniques](http://engineering.nyu.edu/~suel/papers/delta-chap.pdf)。

* 对于 DECIMAL, SHORT, INT, LONG 与时间或日期类型数据，建议采用 Delta 算法压缩。
* 将字符串存储为 SYMBOL 类型数据，实现对字符串类型的压缩。
* 对于小数部分长度在三位以内的 DOUBLE 类型的数据，可以考虑使用 chimp 算法压缩。

**sortColumns** 字符串标量或向量，用于指定每一分区内的排序列，每次写入磁盘的数据在每一分区内将按 *sortColumns*
进行排序。系统默认 *sortColumns* （指定多列时） 最后一列为时间列，其余列字段作为排序的索引列，称作 sort key。每一分区内，同一个
sort key 组合值对应的数据将按时间列顺序连续存放在一起。查询时，若查询条件包含索引列，可以快速定位数据所在的数据块位置，提高查询性能。

* 仅当 dbHandle 指示的数据库采用 "TSDB" 引擎（engine="TSDB"）时，本参数才生效。
* *sortColumns* 只能是 INTEGER, TEMPORAL, LITERAL 类别（除 BLOB） 或 DECIMAL 类型。
  + 若 *sortColumns* 指定为多列，则 *sortColumns*
    的最后一列必须为时间列，其余列为索引列，且索引列不能为为 TIME, TIMESTAMP, NANOTIME, NANOTIMESTAMP
    类型。
  + 若 *sortColumns* 仅指定一列，则该列作为 sort key，其类型不能为TIME, TIMESTAMP,
    NANOTIME, NANOTIMESTAMP。若 *sortColumns* 指定为一列时间列 （非分区列），且同时指定了
    *sortKeyMappingFunction*，则查询的过滤条件中 *sortColumns*
    只能与相同时间类型的值进行比较。
* 频繁查询的字段适合设置为 *sortColumns*（建议不超过 4 列），且建议优先把查询频率高的字段作为 *sortColumns*
  中位置靠前的列。
* 为保证性能最优，建议每个分区内索引列的组合数（sort key）不超过 2000 个。
* *sortColumns* 是每个分区内部 level file 内数据的排序依据，与其是否为分区字段无关。

**primaryKey**字符串标量或向量，用于指定主键列。在数据写入操作中，如果主键相同，新的数据覆盖现有数据。

* 仅当*dbHandle* 指示的数据库采用 “PKEY” 引擎（engine=”PKEY”）时，本参数才生效。
* 主键列必须包含所有的分区列。
* 主键列支持的类型包括：BOOL, CHAR, SHORT, INT, LONG, INT128, STRING, TIME, SECOND,
  MINUTE, DATE, MONTH, DATEHOUR, DATETIME, SYMBOL, TIMESTAMP, NANOTIME,
  NANOTIMESTAMP, UUID, COMPLEX, POINT, IPADDR, DECIMAL32, DECIMAL64,
  DECIMAL128。

**keepDuplicates** 指定在每个分区内如何处理所有 *sortColumns*
之值皆相同的数据。提供以下选项：

* ALL：保留所有数据，为默认值。
* LAST：仅保留最新数据
* FIRST：仅保留第一条数据

**softDelete** 用于启用或禁用软删除功能。默认为
false，即禁用。该参数适于在行数多但删除量小的场景下使用。使用该参数需要同时满足以下条件：

* 由TSDB 存储引擎创建的数据库内的表
* *keepDuplicates* 已设置为 LAST

注： 参数 *sortColumns*,
*keepDuplicates* 仅在 `database` 的 *engine* 参数指定为 TSDB
时才有效。

**indexes** 为一个字典。当引擎为 PKEY 时，用于为表中的列指定索引。字典的键是 STRING
类型标量，表示列名；值是 STRING 类型标量，表示为该列指定的索引类型。目前支持设置 “bloomfilter”
索引类型：适用于对大基数列进行点查，且基数越大，索引效果越好，如身份证 ID、订单号、从业务上游同步的外键等数据列。目前支持的类型包括 BOOL, CHAR,
SHORT, INT, LONG, BLOB, STRING, DECIMAL32, DECIMAL64, DECIMAL128。

注： 引擎会将所有主键列合并为组合主键，并为组合主键设置 bloomfilter
类型索引。

**encryptMode** 可选参数，字符串标量，指定表的加密方式，默认为不加密（明文模式）。仅 Linux
系统支持该参数。目前支持以下可选值（大小写不区分）：plaintext, aes\_128\_ctr, aes\_128\_cbc, aes\_128\_ecb,
aes\_192\_ctr, aes\_192\_cbc, aes\_192\_ecb, aes\_256\_ctr, aes\_256\_cbc, aes\_256\_ecb,
sm4\_128\_cbc, sm4\_128\_ecb。

## 例子

例1

```
db=database("dfs://db1",VALUE,1 2 3)
timestamp = [09:34:07,09:36:42,09:36:51,09:36:59,09:32:47,09:35:26,09:34:16,09:34:26,09:38:12]
sym = `C`MS`MS`MS`IBM`IBM`C`C`C
price= 49.6 29.46 29.52 30.02 174.97 175.23 50.76 50.32 51.29
qty = 2200 1900 2100 3200 6800 5400 1300 2500 8800
t = table(timestamp, sym, qty, price);

dt=db.createDimensionTable(t,`dt).append!(t);
select * from dt;
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:34:07 | C | 2200 | 49.6 |
| 09:36:42 | MS | 1900 | 29.46 |
| 09:36:51 | MS | 2100 | 29.52 |
| 09:36:59 | MS | 3200 | 30.02 |
| 09:32:47 | IBM | 6800 | 174.97 |
| 09:35:26 | IBM | 5400 | 175.23 |
| 09:34:16 | C | 1300 | 50.76 |
| 09:34:26 | C | 2500 | 50.32 |
| 09:38:12 | C | 8800 | 51.29 |

例2

```
db = database("dfs://demodb", VALUE, 1..10)
t=table(take(1, 86400) as id, 2020.01.01T00:00:00 + 0..86399 as timestamp, rand(1..100, 86400) as val)
dt = db.createDimensionTable(t, "dt", {timestamp:"delta", val:"delta"})
dt.append!(t)
```

例3. TSDB 存储引擎下创建维度表

```
if(existsDatabase("dfs://dbctable_createDimensionTable")){
  dropDatabase("dfs://dbctable_createDimensionTable")
}
db = database("dfs://dbctable_createDimensionTable", VALUE, 1..100, , "TSDB")
t1 = table(1 100 100 300 300 400 500 as id, 1..7 as v)
db.createDimensionTable(t1, "dt", , "id").append!(t1)
dt=loadTable("dfs://dbctable_createDimensionTable","dt")
```

例4. PKEY 存储引擎下创建维度表

```
db = database(directory="dfs://PKDB", partitionType=VALUE, partitionScheme=1..10, engine="PKEY")
schematb = table(1:0,`id1`id2`val1`val2`date1`time1,[INT,INT,INT,DECIMAL32(2),DATE,TIME])
pkt = createDimensionTable(dbHandle=db, table=schematb, tableName="pkt", primaryKey=`id1`id2, indexes={"val1": "bloomfilter", "val2": "bloomfilter"})
```

**相关信息**

* [createPartitionedTable](createPartitionedTable.html "createPartitionedTable")

