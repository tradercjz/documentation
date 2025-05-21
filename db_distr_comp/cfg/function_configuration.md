# 功能配置

## 安全与稳定

| 配置参数 | 解释 | 配置节点 |
| --- | --- | --- |
| enableClientAuth | 设置是否开启用户登录验证。默认为 false。设置为 true 时，访客用户必须登录才能执行脚本。具体限制规则参见访问控制与登录安全。 | 控制节点 |
| strictSecurityPolicy | 为集群启用严格的安全策略。启用后的主要变化包括支持设置会话过期时间、自动释放用户自定义对象等。详见访问控制与登录安全。 | 控制节点 |
| thirdPartyAuthenticator | 指定一个函数视图（其参数和 login 函数的参数一致），用于第三方系统校验用户权限。用户通过 DolphinDB 的 HttpClient 等插件与第三方用户系统建立连接。通过指定该参数，在用户登录时，系统会通过第三方系统进行权限验证。 注： 该配置项指定的函数视图，在回调时仍要求调用者具有相关权限。 | 控制节点 |
| thirdPartyCreateUserCallback | 指定一或多个函数视图名称，用于在创建用户时回调从而验证权限。为该配置项指定多个函数视图时，函数视图名称之间以逗号分隔，回调顺序由左向右顺序执行。 注：  * 该配置项指定的函数视图在回调过程中出现异常时，异常将被忽略并分别记录于日志中。回调结束后，最后一次的回调异常消息（例如：`Failed   to call createUser callback [func1] with error   xxx`）将会抛出。 * 该配置项指定的函数视图，在回调时仍要求调用者具有相关权限。 | 控制节点 |
| thirdPartyDeleteUserCallback | 指定一或多个函数视图名称，用于在删除用户时回调从而验证权限。为该配置项指定多个函数视图时，函数视图名称之间以逗号分隔，回调由左向右顺序执行。 注：  * 该配置项指定的函数视图在回调过程中出现异常时，异常将被忽略并分别记录于日志中。回调结束后，最后一次的回调异常消息（例如：`Failed   to call deleteUser callback [func1] with error   xxx`）将会抛出。 * 该配置项指定的函数视图，在回调时仍要求调用者具有相关权限。 | 控制节点 |
| enhancedSecurityVerification=false | 布尔值，表示是否启用密码复杂性验证，及约束密码重试次数的功能。默认值为 false，不启用；若设置为 true，则启用该功能，此时：  * 创建或修改的密码必须满足以下条件：   + 字符个数为8~20   + 至少包含一个大写字母   + 至少包含以下字符之一：!"#$%&'()\*+,-./:;<=>?@[]^\_`{|}~。 * 当某个用户登录时，在1分钟内连续5次输入错误密码，系统将禁止该用户通过相同 IP   地址进行登录。10分钟后才允许该用户通过相同 IP 地址再次登录。   注： 配置项 *failedLoginLockTime*，*failedLoginAttempts*，*passwordMinLength*，*passwordMaxLength*，*passwordMinUpperCase*，*passwordMinLowerCase*，*passwordMinDigital*，*passwordMinSpecial*仅在 *enhancedSecurityVerification*=true 时生效。 | 控制节点 |
| failedLoginLockTime | 用户连续登录失败后被锁定的时间，单位为分钟，默认值为 10。 | 控制节点 |
| failedLoginAttempts | 用户在最近 *failedLoginLockTime* 分钟内，连续登录失败 *failedLoginAttempts* 次，将被锁定 *failedLoginLockTime* 分钟。 | 控制节点 |
| passwordMinLength | 密码的最小长度，默认值为 6。 | 控制节点 |
| passwordMaxLength | 密码的最大长度，默认值为 20。 | 控制节点 |
| passwordMinUpperCase | 密码包含大写字母（A-Z）的最少个数，默认值为 1。 | 控制节点 |
| passwordMinLowerCase | 密码包含小写字母（a-z）的最少个数，默认值为 0。 | 控制节点 |
| passwordMinDigital | 密码包含数字（0-9）的最少个数，默认值为 0。 | 控制节点 |
| passwordMinSpecial | 密码包含特殊字符的最少个数，默认值为 1。  特殊字符包括：!"#$%&'()\*+,-./:;<=>?@[]^\_`{|}~ | 控制节点 |
| passwordEffectTime | 密码的有效期，单位为天。默认值为 0，表示不设置有效期。 | 控制节点 |
| passwordNotifyTime | 密码过期前的提醒时间。系统会在密码到期前 *passwordNotifyTime* 天，在用户登录时提醒其修改密码。默认值为 7。 | 控制节点 |
| strictPermissionMode | 设置在当前节点，是否对磁盘读写、加载插件等操作进行严格权限限制：  * 默认值为 false，表示所有非 guest 用户都可执行上述操作。 * 当设置为 true 时，只有管理员用户可以执行。   注： 通常所有需要严格权限限制的节点都需要添加此配置项。受其影响的操作： saveTextFile, saveAsNpy, backup, restore, restoreDB, restoreTable, backupDB, backupTable, migrate, file, files, writeObject, readObject, loadPlugin, close, fflush, mkdir, rmdir, rm, writeLog, run, runScript, test, saveTable, savePartition, saveDualPartition, saveDatabase, saveText, loadText, loadModule, saveModule | 控制节点，数据节点，计算节点 |
| enableShellFunction | 设置是否允许用户调用 `shell` 函数：  * 默认为 false，禁止任何用户调用。 * 当设置为 true 时，仅允许管理员用户调用。 | 控制节点、数据节点、计算节点 |
| enableCoreDump=true | dolphindb 进程启动时，是否检查并修改 core dump 的启用情况。默认值为 true，此时若发现 core dump 未启用，则在系统硬限制允许的情况下为进程开启 core dump；如果发现 core dump 已开启，则不会做任何修改。当设置为 false 时，则不会进行检查。仅 Linux 系统支持该配置项。 | 数据节点 |
| disableCoreDumpOnShutdown=true | 设置安全关机时是否禁用 core dump。默认值为 true，表示安全关机时禁用 core dump。此参数仅对配置文件对应的节点生效。 | 数据节点 |
| enableHctEncryption | 布尔值，设置是否使用海光密码技术 HCT（Hygon Cryptographic Technology）对静态加密、DolphinModule 加密进行加速。默认值为 false，不会对加密操作进行加速。  * 在海光机器上使用 HCT 时，系统会动态加载操作系统中已存在的 hct.so   相关动态库。若未找到对应路径，则会记录日志：`Failed to initialize the   HCT engine for encryption. Using the default   engine`. 此时，需要通过环境变量 *OPENSSL\_ENGINES*   指定动态库路径，例如`OPENSSL_ENGINES="/usr/lib64/engines-1.1"`. * 在海光机器上加载成功时，会记录 DEBUG 日志：Using HCT engine. * 在非海光机器上配置该配置项，不会对加密操作进行加速，并记录日志：`Failed to initialize   the HCT engine for encryption. Using the default   engine`. | 数据节点 |
| TDEKeyDir | 字符串标量，指定系统加载 TDE 密钥文件目录的绝对路径。仅 Linux 系统支持该配置项。如需启用数据静态加密，集群模式下，需要修改所有控制节点和数据节点配置文件（*controller.cfg* 和 *cluster.cfg*）。 | 控制节点、数据节点 |

在 redo log
章节介绍了重做日志相关的配置项。重做日志机制的目的就是为了防止节点宕机后数据丢失。启用重做日志机制，必须启用参考`Cache
Engine`相关内容，同时配置对应的日志存储路径。

在集群环境下，若某个节点发起的事务未完成时，发生了节点宕机。此时，用户可选择手动重启节点，或者经过
datanodeRestartInterval 的时间，集群会自动重启该节点。

| 配置参数 | 解释 | 配置节点 |
| --- | --- | --- |
| datanodeRestartInterval=0 | 表示不会自动启动数据/计算节点，为一个非负 INT 类型，单位为秒。默认值为 0。配置该参数可以实现以下功能：  * 控制节点启动后自动启动数据/计算节点（需要启动 agent）； * 数据/计算节点离线的时间超过设置时长（t）后自动重启该节点（需要启动 agent）。   注： 若 server 的版本号小于 2.00.9.4，则该参数必须设置为 100+t，其中100是系统预定义值。 | 控制节点 |
| datanodeRestartLevel=CRASH | 指定触发控制节点自动重启数据节点/计算节点的条件。包含如下可选值（区分大小写）：  * CRASH（默认值）：当节点不是通过 [stopDataNode](../../funcs/s/stopDataNode.html) 命令关闭，且超过 *datanodeRestartInterval*时间没有发送心跳给控制节点时，控制节点将会自动启动该节点。 * OFFLINE：节点不在线，且超过 *datanodeRestartInterval*   的时间没有发送心跳给控制节点时，控制节点将自动启动该节点。 | 控制节点 |

## 存算分离

自 3.00.2 版本起，DolphinDB
实现了存算分离架构。该架构通过引入计算组，将计算节点加入计算组，实现真正的存算分离。计算节点可以缓存部分数据。以下将介绍计算节点缓存的相关配置。

注：

为所有计算组或匹配的计算组指定 *computeNodeCacheDir* 或 *computeNodeCacheMeta*
时，必须使用宏变量
<ALIAS>（例如：computeNodeCacheDir=/SCSeparationDDB/Disaggregation/<ALIAS>）；但在为计算节点指定这两个参数时，不能使用宏变量
<ALIAS>。

| 配置参数 | 解释 | 配置节点 |
| --- | --- | --- |
| computeNodeCacheDir = *<HomeDir>/Disaggregation* | 计算节点的缓存目录。支持一个节点上指定多个物理路径作为缓存目录，路径间以逗号（`,`）分隔，系统将根据磁盘负载进行分配。例如：/volume0/path/to/cache, /volume1/path/to/cache, /volume2/path/to/cache。 | 计算节点 |
| computeNodeCacheMeta | 计算节点缓存元数据的唯一地址，默认为*<computeNodeCacheDir>/meta*。如果*computeNodeCacheDir* 指定了多个路径，取第一个。 | 计算节点 |
| computeNodeMemCacheSize | 非负整数，表示计算节点的内存缓存容量上限，单位为 GB，默认值为 1。其取值范围为 [0, 5% \* maxMemSize]，如果设置的值超过了 5% \* maxMemSize，将被自动调整为 5% \* maxMemSize。 | 计算节点 |
| computeNodeDiskCacheSize | 非负整数，表示计算节点的磁盘缓存容量上限，单位为 GB，默认值为 64。 | 计算节点 |
| enableComputeNodeCacheEvictionFromQueryThread | 布尔值，默认为 true。表示是否允许查询线程执行缓存驱逐。缓存驱逐机制提高缓存清理的效率，更好地管理内存和磁盘的使用，减少因内存不足（OOM）导致的错误。然而，当缓存容量紧张时，这种机制可能导致查询延迟增加。 | 计算节点 |
| computeNodeCachingDelay | 非负整数，表示时间间隔，单位为秒，默认值为 360。该参数规定了一个分区在最后一次更新后，需经过设定的时间间隔，才能被缓存到计算节点。 | 控制节点 |
| computeNodeCachingQueryThreshold | 非负整数，表示访问次数。取值范围为 [0, 32767]，默认值为 1。当一个分区的访问次数超过设定的阈值后，才允许将该分区缓存到计算节点。 | 控制节点 |
| enableComputeNodePrefetchData | 布尔值。若设置为 true（默认值），在计算组中，如果某个分区的缓存没有命中（即请求的数据不在缓存中），系统会将该查询请求下推到数据节点执行，同时会异步地在计算节点中执行相同的查询，以缓存数据（这称为”预热缓存“）。若设置为 false，即使缓存没有命中，系统也不会将查询请求下推到数据节点执行，意味着查询只能在计算节点中处理。开启数据预取可以减少查询时因缓存未命中而导致的延迟，但由于需要执行两次查询，这可能会增加网络和 CPU 的负担。 | 控制节点 |

## 多集群管理

自 3.00.2 版本起，DolphinDB
新增多集群管理工具，能够实现多集群网络互通、跨集群资源调度（跨集群访问数据）等功能。多集群管理中的角色有两种：集群管理者（MoM
集群）和成员集群。这里将给出适用于不同角色的配置项说明。

| 配置参数 | 解释 | 配置节点 |
| --- | --- | --- |
| isMasterOfMaster | 布尔值，表示该节点是否为 MoM 节点。 | 单节点或控制节点 |
| momHeartbeatHandler | 字符串，表示回调函数的函数视图名称。当多集群的管理者（Master of Master，简称 MoM）收到成员集群的 Master 汇报的心跳信息时，将心跳信息作为参数调用回调函数。若指定多个函数视图名称，名称之间以逗号分隔。回调函数将按照从左到右的顺序依次执行。 | MoM 节点 |
| masterOfMasterSite | 字符串，格式为host:port，表示 MoM 节点的 IP 地址和端口号。 | 成员集群的控制节点 |
| clusterName | 字符串，表示当前集群的名称。命名规则见[变量](../../progr/objs/var.html)。 | MoM 节点/成员集群的控制节点 |

