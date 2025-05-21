# backup

## 语法

`backup(backupDir, dbPath|sqlObj, [force=false], [parallel=false],
[snapshot=true], [tableName], [partition], [keyPath])`

## 参数

**backupDir** 字符串，表示存放备份数据的目录。如需备份到 AWS S3 存储路径，此参数的值应以 `s3://`
开头。

**dbPath** 字符串，表示数据库路径。若指定该参数，以分区为单位拷贝文件进行备份。

**sqlObj** SQL 元代码，表示备份的数据。若指定该参数，则仅对 SQL 语句过滤出的数据进行备份。

**force** 布尔值，表示是否进行全量备份。进行非首次备份时，若 *force* =
true，系统将待备份数据全部进行备份；否则仅备份有修改或新增的分区数据。

**parallel** 布尔值，表示是否对一个数据表下不同分区进行并行备份。默认值为 false。

以下参数仅在指定 *dbPath* 时有效：

**snapshot** 布尔值，仅在参数 *partition*
为空时有效。表示进行非首次备份时，源数据库中若存在被删除的表/分区，是否同步将备份中对应的表/分区删除。 若设置为
true，则备份文件中存在已经被删除的分区或表，会同步进行删除；否则不会删除。

**tableName** 字符串标量或向量，表示表名。若不指定，表示数据库下的所有表。

**partition** 表示分区，若不指定，则表示所有分区。有两种指定模式：

* 指定路径：以 "/" 开头的字符串标量或向量，表示数据库目录下单个或多个分区的路径。请注意对组合分区，路径必须包括所有层次分区。
* 指定条件：以分区列的一个或多个值作为过滤条件。对于组合分区，*partition*是一个元组，每个元素代表一层分区的过滤条件，如果某层分区不需要过滤，那么相应的过滤条件需置为空。需要注意的是，对于范围分区，需要指定为分区内的一个值。

  假如一个组合分区数据库 "dfs://compoDB"，一级分区采用值分区：2017.08.07；二级分区采用哈希分区：Key0 和
  Key1。分区数据的路径分别为：<HomeDir>/storage/CHUNKS/compoDB/20170807/Key0 和
  <HomeDir>/storage/CHUNKS/compoDB/20170807/Key1。若要备份单个分区
  20170807/Key0，指定路径时需要设置 *partition* = "/20170807/Key0"；指定条件时需要设置
  *partition* = [2017.08.07, 0]。若要备份两个分区 20170807/Key0 和
  20170807/Key1，则 *partition* 指定为 ["/20170807/Key0",
  "/20170807/Key1"]；指定条件时需要设置 *partition* = [2017.08.07,[0,1]]。

**keyPath** 字符串标量，指定备份时使用的密钥文件路径。仅 Linux 系统支持该参数。该密钥用于对备份数据进行加密。设置为空即不加密。

## 详情

以分区为单位，备份分布式表的数据。返回一个整数，表示备份成功的分区数量。该函数必须要用户登录后才能执行。

注：

* 若 [database](../d/database.md)
  创建数据库时，指定 *chunkGranularity* = 'DATABASE'，则只能通过 SQL 语句备份数据。
* 若 *backupDir*
  目录已存在备份文件，则再次向该目录备份数据时，需保证备份方式（*dbPath* 或
  *sqlObj*）一致，否则将备份失败。
* 若 ***backupDir*** 指定为 AWS S3 存储路径，则只能以分区方式备份，即只支持
  *dbPath*，不支持 *sqlObj*。
* 若 ***backupDir*** 指定为 AWS S3 存储路径，需要在数据节点的配置中添加配置项
  *preloadModules=plugins::awss3*，同时设置
  *s3AccessKeyId*、*s3SecretAccessKey* 和
  *s3Region*。

## 补充说明

备份时指定 *dbPath* 和 *sqlObj* 的功能列表：

| 功能 | dbPath | sqlObj |
| --- | --- | --- |
| 一键备份整库 | 支持 | 不支持 |
| 数据一致性 | 保证数据一致性 | 不完全保证 |
| 增量备份 | 支持同步已修改、新增及删除的分区数据 | 只支持同步已修改或新增的分区数据，不支持同步已删除的分区数据 |
| 断点续传 | 支持 | 不支持 |
| 灵活语法 | 不支持 | SQL 语句，具有灵活语法，支持备份整张表或仅备份满足查询条件的数据 |
| 性能 | 拷贝文件方式，内存消耗小，速度快 | 序列化方式，内存消耗大，速度慢 |

## 例子

创建一个组合分区的数据库 dfs://compoDB。

