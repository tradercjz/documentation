# create

create 语句用于创建数据库或者数据表。其语法如下：

自 3.00.0 版本起，支持创建 catalog 中的数据库或者数据表。

## 创建分布式数据库

该语句只支持创建分布式数据库。

```
create database directory partitioned by partitionType(partitionScheme),[partitionType(partitionScheme),partitionType(partitionScheme)],
[engine='OLAP'], [atomic='TRANS'], [chunkGranularity='TABLE']
```

在 create database 语句中，'partitionType' 的个数表示分区的层级，最少1个，最多3个。当指定多个
'partitionType' 时，表示组合分区。其它参数详情请参考函数 [database](../../funcs/d/database.md)。

自 3.00.0 版本起，支持创建 catalog 中的数据库。使用 *catalog.schema* 代替上述语句中的
*directory*。

```
create database catalog.schema partitioned by partitionType(partitionScheme),[partitionType(partitionScheme),partitionType(partitionScheme)],
[engine='OLAP'], [atomic='TRANS'], [chunkGranularity='TABLE']
```

若已设置当前的默认 catalog，则可忽略 catalog 前缀，直接传入 *schema。*

```
use catalog catalog1 //如设置当前默认catalog为catalog1
create database test partitioned by partitionType(partitionScheme),[partitionType(partitionScheme),partitionType(partitionScheme)],
[engine='OLAP'], [atomic='TRANS'], [chunkGranularity='TABLE']
```

## 创建数据表

该语句只支持创建普通内存表和分布式表。

### 语法

```
create table dbPath.tableName (
    schema[columnDescription]
)
[partitioned by partitionColumns],
[sortColumns],
[keepDuplicates=ALL],
[sortKeyMappingFunction]
[softDelete=false]
[comment],
[encryptMode='plaintext']
```

### 参数

* **dbPath** 字符串，表示数据库的路径。创建内存表时，可以不指定该参数。
* **tableName** 可以为表示表名的字符串，或者表示表对象的变量。
* **schema** 表结构，包含两列： *columnName* 和
  *columnType*。
* **columnDescription** 为列字段添加描述，以 keywords
  方式进行添加。可包含以下两项：

  + *comment* 为列字段添加注释;
  + *compress* 指定压缩方式，包含以下4种方式：

    - "lz4"
    - "delta"
    - "zstd"
    - "chimp"
* **partitionColumns**
  分区列或应用于分区列的函数调用（例如：partitionFunc(id)）。对于组合分区，*partitionColumns*
  依次指定多个分区列。
* **softDelete** 用于启用或禁用软删除功能。默认为
  false，即禁用。该参数适于在行数多但删除量小的场景下使用。使用该参数需要同时满足以下条件：

  + 由TSDB 存储引擎创建的数据库内的表。
  + *keepDuplicates* 已设置为 LAST。
* **comment**字符串标量，用于设置表注释。

TSDB 引擎参数：

* **sortColumns** TSDB
  引擎必选参数，字符串标量或向量，用于指定每一分区内的排序列。
* **keepDuplicates** 指定在每个分区内如何处理所有
  *sortColumns* 之值皆相同的数据，默认值为 ALL。提供以下选项：

  + ALL: 保留所有数据
  + LAST：仅保留最新数据
  + FIRST：仅保留第一条数据
* **sortKeyMappingFunction** 由一元函数对象组成的向量，其长度与索引列一致，即 *sortColumns*
  的长度 - 1，若只指定一个映射函数 mapfunc，必须写为
  *sortKeyMappingFunction*=[mapfunc]。用于指定应用在索引列中各列的映射函数，以减少 sort key
  的组合数，该过程称为 sort key 降维。

  索引列中的各列被对应的映射函数降维后，原本的多个 sort key 组合值会被重新映射到一个新的
  sort key 组合值上。而每个新 sort key 组合值对应的数据仍将根据 *sortColumns*
  的最后一列（时间列）进行排序。降维在写入磁盘时进行，因此指定该参数一定程度上将影响写入性能。

**注：**

* 创建维度表时，不可指定该参数。
* *sortKeyMappingFunction*
  指定的函数对象与索引列中的各列一一对应，若其中某列无需降维，则函数对象置为空。