## 高可用

控制节点存储了集群访问所需的元数据信息。普通集群只包含一个控制节点，若控制节点发生宕机，将造成集群瘫痪。为了避免这种情况，DolphinDB 允许多个控制节点组成
raft 组，来实现控制节点的高可用。

启用控制节点高可用，需要在 raft 组中各个 controller 的 config 文件（默认
controller.cfg）中指定配置项 dfsHAMode=Raft。

| 配置参数 | 解释 |
| --- | --- |
| dfsHAMode=Raft | 多个控制节点是否组成 raft 组。 |

同时需要修改所有 agent 的 config 文件（默认为 agent.cfg），代理节点配置的 controllerSite
可指定为 raft 组的任一节点。在代理节点信息后必须增加 sites 参数，需包含本机器代理节点和所有控制节点的局域网信息。

| 配置参数 | 解释 |
| --- | --- |
| sites | 用于指定其它节点局域网信息。格式同 localSite，多个节点间用 "," 隔开。 |

同时需要在 nodesFile 增加所有集群节点的网络信息。

此外，DolphinDB 还提供了配置参数用于设置 raft。该参数需在控制节点的 config 文件配置。

| 配置参数 | 解释 |
| --- | --- |
| raftElectionTick=800 | 确定一个时间区间（单位为10ms）：[raftElectionTick, 2 raftElectionTick]。follower 在收到上一个心跳后，经过该区间内一个随机时刻之后仍然没有收到 leader 的心跳，则会发出竞选 leader 的请求。默认值为800，即8s，确定的时间区间为[8s, 16s]。注意：需要保持 raft 组内所有控制节点的配置一致。 |

为了保证数据的安全和高可用，DolphinDB
支持在不同的服务器上存储多个数据副本，并且采用二阶段提交协议实现数据副本之间以及数据和元数据之间的强一致性。即使一台机器上的数据损坏，也可以通过访问其他机器上的副本数据来保证数据服务不中断。要开启副本数和备份机制，需在控制节点的
config 文件配置以下参数：

| 配置参数 | 解释 |
| --- | --- |
| dfsReplicationFactor=2 | 每个表数据块的所有副本数。集群的默认副本数是2，单节点的默认副本数为1。注意：写入数据时 on-line 的数据节点数必须大于等于 dfsReplicationFactor 的值，否则会抛出异常。 |
| dfsReplicaReliabilityLevel=0 | 多个副本是否可以在同一个物理服务器上。 0表示可以；1表示不可以；2表示在资源允许情况下，副本优先部署在多台物理服务器。默认值是0。 |

多副本集群环境下，若某个数据节点宕机，将会造成集群的副本数和配置项 dfsReplicationFactor 不一致。此时若配置了
dfsRecoveryWaitTime，系统将在等待 dfsRecoveryWaitTime 时间后，将不一致的副本复制给其它节点。该参数默认值为
0，表示一直等待节点恢复，不发起副本复制任务。该参数也需在控制节点的 config 文件配置。

| 配置参数 | 解释 |
| --- | --- |
| dfsRecoveryWaitTime=0 | 数据节点宕机后，控制节点需要把此节点的数据副本在其它数据节点重新恢复，以保持副本数的一致。恢复前的等待时间可通过该参数进行配置（单位为毫秒）。默认值是0，表示不开启恢复。若不为 0，则系统内部最小等待时间为60000毫秒，也就是60秒，如果填入的数值小于60000，则会被设置为60000。 |

## 日志

### 运行日志：log

server 启动后，系统将会自动产生运行时信息，可以通过命令行配置参数 stdoutLog
决定是否将信息输出到命令行或运行日志（log）中。log 文件的路径信息可由配置项 logFile 进行指定：

| 配置参数 | 解释 |
| --- | --- |
| logFile=DolphinDBlog | 日志文件的路径和名称。日志文件包含服务器配置的详细内容，警告和错误信息。该参数只能在命令行中指定。 |

单个日志文件大小存在上限，由 [StandaloneMode](standalone.html) 章节提到的配置参数 maxLogSize 决定。超过该值后，DolphinDB
将自动生成一个前缀为时间戳（精确到秒）的新的日志文件，以此类推。当旧的系统日志占用大量系统资源时，可通过配置 logRetentionTime
定时删除。

| 配置参数 | 解释 | 配置节点 |
| --- | --- | --- |
| logRetentionTime=30 | 设置系统日志的保留时间。超过指定保留时间的日志将被删除。默认值为 30，单位是“天”，类型为浮点型，如：0.5 表示 12 小时。若设置为 0，表示不进行清理。 | 控制节点、代理节点、数据节点 |

为了更快定位问题，DolphinDB 支持输出指定等级的日志。可通过配置项 logLevel
在启动前配置，或通过函数 [setLogLevel](../../funcs/s/setLogLevel.html)
在线修改。

| 配置参数 | 解释 |
| --- | --- |
| logLevel=INFO | 日志文件的保留层次。默认值为 INFO。可设置值从低到高为 DEBUG，INFO，WARNING 和 ERROR。日志文件只保留等于或高于 logLevel 取值的日志记录。 |

### 重做日志：redo log

当事务完成后，系统会自动检测回收其对应的 redo log。DolphinDB 提供了配置项，支持对 redo log
的回收过程进行调优。

| 配置参数 | 解释 |
| --- | --- |
| redoLogPurgeInterval=30 | 删除重做日志（redo log）的时间间隔（单位是秒），默认值是30。每隔 redoLogPurgeInterval 秒，系统会自动删除已完成事务的重做日志。 |
| redoLogPurgeLimit=4 | 重做日志（redo log）占用磁盘空间的上限（单位是 GB），默认值是4。如果重做日志占用磁盘超过 redoLogPurgeLimit，系统会自动删除已完成事务的重做日志。 |

### 作业日志：job log

用户提交的批处理作业和定时作业的执行信息均保存在 batchJobDir 目录下。

| 配置参数 | 解释 | 配置节点 |
| --- | --- | --- |
| batchJobDir | 保存批量作业和定时作业日志和结果的文件夹目录。如果没有指定，单节点模式下，默认目录是 <HomeDir>/batchJobs。集群模式下，默认目录是<HomeDir>/<nodeAlias>/batchJobs。 | 数据节点 |
| batchJobFileRetentionTime | 设置批处理作业和定时任务的输出（保存在 \*.msg 文件中） 和返回值（保存在 \*.obj 文件中）的最长保留时间，避免长期累积占用过多磁盘空间。此参数为 double 类型，单位是天。默认值为 0，表示不清理任务输出和返回值。 | 数据节点 |

### 节点查询信息日志

集群环境下，系统还保存了各节点的查询信息的日志（job log）。

| 配置参数 | 解释 | 配置节点 |
| --- | --- | --- |
| jobLogFile=nodeAlias\_job.log | 节点工作日志的存储路径，用于记录每个节点上已经执行的所有查询的描述性信息。默认和 logFile 指定 log 文件存储在同一路径下。工作日志文件的默认名是 `nodeAlias_job.log`。 | 数据节点 |
| jobLogRetentionTime=0 | 当节点的查询信息日志（\*\_job.log）大小超过 1GB 时，系统会将该日志文件存档，并将后续日志写入新的文件。此参数为 double 类型，单位是天，用于指定存档的最长保留时间。默认值为 0，表示不清理存档。 | 数据节点 |

DolphinDB 在 2.00.11.1 版本中为数据节点加入 enableDFSQueryLog 配置项。

| 配置参数 | 解释 | 配置节点 |
| --- | --- | --- |
| enableDFSQueryLog=false | 用于记录所有对分布式表已完成和进行中的查询和子查询。默认为 false。启用 perfMonitoring 配置项且该配置项设置为 true 后，`nodeAlias_job.log` 所在目录下会生成一个名为 `nodeAlias_query.log` 的查询日志文件，包含以下字段：*node*, *userId*, *sessionId*, *rootId*, *type*, *level*, *time*, *database*, *table*, *jobDesc*，其中 *database* 和 *table* 字段在子查询记录中显示为空。 | 数据节点 |
| queryLogRetentionTime=0 | 当节点查询日志文件 `nodeAlias_query.log` 的大小超过 1GB 时，系统会将该日志文件存档，并将后续日志写入新的文件。此参数类型为浮点型，单位是天，用于指定存档的最长保留时间。默认值为 0，表示不清理存档。 | 数据节点 |

注： `nodeAlias_query.log`
与 `nodeAlias_job.log` 尽管在功能和记录字段上相似，但不同之处在于：

* `nodeAlias_job.log` 仅记录成功的查询；
* `nodeAlias_query.log` 不仅记录成功的查询，也记录进行中的查询。

该配置项的使用有助于发现正在执行中的耗时过长的查询或节点故障时正在执行的查询命令，从而排查可能导致节点阻塞或死锁的原因。

### SQL Trace 日志

SQL Trace 日志的存储位置由 traceLogDir 指定。

| 配置参数 | 解释 |
| --- | --- |
| traceLogDir | SQL Trace 过程日志的存储路径，默认为 <HomeDir>/traces。 |

### 审计操作日志

DolphinDB 可以将数据库上执行的 DDL 操作记录到独立的审计日志文件 <logFile>/<ALIAS>\_audit.log 中，同时将
ACL 操作（登录登出，权限修改、新建连接和配置文件修改）记录到独立的审计日志文件 <logFile>/<ALIAS>\_aclAudit.log
中。当 *enableStructuredAuditLog* 设置为 true 时，审计日志将以二进制格式存储，文件名分别为
<ALIAS>\_audit.audit 和 <ALIAS>\_aclAudit.audit。二进制审计日志无法直接读取或修改，用户可以通过
`getAuditLog` 和 `getAclAuditLog`
函数获取对应的审计日志信息。

单个审计日志文件的大小上限为 128M ，超过该值后，DolphinDB 将自动生成一个前缀为时间戳（单位为秒）的日志文件用于存储历史日志。历史日志可通过配置参数
*logRetentionTime* 定时删除。

| 配置参数 | 解释 | 配置节点 |
| --- | --- | --- |
| enableAuditLog | 是否将数据库上执行的 DDL、ACL（登录登出、权限修改、新建连接和配置文件修改等）操作记录到独立的日志文件中。默认值为 false，表示不开启此功能；设置为 true 时，则开启此功能。 | 数据节点 |
| enableStructuredAuditLog | 是否开启结构化二进制格式的审计日志，默认值为 false。 | 数据节点 |
| auditLogRetentionTime | 设置历史审计日志的保留时间。超过指定时间的日志将被删除。单位是“天”，类型为浮点型。例如：0.5 表示 12 小时。默认值为 0 ，代表不清理存档。 | 数据节点 |

## 线程

DolphinDB 采用多线程技术，有以下几种常见的线程类型：

* worker：常规交互作业的工作线程，接收客户端请求，将任务分解为多个小任务，根据任务的粒度自己执行或者发送给
  local executor 或 remote executor 执行。

  从 2.00.10 版本开始，DolphinDB 引入了多级任务算法，即将作业及其拆分出来的子任务区分为不同的层级，并分配给相应层级的 worker
  来处理。DolphinDB 提供了0~5个级别的 worker。 客户端提交至节点的作业为0级，由0级 worker
  处理。根据作业所涉及到的分区，0级 worker 将作业分解为多个子任务，其中本地节点上的子任务由0级或1级 worker
  并行执行；需要由远程节点执行的子任务则降低为1级，并通过 remote executor 发送到对应节点上的1级 worker
  处理。以此类推，若某个级别的子任务需要进一步拆解，则拆分出来的由远程节点执行的子任务降低一级，发送至远程节点上对应层级的 worker 处理。
  这种根据任务层级分配不同层级 worker 的线程工作机制，可以有效避免因各个子任务执行期间彼此依赖而导致的死锁问题。
* remote
  executor：远程执行线程，将子任务发动到远程节点的独立线程。远程执行线程具有容错机制。在多个计算机都包含任务所需数据的副本的情况下，如果一台计算机出现故障，远程执行线程将该任务发送到另一台计算机。
* batch job worker：批处理作业的工作线程。其上限通过配置项 maxBatchJobWorker
  设置，默认值是workerNum。该线程在任务执行完后若闲置60秒则会被系统自动回收，不再占用系统资源。
