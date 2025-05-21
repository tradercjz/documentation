# 物联网点位管理引擎

DolphinDB 提供物联网点位管理引擎（IOTDB
引擎）以对海量测点进行精细化、低延时的点位管理。用户能够在建表时使用含可变类型的列，并且系统会自动缓存每个点位的最新值数据，从而大幅提升查询性能（目前可达毫秒级）。

## 基础概念

本节将介绍物联网点位管理引擎中的一些基本概念。

### 点位

在物联网（Internet of Things，简称
IoT）中，“点位”通常指被监控或管理的物理对象上的具体信息点或数据采集点。这些点位可以是传感器、执行器、控制器等物联网设备上的具体接口或参数，也可以是设备本身作为一个整体被监控的标识。其中数据对象包括静态属性（ID，名称等）和动态属性（温度，压力，湿度，状态等）。

### 点位数据特点

* **数量巨多**：在电网、车联网、工业制造场景中，点位数从几百万到上亿点不等。
* **采样频率高**：某些极端场景下，点位的采样频率高达 100KHz。
* **数据类型复杂**：点位数据类型涵盖布尔型、整型、浮点型、枚举型等。
* **数据传输形式多样**：同一设备的点位数据，可能同一时间采集、同一批次上传，也可能不同时间采集、单独上传。

### 物联网点位管理引擎 / IOTDB 引擎

DolphinDB 在 3.00.2 版本中推出的基于 TSDB 引擎自研的、针对物联网场景中海量点位数据进行高效管理的存储引擎。

### IOTANY 列

值类型可变的列，能够在单值模型的字段里存储不同类型的属性值。

### 最新值缓存功能

系统实时更新最新值缓存，并直接从缓存而非磁盘中读取数据，创建以分区为单位的最新值缓存表。最新值缓存功能可在 create 或
`createPartitionedTable` 中通过 *latestKeyCache*
参数开启。功能说明小节将详细介绍其原理。

### 点位管理表

* 包含 IOTANY 列的表。（推荐）
* 使用物联网点位管理引擎（IOTDB 引擎）、且开启最新值缓存功能的分布式表、流数据表或共享内存表。

### 静态表

对 sortColumns 中指定的除最后时间列外的其它列进行映射。将其映射为内部 ID。在后续的存储和缓存操作中，系统将通过内部 ID
来代指某个测点，以达到节省存储空间的目的。该表与 SymbolBase 类似，以分区为单位。该映射会存储于静态表中，用户无感知。

## 功能说明

本节将从原理、使用、管理等多个角度详细介绍 IOTANY 列和最新值查询优化。

### IOTANY 列

IOTANY 列即值类型可变的列，建表时最多可以创建一个 IOTANY 列。IOTANY 列类型只能用在 create
语句中，不能单独建一个该类型的向量或者表。DolphinDB 在存储 IOTANY 列数据时， 将在 **TSDB** Level File
层级单独存储不同类型的值。

关于 TSDB 存储引擎，物联网点位管理引擎：

* 规定将唯一标识一组测点的**多个列（一般为 id 列+各种 tag 列）+时间列**设置为 sortColumns。
* 支持三种去重策略：ALL（保留所有数据，为默认值）， LAST（仅保留最新数据），FIRST（仅保留第一条数据）。
* 支持 HashMappingFunction。
* 暂不支持 softDelete。
* 最新值查询功能暂不支持 snapshot read。
* 暂不支持 level 4 compaction。
* 暂不支持向量数据库等。
* 暂不支持添加 IOTANY 列。
* 不支持 sortColumns 中包含 DECIMAL 类型。
* 不支持 upsert! 时设置 ignoreNull=true。
* 不支持 upsert! 时传入 IOTANY 向量。

### 最新值查询优化

最新值查询的优化有最新值缓存表和最新值查询优化两种方式。

一般情况下，我们通过`context by`
**id+tag 列**
`csort`
**时间列**
`limit
-1`语法来查询最新值：

```
select deviceId, timestamp, metrics1... from pt
where deviceId = xxx context by deviceId csort timestamp limit -1
```

针对最新值查询，物联网点位管理引擎引入两种优化：

* **最新值缓存表**：引入以分区为单位的最新值缓存表。系统将**实时更新**最新值缓存，并直接从**缓存**而非磁盘中读取数据。此外，物联网点位管理引擎提供预热机制，重启后自动加载最近时间分区的缓存数据，优化冷启动场景。
* **存储引擎层的最新值查询优化**：在存储引擎层实现 context by 最新值算法，根据 index zonemap
  进行过滤，只读取磁盘上部分的 block。用于支持缓存表 cache miss 的情况。

