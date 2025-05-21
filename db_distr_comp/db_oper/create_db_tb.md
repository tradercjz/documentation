# 建库建表

在 DolphinDB 中，创建数据库和表既可以通过 SQL 语句实现，也可以使用函数来完成。本文将分别以这两种方式进行介绍。

注： 本文中 SQL 语句的关键字对大小写不敏感；对于前文创建过的数据库，后文将直接使用而非再次定义。

## 创建数据库

在 DolphinDB 中，数据库分为分布式数据库和内存数据库。本节将分别举例介绍他们的创建方式。

### 创建分布式数据库

只有具备 DB\_OWNER 权限的用户才可以通过数据节点或计算节点创建分布式数据库。可通过 [getUserAccess](../../funcs/g/getUserAccess.md) 查看当前用户是否具有该权限，如果没有，请联系管理员赋权。

若您刚刚下载 DolphinDB ，可登录默认管理员账号：

```
login(`admin,`123456)
```

DolphinDB 支持通过 CREATE DATABASE 语句和 `database`
函数两种方式创建数据库。下例分别使用这两种方式，创建了一个名为 “dfs://valuedb“ 的分布式数据库。其中 “dfs://“
是分布式数据库的标识；指定了分区类型为值分区；设置了 2023.01.01 到 2023.12.31 共 365 个初始分区；并指定存储引擎的类型为
TSDB。执行前须确保不存在同名数据库。

**通过** `CREATE DATABASE` **语句：**

```
CREATE DATABASE "dfs://valuedb"
PARTITIONED BY VALUE(2023.01.01..2023.12.31),
ENGINE="TSDB"
```

**通过** `database` **函数：**

```
database(directory="dfs://valuedb", partitionType=VALUE,
  partitionScheme=2023.01.01..2023.12.31, engine='TSDB')
```

两种方式的区别在于：CREATE DATABASE 语句没有返回值；`database`
函数会返回一个数据库句柄(dbHandle)。

关于 CREATE DATABASE 语句，细节请参见 [create](../../progr/sql/create.md)。

关于 `database` 函数，细节请参见 [database](../../funcs/d/database.md)。

关于数据分区：

* DolphinDB 支持 5 种分区类型
  (*partitionType*)，分别是值分区、哈希分区、范围分区、列表分区与复合分区。分区类型一经确定，不可更改。
* 数据分区方式的选择应保证每个分区的大小均匀，且大小在 100M-1G 之间。
* 同一数据库下的所有表都是采用相同的分区方案。
* 数据库分区方案 (*partitionScheme*) 设定后，分布式表的值分区（VALUE）允许增加分区；分布式表的范围分区 (RANGE)
  允许在最后一个现有数据分区后面增加分区；其它分布类型不允许增加分区。
* 更多关于数据分区的内容请参考[数据分区](../db/db_partitioning.md)。

关于存储引擎（*engine*）：DolphinDB 支持 [TSDB](../db/tsdb.md) ，[OLAP](../db/olap.md)，[PKEY](../db/pkey_engine.md)等多种存储引擎，一个数据库的存储引擎一经确定，不可修改。

类似的，若要创建组合分区数据库：

**通过** `CREATE DATABASE` **语句**

```
CREATE DATABASE "dfs://compodb"
PARTITIONED BY VALUE(2020.01.01..2021.01.01),HASH([SYMBOL,25])
```

**通过** `database` **函数**

```
db1 = database("", VALUE, 2020.01.01..2021.01.01)
db2 = database("", HASH, [SYMBOL,25])
compoDb=database(directory="dfs://compodb", partitionType=COMPO, partitionScheme=[db1,db2])
```

### 创建内存数据库

内存数据库将数据直接存储在内存中，相较于传统的磁盘数据库，它具有更快的数据访问速度和更低的延迟。此外，在内存数据库中创建内存分区表，可对内存表进行并行处理，从而进一步提升数据处理效率。

内存数据库只支持通过函数 `database` 创建。当函数 `database` 的参数
*directory* 设置为空时，代表创建一个内存数据库。示例脚本如下：

```
mdb = database(directory="", partitionType=VALUE, partitionScheme=1..10)
```

## 创建表

DolphinDB 中，数据表分为内存表和分布式表。本节将分别举例介绍他们的创建方式。

### 创建分布式表

只有具备 DBOBJ\_CREATE 和 DB\_MANAGE 权限的用户或当前数据库创建者才能够创建分布式表。可通过 [getUserAccess](../../funcs/g/getUserAccess.md)
查看当前用户是否具有创建分区表的权限，如果没有，请联系管理员赋权。