* dynamic worker：动态工作线程，作为 worker 的补充。其上限通过配置项
  maxDynamicWorker 设置，默认值是
  workerNum。如果所有的工作线程被占满，有新任务时，系统会创建动态工作线程来执行任务。根据系统并发任务的繁忙程度，总共可以创建三组动态工作线程，每一个级别可以创建
  maxDynamicWorker 个动态工作线程。该线程在任务执行完后若闲置60秒则会被系统自动回收，不再占用系统资源。
* web worker：处理 HTTP 请求的工作线程。DolphinDB 提供了基于 web
  的集群管理界面，用户可以通过web 与 DolphinDB 节点进行交互。其上限通过配置项 webWorkerNum 设置，默认值是1。
* urgent worker：紧急工作线程，只接收一些特殊的系统级任务，譬如登录，取消作业等。其上限通过配置项
  urgentWorkerNum 设置，默认为1。

注： worker 的数量直接决定了系统的并发计算的能力。

相关配置参数：

| 配置参数 | 解释 |
| --- | --- |
| workerNum | 常规作业的工作线程的数量。默认值是 CPU 的内核数。 |
| remoteExecutors=1 | 远程执行线程的数量。默认值是 1，建议配置为集群节点数减 1。 |
| maxBatchJobWorker=4 | 批处理作业的最大工作线程数量。默认值是 workerNum 的值。 |
| maxDynamicWorker=4 | 动态工作线程数量的最大值。默认值是 workerNum 的值。 |
| webWorkerNum=1 | 处理HTTP请求的工作线程的数量。默认值是 1。 |
| urgentWorkerNum=1 | 紧急工作线程的数量。默认值是 1。 |
| enableMultiThreadMerge | 布尔值，表示是否允许在执行 SELECT 查询的分区任务后按列多线程合并结果表。默认值为 false，表示禁用多线程合并。该配置参数对具有大量分区数量和分区查询结果的场景会有明显提升效果。注意：该参数设置为 true 后，须保证分区查询结果的列数不小于 2、且总行数 \* 总列数大于 5000 万，满足该条件才会进行多线程合并；否则不生效。 |

参考线程教程：[线程模型](../../tutorials/threading_model.html)

下述配置参数应用于编程时，可能影响计算规则或者计算性能：

| 配置参数 | 解释 | 配置节点 |
| --- | --- | --- |
| openblasThreads | openBLAS 可以工作的线程数。应用于矩阵计算场景。 | 数据节点 |

## 内存

在使用 DolphinDB 进行大数据查询和计算时，可能会遇到内存不足导致的 OOM（内存溢出）问题。为尽量避免这种情况，DolphinDB
提供了一些内存调优参数，帮助管理内存使用。

最大内存限制（*maxMemSize* 指定）决定了 DolphinDB
运行在服务器的内存上限，它是常规内存区、小对象内存区（*reservedMemSize*指定）和紧急内存区（*emergencyMemSize*）三部分的总和。具体来说：

* 当使用内存超过常规内存时，DolphinDB 会进入“小对象分配”状态，避免一次性申请过多内存导致溢出。会对每次分配的内存大小进行限制，通过
  *maxBlockSizeForReservedMemory* 控制。
* 当小对象内存区用满后，系统会停止为常规任务分配内存。此时，紧急内存区会为一些紧急任务分配内存，例如存储引擎的刷盘操作，或分布式写入事务提交时的关键步骤等。
* 当紧急内存区也用满，即 *maxMemSize* 完全用满后，DolphinDB 将停止为所有任务分配内存，仅允许管理员取消任务（详见[系统卡死](../../omc/omc_server_hang_guidelines.html)）。

配置参数详情如下：

| 配置参数 | 解释 |
| --- | --- |
| maxMemSize=0 | 分配给 DolphinDB 的最大内存空间（以 GB 为单位）。如果该参数设为0，表明 DolphinDB 的内存使用没有限制。建议设置为比机器内存容量低的值。 |
| reservedMemSize=5% \* maxMemSize | 一个大于 0 的数字，单位为GB。当 DolphinDB 的可用内存小于 reservedMemSize 时，但仍有新的内存申请时，DolphinDB 将仅分配由 maxBlockSizeForReservedMemory 指定大小的内存块，这是为了尽可能保证报错、事务回滚等需要内存量少但较为关键的操作能有足够的内存，以降低此类操作失败的概率。例如，当因内存不足导致写入失败时，尽量保证仍然能正常回滚，避免数据不一致。若不指定该参数，系统默认按照 maxMemSize 的5%预留内存（此时，预留内存最小为64MB，最大为1GB）。*emergencyMemSize* 与 *reservedMemSize*的总和不可超过*maxMemSize* 的 50% 。 |
| emergencyMemSize=5% \* maxMemSize | 用于配置紧急内存区的大小，单位为GB。注意：（1）不可超过 *maxMemSize* 的50%；（2）emergencyMemSize 与 reservedMemSize 的总和不可超过*maxMemSize* 的50% 。若不指定时，默认为 *maxMemSize* 的5%，最小不低于512M，最大不能超过5G。 |
| maxBlockSizeForReservedMemory=8 | 表示 DolphinDB 可使用内存少于 reservedMemSize 时，每次申请内存的请求可以分配的最大内存块（单位为KB），默认值为 8。不建议设置过大值，否则系统可能因内存被占满，而导致关键操作申请不到内存，进而出现异常或崩溃。 |

当内存占用达到 warningMemSize 时，系统会自动清理数据库的缓存，释放一部分内存，以避免 OOM。

| 配置参数 | 解释 |
| --- | --- |
| warningMemSize | 当内存使用量超过 warningMemSize （以 GB 为单位）时，系统会自动清理部分数据库的缓存，以避免出现 OOM 异常。默认值为 maxMemSize 的75%。 |

用户也可限制事务的最大**写入**大小，从而避免出现内存问题：

| 配置参数 | 解释 |
| --- | --- |
| maxTransactionRatio=0.2 | 0.1~1.0之间的浮点数，表示 TSDB 或 OLAP存储引擎的单次写入事务大小上限与 cache engine 大小的比值。假设TSDB Cache Engine=16G，此参数设置为0.2，则表示**写入**事务不能超过 16 \* 0.2 = 3.2G。若多节点 Cache Engine 大小不同（如 Node1=4G，Node2=2G），则按平均值（3G）计算。**注意**：若 OLAP 引擎未开启 cache engine，此参数对OLAP 的事务写入无限制。 |

IOTDB相关内存参数：

| 配置参数 | 解释 |
| --- | --- |
| IOTDBLatestKeyCacheSize | 浮点数，用于管理最新值缓存表的最大值，单位为 GB。默认值为 *maxMemSize*的 5%。 |
| IOTDBStaticTableDir | 用于配置静态表目录路径。默认值为 Home 目录下的 IOTDBStaticTable 目录。 |
| IOTDBStaticTableCacheSize | 浮点数，用于管理静态表缓存最大值，默认为maxMamSIze 的 5%。 |

此外 DolphinDB 还提供了配置项，用来调整内存释放的速度。该参数等价于设置了 [TCMalloc](https://gperftools.github.io/gperftools/tcmalloc.html) 的 tcmalloc\_release\_rate。

| 配置参数 | 解释 |
| --- | --- |
| memoryReleaseRate=5 | 将未使用的内存释放给操作系统的速率，是0到10之间的浮点数。 memoryReleaseRate=0 表示不会主动释放未使用的内存，memoryReleaseRate=10 表示以最快的速度释放内存。默认值是5。 |

设置 dataSync=1 后，每个节点的内存将维护 OLAP Cache Engine 和 TSDB Cache Engine。该参数配置需在 controller 的 config
文件配置（默认为 controller.cfg）。

| 配置参数 | 解释 |
| --- | --- |
| dataSync=0 | 表示是否采用数据强制刷盘策略。默认值为0，表示是否由操作系统决定什么时候刷盘。如果 dataSync=1，表示将 redo log、数据和元数据强制刷盘。 |

DolphinDB 提供普通数组（array）和大数组（bigArray）两种数组类型，array
要求连续内存，优点是性能稍高，缺点是如果要求的内存太大，系统可能由于无法提供连续的内存而分配失败；bigarray
不要求连续内存，优点是可以利用碎片小内存提供大的内存请求，缺点是性能会稍差。

DolphinDB 提供了 *regularArrayMemoryLimit* 参数来设置普通数组 array
的最大内存上限，如果超过该限制，那么 array 定义的变量会采用 bigArray 方式分配内存。

| 配置参数 | 解释 |
| --- | --- |
| regularArrayMemoryLimit=2048 | 常规数组的内存限制（以 MB 为单位）。该参数必须是2的指数幂。默认值为 2048，系统运行时的实际值为 min(regularArrayMemoryLimit, maxMemSize/2)。 |

## 磁盘

DolphinDB 数据存储的路径取决于配置参数 volumes。

| 配置参数 | 解释 |
| --- | --- |
| volumes= /hdd/hdd1/volumes/<ALIAS>,  /hdd/hdd2/volumes/<ALIAS>,  /hdd/hdd3/volumes/<ALIAS>,  /hdd/hdd4/volumes/<ALIAS> | 数据文件目录。如果没有指定，单节点模式下，默认目录是 <HomeDir>/storage。集群模式下，默认目录是<HomeDir>/<nodeAlias>/storage。 |
| allowVolumeCreation=true | 布尔值，当 volumes 指定的路径不存在时，是否允许自动创建该路径。默认值为 true，表示允许自动创建。若配置为 false，当 volumes 指定的路径不存在时，系统会自动退出，同时输出错误日志到 log 文件。 |
| volumeUsageThreshold=0.97 | 浮点数，范围为（0, 1]，默认值为 0.97。设置数据节点上磁盘卷的使用率阈值，仅适用于数据节点。当一个数据节点指定的磁盘卷的总使用率达到该值时，该节点将无法新增 chunk，但仍可继续向已存在的 chunk 写入数据。 |

在对读写要求较高的场景下，用户可以选择指定多个
volumes，并将其配置在多个磁盘上。此外，用户可以通过配置磁盘读写线程的数量，来提升磁盘的 I/O。

| 配置参数 | 解释 |
| --- | --- |
| diskIOConcurrencyLevel=1 | 读写磁盘数据的线程数，默认为1。若设置 diskIOConcurrencyLevel = 0，表示使用当前任务执行的线程来读写磁盘数据；若设置 diskIOConcurrencyLevel > 0，则会创建指定个数的线程来读写磁盘数据。合理设置该参数，可以优化读写性能，因此建议配置如下：若 volumes 配置了 SSD 硬盘，建议设置 diskIOConcurrencyLevel = 0；若 volumes 全部配置为 HDD 硬盘，建议 diskIOConcurrencyLevel 设置为同 HDD 硬盘个数相同的值。 |

某些文件系统不支持 hardLink 功能，需修改配置 hardLink = false。

| 配置参数 | 解释 |
| --- | --- |
| useHardLink=true | 是否使用文件系统 hardlink 的功能。若为 true，表示使用文件系统 hardlink 功能；若为 false，则不使用 hardlink 功能。默认值为 true。 |

通过 maxFileHandles 配置项可以调整一个 dolphindb 进程允许打开文件数。

| 配置参数 | 解释 |
| --- | --- |
| maxFileHandles=1024 | 一个进程维护的文件描述符上限。 |

2.00.9 版本开始支持自定义交易日历。以下函数 [temporalAdd](../../funcs/t/temporalAdd.html), [resample](../../funcs/r/resample.html), [asFreq](../../funcs/a/asFreq.html),
[transFreq](../../funcs/t/transFreq.html) 中指定交易日历。

| 配置参数 | 解释 |
| --- | --- |
| marketHolidayDir | 交易市场节假日文件的存储目录，可以是绝对路径或者是相对目录，默认为 <HomeDir>/marketHoliday。 系统搜寻相对目录的顺序如下：先到节点的 home 目录寻找，再到节点的工作目录寻找，最后到可执行文件所在目录寻找。 存储的文件必须满足以下条件：文件格式为 csv；仅包含一个 DATE 类型的列。 |

根据 *marketHolidayDir*
下已存在的节假日文件生成交易日历，并采用文件名作为交易日历的标识。交易日历文件在系统启动时被加载到内存中。需要注意：

* 系统默认周末为节假日，因此文件内只需填写非周末的休市日期。
* 建议将交易日历文件以交易所编码命名，如 “CEFG.csv”。

数据节点的元数据文件为 *editlog.xxx* 和
*checkpoint.xxx*，其存储路径可通过下述参数配置。

| 配置参数 | 解释 |
| --- | --- |
| chunkMetaDir | 数据节点的元数据目录。如果没有指定，默认目录为配置参数 volumes 指定的第一个路径。 |

分布式文件系统中，集群的元数据信息存储在控制节点上，对应文件为： *DFSMetaLog.xxx* 和
*DSFMetaCheckpoint.xxx*。可通过下述配置项指定存储目录：

