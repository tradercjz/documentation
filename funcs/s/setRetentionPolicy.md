# setRetentionPolicy

## 语法

`setRetentionPolicy(dbHandle, retentionHours,
[retentionDimension], [hoursToColdVolume])`

## 参数

**dbHandle** 分布式数据库的句柄。数据库的分区方案必须包含 DATE 类型或 DATEHOUR 类型。

**retentionHours** 正整数，表示数据保留时间，单位是小时。

**retentionDimension** 整数，表示时间分区所在的层次。默认值是0，表示第一层分区是按时间分区。

**hoursToColdVolume** 正整数，表示 volumes 数据的保留时间，单位是小时。存储在 volumes
中的数据，经过 *hoursToColdVolume* 指定的时间后，将会自动迁移至
coldVolumes（该配置项需在配置文件中预先指定）。若不指定该参数，则 volumes 数据不会自动迁移。

注：

必须满足 *retentionHours* - *hoursToColdVolume* > 7 \*
24（即 7 天）

## 详情

设置数据保留策略以及 [TieredStorage](../../db_distr_comp/db/tiered_storage.html) 策略。若用户只通过该函数配置分级存储策略，建议将参数 *retentionHours*
指定为一个尽可能大的值。

分级存储和数据保留策略都以分区为单位进行，因此 *retentionHours* 和
*hoursToColdVolume* 配置的时间必须是分区精度的倍数，如按天分区，则需要为 24 的整数倍。

数据库会根据当前系统的机器时间，保留数据时间戳为最近 *retentionHours* 小时的数据。其中最新
*hoursToColdVolume* 小时的数据将继续存储在 volumes 中。在 [当前时间 -
*hoursToColdVolume* - 10天，当前时间 - *hoursToColdVolume*) 范围内的数据将被迁移到
*coldVolumes*。若 *coldVolumes* 配置了多个路径，则数据将随机分布在各个存储路径下 。

对于保留时间外的数据，只会删除 [当前时间 - *retentionHours* - 10 天, 当前时间 -
*retentionHours*) 范围的数据。若需要删除之前的数据，可以调用 [dropPartition](../d/dropPartition.html) 函数实现。

注： 该函数只能对分布式数据库使用。

可以通过 [schema](schema.html) 函数查看数据库的数据保留时间。

## 例子

```
db=database("dfs://db1",VALUE,2019.06.01..date(now()))
retentionHour=9*24
hoursToColdVolume=1*24
setRetentionPolicy(db,retentionHour,0, hoursToColdVolume);

schema(db);
// output
partitionSchema->[2022.05.05,2022.05.04,2022.05.03,2022.05.02,2022.05.01,2022.04.30,2022.04.29,2022.04.28,2022.04.27,2022.04.26,...]
partitionSites->
partitionTypeName->VALUE
hoursToColdVolume->24
atomic->TRANS
databaseDir->dfs://db1
engineType->OLAP
chunkGranularity->TABLE
retentionDimension->0
partitionType->1
retentionHours->216
```

