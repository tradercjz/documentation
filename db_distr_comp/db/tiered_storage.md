# 分级存储

在数据库领域，分级存储是一种常见的需求。较旧的数据（冷数据）通常不会被用户频繁查询或计算，但是存储在本地会占用大量磁盘资源。DolphinDB
集群模式支持对数据进行分级存储，即将一部分较旧的数据从高速磁盘（如 SSD）转存至较低速的磁盘（如 HDD）或云端（如 S3），从而有效节约资源。

整体逻辑流程可概括为：

热数据（volumes）→ 冷数据（coldVolumes）→ 过期数据（删除）。

DolphinDB 支持通过函数设置数据保留策略和分级存储策略，通过自动或手动的方式触发迁移流程，通过配置项指定冷盘存储目录。

## DolphinDB 的数据保留策略

数据的存活时间（TTL, Time to Live）通常用于定义数据记录的有效期限。一旦数据的存活时间超过 TTL，数据库系统将认定此记录过期，并将其删除。

数据保留策略以数据库的分区为单位，即数据库下所有表都遵循相同的数据保留策略，且要求分区方案必须包含 DATE 类型或 DATEHOUR 类型。

DolphinDB 通过 [setRetentionPolicy](../../funcs/s/setRetentionPolicy.html) 函数设置数据的保留时间。系统会根据当前的机器时间，保留时间戳在最近保留时间范围内的数据，并删除超过保留期限
10 天之内的数据。

注： 数据保留策略比较的是系统的机器时间与数据分区字段的时间，而非数据写入的时间。

## DolphinDB 的分级存储策略

DolphinDB 的分级存储策略以数据库的分区为单位，即数据库下所有表都遵循相同的分级存储策略。

DolphinDB 通过 [setRetentionPolicy](../../funcs/s/setRetentionPolicy.html) 函数设置热数据的保留时间。系统会根据当前的机器时间，保留规定的保留时间范围内的热数据。超过该保留时间 10
天内的热数据，系统会将其作为冷数据转移存储。

注： 分级存储策略比较的是系统的机器时间与数据分区字段的时间，而非数据写入的时间。

## 数据迁移机制

分级存储以分区为单位，将每个节点的分区副本迁移到低速磁盘或者 S3 对象存储中。数据迁移内部的大致流程：

1. 用户使用 [setRetentionPolicy](../../funcs/s/setRetentionPolicy.html) 函数设置 *hoursToColdVolume* 来配置热数据的保留时间。
2. DolphinDB 后台线程根据时间分区检查需要被迁移的数据，创建数据迁移任务。
3. 执行迁移任务，拷贝对应的数据文件到本地路径，或使用 AWS S3 插件多线程上传数据到 S3 路径。在迁移时，分区会暂时不可用。
4. 修改已迁移分区的元数据，更新分区路径，修改分区权限为 `READ_ONLY`，即可以使用
   `select` 语句进行查询，但是不能使用 `update`,
   `delete`, `append!` 等语句进行更新、删除或写入。

### 自动数据迁移触发机制

使用 [setRetentionPolicy](../../funcs/s/setRetentionPolicy.html)
函数设置好 *hoursToColdVolume* 后，DolphinDB 会使用后台工作线程，每隔1小时以分区为单位检查部分数据库在
`[当前时间 - hoursToColdVolume - 10天，当前时间 -
hoursToColdVolume)`范围内是否存在需要被迁移的数据，如果存在，则触发数据迁移，生成对应的数据迁移任务。由于每次只检查并触发部分数据库的数据迁移，可以有效减少迁移的压力，提高可用性。

举例来说，假设有两个按时间分区的数据库 `dfs://db1` 和 `dfs://db2`，包含
[2023.02.05, 2023.02.15) 的数据。*hoursToColdVolume* 设置为 120h，即保留 5 天内的数据：

* 在 2023.02.20 某个时间（例如17:00），工作线程可能会将 db1 下 [2023.02.05, 2023.02.15)
  分区进行迁移。
* 在 2023.02.20 某个时间（例如18:00），工作线程可能会将 db2 下 [2023.02.05, 2023.02.15)
  分区进行迁移。

### 手动触发数据迁移

使用 [moveHotDataToColdVolume](../../funcs/m/moveHotDataToColdVolume.dita) 函数，强制触发将指定范围的数据迁移。

### 自动触发和手动触发的区别

自动触发和手动触发的区别如下表所示：

| 区分点 | setRetentionPolicy | moveHotDataToColdVolume |
| --- | --- | --- |
| 触发方式 | 系统为每个数据库分配固定的检查时间点。当到达每个数据库的检查时间点时，系统会检查库中是否存在需要迁移的数据，若存在，则进行迁移。每天每个数据库仅被检查一次。 | 强制在当前数据节点触发一次数据迁移。 |
| 迁移数据的时间范围 | 只迁移 10 天的数据，范围为 `[当前时间 - hoursToColdVolumes - 10 天, 当前时间 - hoursToColdVolumes)` | 迁移数据的范围由参数 *checkRange* 指定，为 `[当前时间 - hoursToColdVolumes - checkRange, 当前时间 - hoursToColdVolumes)` |

在实际场景应用分级存储策略时，建议用户在第一次转存大量历史数据时，先通过 `setRetentionPolicy`
配置合理的自动转存策略，再通过 `moveHotDataToColdVolume`
进行批量迁移，最后由系统自动迁移冷数据。

可以通过 [getRecoveryTaskStatus](../../funcs/g/getRecoveryTaskStatus.html) 函数来查看数据迁移任务的执行状态：