| 配置参数 | 解释 |
| --- | --- |
| dfsMetaDir | 分布式文件系统的元数据信息的存储路径。单节点模式下，该文件默认存储在 <HomeDir>/<nodeAlias>/dfsMeta 文件夹下。普通集群模式下，该文件默认存储在控制节点的 <HomeDir> 文件夹下。高可用集群模式下，该文件默认存储在 <HomeDir>/<nodeAlias>/dfsMeta，其中 <nodeAlias> 为 leader 控制节点的别名。 |

注： 该配置项需在 controller 的 config 文件中配置（默认为 controller.cfg）。

## 网络

为了减少网络传输的开销，建议集群所有节点配置在同一局域网下。

单节点模式下默认 server 的 ip 为本机 ip，端口号为 8848。若端口号被占用，可前往 config 指定的配置文件进行修改。

| 配置参数 | 解释 |
| --- | --- |
| localSite | 节点的局域网信息，格式为 host:port:alias。单节点模式中默认值为 localhost:8848:local8848。 |

集群环境下，控制节点和代理节点启动前，需在各自的 config 文件中配置自身的 localSite；代理节点还需额外配置
controllerSite。

| 配置参数 | 解释 |
| --- | --- |
| controllerSite | 代理节点的控制节点的局域网信息，必须与 controller.cfg 中某个控制节点的 localSite 相同。代理节点启动时，会使用该参数与控制节点通讯。 |

localSite 中的 host:port 为节点的 ip 和端口号，alias
将作为节点的别名。设置别名可以便于脚本编程中快速定位到指定节点，并与之建立通信连接，如 [subscribeTable](../../funcs/s/subscribeTable.html) 函数中指定 server
参数为远端节点的别名，即可订阅远端节点发布的流数据表。用户可在线调用 [getNodeAlias](../../funcs/g/getNodeAlias.html) 获取当前节点的别名，或 [getControllerAlias](../../funcs/g/getControllerAlias.html)
获取控制节点的别名。

节点的属性通过配置项 mode 声明，目前的可选值为
controller（控制节点），agent（代理节点），datanode（数据节点）以及 computenode（计算节点）。该配置项需在所有节点 config
文件声明。

| 配置参数 | 解释 |
| --- | --- |
| mode | 节点的模式 |

若需要配置计算组，需要在属性 computeGroup 中进行声明。

| 配置参数 | 解释 |
| --- | --- |
| computeGroup | 计算组名称，只能在计算节点后添加。添加后表示该计算节点属于该组。例如：host:port:alias,computenode,orca |

除了 config 文件外，controller 服务器配置的 nodesFile
文件中，也包含了所有集群代理节点、数据节点和计算节点的 localSite 和 mode，该文件为 controller
提供了集群的网络信息，以便控制节点可以访问到其它节点。

节点与节点之间基于 TCP 协议传输数据，DolphinDB 提供了 TCP 配置选项
tcpNoDelay，便于用户在实际生产场景下，进行通信调优。启用该参数在一定程度上可以减小传输延迟，但可能带来更大的网络负载。

| 配置参数 | 解释 |
| --- | --- |
| tcpNoDelay=true | 启动 *TCP\_NODELAY* 套接字选项。默认值是 false。 |
| tcpUserTimeout=300000 | 设置 *TCP\_USER\_TIMEOUT*套接字选项，单位是毫秒，默认值为300000。 |

控制节点通过心跳机制监控其它节点的存活状态，心跳可以采用 TCP/UDP 传输，通过配置项 lanCluster
指定。该参数需配置在代理节点、数据节点和计算节点的 config 文件。若心跳超时，则控制节点会认为该节点已经宕机。因此，在网络较差的场景下，建议配置较大的
dfsChunkNodeHeartBeatTimeout。

| 配置参数 | 解释 |
| --- | --- |
| lanCluster=true | 集群是否建立在 LAN（local area network）上。若为 true，心跳采用 UDP 协议；若为 false，心跳采用 TCP 协议。默认值为 true。对部署在云上的集群，应当设为 false。 |
| dfsChunkNodeHeartBeatTimeout=8 | INT 类型，控制节点配置项，用于设置数据节点、计算节点、代理节点心跳超时的临界时间（单位为秒）。若超过该值，控制节点仍未收到对应节点的心跳，则认为该节点已宕机。默认值是 8s。 |

集群内每个节点都与集群其它远程节点相连接。每个节点连接上限数取决于配置项 maxConnectionPerSite。

| 配置参数 | 解释 |
| --- | --- |
| maxConnectionPerSite | 从本地节点到远程节点可以创建的最大连接数量，不能小于 16。默认值是 max(*workernum*+*webworkernum*+1, 16) 。 |

特别地，DolphinDB 设计开发了 RDMA（Remote Direct Memory
Access，远程直接数据存取）全新通讯架构。区别于 TCP/IP 网络架构， RDMA
实现了对远程计算机内存的直接访问能力，特别适用于需要高速、低延迟通信的场景，如使用分布式内存表、处理 RPC 操作等（不支持处理流数据）。

在使用 RDMA 功能时，可直接延用已传入的参数 *ip* 和 *port*，且原有代码可以实现完全复用。目前
RDMA 仅支持 Linux 系统中集群内部调用 RPC（远程过程调用）的情况。

使用时，请确保已在当前机器中下载依赖的 [libibverbs](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/networking_guide/sec-infiniband_and_rdma_related_software_packages) 库，并且在当前的所有节点（包括
controller、datanode、computenode 和 agent）的配置中都已启用 RDMA 功能。否则集群无法正常工作。以下为配置项的具体介绍。

| 配置参数 | 解释 |
| --- | --- |
| enableRDMA | BOOL 类型，表示是否开启 RDMA。默认值是 false，表示不开启。 |

注意：开启 RDMA 后不可使用 SSL 功能。

用户通过 API, GUI, Web notebook
开启一个会话，并通过会话和对应节点建立一个连接。每个节点的最大外部会话连接上限数由配置参数 *maxConnections* 决定。

| 配置参数 | 解释 |
| --- | --- |
| maxConnections=64 | 最多可以从多少个外部 GUI，API 或其它节点连接到本地节点。Windows 的默认值为64，有效最大值也是64；Linux 的默认值为512。 |

Web notebook、VS Code 等编辑器与 DolphinDB server 默认采用 HTTP 协议传输数据。可通过配置
enableHTTPS，决定是否采用安全传输协议 HTTPS 进行传输。

| 配置参数 | 解释 |
| --- | --- |
| enableHTTPS=false | 是否启用 HTTPS 安全协议，默认值为 false。 |

自 2.00.15 版本开始，DolphinDB 在 TCP 基础上集成了 SSL/TLS 加密传输功能，实现集群内部节点间的加密传输。

| **配置参数** | **解释** | **配置节点** |
| --- | --- | --- |
| enableRpcSSL | 布尔值，用于指定是否在集群内部节点之间的数据传输和使用 `rpc` 函数时启用 SSL 协议进行加密传输。默认值为 false。  **注意**：开启 *enableRpcSSL* 需要所有节点同时配置 *enableHTTPS* = true，否则连接失败。 | 集群内所有节点 |

局域网环境下通过控制节点的 ip:port 可以直接访问集群的 web
管理器，若控制节点和其它节点不在同一局域网下，需指定控制节点的外网网络信息。该配置项需在 controller 的 config 文件进行配置（默认为
controller.cfg）。

| 配置参数 | 解释 |
| --- | --- |
| publicName | 控制节点外网 IP 或域名。如果 enableHTTPS 为 true，publicName 必须为域名。 |

自 3.00.2 版本起，DolphinDB
支持软件许可证管理，即公网 license server。在 license server 的架构中，主要分为服务端和客户端两部分。license server
通过心跳机制与客户端保持通信，监控客户端的资源使用情况，并在客户端节点状态变化时做出相应处理。

若需要使用 license server，必须使用 Type3 类型的 license，且需要进行调用函数进行用户与资源注册，并通过配置项进行相关配置。详情咨询技术支持。
license server 配置包括服务器和客户端两部分，相关配置项如下：

**服务端**

| 配置参数 | 解释 | 配置节点 |
| --- | --- | --- |
| isLicenseServer | 布尔值，表示当前节点是否为 license server。仅当 license 的 type 是 3 时，将该参数配置为 true，才能将该节点设置为 license server。  license server 以单机模式运行。其结合 license 文件，给集群中各节点（代理节点除外）分配硬件资源。 | 单节点 |

**客户端**

用户需要先联系 DolphinDB 取得 licenseServer.lic
文件，并将其放至节点所在目录中。然后，在节点的配置文件（controller.cfg/agent.cfg/cluster.cfg）中设置
useLicenseServer，并可以选配 coreAffinity。

| 配置参数 | 解释 | 配置节点 |
| --- | --- | --- |
| useLicenseServer | 布尔值，若设置为 true，则表示以 license server 方式启动。否则，以普通节点启动，并使用本地 license 文件。 | 单节点、控制节点、数据节点、计算节点、代理节点 |
| coreAffinity | 字符串，为节点指定 CPU 内核编号。多个编号间用","分隔；连续的编号可用"-"连接起始编号。例如，绑定 1 到 4 的内核，可写为 1, 2, 3, 4 或 1-4。仅向 license server 申请资源的节点可配置该参数:   * 指定该参数时，进程将在指定内核上运行； * 不指定该参数时，则绑定前 *workerNum* 个内核。   注意，必须满足以下两点才能成功启动节点：   * 所指定的 CPU 内核在物理机上存在； * 绑定的核数小于等于*workerNum*。 | 单节点、控制节点、数据节点、计算节点、代理节点 |

## 恢复（recovery）和再平衡（rebalance）

处于宕机、离线和同步恢复中的节点，不参与事务的处理。在此期间，若其它节点发起的事务涉及到该节点上的
CHUNK，根据集群是否为多副本，可分为以下两种情况：

* 集群为单副本，事务无法进行；
* 集群为多副本，系统将发起节点间恢复。

节点间恢复分为在线增量恢复和全量同步恢复。系统会优先尝试在线增量恢复，即通过其它节点的副本数据，增量补齐该节点由于无法参与事务而缺失的数据量。若存在数据不一致等问题，造成增量的在线恢复无法进行，系统将自动转换全量同步恢复。

节点间的全量恢复将以 CHUNK 副本为单位，将完整的副本复制到宕机节点中，因此网络开销较大。

节点间的在线增量恢复，只需复制缺失的事务数据，数据量较小。其通常分为两个阶段，异步恢复和同步恢复。当数据量较大时，同步恢复会导致源节点长时间阻塞，无法参与任何事务。因此在线恢复的第一阶段采用异步恢复，源节点在此期间仍可参与其它事务。等待恢复的数据量小于
dfsSyncRecoveryChunkRowSize 配置的值时，开始第二阶段的同步恢复，在较短的时间便可以完成。

| 配置参数 | 解释 |
| --- | --- |
| dfsSyncRecoveryChunkRowSize=1000 | 一个正整数，默认值为1000。节点间进行数据恢复时，默认采用异步恢复，当待恢复的目的 chunk 的记录数与最新版本的记录数的差值小于该设置值，就会启用同步复制。 |

为了进一步提升节点间数据恢复任务的速度，可以通过调整配置项 dfsRecoveryConcurrency
来增加任务的并发度。

| 配置参数 | 解释 |
| --- | --- |
| dfsRecoveryConcurrency | 节点恢复时，执行 recovery 任务的并发度（worker 的数量），默认是集群数据节点个数的2倍。 |

同步恢复阶段，执行恢复任务的工作线程数可由参数 recoveryWorkers 配置。

| 配置参数 | 解释 | 配置节点 |
| --- | --- | --- |
| recoveryWorkers=1 | INT 类型，用于设置当前数据节点用于执行 recovery 的线程数量，默认值为 1。  注意：   * 如果当前线程数少于新配置线程数，则会创建缺少数量的线程；如果当前线程数大于新配置线程数，系统会阻塞回收多余数量的线程。 * 对 recoveryWorkers 的上限没有做硬限制，但是会受到操作系统限制。 | 数据节点 |

数据再均衡（rebalance）分为节点内数据均衡和节点间数据均衡。

节点内数据均衡主要指某个节点配置了多个磁盘卷，增加新的磁盘卷后，需要把数据重新分配，以提高 I/O 效率。对应函数 [rebalanceChunksWithinDataNode](../../funcs/r/rebalanceChunksWithinDataNode.html)。

节点间数据均衡指由于集群数据在各个节点上分配不均，可通过再均衡重新分配，提高分布式计算的效率。对应函数 [rebalanceChunksAmongDataNodes](../../funcs/r/rebalanceChunksAmongDataNodes.html)。