* 当 *sortKeyMappingFunction* 中的函数对象为 hashBucket，且需要对采用 Hash
  分区的分区字段进行降维时，应确保 Hash 分区的数量和 hashBucket 中的 buckets
  之间不存在整除关系，否则会导致同一分区内的所有 Hash 值得到的 key 都相同。

**indexes** 为一个字典，用于为表中的列指定索引。仅当 *dbHandle* 指示的数据库采用 “TSDB” 或 “PKEY” 引擎（engine=”TSDB”
或 engine=”PKEY”）时，本参数才生效。

当引擎为 TSDB 时，用于为某一列设置向量索引，以便在查询时对该列进行高效的欧氏距离计算。目前，每个表仅支持为单个列设置向量索引。字典的键为 STRING
类型，表示列名，且该列的类型必须为 FLOAT[]；字典的 value 为 STRING 类型，其形式为
`"vectorindex(type=flat, dim=128)"`，其中：

type 可选值为 Flat, PQ, IVF, IVFPQ, HNSW：

* Flat 适用于数据规模在数百至数万级别的向量数据，或需要最高精度的场景。
* PQ 适用于数据规模在数十万至数千万级别的向量数据，且对搜索精度要求不高的场景。常见应用场景如大型数据库、视频库等。
* IVF 适用于数据规模在数万至数百万级别的向量数据，常见应用场景如图片检索、文本检索等。
* IVFPQ
  适用于数据规模在数百万至数千万级别的向量数据，需要在检索速度和精度之间找到最佳平衡的场景。常见应用场景如大型推荐系统、社交网络中的用户匹配。
* HNSW
  适用于数据规模在数亿至数十亿级别的向量数据，并对检索速度，精度和动态更新有高要求的场景，常见应用场景如实时推荐系统、在线搜索、RAG等。

**encryptMode** 字符串标量，指定表的加密方式，默认为不加密（明文模式）。目前支持以下可选值（大小写不区分）：plaintext,
aes\_128\_ctr, aes\_128\_cbc, aes\_128\_ecb, aes\_192\_ctr, aes\_192\_cbc, aes\_192\_ecb,
aes\_256\_ctr, aes\_256\_cbc, aes\_256\_ecb, sm4\_128\_cbc, sm4\_128\_ecb

dim 为属于 [1,n] 的整数，表示向量的维度。后续插入的向量维度必须为 d，否则会插入失败。若 *type* 指定为 PQ 或 IVFPQ，则要求
dim 为 4 的倍数。

如果已为某一列设置了向量索引，在查询语句中，若同时满足以下条件：不包含 join 语句，where 子句中不包含 sort key， 包含 order by
子句且其中只包含对该列应用 rowEuclidean 函数并按升序排序，包含 limit 子句，则会应用向量索引提升查询性能。

create table 语句内的参数和详情说明请参考相关函数 [createPartitionedTable](../../funcs/c/createPartitionedTable.md) / [createDimensionTable](../../funcs/c/createdimensiontable.md)。

## 创建catalog 中的数据表

自 3.00.0 版本起，支持创建 catalog 中的数据表。使用 *catalog.schema* 代替上述语句中的 *dbPath*。

```
create table catalog.schema.tableName(
    schema[columnDescription]
)
[partitioned by partitionColumns],
[sortColumns],
[keepDuplicates=ALL],
[sortKeyMappingFunction]
```

若已设置当前的默认 catalog，则可忽略 catalog 前缀，直接传入 *schema*。

```
use catalog catalog1 //如设置当前默认catalog为catalog1
create table schema.tableName(
    schema[columnDescription]
)
[partitioned by partitionColumns],
[sortColumns],
[keepDuplicates=ALL],
[sortKeyMappingFunction]
```

## 创建临时内存表

通过在 `create` 后添加关键字 local temporary
（不区分大小写）以声明创建一张本地临时内存表。语法如下：

```
create local temporary table  tableName(
schema
) [on commit preserve rows]
```

其中：

* **tableName** 表示表名的字符串，或者表示表对象的变量。
* **schema** 表结构声明，包含两列： *columnName* 和
  *columnType*。
* **on commit preserve rows**
  为可选关键字，不区分大小写，用于声明该表为会话级临时表。

注：

* DolphinDB `create table`
  语句创建的内存表即为本地临时表且仅对当前会话有效，因此该语句和 `create table` 语句等价。