```
n=1000000
ID=rand(100, n)
dates=2017.08.07..2017.08.11
date=rand(dates, n)
x=rand(10.0, n)
t=table(ID, date, x)

dbDate = database(, VALUE, 2017.08.07..2017.08.11)
dbID=database(, RANGE, 0 50 100);
db = database("dfs://compoDB", COMPO, [dbDate, dbID])
pt = db.createPartitionedTable(t, `pt, `date`ID)
pt.append!(t)
```

例1. 备份表 pt 的所有数据。

```
backup("/home/DolphinDB/backup",<select * from loadTable("dfs://compoDB","pt")>,true);
// output
10
```

例2. 备份表 pt 中日期超过2017.08.10的数据。

```
backup("/home/DolphinDB/backup",<select * from loadTable("dfs://compoDB","pt") where date>2017.08.10>,true);
// output
2
```

例3. 备份数据库中表数据。

(1) 备份指定表或所有表

```
// dfs://compoDB 数据库下创建第2张表
pt1 = db.createPartitionedTable(t, `pt1, `date`ID)
pt1.append!(t)

// 同时备份数据库中的两张表
backup(backupDir="/home/DolphinDB/backup",dbPath="dfs://compoDB",force=true);
// output
20
```

(2) partition 指定分区范围

```
// 备份数据库中表 pt 的指定的5个分区
partitions=["/20170807/0_50","/20170808/0_50","/20170809/0_50","/20170810/0_50","/20170811/0_50"]
backup(backupDir="/home/DolphinDB/backup",dbPath="dfs://compoDB",force=true,tableName=`pt,partition=partitions);
// output
5
```

(3) partition 指定过滤条件。请注意，对于范围分区，指定分区范围内的一个值，表示整个分区。

```
// 备份数据库中表 pt 的一级分区 20170807 内的 50_100 的分区
partitions=[2017.08.07,50]
backup(backupDir="/home/DolphinDB/backup",dbPath="dfs://compoDB",force=true,tableName=`pt,partition=partitions);
// output
1
// 备份数据库中表 pt 的所有一级分区内的 0_50 的分区
partitions=[,[0]]
backup(backupDir="/home/DolphinDB/backup",dbPath="dfs://compoDB",force=true,tableName=`pt,partition=partitions);
// output
5
```

例4. 通过下例说明 *snapshot* 参数的作用

```
// 删除表 pt 中分区"/20170811/0_50"
db.dropPartition("/20170811/0_50",`pt)
//再次备份，指定snapshot=false
backup(backupDir="/home/DolphinDB/backup1",dbPath="dfs://compoDB",force=true,snapshot=false,tableName=`pt);
// output
9
// 从备份中恢复的分区仍包含 /20170811/0_50 这个分区，说明备份文件中并没有删除/20170811/0_50 这个分区
restore(backupDir="/home/DolphinDB/backup1",dbPath="dfs://compoDB",tableName=`pt,partition="%",force=true)
// output
["dfs://compoDB/20170807/0_50/9m9","dfs://compoDB/20170807/50_100/9m9","dfs://compoDB/20170808/0_50/9m9",
    "dfs://compoDB/20170808/50_100/9m9","dfs://compoDB/20170809/0_50/9m9","dfs://compoDB/20170809/50_100/9m9",
    "dfs://compoDB/20170810/0_50/9m9","dfs://compoDB/20170810/50_100/9m9","dfs://compoDB/20170811/0_50/9m9",
    "dfs://compoDB/20170811/50_100/9m9"]

// 再次删除表pt中分区"/20170811/0_50"
db.dropPartition("/20170811/0_50",`pt)

// 再次备份，指定snapshot=true
backup(backupDir="/home/DolphinDB/backup",dbPath="dfs://compoDB",force=true,snapshot=true,tableName=`pt);
// output
9
// 从备份中恢复的分区不包含 /20170811/0_50 这个分区，说明备份文件中删除了/20170811/0_50 这个分区
restore(backupDir="/home/DolphinDB/backup",dbPath="dfs://compoDB",tableName=`pt,partition="%",force=true)
// output
["dfs://compoDB/20170807/0_50/9m9","dfs://compoDB/20170807/50_100/9m9","dfs://compoDB/20170808/0_50/9m9",
    "dfs://compoDB/20170808/50_100/9m9","dfs://compoDB/20170809/0_50/9m9","dfs://compoDB/20170809/50_100/9m9",
    "dfs://compoDB/20170810/0_50/9m9","dfs://compoDB/20170810/50_100/9m9","dfs://compoDB/20170811/50_100/9m9"]
```

相关函数：[backupDB](backupDB.md), [backupTable](backupTable.md), [restore](../r/restore.md), [migrate](../m/migrate.md)