以下介绍两种优化方法的使用前提和优先顺序：

| 优化逻辑 | 使用前提（符合任一） |
| --- | --- |
| 最新值缓存表 | * 查询语句不包含任何 where 条件。 * 查询语句包含 where 条件，过滤条件仅包含部分或全部 firstSortKey   列，firstSortKey 支持的过滤类型：=, <, <=, >, >=,   between, in。 * 查询语句的 where 过滤条件涉及 lastSortKey 列且不涉及其他任何非   sortKey 列，lastSortKey列支持的过滤类型为<, <=, >, >=,   between。 |
| 最新值查询优化 | * 查询的 where 条件需要包含所有的 firstSortKey   列，并且可以包含时间列（时间列 where 条件支持的过滤类型：=, <, <=, >,   >=, between）。 * 如果 firstSortKey 有多列，则每一列的过滤条件只支持等值过滤（即=）。 * 如果 firstSortKey 只有一列，则过滤条件支持等值过滤和 in 过滤。 |

注意：

* 最新值缓存表的条件三中，当 lastSortKey 列的过滤类型为 <, <=, between
  时，需要最新值缓存表内 lastSortKey 列中的所有数据均满足 where
  过滤条件才会通过缓存表返回结果。例如，最新值缓存表 lastSortKey
  列`ts`的范围为`[2024.01.01,
  2024.01.15]`，且 where 条件为`ts <
  2024.01.16`，此时可以通过查询最新值缓存表获取查询结果。
* 若满足最新值缓存的使用条件，则优先从最新值缓存表中读取数据。
* 若不满足最新值缓存的使用条件，则尝试最新值查询优化。
* 若均不符合条件，则遵循先前版本逻辑。