* 系统暂不支持创建全局临时内存表及 `on commit delete
  rows` 关键字。

## 创建点位管理表

点位管理表的相关概念请参阅[物联网点位管理引擎](../../db_distr_comp/db/iotdb.md)。在使用 create
语句创建点位管理表时，通过创建一个 IOTANY 类型的列或开启最新值缓存功能（*latestKeyCache*）以建立点位管理表。使用前须保证库表已指定
IOTDB 引擎。

相关参数：

**latestKeyCache** 可选参数，布尔标量，用于设置是否开启最新值缓存功能。默认值为 false，即关闭。支持分区表、流数据表和共享内存表。

注意：

* 当创建点位管理表时，数据库的 engine 必须为 IOTDB。
* 当 engine 为 IOTDB 的数据库中只能包含点位管理表，不能有非点位管理表，如正常的分区表，维度表等。
* 最多可以创建一个 IOTANY 列。不能单独建一个该类型的向量或表。
* 物联网点位管理引擎规定**将唯一标识一组点位的多个列（一般为 ID 列+各种 tag 列）+时间列**设置为sortColumns。当设置
  latestKeyCache=true 时，sortColumns 里至少需要两列。
* IOTANY 列是可选操作。即支持仅开启最新值缓存功能，但表中无 IOTANY 列。但若表中包含 IOTANY 列则必须指定
  latestKeyCache=true。
* 建立点位管理表时，数据库分区方案必须为复合分区、必须存在一个时间分区，且时间分区位于最后一个维度。

## 例子

### 例1. 创建内存表

```
create table tb(
            id SYMBOL,
            val DOUBLE
    )
     go;   //必须使用 go 语句使上面的代码先解析执行，否则会报不识别变量 tb 的错误
     tb.schema()

    partitionColumnIndex->-1
    chunkPath->
    colDefs->
    name typeString typeInt comment
    ---- ---------- ------- -------
    id   SYMBOL     17
    val  DOUBLE     16
```

### 例2. 创建 TSDB 引擎下的分布式数据库

```
if(existsDatabase("dfs://test")) dropDatabase("dfs://test")
     create database "dfs://test" partitioned by VALUE(1..10), HASH([SYMBOL, 40]), engine='TSDB'
```

**TSDB 引擎下的分布式表**

```
create table "dfs://test"."pt"(
        id INT,
        deviceId SYMBOL,
        date DATE[comment="time_col", compress="delta"],
        value DOUBLE,
        isFin BOOL
    )
    partitioned by ID, deviceID,
    sortColumns=[`deviceId, `date],
    keepDuplicates=ALL

 pt = loadTable("dfs://test","pt")
 pt.schema()

// output
engineType->TSDB
keepDuplicates->ALL
partitionColumnIndex->[0,1]
colDefs->
name     typeString typeInt extra comment
-------- ---------- ------- ----- --------
id       INT        4
deviceId SYMBOL     17
date     DATE       6             time_col
value    DOUBLE     16
isFin    BOOL       1

partitionType->[1,5]
partitionColumnName->[id,deviceId]
partitionSchema->([1,2,3,4,5,6,7,8,9,10],40)
partitionSites->
partitionColumnType->[4,17]
partitionTypeName->[VALUE,HASH]
sortColumns->[deviceId,date]
softDelete->false
tableOwner->admin
chunkGranularity->TABLE
chunkPath->
```

**TSDB 引擎下的维度表**

```
create table "dfs://test"."pt1"(
        id INT,
        deviceId SYMBOL,
        date DATE[comment="time_col", compress="delta"],
        value DOUBLE,
        isFin BOOL
    )
    sortColumns=[`deviceId, `date]

 pt1 = loadTable("dfs://test","pt1")
 pt1.schema()

// output
sortColumns->[deviceId,date]
softDelete->false
tableOwner->admin
engineType->TSDB
keepDuplicates->ALL
chunkGranularity->TABLE
chunkPath->
partitionColumnIndex->-1
colDefs->
name     typeString typeInt extra comment
-------- ---------- ------- ----- --------
id       INT        4
deviceId SYMBOL     17
date     DATE       6             time_col
value    DOUBLE     16
isFin    BOOL       1
```

### 例3. 创建 PKEY 引擎下的分布式数据库