在均衡的工作并发度可通过配置项 dfsRebalanceConcurrency 指定。

| 配置参数 | 解释 |
| --- | --- |
| dfsRebalanceConcurrency | 节点数据再均衡时，执行 rebalance 任务的并发度（worker 的数量），默认是集群数据节点个数的2倍。 |

在节点恢复过程中，为了避免节点宕机或离线对恢复过程造成太大影响，可以开启节点恢复事务的重做日志，配置
enableDfsRecoverRedo = true。开启后，在节点恢复的过程中，会将恢复事务相关的数据先写入 recover redo log 中。

| 配置参数 | 解释 |
| --- | --- |
| enableDfsRecoverRedo=true | 启用节点恢复过程的重做日志。 |
| recoverLogDir=<HomeDir>/recoverLog | 节点恢复事务重做日志的存储路径，默认路径为 <LogDir>/recoverLog。需和数据目录存储在不同的磁盘，建议配置为 SSD 高速磁盘的路径。 |

## 异步复制

自 2.00.15 版本起，异步复制支持主从集群间使用 SSL 协议进行加密传输，可通过以下配置开启。

| **配置参数** | **解释** | **配置节点** |
| --- | --- | --- |
| enableClusterReplicationSSL | 布尔值，用于指定是否在主从集群异步复制时启用 SSL 协议进行加密传输。默认值为 false。  **注意**：开启 *enableClusterReplicationSSL* 需要主集群同时配置 *enableHTTPS* = true，否则连接失败。 | 主从集群的控制节点、数据节点、计算节点 |

### 主集群

clusterReplicationSlaveNum 和 clusterReplicationMode 为必选参数。

| 配置参数 | 解释 | 配置节点 |
| --- | --- | --- |
| clusterReplicationSlaveNum=2 | 允许配置的从集群数量上限。 | 控制节点 |
| clusterReplicationMode | 集群间的异步复制模式。可选值为 master 和 slave，表示主集群和从集群。 | 数据节点 |
| clusterReplicationWorkDir=<HomeDir> | 指定异步复制的工作目录，存储写任务的数据。默认为数据节点的<HomeDir>/clusterReplication。建议配置为容量比较大的 SSD 高速磁盘的路径。 | 数据节点 |
| clusterReplicationSyncPersistence=false | 布尔值，表示是否开启写任务数据的同步持久化，默认为为 false，表示持久化异步进行。注意：开启异步持久化，数据节点宕机可能造成数据丢失；开启同步持久化，会降低主集群的事务效率。 | 数据节点 |

### 从集群

*clusterReplicationMasterCtl* 和
*clusterReplicationMode* 为必选参数。

| 参数名 | 解释 | 配置节点 |
| --- | --- | --- |
| clusterReplicationMasterCtl | 指定主集群控制节点的 ip:port。若主集群为高可用集群，则指定为控制节点 raft 组中的任意节点即可。 | 控制节点 |
| clusterReplicationMode | 集群间的异步复制模式。可选值为 master 和 slave，表示主集群和从集群。 | 数据节点 |
| clusterReplicationExecutionUsername=admin | 用于执行集群间异步复制的用户名，默认为 admin。必须确保该用户有事务操作的相关权限，否则异步复制任务会失败。进行回放任务时，用户必须登录。 | 数据节点 |
| clusterReplicationExecutionPassword=123456 | 用于执行集群间异步复制的用户密码，默认为 123456。 注： 自 3.00.1 版本起，采用 RSA 加密算法进行身份认证，用户无需指定此参数。 | 数据节点 |
| clusterReplicationQueue | 执行队列的数量，必须是正整数，默认值是数据节点数量的4倍。 | 控制节点 |
| clusterReplicationWorkerNum | 每个数据节点执行任务的工作线程数，默认值是max(workerNum/4, 4)。 | 数据节点 |
| slaveReplicationDBScope | 用于指定回放的数据库范围。可以通过输入数据库路径来设置该范围，多个数据库之间以逗号分隔，例如：dfs://db1,dfs://db2,dfs://db3。若不配置该参数，则回放所有数据库的任务。 | 控制节点 |

## 作业

参考教程： [作业管理](../../tutorials/job_management_tutorial.html) 。

DolphinDB
中有两类作业形式，同步作业和异步作业。绝大部分脚本提交的任务都称为同步作业。异步作业主要指批处理作业、定时作业。

### 同步作业

一个节点能同时执行的同步作业数取决于 worker 数量（使用非 web 客户端时，通过配置项 workerNum 设置）和
web worker 数量（使用 web 客户端时，通过配置项 webWorkerNum 设置）。

| 配置参数 | 解释 |
| --- | --- |
| workerNum=4 | 常规作业的工作线程的数量。默认值是 CPU 的内核数。 |
| webWorkerNum=1 | 处理HTTP请求的工作线程的数量。默认值是1。 |

### 异步作业

批处理作业指使用 [submitJob](../../funcs/s/submitJob.html) 或 [submitJobEx](../../funcs/s/submitJobEx.html) 函数创建的作业任务。在系统中，批处理作业工作线程数的上限是由配置参数 maxBatchJobWorker
设置的。如果批处理作业的数量超过了限制，新的批处理作业将会进入队列等待，队列深度由配置参数 maxCachedBatchJobNum
设置。批处理作业工作线程在闲置超过60秒后会自动销毁。

| 配置参数 | 解释 |
| --- | --- |
| maxBatchJobWorker=4 | 批处理作业的最大工作线程数量。默认值是 workerNum 的值。 |
| maxCachedBatchJobNum=2048 | 批处理作业队列的最大深度，即队列中最多的批处理作业数量，默认值是 2048。 |

### 作业并行度管理

| 配置参数 | 解释 | 配置节点 |
| --- | --- | --- |
| jobParallelismHardLimit=false | 布尔值。  * 值为 false 时，不限制任务最多使用的 worker 的数量； * 值为 true 时，表示将任务最多使用的 worker 数设置为该任务的并行度。 | 控制节点、代理节点、数据节点 |
| defaultJobParallelism=2 | 用户提交任务的默认并行度。正整数，默认值：2，值域为：(0, 64]。 注： 该配置项赋值应遵守值域限定，否则会造成 server 启动失败，并在错误日志中显示为：`defaultJobParallelism must be an integer between 1 and 64.` | 控制节点 |

## 流数据

参考教程：[流数据教程](../../tutorials/streaming_tutorial.html)。

DolphinDB 提供了流数据持久化的功能，其作用主要为：

* 备份恢复流数据表，避免发布节点宕机，造成流数据表数据丢失。
* 避免流数据表过大造成内存不足。
* 支持从任意位置开始重新订阅。

开启持久化只需为发布节点的配置以下选项：

| 配置参数 | 解释 |
| --- | --- |
| persistenceDir=/home/DolphinDB/Data/Persistence | 共享流数据表的保存路径。如果要将流数据表保存到磁盘上，必须指定 persistenceDir。在集群模式中，需要保证同一机器上的数据节点配置了不同的 persistenceDir。 |
| persistenceWorkerNum=1 | 负责以异步模式保存流数据表的工作线程数。若为高可用流数据表，该参数的默认值为 1；否则默认值为 0。 |

### 发布节点

发布节点支持配置一些发布数据相关的信息，如发布的消息块大小，消息队列深度。此外还需指定可以连接的订阅节点的连接数上限
maxPubConnections，由于该参数默认为 0，因此若启用流数据必须指定该参数为一个正数。

| 配置参数 | 解释 |
| --- | --- |
| maxMsgNumPerBlock=1024 | 一个消息块中最多的记录条数。默认值为1024。 |
| maxPersistenceQueueDepth=10000000 | 把流数据表保存到磁盘时，消息队列的最大深度（记录条数）。默认值为10,000,000。 |
| maxPubQueueDepthPerSite=10000000 | 发布节点的消息队列的最大深度（记录条数）。默认值为10,000,000。 |
| maxPubConnections=0 | 发布节点可以连接的订阅节点数量上限，默认值为0。只有指定 maxPubConnections 为正整数后，该节点才可作为发布节点。 |

### 订阅节点

订阅节点订阅流数据表数据。其同发布节点一样，支持指定订阅消息的队列深度以及连接发布节点的数量上限（可以选择不指定，按默认值即可）。此外，订阅节点还可以对流数据进行消费，因此还支持对消息处理的线程数、消息处理时间间隔等进行配置。

| 配置参数 | 解释 |
| --- | --- |
| subPort=8000 | 订阅线程监听的端口号。对于2.00.9之前版本，若要该节点作为订阅节点，必须指定该参数；2.00.9及之后版本无需指定。 |
| maxSubConnections=64 | 该订阅节点可以连接的的发布节点数量上限。默认值为 64。 |
| maxSubQueueDepth=10000000 | 该订阅节点的消息队列的最大深度（记录条数）。 |
| subExecutorPooling=false | 表示流计算线程是否为 pooling 模式。默认值为 false。注意：使用响应式状态引擎时，必须设置该参数为 false。 |
| subExecutors=1 | 该订阅节点中消息处理线程的数量。只有当启用订阅功能时，该参数才有意义。默认值为1。如果 *subExecutors* = 0，表示该线程既可以进行消息转换也可以处理消息。 |
| subThrottle | 非负整数，单位为毫秒，默认值为 1000。系统检查订阅函数（`subscribeTable`）消息处理情况的时间间隔。若 `subscribeTable` 的 *throttle*参数指定了小于配置参数 *subThrottle* 的值，则触发消息处理的时间间隔为 *subThrottle*。若要设置订阅函数消息处理的时间间隔小于1秒，则需要先修改配置项 *subThrottle*。例如：要使 *throttle=0.001* 秒生效，需设置 *subThrottle =1*。 注： 指定 `subscribeTable` 函数的参数 *batchSize* 后，该参数设置才会生效。 |
| localSubscriberNum=1 | 设置本地订阅对发布队列中的消息进行分发的线程数量，默认为1。若设置为大于1的数，则会分配相应数量的分发线程，并行分发消息至本地订阅消息处理线程中。 |

若订阅节点消费流数据时发生宕机，重启后可能会无法获知之前消费的进度。DolphinDB
支持将订阅消费数据的偏移量进行持久化，以避免此类情况的发生。

| 配置参数 | 解释 |
| --- | --- |
| persistenceOffsetDir=/home/DolphinDB/streamlog | 持久化订阅端消费数据偏移量的保存路径，用于保存订阅消费数据的偏移量。若没有指定 *persistenceOffsetDir*，但指定了 *persistenceDir*，则会保存至 *persistenceDir* 目录；如果既没指定 *persistenceOffsetDir* 也没指定 *persistenceDir*，会在节点目录下生成 *streamlog* 目录。 |

### 高可用

参考教程： [DolphinDB教程：流数据高可用](../../tutorials/haStreaming.html)

流数据高可用和集群高可用一样采用 raft
机制，不同的是集群高可用是控制节点的高可用，而流数据高可用为数据节点的高可用。流数据高可用分为发布端、订阅端、流数据计算引擎高可用三种，其高可用的
raft 组都通过 streamingRaftGroups 参数进行配置。

* 发布端高可用（高可用流数据表）：开启发布端高可用后，高可用流数据表自动在 raft
  组内的节点进行同步。订阅端只需向 leader 节点订阅高可用流数据即可。若发布端 raft 组 leader
  宕机，系统也可以迅速重新选举出新的 leader，供订阅端继续订阅。
* 订阅端高可用：需在订阅函数 [subscribeTable](../../funcs/s/subscribeTable.html) 中设置
  reconnect=true，并指定 raftGroup。若订阅端 raft 组 leader 宕机，系统也可以迅速重新选举出新的
  leader，继续从发布端订阅数据。
* 流数据计算引擎高可用：通过配置引擎创建函数的参数 snapshot 和 raftGroup
  实现高可用。参考流计算引擎详情页：[流计算引擎](../../funcs/themes/streamingEngine.html)。

注： 启用高可用流数据表，必须开启发布节点的流数据表持久化。

| 配置参数 | 解释 |
| --- | --- |
| streamingHAMode=raft | 高可用功能采用的协议，目前固定配置为 raft，表明流数据高可用功能采用了 raft 协议。 |
| streamingRaftGroups=2:NODE1:NODE2:NODE3,3:NODE3:NODE4:NODE5 | raft 组信息，包含 ID 和组成 raft 组的数据节点别名，使用冒号分隔。raft 组的 ID 必须是大于1的整数，一个 raft 组至少包含3个不同的数据节点。如果有多个 raft 组，使用逗号分隔每个 raft 组的信息。 |
| streamingHADir=/home/DolphinDB/Data/NODE1/log/streamLog | 流数据 raft 日志文件的存储目录。如果没有指定，默认值为 <HomeDir>/log/streamLog 。每个数据节点应当配置不同的 streamingHADir。 |
| streamingHAPurgeInterval=300 | raft 日志垃圾回收周期。默认值300，单位为秒。 |