假设一个 TSDB 分布式表 test 的 sortColumns
为``c1`c2`timestamp`（其中称 c1, c2 为 firstSortKey，timestamp 为
lastSortKey），则可以按照以下格式指定最新值查询：

`select [cols] from test
[where] context by c1,c2 csort timestamp limit
-1.`

下面给出一些查询语句示例以及这些查询会使用的优化方式：

| sortColumns | SQL | 方式1：最新值缓存表 | 方式2：最新值查询优化 |
| --- | --- | --- | --- |
| c1, c2, timestamp | `select [cols] from pt context by c1, c2 csort timestamp limit -1`  （不包含任何过滤条件） | 可使用 |  |
| c1, c2, timestamp | ``` select [cols] from pt where c1 in [x,x,x] and c2 = xxx context by c1, c2 csort                 timestamp limit -1 ```  （多个firstSortKey，且有firstSortKey的过滤类型为非等值过滤） | 可使用 |  |
| c1, c2, timestamp | ``` select [cols] from pt where c1 = xx and c2 = xx timestamp >= xxx context by c1, c2                 csort timestamp limit -1 ```  （涵盖所有firstSortKey，并且有lastSortKey过滤） | 可使用 | 可使用 |
| c1, c2, timestamp | ``` select [cols] from pt where c1 = xx and c2 = xx  context by c1, c2 csort timestamp                 limit -1 ```  （过滤条件包含所有firstSortKey） | 可使用 | 可使用 |
| c1, c2, timestamp | ``` select [cols] from pt where c1 = xx and timestamp > xxx  context by c1, c2 csort                 timestamp limit -1 ```  （过滤条件包含部分firstSortKey以及lastSortKey） | 可使用 |  |
| c1, timestamp | ``` select [cols] from pt where c1 in [x,x,x] context by c1, c2 csort timestamp limit                 -1 ```  （过滤条件包含所有firstSortKey，且firstSortKey过滤类型为in） | 可使用 | 可使用 |
| c1, timestamp | ``` select [cols] from pt where c1 in [x,x,x] and timestamp between xxx and xxx context                 by c1, c2 csort timestamp limit -1 ```  （过滤条件包含所有firstSortKey和lastSortKey） | 可使用 | 可使用 |
| c1, timestamp | ``` select [cols] from pt where c1 > x context by c1, c2 csort timestamp limit               -1 ```  （过滤条件包含所有firstSortKey，firSortKey过滤类型不是 `in` 或 `=` ) | 可使用 |  |

#### 通过 HINT\_EXPLAIN 查看是否使用优化

可以通过 HINT\_EXPLAIN 查看是否使用、以及具体使用了什么优化。

如果查询是最新值查询（即 context by firstSortKey 列，csort lastSortKey 列，并且 limit
为-1），则查询开启HINT\_EXPLAIN 后，将可以在输出中看到 lastQuery 字段，该字段包含以下三种可能的输出形式：

1. 采用最新值缓存查询：

    `"lastQuery": { "optimizationMethod":
   LatestKeyCache },`
2. 采用最新值查询优化查询：

    `"lastQuery": { "optimizationMethod":
   LatestKeyQuery },`
3. 两种优化方式均不满足:

    `"lastQuery": { "optimizationMethod": None
   },`

#### 有重复数据时的最新值查询语义

如果存在两条 id 相同、时间戳相同的数据，当使用 context by 查询最新值时，只会保留其中的一条。比如：

| id | timestamp | value |
| --- | --- | --- |
| 1 | 10:00 | 1 |
| 1 | 10:00 | 2 |

```
select * from pt where id = 1 context by context by id csort timestamp limit -1
```

当对普通分区表使用 context by 时，并未明确规定保留对象，故将随机保留一条数据。但在 IOTDB 引擎中，对点位管理表使用 context by
时，已明确规定**保留最新一条**，不会被 KEEP\_LAST 或 KEEP\_ALL 的设定影响。

##### 最新值缓存表管理

最新值缓存表以分区为单位，存储该分区内所有测点的最新值。写入时实时更新，随 Cache Engine 一同flush。持久化保存在每个分区的
tableDir 目录下。文件名为 *timeseries.cache*。

缓存管理与 symbolBase 一致，定期移除最近未使用的分区。参数 *IOTDBLatestKeyCacheSize*专用于控制最新值缓存表管理，默认为 maxMemSize 的 5%。

```
IOTDBLatestKeyCacheSize=0.5 //浮点数，单位为G
```

## 数据类型

IOTANY 类型目前支持如下几种类型：

| categroy | 类型 |
| --- | --- |
| Integral | CHAR |
| SHORT |
| INT |
| LONG |
| Logical | BOOL |
| Floating | FLOAT |
| DOUBLE |
| Literal | SYMBOL |
| STRING |

## 使用示例

本节将对创建点位管理表，表数据写入和查询、最新值查询等操作进行示例说明。

### 创建示例

推荐通过 create 语句创建含 IOTANY 列的点位管理表。

下例中，我们通过复合分区方案按 deviceId 和 timestamp 分区，创建了一个名为 pt 的点位管理表。该表使用 deviceId 和
location 作为唯一识别一个点位的两列，启用最新值缓存，且 value 为 IOTANY 类型，可存储不同类型的测点数据；启用了 hashSortKey
压缩。

```
dbName = "dfs://db"
if (existsDatabase(dbName)) {
    dropDatabase(dbName)
}
// 创建数据库，存储引擎为IOTDB
create database "dfs://db" partitioned by HASH([INT, 20]),VALUE(2017.08.07..2017.08.11), engine='IOTDB'
// 创建点位表，其中 firstSortKey 为 deviceId 和 location，lastSortKey(时间戳列)为 timestamp
create table "dfs://db"."pt" (
        deviceId INT,
        location SYMBOL,
        timestamp TIMESTAMP,
        value IOTANY
)
partitioned by deviceId, timestamp,
sortColumns = [`deviceId, `location, `timestamp],
latestKeyCache = true
```

### 写入示例

对于每个测点，第一次写入时会确定其 IOTANY 列的类型，如果之后对该测点写入不同的类型，会报错。

在**非 KEEP\_LAST** 的情况下，可以使用 update 语句修改测点 IOTANY 列的类型，但是 **where
条件里只能包含firstSortKey**，这样能保证每次更新所有该测点的记录，以确保同一个测点的 IOTANY 列的类型一直统一。

基于上例已建立的表，进行写入对比操作。首先第一次写入数据，结果为可以正常写入，测点[1, `loc1`]的类型确定为
INT。

```
// 测点[1, `loc1`] 第一次写入
pt = loadTable("dfs://db", "pt")
t = table([1] as deviceId,
  [`loc1] as location,
  [now()] as timestamp,
  [int(233)] as value)