```
if(existsDatabase("dfs://test")) dropDatabase("dfs://test")
create database "dfs://test" partitioned by VALUE(1..10), engine="PKEY"
```

**PKEY 引擎下的分布式表**

```
create table "dfs://test"."pt"(
     id INT,
     deviceId SYMBOL [indexes="bloomfilter"],
     date DATE [comment="time_col", compress="delta"],
     value DOUBLE,
     isFin BOOL
 )
 partitioned by ID,
 primaryKey=`ID`deviceID
```

**PKEY
引擎下的维度表**

```
create table "dfs://test"."dt"(
     id INT,
     deviceId SYMBOL [indexes="bloomfilter"],
     date DATE [comment="time_col", compress="delta"],
     value DOUBLE,
     isFin BOOL
 )
 partitioned by ID,
 primaryKey=`ID`deviceID
```

### 例4. 创建临时内存表

```
create local temporary table "tb" (
        id SYMBOL,
        val DOUBLE
    ) on commit preserve rows
     tb.schema()

    partitionColumnIndex->-1
    chunkPath->
    colDefs->
    name typeString typeInt extra comment
    ---- ---------- ------- ----- -------
    id   SYMBOL     17
    val  DOUBLE     16
```

### 例5. 创建catalog 中的数据库和数据表

```
//建catalog
createCatalog("trading")
use catalog trading;
//建库
create database stock partitioned by VALUE(1..10), engine='OLAP'
//建表
create table stock.quote (
     id INT,
     date DATE[comment="time_col", compress="delta"],
     value DOUBLE,
 )
 partitioned by id
```

### 例6. 为分区列指定函数

本例中分区列的数据比较特殊，格式形如 "id\_date\_id"。在写入数据库时需要调用函数从原始数据中提取日期，并按照日期进行分区。

```
login(`admin, `123456)
// 首先定义处理分区列数据（形如如"id_date_id"）的函数
def myPartitionFunc(str,a,b) {
	return temporalParse(substr(str, a, b),"yyyyMMdd")
}
// 分区列数据
data = ["ax1ve_20240101_e37f6", "475b4_20240101_6d9b2", "91f86_20240102_b781d"]
tb = table(data as id_date, 1..3 as value, `a`b`c as sym)

dbName = "dfs://partitonFunc"
if(existsDatabase(dbName)){
        dropDatabase(dbName)
}

create database "dfs://partitonFunc" partitioned by VALUE(2024.02.01..2024.02.02), HASH([SYMBOL, 5]), engine='TSDB'

create table "dfs://partitonFunc"."pt"(
	date STRING,
	value INT,
	sym SYMBOL
	)
	// 采用组合分区方式，partitionColumns 中指定 myPartitionFunc 函数对第一个分区列的数据进行处理
	partitioned by myPartitionFunc(date, 6, 8), sym,
	sortColumns="sym"

pt = loadTable(dbName,"pt")
pt.append!(tb)
flushTSDBCache()
// 查询数据
select * from pt
```

| date | value | sym |
| --- | --- | --- |
| 475b4\_20240101\_6d9b2 | 2 | b |
| ax1ve\_20240101\_e37f6 | 1 | a |
| 91f86\_20240102\_b781d | 3 | c |

## 例7. 创建点位管理表

本例中，我们通过复合分区方案按 id 和 ts 分区，创建了一个名为 pt 的点位管理表。该表使用 ticket 和 id2
作为唯一识别一个点位的两列；启用最新值缓存，且 value 为 IOTANY 类型，可存储不同类型的测点数据；启用了 hashSortKey
压缩。

```
dbName = "dfs://db"
if (existsDatabase(dbName)) {
    dropDatabase(dbName)
}
// 创建数据库，存储引擎为IOTDB
create database "dfs://db115" partitioned by HASH([INT, 20]),VALUE(2017.08.07..2017.08.11), engine='IOTDB'
// 创建点位表，其中 firstSortKey 为 deviceId 和 location，lastSortKey(时间戳列)为 timestamp
create table "dfs://db"."pt" (
        deviceId INT,
        location SYMBOL,
        timestamp TIMESTAMP,
        value IOTANY
)
partitioned by deviceId, timestamp,
sortColumns = [`deviceId, `location, `timestamp],
sortKeyMappingFunction = [hashBucket{, 50}, hashBucket{, 50}],
latestKeyCache = true
```