```
rpc(getControllerAlias(), getRecoveryTaskStatus)
```

## 配置项

分级存储的配置项根据存储的数据可分为热数据磁盘卷配置项和冷数据磁盘卷配置项。

热数据磁盘卷配置项包括 volumes，allowVolumeCreation，volumeUsageThreshold

冷数据磁盘卷配置项为 coldVolumes

在使用分级存储前，需要先配置相应的参数：

* 冷数据磁盘卷配置项 coldVolumes

```
coldVolumes=file:/{your_local_path},s3://{your_bucket_name}/{s3_path_prefix}
```

我们使用 `coldVolumes` 配置项来指定存储冷数据的文件目录。该参数支持配置为本地路径（以”file:/“开头）或者 s3
路径（以”s3://“开头）。也可指定多个路径，路径间用逗号隔开。

例如：

```
coldVolumes=file://home/mypath/hdd/<ALIAS>,s3://bucket1/data/<ALIAS>
```

注： 不同数据节点需要配置不同的 coldVolumes
路径，否则可能会造成不同datanode间数据的相互覆盖。这里通过”<ALIAS>”宏定义，让每个datanode将数据放到/home/mypath/hdd/目录下按照节点别名命名的目录中。

如果您配置了S3路径，那么还需要配置 AWS S3 插件，以及S3的AccessKeyId，SecretAccessKey，Region等信息。

```
pluginDir=plugins //指定节点的插件目录，需要将AWS S3插件放到plugins目录下
preloadModules=plugins::awss3 //系统启动后自动加载AWS S3插件
s3AccessKeyId={your_access_key_id}
s3SecretAccessKey={your_access_screet_key}
s3Region={your_s3_region}
```

关于配置项的更多细节请参考[功能配置](../cfg/function_configuration.html)。

## 使用示例

### 配置分级存储策略

假设在上文中，我们已经配置了 `coldVolumes`：

```
coldVolumes=file://home/dolphindb/tiered_store/<ALIAS>
```

DolphinDB 通过数据的时间列来确定需要迁移的数据，所以需要对应的数据库设置按照时间分区的分区方案。首先，我们先创建一个时间列
`VALUE` 分区的数据库，并写入最近十五天的数据：

```
//创建一个按照时间列VALUE分区的数据库
db = database(directory="dfs://db1", partitionType=VALUE, partitionScheme=(date(now()) - 14)..date(now()))
//创建一个table，时间列为最近15天
data = table((date(now()) - 14)..date(now()) as cdate, 1..15 as val)
tbl = db.createPartitionedTable(data, "table1", `cdate)
tbl.append!(data)
```

接下来，我们使用 `setRetentionPolicy` 函数做如下配置：

超过五天（120h）的数据将会被迁移至冷数据层，超过三十天（720h）的数据将会删除。因为 `database` 只有一层
`VALUE` 分区，所以时间列分区维度为 0。

```
setRetentionPolicy(dbHandle=db, retentionHours=720, retentionDimension=0, hoursToColdVolume=120)
```

### 触发数据迁移

设置之后，DolphinDB 会在后台每隔 1 小时检查并迁移范围内的数据。这里为了演示方便，我们使用
`moveHotDataToColdVolume`函数来手动触发迁移。

```
//在每个datanode上执行函数，手动触发迁移
pnodeRun(moveHotDataToColdVolume)
```

之后，DolphinDB 会发起最近 15 天到最近 7 天的分区的数据迁移任务。DolphinDB 使用原有的 Recovery 机制实现数据的迁移，可以通过
`getRecoveryTaskStatus`函数来查看迁移任务的执行状态：

```
//可以看到创建了最近15天到最近7天的数据迁移任务
rpc(getControllerAlias(), getRecoveryTaskStatus)
```

可能的结果样式（省略某些列）：

| TaskId | TaskType | ChunkPath | Source | Dest | Status |
| --- | --- | --- | --- | --- | --- |
| 2059a13f-00d7-1c9e-a644-7a23ca7bbdc2 | LoadRebalance | /db1/20230209/4 | NODE0 | NODE0 | Finish |
| ... | ... | ... | ... | ... | ... |

注意：

1. 如果配置了多个 `coldVolumes`，会随机将分区迁往不同的
   `coldVolumes`。
2. 如果 `coldVolumes` 是 S3 路径，迁移速度相对于本地路径可能较慢。
3. 在迁移时，分区会暂时不可用。

当迁移任务结束之后，已经被迁移的分区权限变为 `READ_ONLY`，我们可以使用 `select`
语句进行查询，但是不能使用 `update`, `delete`,
`append!` 等语句进行更新、删除或写入。

```
//查询迁移后的数据
select * from tbl where cdate = date(now()) - 10

//更新迁移后的数据,会报错 "Writing to chunk {ChunkID} is not allowed."
update tbl set val = 0 where cdate = date(now()) - 10
```

特殊地，我们使用
`dropTable`，`dropParititon`，`dropDatabase`
等 drop DDL 操作来进行数据的整体删除时，对象存储上对应的分区数据也会被删除。这里不再赘述。

您可以使用 `getClusterChunksStatus` 函数查看对应分区的权限：

```
rpc(getControllerAlias(), getClusterChunksStatus)
```

可能的结果样式（省略某些列）：

| ChunkId | file | permission |
| --- | --- | --- |
| ef23ce84-f455-06b7-6842-c85e46acdaac | /db1/20230216/4 | READ\_ONLY（已经被迁移的分区） |
| 260ab856-f796-4a87-3d4b-993632fb09d9 | /db1/20230223/4 | EAD\_WRITE（没有被迁移的分区） |