pt.append!(t)
```

第二次写入该测点，value 类型为
DOUBLE。因为类型不匹配，故结果为不能写入。

```
// 测点[1, `loc1`] 第二次写入，value类型为double
t = table([1] as deviceId,
  [`loc1] as location,
  [now()] as timestamp,
  [double(233)] as value)
pt.append!(t)
```

尝试修改测点类型。

```
// 修改测点类型为double
// 修改失败，where条件只能包含firstSortKey
update pt set value=double(233) where deviceId = 1 and location=`loc1 and timestamp >= 2017.08.07
// 修改成功
update pt set value=double(233) where deviceId = 1 and location=`loc1
```

此时再次执行第二次写入的脚本，结果为写入成功。

### 更新示例

在非 KEEP\_LAST 的设置情况下，支持调用 update 时变更某个点位 IOTANY 列的类型。

在写入示例的最后也涉及到了更新操作，此处聚焦后再次讲解。

当更新列为 IOTANY列 时，where 中不能包含除 first sort key
以外的列，否则会报错。这样是为了保证修改类型时要更新所有该点位的记录，以确保同一个点位的 IOTANY
列的类型一直统一。

```
t = table([`dev1] as deviceId,
  [now()] as timestamp,
  [`loc1] as location,
  [int(233)] as value)
pt.append!(t) //该测点的类型为INT
update pt set value = 2.33 where deviceId = `dev1 and location = `loc1
// 将测点值更新为double
update pt set value = 2.33 where deviceId = `dev1
// ok
update pt set value = 2.33 where deviceId = `dev1 and location = `loc1 and timestamp > xxx
// 不行，一次需要更新该点位所有的记录
```

### IOTANY 列查询示例

基于已建立的表，进行如下查询操作：

```
select deviceId, location, sum(long(value)), timestamp from pt where deviceId = 1 and
  location = `loc1 and timestamp >= 2017.08.07
//成功执行
```

## IOTANY 列计算示例

基于已建立的表，进行如下计算：

```
// 判断相等关系
select * from pt where value = 233

// 聚合计算
select deviceId, location, sum(value), timestamp from pt where deviceId = 1 and
  location = `loc1 and timestamp >= 2017.08.07
```

### 最新值查询（context by）示例

前文介绍，最新值查询的优化有最新值缓存表和最新值查询优化两种方式。在满足不同条件时会用到不同的优化策略。本例为方便展示，将创建一个新的点位管理表。

```
dbName = "dfs://test";
if(existsDatabase(dbName)){
	dropDatabase(dbName)
}
// 创建数据库，存储引擎为IOTDB
create database "dfs://test"
partitioned by HASH([LONG,1]),HASH([DATE, 1]),
engine = 'IOTDB'
dummy = table(1000000:0, `date`deviceId`key1`val_any, [DATE, LONG, INT, DOUBLE])
// 创建点位表，其中 firstSortKey 为 deviceId 和 key1，lastSortKey(时间戳列)为 date
create table "dfs://test"."pt1"(
        date DATE,
        deviceId LONG,
        key1 INT,
        val_any DOUBLE
)
partitioned by deviceId, date
sortColumns = [`deviceId,`key1,`date]
keepDuplicates = ALL
latestKeyCache = true
pt1 = loadTable(dbName, "pt1")
// 导入测试数据
n = 200000
date = rand(2012.01.01..2012.12.31, n)
key1 = take(200199..(200199+n), n)
deviceId = take(200..(200+n), n)
val = rand(double(n), n)
t = table(date, deviceId, key1, val)
pt1.append!(t)
```

以下查询将使用最新值缓存优化：

```
select [HINT_EXPLAIN] * from pt1 where deviceId in [200, 201, 202]
context by deviceId, key1 csort date
limit -1
// HINT_EXPLAIN 输出
{
    .......
    "lastQuery": {
        "optimizationMethod": LatestKeyCache
    },
    ......
}
```

以下查询将使用最新值查询优化：

```
select [HINT_EXPLAIN] * from pt1 where deviceId = 200 and key1 = 200199
and date > 2010.12.31
context by deviceId, key1 csort date
limit -1
// HINT_EXPLAIN 输出
{
    .......
    "lastQuery": {
        "optimizationMethod": LatestKeyQuery
    },
    ......
}
```

以下查询不会使用存储层的任何优化（过滤条件中包含了非 sortkey
列）：

```
select [HINT_EXPLAIN] * from pt1 where deviceId = 200
and val_any = 123
context by deviceId, key1 csort date
limit -1
// HINT_EXPLAIN 输出
{
    .......
    "lastQuery": {
        "optimizationMethod": None
    },
    ......
}
```

相关文档：

* [create](../../progr/sql/create.html)
* [createPartitionedTable](../../funcs/c/createPartitionedTable.html)
* [schema](../../funcs/s/schema.html)
* [getSessionMemoryStat](../../funcs/g/getSessionMemoryStat.html)
* [参数配置](../cfg/function_configuration.html)