### Orca

| 配置参数 | 解释 | 配置节点 |
| --- | --- | --- |
| enableORCA | 布尔类型标量，表示是否开启 Orca。默认值为 true 代表开启。 | 控制节点、数据节点、计算节点 |
| orcaMaxGraphRescheduleAttempts | 正整数，表示 ERROR 状态的流图最大的重试次数。默认值为 10。 | 控制节点 |

## SQL 查询

集群环境下，用户在所连接的节点（协调节点）发起一次分布式表的查询，协调节点首先会根据查询所涉及的分区拆分为子查询语句并 map
到相关的节点。在该过程中，查询的分区数若过多，数据量过大可能造成最后汇总数据时，造成内存溢出。DolphinDB 提供了一系列配置参数来限制查询。

| 配置参数 | 解释 | 配置节点 |
| --- | --- | --- |
| maxPartitionNumPerQuery=65536 | 单个查询语句可查找的最大分区数。默认值是65536。 | 数据节点/计算节点 |
| checkExistingPartitionNumForQuery | 开启该配置参数后，*maxPartitionNumPerQuery* 将根据从控制节点获取到的实际分区数来估计查询分区限制。若不配置则默认为 false，表示关闭。注意：仅对 DFS 表有效。 | 数据节点/计算节点 |
| memLimitOfQueryResult | 设置单次查询结果占用的内存上限。默认取值为 min(50% \* maxMemSize,8G)。若配置该参数，则设置值必须小于 80% \* maxMemSize。 | 数据节点/计算节点 |
| memLimitOfTaskGroupResult | 在 map 阶段，单次查询任务被分解为若干个子任务，需要由远端节点执行的子任务批量发送给远端节点。该参数用于设置当前节点发送的批量子查询占用的内存上限。默认取值为 min(20% \* maxMemSize,2G)。若配置该参数，则设置值必须小于 50% \* maxMemSize。 | 数据节点/计算节点 |
| memLimitOfTempResult=1 | 在表连接操作过程中，可能会产生多个临时数据表，该配置项用于设置每个临时数据表允许占用的内存上限，单位是 GB。它的默认值是1，最大值取决于 maxMemSize 的设置值。 若单个临时数据表的内存超过配置值，则会被存放到磁盘的一个临时目录中（由 tempSpillDir 设置）。在表连接完成后，临时文件会被自动回收。 注意，自 3.00.1 版本起，该配置项不再生效。可使用 memLimitOfAllTempResults。 | 数据节点/计算节点 |
| tempResultsSpillDir=tempResults | 在某些计算过程（例如表连接操作）中，可能会产生临时表用于存储中间结果。该配置项用于指定存储这些中间结果表的临时目录，以避免内存不足或性能问题。默认目录是 <HomeDir>/tempResults。当所有中间结果表的数据量达到 *memLimitOfAllTempResults* 的设置值时，数据文件会被临时存放到该目录中。计算完成后，由其产生的数据文件会被自动删除。注意：每次 server 启动时，该目录及其下的所有内容会被先删除，然后重新创建。 | 数据节点/计算节点 |
| memLimitOfAllTempResults | 某些分布式查询操作（例如表连接、GROUP BY、CONTEXT BY、PIVOT BY），可能会产生临时表用于存储查询中产生的结果。该配置项用于设置所有临时表允许占用的内存上限，单位是 GB，默认值是 *maxMemSize* \* 20%。若所有临时表的内存超过配置值，则会被存放到磁盘的一个临时目录中（由 *tempSpillDir* 设置）。在查询完成后，临时文件会被自动回收。 | 数据节点/计算节点 |
| maxQueryExecutionTime=0 | 单个查询语句的最长执行时间，单位为秒。为整型标量，默认值为 0。当取值小于或等于 0 时，表示不限制执行时间。 | 数据节点/计算节点 |
| maxJoinTaskRetry | 正整数，设置内存紧张时单个 SQL JOIN 子任务的最大重试次数。默认值为 2147483647，表示无限次重试。当子任务重试达到 *maxJoinTaskRetry* 上限后，包含该子任务的 SQL 查询将被取消。 | 数据节点/计算节点 |

创建数据库和数据表时，除了直接指定函数参数进行配置，DolphinDB 还提供了一部分配置文件中的配置项：

## 数据库与数据表

| 配置参数 | 解释 |
| --- | --- |
| enableChunkGranularityConfig=false | DolphinDB 内 chunk 的粒度决定了事务锁的位置。写入一个 chunk 时，系统会对该 chunk 上锁，不允许其他事务写入。2.00.4之前的版本，chunk 的粒度为数据库级别，即数据库的每个分区（partition）为一个 chunk。此时，不允许并发写入同一个分区的不同表。2.00.4版本引入了该配置项，默认为 false，表示 chunk 的粒度为表级别，即每个分区（partition）下的每个表为一个 chunk。此时，允许并发写入同一分区的不同表。设置为 true 时，允许通过 database 的 chunkGranularity 参数指定 chunk 的粒度为数据库级或表级。 |
| newValuePartitionPolicy=skip | 对于值分区（或复合分区中的值分区）的数据库，若新增数据不属于已有分区，如何处理。它的取值可以是 add, skip 和 fail。 默认值是 skip，表示如果新增数据中包含分区方案外的数据，系统会保留分区方案中的数据，不保留分区方案外的数据。 注意：从 2.00.10 版本开始，新增了配置项allowMissingPartitions。当 allowMissingPartitions=true（默认值） 时，skip 的行为保持不变。但是当 allowMissingPartitions=false 时，skip 的行为将变成：如果新增数据中包含分区方案外的数据，则系统不会写入任何数据，且抛出异常。 如果 newValuePartitionPolicy=add，表示系统会自动划分新的分区，保留分区方案外的数据。 如果 newValuePartitionPolicy=fail，表示如果新增数据中包含分区方案外的数据，系统不会保留任何数据，且抛出异常。根据大多数场景需求，推荐设置 newValuePartitionPolicy= add。 |
| oldChunkVersionRetentionTime=60 | 设置过期版本 chunk 的保留时长，默认为 60（单位：分钟），上限为 240。执行 SQL update/upsert/delete 操作时，系统会先生成一个新的 chunk 副本（以”物理表名\_tid”命名），并在该副本上进行数据的更新和删除。操作完成后，旧的 chunk 不会被立即删除。系统最多保留 5 个历史 chunk，且每个历史 chunk 的保留时长由此配置参数指定。 |
| allowMissingPartitions=true | 当新增数据中包含分区方案外的数据时，是否忽略（不保留）分区方案范围外的数据。默认为 true，即保留分区方案中的数据，不保留分区方案外的数据。若设置为 false，则不会写入任何数据，且抛出异常。 注意：对于 VALUE 分区，当 newValuePartitionPolicy 为 add 或 fail 时，是否会忽略分区方案范围外的数据不受该配置项的影响。 |
| enableLocalDatabase=true | 布尔值，表示是否允许创建本地磁盘数据库。默认值为 true，允许；若设置为 false，则不允许。一旦配置，则对集群内的所有节点都生效。该配置项的配置节点为控制节点。 |
| enableInsertStatementForDFSTable | BOOL 类型，表示是否支持使用 insert into 语句插入 DFS 表。默认为 false，即不支持。 |

| 配置参数 | 解释 |
| --- | --- |
| enableConcurrentDimensionalTableWrite=false | 是否允许维度表并发写入、修改、删除。默认值为 false。若为 true，表示允许维度表并发写入、修改、删除。 |
| removeSpecialCharInColumnName=false | 是否规范化包含特殊符号的列名，默认值是 false，表示自动产生的数据表的列名允许包含特殊符号，即列名可以以非字母和中文开头，且可以包含下划线之外的符号。如果要跟以前版本兼容，可以将该变量配置为 true。 |

每个持久化的 mvcc 表都有一个 log 文件。对 mvcc 表的增、删、改操作会先写入
log，直至操作次数达到一定数量，才会创建 mvcc 表检测点（checkpoint）， 将数据写入 mvcc 表，并清空 log。通过 [loadMvccTable](../../funcs/l/loadMvccTable.html) 加载 mvcc 表时，需要回放 log
文件。若 log 的数据量过大，可能导致回放耗时过长，甚至出现 OOM。 为解决此类问题，DolphinDB 提供以下配置项，用于控制 log 中的数据量。

| 配置参数 | 解释 |
| --- | --- |
| mvccCheckpointThreshold=5000000 | 设置创建检查点的操作次数阈值。当对 mvcc table 的操作次数达到此值时，会创建检查点。取值范围为：[100,000, 2^31-1]，默认值为 5,000,000。增、删、改对应的 mvcc table 的操作次数定义如下：新增（append!, tableInsert, insert into），更新（update）操作的行数 \* 列数 - 删除（delete）操作的行数。 |

## TSDB

DolphinDB TSDB 引擎的 redo log 的存储路径可通过以下参数进行配置：

| 配置参数 | 解释 |
| --- | --- |
| `TSDBRedoLogDir=/TSDBRedo` | TSDB 存储引擎重做日志(redo log)的目录。默认值是 `/log/TSDBRedo`。 |

其中，TSDBMeta（包含 level file 元数据）与 TSDBRedo 位于同级目录，存放于
<HomeDir>/log 目录。事务数据存放于 <HomeDir>/storage/CHUNKS 目录。 配置方式如下：

1. 使用相对路径, 即不以 '/' 开头；
2. 路径中包含 <ALIAS>, 如
   /home/xxx/<ALIAS>/redolog；
3. 每个节点单独配置：node1.TSDBRedoLogDir=/home/xxx/node1/redolog,
   node2.TSDBRedoLogDir=/home/xxx/node2/redolog

在集群模式中，需要保证同一机器上的数据节点配置了不同的 TSDBRedoLogDir。

TSDB 引擎在读取或写入数据时，会对相关分区的 symbolBase 数据进行缓存。系统采用 LRU（最近最少使用）策略管理 symbolBase
缓存，提供以下两个配置项，可以根据缓存时间或缓存容量来决定何时逐出未被使用的 symbolBase 数据。其中，未被使用的 symbolBase
是指其对应的分区数据不在 Cache Engine 中，也不在执行的任何事务中。

| 配置参数 | 解释 | 配置节点 |
| --- | --- | --- |
| TSDBSymbolBaseEvictTime=3600 | 一个正整数，表示一个 symbolBase可以缓存的最大时长。单位为秒，默认值为 3600。当未被使用的 symbolBase 在缓存中停留时长超过设置值时，系统会将其逐出缓存。 | 数据节点 |
| TSDBCachedSymbolBaseCapacity | 一个大于 0 的数字，表示内存中最多可以缓存的 symbolBase 总容量。单位为 GB，默认值为 *maxMemSize* \* 5%，最小值为 128MB。当总容量超过设置值时，系统将按照 symbolBase 的时间戳从旧到新的顺序，依次逐出当前未被使用的 symbolBase，直至总容量小于等于设置值。 | 数据节点 |

DolphinDB TSDB 引擎的 Cache Engine 的大小可通过以下配置项设置：

| 配置参数 | 解释 |
| --- | --- |
| TSDBCacheEngineSize=1 | 设置 TSDB 存储引擎 Cache Engine 的容量（单位为GB），必须为正数，默认值为1。当 Cache Engine 的内存占用达到设置值的一半时，系统开始对内存中的数据刷盘，数据可继续写入；当 Cache Engine 的内存占用达到设置值时，写入线程将被阻塞。TSDBCacheEngineSize 需合理设置，若设置过小，可能导致 Cache Engine 频繁刷盘，影响系统性能；若设置过大，由于 Cache Engine 内缓存的数据量很大，但由于未达到 Cache Engine 的一半大小（且未达到十分钟），因此数据尚未刷盘，此时若发生了机器断电或关机，重启后就需要回放大量事务，导致系统启动过慢。 |

根据 TSDB 引擎的数据模型，数据写入需要经过“排序-压缩-落盘”三个阶段。

* 排序在 Cache Engine 内部进行，排序的线程数可通过配置项
  TSDBAsyncSortingWorkerNum 设置。
* 落盘时，为提升 TSDB Cache Engine 的刷盘速度，可以配置
  TSDBCacheFlushWorkNum 设置工作线程数。