#### 创建分区表

**通过** `CREATE TABLE` **语句创建 TSDB 分区表**

```
CREATE DATABASE "dfs://valuedb" PARTITIONED BY VALUE(2023.01.01..2023.12.31),engine="TSDB"
CREATE TABLE "dfs://valuedb"."pt"(
    date DATE,
    time TIME,
    sym SYMBOL,
    price DOUBLE
)
PARTITIONED BY date,
sortColumns=`time
```

**通过函数 [createPartitionedTable](../../funcs/c/createPartitionedTable.md) 创建 TSDB 分区表**

```
// 获取已创建的数据库句柄
valueDb = database("dfs://valuedb")
// 创建内存表 schemaTb
schemaTb = table(1:0,`date`time`sym`price,[DATE,TIME,SYMBOL,DOUBLE])
// 根据内存表 schemaTb 的结构创建 TSDB 分区表
pt = createPartitionedTable(dbHandle=valueDb, table=schemaTb, tableName=`pt, partitionColumns=`date, sortColumns=`sym`time)
```

更多实用细节请参考[**createPartitionedTable**。](../../funcs/c/createPartitionedTable.md)

对于组合分区的数据库，在创建分区表时，分区列个数应匹配对应的分区方案：

**通过** `CREATE TABLE` **语句**

```
CREATE TABLE "dfs://compodb"."pt"(
    date DATE,
    time TIME,
    sym SYMBOL,
    price DOUBLE
)
partitioned by date, sym
```

**通过** `createPartitionedTable` **函数**

```
// 获取已创建的数据库句柄
compoDb = database("dfs://compodb")
// 创建内存表 schemaTb
schemaTb = table(1:0,`date`time`sym`price,[DATE,TIME,SYMBOL,DOUBLE])
// 根据内存表 schemaTb 的结构创建组合分区表
pt = createPartitionedTable(dbHandle=compoDb, table=schemaTb, tableName=`pt, partitionColumns=`date`sym)
```

#### 创建维度表

**通过** `CREATE TABLE` **语句创建维度表**

```
CREATE TABLE "dfs://valuedb"."dt"(
    date DATE,
    time TIME,
    sym SYMBOL,
    price DOUBLE
)
sortColumns=`sym`time
```

**通过函数 `createDimensionTable` 创建维度表**

```
// 获取已创建的数据库句柄
valueDb = database("dfs://valuedb")
// 创建内存表 schemaTb
schemaTb = table(1:0,`date`time`sym`price,[DATE,TIME,SYMBOL,DOUBLE])
// 根据内存表 schemaTb 的结构创建维度表
dt = createDimensionTable(dbHandle=valueDb, table=schemaTb, tableName=`dt, sortColumns=`sym`time)
```

更多使用细节，请参考 [createDimensionTable](../../funcs/c/createdimensiontable.md) 。

### 创建内存表

DolphinDB 支持多种内存表，包括普通内存表、索引内存表、键值内存表、流数据表、mvcc 内存表、内存分区表和缓存表等，详情请见[表](../../progr/data_types_forms/Table.md)。

**通过** `CREATE LOCAL TEMPORARY TABLE`**语句创建普通内存表**

```
CREATE LOCAL TEMPORARY TABLE t(
      col1 INT,
      col2 DOUBLE,
      col3 STRING
)
```

**通过函数 [table](../../funcs/t/table.md) 创建普通内存表**

* 创建空表

  ```
  t = table(1:0, `ool1`col2`col3, [INT,DOUBLE,STRING])
  ```
* 根据现有数据创建内存表

  ```
  t = table(1 2 as col1, 1.1 2.2 as col2, `A1`B2 as col3)
  ```

通过 CREATE 语句和 `table` 函数创建内存表的区别在于， `table`
函数可以通过现有向量创建含有数据的内存表，CREATE 语句只能创建空表。

**通过函数 [createPartitionedTable](../../funcs/c/createPartitionedTable.md)可以创建内存分区表**

```
// 创建一个内存数据库
mdb = database("", VALUE, 1..10)
// 创建一个内存表
t = table(1:0,`id`sym`price`qty,[INT,SYMBOL,DOUBLE,INT])
// 根据内存表 t 的结构创建内存分区表
mpt = createPartitionedTable(dbHandle=mdb, table=t, tableName=`pt, partitionColumns=`id)
```