| 配置参数 | 解释 |
| --- | --- |
| TSDBAsyncSortingWorkerNum=1 | 非负整数，默认值为1，用于指定 TSDB Cache Engine 异步排序的工作线程数。若该参数设置为0，表示写入和排序同步进行。TSDB 写入 Cache Engine 中的数据将会根据 sortColumns 排序。数据写入 Cache Engine 和排序任务可以同步或异步进行，异步可以提升写入性能。注意：异步排序可以提高数据写入性能，但会降低查询性能，因为查询需要等待相关 chunk 的异步排序线程结束才能进行。 |
| TSDBCacheTableBufferThreshold=16384 | TSDB 引擎缓存数据进行批量排序的阈值。当缓存数据的记录数达到该值后，Cache Engine 将对该部分数据进行排序。 |
| TSDBCacheFlushWorkNum | 配置 TSDB Cache Engine 刷盘的工作线程数。默认值是 volumes 指定的磁盘卷数。若配置值小于磁盘卷数，则仍取默认值。 |

除了 Cache Engine, TSDB 引擎在内存还维护了到 level file 数据块的索引，索引大小可由配置项
TSDBLevelFileIndexCacheSize 指定。

| 配置参数 | 解释 |
| --- | --- |
| TSDBLevelFileIndexCacheSize=5% \* maxMemSize | 设置 TSDB 存储引擎 level file 元数据内存占用空间上限。单位为 GB，类型为浮点型。默认值为 DolphinDB 系统可使用（由 *maxMemSize* 设置）的5%，最小值为0.1(GB)。 |

若读取的索引超过 TSDBLevelFileIndexCacheSize，DolphinDB
内部会根据访问时间，将最不常访问的索引进行置换。

| 配置参数 | 解释 |
| --- | --- |
| TSDBLevelFileIndexCacheInvalidPercent=0.95 | TSDB 引擎 level file 索引缓存淘汰算法的阈值，默认值是 0.95。 |
| allowTSDBLevel3Compaction | 系统是否启用 level 3 层级的 Level File 的合并：   * 默认值为 false，此时系统不会主动触发 level 3 层级 Level File 的合并。 * 当设置为 true 时，对于 *keepDuplicates* 设置为 FIRST 和 LAST   的表，满足合并条件时将触发 level 3 层级 Level File 的合并；而对于   *keepDuplicates* 设置为 ALL 的表，其 Level File   不受此参数影响，始终不会合并 level 3 层级。 |

为提高计算资源利用率，降低使用 TSDB 引擎时合并 level file 的耗时，以及尽可能平衡负载，DolphinDB 在 2.00.11 版本提供了用于调整每个
volume 下可处理合并任务的线程数量（worker）的配置项 *compactWorkerNumPerVolume*。

| 配置参数 | 解释 |
| --- | --- |
| compactWorkerNumPerVolume | 一个 volume 下用于合并 level file 的 worker 数量，默认值是 1。 |

为了提升向量索引的查询速度，TSDB 引擎维护了向量索引缓存，大小可通过配置项 TSDBVectorIndexCacheSize
设置。系统采用 LRU（最近最少使用）策略管理缓存。

| 配置参数 | 解释 | 配置节点 |
| --- | --- | --- |
| TSDBVectorIndexCacheSize=0 | 非负浮点数，指定 TSDB 向量索引的缓存大小，单位为 GB。默认值为 0，表示关闭缓存；当配置项大于 0 时，此功能将启用。 | 数据节点 |

## OLAP

DolphinDB OLAP 引擎的 redo log 的存储路径可通过以下参数进行配置：

| 配置参数 | 解释 |
| --- | --- |
| `redoLogDir=/redoLog` | OLAP 存储引擎重做日志（redo log）的目录。默认值是 `/log/redoLog`。在集群模式中，需要保证同一机器上的数据节点配置了不同的 redoLogDir。 |

DolphinDB OLAP 引擎的 Cache Engine 的大小可通过以下配置项设置：

| 配置参数 | 解释 |
| --- | --- |
| OLAPCacheEngineSize=0 Alias: chunkCacheEngineMemSize | 指定 OLAP 存储引擎 Cache Engine 的容量（单位为 GB）。 Cache Engine 开启后，写入数据时，系统会先把数据写入缓存，当缓存中的数据量达到 OLAPCacheEngineSize 的30%时，才写入磁盘。默认值是0，即不开启 Cache Engine。开启 Cache Engine 的同时，必须设置 dataSync=1。 |

## PKEY

| 配置参数 | 解释 |
| --- | --- |
| enablePKEYEngine | 表示是否开启 PKEY 引擎。默认值为 true。 |
| PKEYMetaLogDir | 元数据日志的存储目录。默认值为 `<ALIAS>/log/PKEYMeta`。 |
| PKEYRedoLogDir | 重做日志(redo log)的存储目录。默认值为 `<ALIAS>/log/PKEYRedo`。 |
| PKEYCacheEngineSize | 设置 PKEY 存储引擎 cache engine 的容量（单位为GB），必须为正数，默认值为1。如果写入压力太大，系统 cache engine 内存占用可能会达到该参数值的2倍大小。因为若当前申请的大小为 PKEYCacheEngineSize 的内存写满后，该内存中的数据开始刷盘，此时若有数据继续写入，系统会再分配一块内存来接收新数据。需要注意的是，若数据刷盘不及时，可能导致新分配的内存也达到 PKEYCacheEngineSize 大小，此时写入线程会被阻塞。PKEYCacheEngineSize 需合理设置，若设置过小，可能导致 cache engine 频繁刷盘，影响系统性能；若设置过大，由于 cache engine 内缓存的数据量很大，但由于未达到 cache engine 的大小（且未达到十分钟），因此数据尚未刷盘，此时若发生了机器断电或关机，重启后就需要回放大量事务，导致系统启动过慢。 |
| PKEYBlockCacheSize | 设置 PKEY 存储引擎的block cache容量，单位为GB，必须为正数，默认值为1。 |
| PKEYDeleteBitmapUpdateThreshold | 设置PKEY存储引擎的delete bitmap的更新阈值，单位为MB，必须为正数，默认值为100。  为了在后台批量更新 delete bitmap，需要在刷盘时暂存主键和 CID 列。当暂存缓冲区大小到达阈值时，将触发一次 delete bitmap 的更新，并清空该缓冲区。  该参数需合理设置。若设置过小，将导致 delete bitmap 频繁更新，占用磁盘带宽，进而影响查询、cache engine 刷盘及后台 compaction 任务。若设置过大，则查询的去重开销增加，查询时间延长。过大的设置还会导致重启后的恢复过程变慢。 |
| PKEYStashedPrimaryKeyBufferSize | 设置 PKEY 存储引擎的暂存主键缓冲区的容量，单位为 MB，必须为正数，默认值为 1024。该参数在系统面对高写入压力时，可防止暂存缓冲区无限增长导致 OOM 的问题。在高写入压力下，缓冲区大小可能会达到该参数的两倍。  如果系统写入压力过大，会导致 cache engine 频繁刷盘并暂存主键和 CID 列。而delete bitmap 的更新速度较慢，因此缓冲区会持续增长。为防止暂存缓冲区大小无限增长，系统会按照该参数来暂停刷盘。 |
| PKEYBackgroundWorkerPerVolume | 配置每个 volume 的 PKEY 后台工作线程数，后台工作包括 compaction 和 delete bitmap 更新。默认值和最小值均为1。（后台总工作线程数为 volumes 数量乘以该参数值，若未手动指定 volumes 参数，则volumes数量为1） |
| PKEYCacheFlushWorkerNumPerVolume | 配置每个 volume 的 PKEY Cache Engine 刷盘工作线程数，默认值和最小值均为1。（PKEY 刷盘总工作线程数为 volumes 数量乘以该参数值，若未手动指定 volumes 参数，则 volumes 数量为1） |

## IMOLTP

| 配置参数 | 解释 |
| --- | --- |
| enableIMOLTPEngine | bool 类型。表示是否开启 OLTP 引擎。默认为 false。 |
| enableIMOLTPRedo | bool 类型。表示是否开启预写日志（WAL, Write-Ahead-Log），开启之后才能保证数据不会丢失。默认为 true。 |
| IMOLTPRedoFilePath | string 类型。表示 redo 文件（即 WAL 文件）的文件路径，可以设置为绝对路径或相对路径。当设置为相对路径时，其相对性以 *home* 目录下的 `IMOLTP` 目录作为参照。默认为 home 目录下的`IMOLTP/im_oltp.redo`。 注： 设置该参数时，必须确保路径实际存在且唯一，否则将导致 OLTP 启动失败。 |
| IMOLTPSyncOnTxnCommit | bool 类型。表示当 WAL 开启时，是否在事务对数据修改前预先写日志到持久化存储，默认为 false。该参数及 enableIMOLTPRedo 均设置为 true 后，事务会在修改数据前写日志至磁盘存储。该配置项有助于在系统崩溃后，通过重新启动系统并回放 redo 文件里的日志，从而将数据库恢复到崩溃前的状态。 注： 如果该配置项保持默认值，事务在 commit 成功后预先写的日志存储于系统缓存而非磁盘存储，因此无助于断电后的数据恢复。 |
| enableIMOLTPCheckpoint | bool 类型。表示是否开启数据检查点机制（checkpoint），即将内存中的数据定期写入磁盘，以确保数据持久化和可靠性。默认为 true。 |
| IMOLTPCheckpointFilePath | string 类型。表示 checkpoint 文件的路径（文件路径而非文件所在目录），可以设置为绝对路径或相对路径。当设置为相对路径时，其相对性以 *home* 目录下的 `IMOLTP` 目录作为参照。默认为 home 目录下的`IMOLTP/im_oltp.ckp`。 注： 设置该参数时，必须确保路径实际存在且唯一，否则将导致 OLTP 启动失败。 |
| IMOLTPCheckpointThreshold | long 类型。单位为 MiB。用于将 redo 文件中 log 的大小作为触发 checkpoint 机制的条件。默认为 100 MiB。 |
| IMOLTPCheckpointInterval | long 类型。单位为秒。用于设置强制执行 checkpoint 的周期。默认为 60 秒。 |

## TextDB

在 TextDB 中，中文分词器必须加载相应的字典才能正常运行。字典目录 `dict` 所在目录可通过配置项 jiebaDictDir
指定。如果没有指定，或指定的目录不存在，则会依次在 `HOME_DIR`
`WORKING_DIR`
`EXEC_DIR` 下寻找名为 `dict` 的目录。`dict`
目录的预期结构如下，如果找到的目录不符合该结构，同样视为未找到 `dict`
目录。

```
dict
├── hmm_model.utf8
├── idf.utf8
├── jieba.dict.utf8
├── stop_words.utf8
└── user.dict.utf8
```

| 配置参数 | 解释 |
| --- | --- |
| jiebaDictDir | string 类型。表示字典文件的存放目录。 |

## 分级存储

详情参考：[TieredStorage](../db/tiered_storage.html)

要开启分级存储，首先需要配置冷数据存储的磁盘路径。

| 配置参数 | 解释 |
| --- | --- |
| coldVolumes= [file://home/mypath/hdd](file://home/mypath/hdd), s3://bucket1/data | 用于配置冷数据的存储目录。通过函数 [moveHotDataToColdVolume](../../funcs/m/moveHotDataToColdVolume.html) 和 [setRetentionPolicy](../../funcs/s/setRetentionPolicy.html) 开启分级存储后，过期的冷数据将从 volumes 迁移至 coldVolumes。 |

若需要将过期数据存储在云端，DolphinDB 提供了 AWS S3 的相关配置：

| 配置参数 | 解释 |
| --- | --- |
| s3AccessKeyId | S3 访问账户的 id。 |
| s3SecretAccessKey | S3 访问账户的密钥。 |
| s3Region | S3 存储桶所在的区域。 |
| s3Endpoint | 用于访问 S3 的端点。 |

注：

* 配置了 AWS S3 的相关配置后，须配置 preloadModules=plugins::awss3，确保 server 顺利初始化。
* *s3Endpoint* 不能包含 `http://` 和
  `https://`。
* 在配置 *s3Endpoint* 时，支持在 endpoint 后再输入一个 BOOL 值，以表示通过 HTTP 或者 HTTPS 协议访问
  endpoint，其默认值为 false，表示以 HTTPS 协议访问。例如
  `s3Endpoint=192.168.1.160:980,true`，表示以 HTTP 协议访问
  192.168.1.160:980。
* *s3Region* 默认为 us-west-1，如果配置的 *s3Endpoint* 属于该区域，则可以不配置
  *s3Region*，否则该配置项不可省略。

## 单点登录

OAuth 是单点登录（SSO）的一种实现方式。目前 DolphinDB 已支持其三种鉴权方式：Authentication Code（授权码模式，支持
Web）、Implicit（隐式授权模式，支持 Web）、Client Credentials（客户端凭证模式，支持 API）。在启用 OAuth
单点登录时，用户须先在 DolphinDB server 中指定相关配置项以获取权限，然后在 DolphinDB 的 Web
页面中进行具体使用。如下为相关配置参数的介绍。

| 配置参数 | 解释 |
| --- | --- |
| oauth | 布尔值，是否在 Web 页面启用 OAuth 单点登录功能。默认值为 0，表示不启用。 |
| oauthWebType | 可选参数，字符串类型，用来指定 Web 使用的 OAuth 类型。 可选值为：'authorization code'(默认), 'implicit' 。 |
| oauthAuthUri | 字符串类型，用来指定授权服务器的 URI。如 'https://xxx.com/authorize '。 |
| oauthClientId | 字符串类型，用来指定客户端的 ID。 |
| oauthClientSecret | 字符串类型，用来指定客户端的密码。若 *oauthWebType* 为 authorization code 时则该参数为必填。 |
| oauthRedirectUri | 可选参数，字符串类型，用来指定 Web 的地址。注意：若配置该参数，则须和第三方 callback URL 保持一致；若不配置，则将默认按第三方 callback 进行跳转。 |
| oauthTokenUri | 可选参数，字符串类型，用来指定 token 接口的地址。   * 若 *oauthWebType* 为 authorization code 时则必填该参数。 * 若 *oauthWebType* 为 implicit 时则不填该参数。 |
| oauthTokenRequestMethod | 可选参数，字符串类型，用来指定获取 token 接口请求方法。可选值为：'GET', 'POST'(默认)。 |
| oauthUserUri | 字符串类型，用来指定获取用户名的接口地址。如'[x.com](http://x.com/esc-sso/oauth2.0/profile) '。 |
| oauthUserRequestMethod | 可选参数，字符串类型，用来指定获取用户名的接口请求方法。可选值为：'GET'(默认), 'POST'。 |
| oauthUserField | 字符串类型，用来指定获取用户名的接口响应字段。注意：若配置与返回不一致会导致报错。 |

注意：配置参数如 *oauthAuthUri*, *oauthRedirectUri*,
*oauthTokenUri*, *oauthUserUri* 等，仅支持传入有引号包裹的字符串；含有
`&`, `;` 等 Shell 特殊符号的值需要用引号包裹整个输入值。

## 性能监控与资源跟踪

通过下述参数开启系统性能监控后，可以通过 [getCompletedQueries](../../funcs/g/getCompletedQueries.html), [getRunningQueries](../../funcs/g/getRunningQueries.html)
函数，获取查询的性能和状态信息；或者通过 [getSystemCpuUsage](../../funcs/g/getSystemCpuUsage.html), [getSystemLoadAvg](../../funcs/g/getSystemLoadAvg.html) 获取系统的性能信息。

| 配置参数 | 解释 |
| --- | --- |
| perfMonitoring=1 | 启用性能监控。在单实例中，默认值是 false；在集群中，默认值是 true。 |

DolphinDB 提供了能够追踪数据节点或计算节点上用户级别的资源使用情况和查询分布式表操作的功能。此功能包括获取 CPU 和 内存使用量、记录用户对分布式表发起的
SQL 查询的次数、读取表的行数及数据量大小等能。配置这些功能通常涉及一些参数，用户可以根据具体的需求对这些配置项进行设置。

| 配置参数 | 解释 | 配置节点 |
| --- | --- | --- |
| resourceSamplingInterval=-1 | 整数，控制是否开启资源跟踪功能及设置开启后采样的时间间隔，单位为秒。默认值为 -1，表示不开启资源跟踪功能。 | 数据节点、计算节点 |
| resourceSamplingMaxLogSize=1024 | 正整数，表示资源跟踪日志切割阈值。默认值为1024，单位为 MB。开启资源跟踪功能后，采样的信息将写入文件中。为防止文件大小持续增长，DolphinDB 采用日志滚动策略，一旦文件大小达到阈值就会生成滚动日志文件。文件名以时间戳作为前缀。例如20231101162302\_access.log，表示 2023.11.01T16:23:02 拆分出来的滚动日志。 | 数据节点、计算节点 |
| resourceSamplingLogRetentionTime=-1 | 整数，指定资源跟踪日志的最长保留时间。单位为天，默认值是-1，表示不回收。 | 数据节点、计算节点 |
| resourceSamplingLogDir | 字符串，表示资源跟踪日志的存储路径，默认为 <HomeDir>/resource。 | 数据节点、计算节点 |

注：

* 2.00.13/3.00.1 之前版本、1.30.xx 系列版本：数据访问量的依据是存储引擎返回的表的大小。但这会造成结果不准确。比如在 OLAP
  分布式表上查询行数。存储引擎会从元数据里获取行数，然后构造一个相同行数的表并返回给计算层。此时在计算层记录表的行数会是整个表的行数，但实际上存储引擎并没有真正地扫描文件。
* 3.00.1
  及之后版本：数据访问量的依据是存储引擎中真实扫描的数据量。其中：
  + OLAP 引擎：从分区文件、分区缓存、分区对象本身中获取实际行数。
  + TSDB 引擎：从数据块、Cache Engine 和 Block Cache 中获取实际行数。注意：TSDB 引擎支持
    KEEP\_LAST 和 KEEP\_FIRST，支持在查询时对 sortColumns 相同的行做去重。比如一次查询访问多个
    LevelFile 后，经过去重会返回一行数据，但实际上可能扫描了多个 block。该情况下，资源跟踪会记录去重前的、多个 block
    的行数。
  + PKEY 引擎：从数据块、Cache Engine 和 Block Cache
    中获取实际行数。注意：PKEY 引擎能保证查询结果的主键唯一性，支持在查询时对 primaryKeys
    相同的行做去重。比如一次查询访问多个 LevelFile 后，经过去重会返回一行数据，但实际上可能扫描了多个
    block。该情况下，资源跟踪会记录去重前的、多个 block 的行数。

## 兼容性配置

3.00.3
以下版本，内存表中由元素类型相同的元组（ANY）构成的列，会被系统自动转换为列式元组（ColumnarTuple）。转换后该列仅允许插入相同类型的数据，否则会报错。自
3.00.3
起，系统默认不再进行此类自动转换，保留为普通 ANY 类型列，可插入不同类型的数据。为兼容旧行为，引入了配置项
*autoConversionToColumnarTuple*。如已有代码因该变更出现兼容性问题，可选择以下任一方式处理：

1. 使用 `setColumnarTuple!` 将原始列显式转换为 Columnar Tuple（推荐）；
2. 将 *autoConversionToColumnarTuple* 设置为 true，启用自动转换。

| 配置参数 | 解释 |
| --- | --- |
| autoConversionToColumnarTuple=false | 布尔值，用于控制在构造内存表时是否自动将 tuple 列转换为列数元组（ColumnarTuple）。默认值为 false，表示不自动转换，保留为原始的 ANY 类型。 |

DECIMAL 与其他类型之间的转换规则发生变化，包括以下场景：

* 浮点数字符串解析为 DECIMAL 类型（例如 loadText 等函数加载数据文件）
* 浮点数转换为 DECIMAL 类型
* DECIMAL 类型转换为整型
* 高精度的 DECIMAL 类型数转换为低精度 DECIMAL 类型

2.00.10 版本，浮点数字符串解析为 DECIMAL 类型的情况，采用的舍入模式由直接截断修改为四舍五入；

其他场景在 2.00.12 版本之前一直采用直接截断的方式。

2.00.12 版本提供了配置项 decimalRoundingMode 统一设置舍入模式。

| 配置参数 | 解释 | 配置节点 |
| --- | --- | --- |
| decimalRoundingMode | 表示在以上场景采取的舍入模式。默认为 round，表示四舍五入；如果设置为 trunc，则直接截断。 | 数据节点 |

在采用值分区，且以类型为 STRING 或 SYMBOL 的列作为分区列的分布式数据表中，若分区列写入的字符包含 ':' 和 '.'，2.00.11之前的版本会忽略 ':'
和 '.'，而2.00.11
版本提供了配置项 *ignoreSpecialCharacterInPartitionId* 用于设置是否忽略它们。

| 配置参数 | 解释 | 配置节点 |
| --- | --- | --- |
| ignoreSpecialCharacterInPartitionId=true | 布尔值，设置创建分区路径时是否忽略分区列中的字符 ':' 和 '.'。默认为 true，即忽略。若设置为 false，则不会忽略。例如：当需要向分区列写入 ".a:bc." 和 "abc" 时，若设置 *ignoreSpecialCharacterInPartitionId*=true，则在创建分区路径时会忽略 '.a:bc.' 中的 ':' 和 '.'，导致两个不同分区的数据拥有相同的分区路径 'abc'。而如果设置 *ignoreSpecialCharacterInPartitionId*=false，则在分区路径中不会忽略 ".a:bc." 中的 ':' 和 '.' ，而会写为 ".a:bc."，从而有效避免上述问题。 | 数据节点 |
| keepTupleInRowFunction | 表示 row 系列的向量函数和参数 *func* 是向量函数的 `byRow` 函数，在输入是列式元组时，返回的结果是否是列式元组。默认值为true，此时返回结果是列式元组；若设为 false，则返回结果为数组向量。 | 数据节点 |

2.00.11版本新增配置项 *movingIndexedObjectByIndexedLabel*：

| 配置参数 | 解释 |
| --- | --- |
| movingIndexedObjectByIndexedLabel | 部分m系列函数在作用于索引矩阵和索引向量时，按照索引列操作还是按照行操作。默认值为true，表示按照索引列操作；当设置为false时，按照行操作。此配置参数影响的函数包括：`move`, `mcovar`, `mcorr`, `mbeta`, `mwavg`, `mwsum`, `mpercentile`, `mrank`, `mcount`, `mfirst`, `mlast`, `mavg`, `mmed`, `mprod`, `msum`, `msum2`, `mstd`, `mvar`, `mstdp`, `mvarp`, `mskew`, `mkurtosis`, `mmin`, `mmax` |

2.00.5 以下版本，NULL 值被当作最小值处理。及以上版本可通过配置项 *nullAsMinValueForComparison* 改变这种行为：

| 配置参数 | 解释 |
| --- | --- |
| nullAsMinValueForComparison=true | NULL 值在比较运算符操作中是否当作对应数据类型的最小值处理，默认值为 true。若设置为 false，则 NULL 元素对应的结果为 NULL。 |

2.00.9.4 以下版本，*or* 函数不忽略操作符中的 NULL，所以始终返回 NULL。对于 2.00.9.4 及以上版本，由配置项 *logicOrIgnoreNull* 控制是否忽略 NULL；若需要保持 *or* 函数的这种行为，则应该设置
logicOrIgnoreNull=false。

| 配置参数 | 解释 |
| --- | --- |
| logicOrIgnoreNull=true | 设置 or 函数在一个操作数包含 NULL 时是否忽略 NULL。设置为 true（默认值）时：当另一个操作数非零时，返回 true； 当另一个操作数为零时，返回 false。当另一个操作数为 NULL 时，返回 NULL。设置为 false 时：无论另一个操作数的值如何，始终返回 NULL。 |

2.00.10 以前版本，在执行
JOIN 操作时，连接列中的 NULL 与 NULL 被视为匹配成功，这不符合 ANSI SQL 语义；为提高对 ANSI SQL 的兼容性：

* 自 2.00.10 版本起，在
  DolphinDB 中执行 JOIN 操作时，连接列中的 NULL 与 NULL 视为匹配失败。
* 为进一步提高 NULL 值匹配的灵活性，自 2.00.12 版本起，增加以下配置项，用于设置 NULL 值的匹配逻辑。

| 配置参数 | 解释 |
| --- | --- |
| enableNullSafeJoin | 设置执行 JOIN 操作时，连接列中的 NULL 与 NULL 是否可以匹配成功。  * true：匹配成功，得到 NULL 的结果。 * false（默认值）：匹配不成功。 |

| 配置参数 | 解释 |
| --- | --- |
| removeSpecialCharInColumnName=false | 是否规范化包含特殊符号的列名，默认值是 false，表示自动产生的数据表的列名允许包含特殊符号，即列名可以以非字母和中文开头，且可以包含下划线之外的符号。如果要跟以前版本兼容，可以将该变量配置为 true。 |
| appendTupleAsAWhole=true | 通过 [append!](../../funcs/a/append%21.html) 追加或通过 [join!](../../funcs/j/join%21.html) 合并元组，是否将元组作为一个整体。默认值为 true，表示将元组作为整体追加或合并。设为 false 时，将元组的每个元素逐一追加或合并。 |

2.00.10.4 以下版本，系统默认将小数常量解析为 DOUBLE 类型。对于 2.00.10.4 及以上版本，可通过配置项
*parseDecimalAsFloatingNumber* 设置系统解析小数常量类型的默认行为。

| 配置参数 | 解释 |
| --- | --- |
| parseDecimalAsFloatingNumber=true | 是否将小数常量解析为浮点数的 DOUBLE 类型，默认值为 true。若设置为 false，系统则会将小数常量解析为定点数的 DECIMAL64 类型。 |

