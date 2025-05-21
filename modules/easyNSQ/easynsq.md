# easyNSQ 实时行情数据接入功能模块

为了实时获取 level-2 行情数据，DolphinDB 对接恒生 NSQ 极速行情服务软件，开发了能够获取上海和深圳市场行情数据的 NSQ 插件。安装好插件后，用户需要创建用于接收实时数据的持久化共享流表和分区表，并且发起相关订阅。为了方便用户快速搭建 NSQ 实时行情数据的流计算环境，DolphinDB 开发了 DolphinDBModules::easyNSQ 模块（简称 easyNSQ 模块），主要用于 NSQ 实时行情数据的自动化接收和存储。目前已经支持的数据源包括上海和深圳市场的：

* 现货逐笔委托行情主推回调（OnRtnSecuTransactionEntrustData->orders）
* 现货逐笔成交行情主推回调（OnRtnSecuTransactionTradeData->trade）
* 现货深度行情主推回调（OnRtnSecuDepthMarketData->snapshot）

**注意**：DolphinDB 仅提供对接 HSNsqApi 的 NSQ 插件，数据源和接入服务可咨询数据服务商或证券公司。

NSQ 插件的版本支持情况请参考 [插件市场下载页](https://marketplace.dolphindb.cn/18)。本模块基于 DolphinDB 2.00.11 版本开发，请在使用本模块时确保安装了 2.00.11 及以上版本的 DolphinDB server。

## 1. 安装说明

使用 DolphinDBModules::easyNSQ 模块前，请确保在 DolphinDB 服务器上正确安装和加载了 NSQ 插件和 DolphinDBModules::easyNSQ 模块文件。

**注意**：对于之前从未使用过 DolphinDB 插件和模块功能的读者，推荐在阅读以下章节的同时阅读 [DolphinDB NSQ 行情插件文档](https://docs.dolphindb.cn/zh/plugins/nsq/nsq.md) 以及 [DolphinDB 模块说明](https://docs.dolphindb.cn/zh/tutorials/tu_modules.md)。
easyNSQ 模块依赖于 NSQ 插件，**请确保先加载 NSQ 插件，再加载 easyNSQ 模块**。

### 1.1 安装 NSQ 插件

* **在线安装插件**

用户可以通过 DolphinDB 官方的插件市场在线安装 NSQ 插件，具体操作步骤如下：

1. 在 DolphinDB 客户端（DolphinDB GUI、Web 页面或者 Vscode 插件）中运行 [listRemotePlugins](https://docs.dolphindb.cn/zh/funcs/l/listRemotePlugins.md) 函数，查看插件市场中与当前 DolphinDB server 适配的 NSQ 插件及其版本信息。

   ```
   listRemotePlugins("nsq")
   ```

   该函数执行后会返回一个如下的表。

   图 1-1 listRemotePlugins 函数的返回结果示例

   ![图 1-1 listRemotePlugins 函数的返回结果示例](images/1.1.png)
2. 使用 [installPlugin](https://docs.dolphindb.cn/zh/funcs/i/installPlugin.md) 函数从插件市场下载并安装 NSQ 插件。

   ```
   installPlugin("nsq")
   ```

   该函数会在安装完成后返回插件的安装路径。

   图 1-2 installPlugin 函数的返回结果示例

   ![图 1-2 installPlugin 函数的返回结果示例](images/1.2.png)

* **离线安装插件**

如果 DolphinDB server 所在机器与插件市场的网络不互通，用户还可以选择使用离线方式安装 NSQ 插件。

1. 根据 DolphinDB server 版本和及其所在机器的操作系统，从 [DolphinDB 插件市场](https://marketplace.dolphindb.cn/18) 或者 [Github](https://github.com/dolphindb/DolphinDBPlugin/tree/release200.11/nsq) 和 [Gitee](https://gitee.com/dolphindb/DolphinDBPlugin/tree/release200.11/nsq) 下载 NSQ 插件。注意，如果从 Github 或 Gitee 代码仓库下载 NSQ 插件，部分版本可能需要用户自行编译，插件编译的步骤可以参考 [此文档](https://docs.dolphindb.cn/zh/2.00.11/plugins/nsq/nsq.html#%E8%87%AA%E8%A1%8C%E7%BC%96%E8%AF%91)。
2. 将 NSQ 插件的所有文件（包括动态库文件）放到 DolphinDB server 所在机器的该路径下： */DolphinDB/server/plugins/nsq*。
3. 若使用 Linux 系统，还需要将 NSQ 插件的路径添加到 Linux 环境变量，然后重启 DolphinDB：

   ```
   export LD_LIBRARY_PATH=/DolphinDB/server/plugins/nsq/:$LD_LIBRARY_PATH
   ```

### 1.2 加载 NSQ 插件

* **手动加载插件**

安装 NSQ 插件完之后，可以使用 [loadPlugin](https://docs.dolphindb.cn/zh/funcs/l/loadPlugin.md) 函数加载插件。任意会话中成功加载插件，即可在当前 server 节点的其他会话中使用插件。若 DolphinDB server 重启，则需要重新加载插件。

2.00.11 及以上版本的 server，支持使用插件名来加载插件。

```
loadPlugin("nsq")
```

也可以使用插件描述文件的绝对路径来加载插件。

```
loadPlugin("/DolphinDB/server/plugins/nsq/PluginNsq.txt")
```

若插件加载成功，该函数会返回一个包含所有插件函数的向量。

图 1-3 loadPlugin 函数的返回结果示例

![图 1-3 loadPlugin 函数的返回结果示例](images/1.3.png)

* **自动预加载插件**

DolphinDB server 启动后，插件只需加载一次就会一直生效，但是如果 server 重启就需要重新加载插件。为了避免重复手动加载插件的麻烦，DolphinDB 提供了自动预加载插件的功能。可以通过配置项 [preloadModules](https://docs.dolphindb.cn/zh/db_distr_comp/cfg/standalone.html#ariaid-title4) 指定系统启动后自动加载的插件或模块。

在配置文件 *dolphindb.cfg* 中加上：

```
preloadModules=plugins::nsq
```

然后启动 DolphinDB，系统自动会到 */DolphinDB/server/plugins/* 目录下加载 NSQ 插件。

* **验证加载**

可以运行以下代码来验证 NSQ 插件加载成功：

```
defs("nsq::%")
```

以上代码用于查询 DolphinDB 系统中 ”nsq“ 命名空间的函数，插件加载成功会返回如下列表：

图 1-4 defs 函数的返回结果示例

![图 1-4 defs 函数的返回结果示例](images/1.4.png)

### 1.3 安装 easyNSQ 模块

以 Linux 单节点为例，将模块文件拷贝到 */DolphinDB/server/modules/* 目录下，即模块脚本 *easyNSQ.dos* 的路径应为 */DolphinDB/server/modules/DolphinDBModules/easyNSQ.dos 。*

模块文件安装好，运行以下代码加载模块：

```
use DolphinDBModules::easyNSQ
```

如果没有返回错误信息，则说明 easyNSQ 模块已经成功加载。

安装插件时常见的错误信息如下：

1. 插件与 DolphinDB server 版本不匹配，需要改用适配 server 版本的插件：`The first line must be the module name, dynamic library file name and version, separated by comma` 或 `Failed to loadPlugin file [...] for the plugin version [...] is not same to the server version [...]`
2. 没有将 NSQ 插件的路径添加到 Linux 环境变量，需要添加环境变量再重启 DolphinDB server ：`Couldn't load the dynamic library [.../libPluginNsq.so]: libHSNsqApi.so: cannot open shared object file: No such file or directory [...]`

如果遇到其他问题，可以在社区中交流或者联系 DolphinDB 的技术支持工程师。

## 2. 使用示例

* **第一步：** 按照上一章节的说明，安装并加载 NSQ 行情插件和 easyNSQ 模块。
* **第二步**：准备好 NSQ 行情数据服务器配置文件 *sdk\_config.ini*，上传到 DolphinDB server 所在的服务器上。下图中，配置文件放置在 *server/plugins/nsq/* 路径。

图 2-1 server/plugins/ 文件结构示例

![图 2-1 server/plugins/ 文件结构示例](images/2.1.png)

* **第三步**：打开浏览器，在地址栏输入 DolphinDB server 的 IP 地址与端口号，连接到该节点的 Web 管理页面。点击右上角的用户按钮进行登录。

图 2-2 DolphinDB Web 管理页面示例

![图 2-2 DolphinDB Web 管理页面示例](images/2.2.png)

* **第四步**：在交互编程页面，执行以下脚本订阅行情数据和落库存储：

```
// 加载插件
try{ loadPlugin("nsq") } catch(ex) { print(ex) }
go
// 调用模块
use DolphinDBModules::easyNSQ

// nsq 行情配置文件路径
configFilePath = "<your_path_to>/nsq_sdk_config.ini";

// nsq 账号（可选参数）
nsq_username = "<your_nsq_username>";
nsq_password = "<your_nsq_password>";

// 数据接收选项（可选参数）
nsq_data_option = dict(STRING, ANY)
nsq_data_option["receivedTime"]=true  // 在行情数据中增加一列接收时间
nsq_data_option["getAllFieldNames"]=true // 接受 nsq 原始行情中所有字段

// 初始化环境
iniNsqEnv()
iniNsqDfs()

// 建立对沪深交易所L2快照、逐笔委托和逐笔成交行情数据的订阅，接收数据后自动落库存储
subscribeNsq(configFilePath, "orders", ["sh","sz"], merge=true, saveToDfs=true, options=nsq_data_option, username=nsq_username, password=nsq_password)
subscribeNsq(configFilePath, "trade", ["sh","sz"], merge=true, saveToDfs=true, options=nsq_data_option, username=nsq_username, password=nsq_password)
subscribeNsq(configFilePath, "snapshot", ["sh","sz"], merge=true, saveToDfs=true, options=nsq_data_option, username=nsq_username, password=nsq_password)

/*
// 不使用 nsq 账号和数据接收选项的订阅方式
subscribeNsq(configFilePath, "orders", ["sh","sz"], merge=true, saveToDfs=true)
subscribeNsq(configFilePath, "trade", ["sh","sz"], merge=true, saveToDfs=true)
subscribeNsq(configFilePath, "snapshot", ["sh","sz"], merge=true, saveToDfs=true)
*/
```

* **第五步**：查询订阅状态

使用插件函数 `nsq::getSubscriptionStatus()` 可以获取 NSQ 行情的订阅状态。

```
nsq::getSubscriptionStatus()
```

图 2-3 nsq::getSubscriptionStatus 函数的返回结果示例

![图 2-3 nsq::getSubscriptionStatus 函数的返回结果示例](images/2.3.png)

* **第六步**：查询流数据表。

（1）逐笔委托

```
select * from nsqStockOrdersStream limit 10
```

图 2-4 逐笔委托流表的查询结果示例

![图 2-4 逐笔委托流表的查询结果示例](images/2.4.png)

（2）逐笔成交

```
select * from nsqStockTradeStream limit 10
```

图 2-5 逐笔成交流表的查询结果示例

![图 2-5 逐笔成交流表的查询结果示例](images/2.5.png)

（3）L2 快照

```
select * from nsqStockSnapshotStream limit 10
```

图 2-6 L2 快照流表的查询结果示例

![图 2-6 L2 快照流表的查询结果示例](images/2.6.png)

* **第七步**：查询分区表

（1）逐笔委托

```
select * from loadTable("dfs://nsqStockOrders", "orders") limit 10
```

图 2-7 逐笔委托分区表的查询结果示例

![图 2-7 逐笔委托分区表的查询结果示例](images/2.7.png)

（2）逐笔成交

```
select * from nsqStockTradeStream limit 10
```

图 2-8 逐笔成交分区表的查询结果示例

![图 2-8 逐笔成交分区表的查询结果示例](images/2.8.png)

（3）L2 快照

```
select * from loadTable("dfs://nsqStockSnapshot", "snapshot") limit 10
```

图 2-9 L2 快照分区表的查询结果示例

![图 2-9 L2 快照分区表的查询结果示例](images/2.9.png)

## 3. 实时行情数据存储说明

### 3.1 接收行情数据到流数据表

图 3-1 easyNSQ 模块接收行情数据到流数据表

![图 3-1 easyNSQ 模块接收行情数据到流数据表](images/3.1.png)

用户指定希望接收的行情数据源（逐笔委托、逐笔成交或 L2 快照），easyNSQ 模块会根据用户的需要创建不同的持久化共享流表，并通过 NSQ 插件订阅交易所数据，将上海和深圳市场的实时行情数据写入持久化共享流表中。

持久化共享流表是进行共享并做了持久化处理的流数据表。将流表共享是为了让该流表在连接当前节点其它会话中也可见。比如通过 C++ API 实时查询流数据表的会话与定义流表的会话不会是同一个，如果不将流表共享，查询的需求就无法实现。

对流数据表进行持久化的目的主要有以下两点：

* 控制该表的最大内存占用。通过设置 `enableTableShareAndPersistence` 函数中的 *cacheSize* 参数，可以控制流表在内存中最多保留多少条记录，超出的部分被写入持久化数据文件、从内存中清除，进而控制该表的最大内存占用。
* 在节点异常关闭的极端情况下，可以从持久化数据文件中恢复已经写入流数据表但是未消费的数据，保证流数据“至少消费一次”的需求。

流数据表持久化采用异步的方式进行，对流表写入吞吐量几乎没有影响。

**注意**：

虽然名字里带有“持久化”，但是持久化流表并不能满足行情数据持久化存储的需求。

首先，流数据表持久化到磁盘上的数据的规模在增长到一定大小，或者超过一定时间之后，会触发系统的回收校验，并不能做到真正的永久化存储。

其次，流数据表持久化到磁盘上的数据并没有进行结构化的存储，查询和更新的效率比不上在分区表中存储的数据，不适合用于实际生产环境。

如果用户有将行情数据在磁盘上进行持久化存储的需求，请阅读本篇文档[2.2](https://gitee.com/dolphindb/DolphinDBModules/blob/master/easyNSQ/README.md#22-%E6%8E%A5%E6%94%B6%E8%A1%8C%E6%83%85%E6%95%B0%E6%8D%AE%E5%88%B0%E6%B5%81%E6%95%B0%E6%8D%AE%E8%A1%A8%E5%B9%B6%E6%8C%81%E4%B9%85%E5%8C%96%E5%88%B0%E5%88%86%E5%8C%BA%E8%A1%A8)及[2.3](https://gitee.com/dolphindb/DolphinDBModules/blob/master/easyNSQ/README.md#23-%E5%90%88%E5%B9%B6%E5%AD%98%E5%82%A8%E4%B8%8A%E6%B5%B7%E5%92%8C%E6%B7%B1%E5%9C%B3%E5%B8%82%E5%9C%BA%E8%A1%8C%E6%83%85%E6%95%B0%E6%8D%AE)小节的方案说明。

用户可以为这些持久化的共享流表指定名字，也可以选择使用模块默认的表名。在用户没有指定表名的情况下，模块对持久化共享流表的命名如下：

* 上交所逐笔委托：流表名称为 ”nsqStockOrdersSHStream“。
* 深交所逐笔委托：流表名称为 ”nsqStockOrdersSZStream"。
* 上交所逐笔成交：流表名称为 “nsqStockTradeSHStream"。
* 深交所逐笔成交：流表名称为 ”nsqStockTradeSZStream"。
* 上交所 L2 所快照：流表名称为 “nsqStockSnapshotSHStream"。
* 深交所 L2 所快照：流表名称为 ”nsqStockSnapshotSZStream“。

基于过往项目的实践，推荐如下的持久化共享流表参数配置方案：

| 配置项 | 配置值 |
| --- | --- |
| asynWrite | true |
| compress | true |
| cacheSize | 500,000 |
| preCache | 100,000 |
| retentionMinutes | 1440 |
| flushMode | 0 |

### 3.2 接收行情数据到流数据表，并持久化到分区表

图 3-2 easyNSQ 模块接收行情数据到流数据表，并持久化到分区表

![图 3-2 easyNSQ 模块接收行情数据到流数据表，并持久化到分区表](images/3.2.png)

easyNSQ 模块还支持将实时行情数据写入分区表进行持久化的存储。在此种订阅模式下，用户指定希望接收的行情数据源（逐笔委托、逐笔成交或 L2 快照），easyNSQ 模块会通过 NSQ 插件订阅交易所数据，将上海和深圳市场的实时行情数据分别写入持久化共享流表，然后通过 DolphinDB 内置的订阅-发布功能，将流表的增量数据实时写入分区表。

用户可以指定用于存储行情数据的数据库和分区表的名字。在用户没有指定数据库和分区表名字的情况下，模块会使用默认名字的数据库和分区表：

* 上交所逐笔委托：数据库名称为 "dfs://nsqStockOrders"，分区表名称为 "ordersSH"。
* 深交所逐笔委托：数据库名称为 "dfs://nsqStockOrders"，分区表名称为 "ordersSZ"。
* 上交所逐笔成交：数据库名称为 "dfs://nsqStockTrade"，分区表名称为 "tradeSH"。
* 深交所逐笔成交：数据库名称为 "dfs://nsqStockTrade"，分区表名称为 "tradeSZ"。
* 上交所 L2 所快照：数据库名称为 "dfs://nsqStockSnapshot"，分区表名称为 "snapshotSH"。
* 深交所 L2 所快照：数据库名称为 "dfs://nsqStockSnapshot"，分区表名称为 "snapshotSZ"。

细心的读者已经注意到 easyNSQ 模块会将同一行情数据源的数据放在同一个数据库中，比如上交所逐笔委托和深交所逐笔委托数据都会存储在数据库 "dfs://nsqStockOrders"。这样的做法，部分是出于业务逻辑的考虑，即后续往往会对上交所和深交所的逐笔委托数据进行同样的处理操作；此外，NSQ 插件已经对上海和深圳市场的行情数据表结构做了统一处理，上交所和深交所的数据适用于同一套数据库分区规则，可以存储在同一个数据库中。

**注意**：

出于数据安全的考虑，easyNSQ 模块在存储数据到分区表的过程中，如果发现要做写入的分区表不存在，会创建新分区表；如果发现同名分区表已存在，会直接向该分区表写入数据，而不是进行删除和重新创建。

因此，用户在使用 easyNSQ 模块时，需要注意：如果已存在分区表的表结构与行情数据结构不同，写入数据的时候就会抛出异常。建议用户使用 easyNSQ 模块时，在订阅行情数据前对用于行情数据入库存储的分区表进行检查。

基于过往项目的实践，对分区表确定了如下的分区方案：

| 行情数据类型 | 分区方案 | 分区列 | 排序列 |
| --- | --- | --- | --- |
| 逐笔委托（orders） | 组合分区：时间维度按天分区 + 证券代码维度 HASH 25 分区 | TradeDate + InstrumentID | InstrumentID + TransactTime |
| 逐笔成交（trade） | 组合分区：时间维度按天分区 + 证券代码维度 HASH 25 分区 | TradeDate + InstrumentID | InstrumentID + TransactTime |
| L2 快照（snapshot） | 组合分区：时间维度按天分区 + 证券代码维度 HASH 25 分区 | TradeDate + InstrumentID | InstrumentID + UpdateTime |

### 3.3 合并存储上海和深圳市场行情数据

图 3-3 easyNSQ 模块对沪深市场的行情数据进行合并处理

![图 3-3 easyNSQ 模块对沪深市场的行情数据进行合并处理](images/3.3.png)

easyNSQ 模块支持将上海和深圳市场的实时行情数据进行合并处理。用户可以指定用于接收实时数据的流数据表的名字，以及用于存储行情数据的数据库和分区表的名字。在用户没有进行指定的情况下，模块会使用默认的名字：

* 逐笔委托：流表名称为 ”nsqStockOrdersStream“， 数据库名称为 "dfs://nsqStockOrders"，分区表名称为 "orders"。
* 逐笔成交：流表名称为 ”nsqStockTradeStream“，数据库名称为 "dfs://nsqStockTrade"，分区表名称为 "trade"。
* L2 所快照：流表名称为 ”nsqStockSnapshotStream“，数据库名称为 "dfs://nsqStockSnapshot"，分区表名称为 "snapshot"。

对于沪深行情数据合并存储，持久化共享流表的参数配置方案同沪深行情分开存储的参数配置方案。而分区表的分区方案如下：

| 行情数据类型 | 分区方案 | 分区列 | 排序列 |
| --- | --- | --- | --- |
| 逐笔委托（orders） | 组合分区：时间维度按天分区 + 证券代码维度 HASH 50 分区 | TradeDate + InstrumentID | InstrumentID + TransactTime |
| 逐笔成交（trade） | 组合分区：时间维度按天分区 + 证券代码维度 HASH 50 分区 | TradeDate + InstrumentID | InstrumentID + TransactTime |
| L2 快照（snapshot） | 组合分区：时间维度按天分区 + 证券代码维度 HASH 50 分区 | TradeDate + InstrumentID | InstrumentID + UpdateTime |

## 4. easyNSQ 模块接口介绍

### 4.1 subscribeNsq

**语法**

```
easyNSQ::subscribeNsq(configFilePath, dataSource, [markets], [merge], [saveToDfs], [streamTableNames],
  [dbPath], [tableNames], [options], [username], [password])
```

**参数**

*configFilePath* ：一个字符串，表示 NSQ 行情服务器配置文件 *sdk\_config.ini* 的绝对路径；若拷贝配置文件至 *dolphindb server*，则可以是相对于 *dolphindb server* 的相对路径。

*dataSource* ：一个字符串，表示行情的类型，可以是以下值：

* “orders”：表示回调函数 OnRtnSecuDepthMarketData（主推 - 现货深度行情）获取的行情数据。
* ”trade”：表示回调函数 OnRtnSecuDepthMarketData（主推 - 现货深度行情）获取的行情数据。
* “snapshot”：表示回调函数 OnRtnSecuDepthMarketData（主推 - 现货深度行情）获取的行情数据。

*markets*： 可选参数。一个字符串或字符串向量，表示行情市场，上海证券交易所用 `sh` 表示，深圳证券交易所用 `sz` 表示，参数默认值为 `["sz", "sh"]`。

*merge*： 可选参数。一个布尔值，表示是否合并处理上海和深圳市场的行情数据，参数默认值为 false。

*saveToDfs*： 可选参数。一个布尔值，表示是否持久化存储到分区表，参数默认值为 false。

*streamTableNames*： 可选参数。一个字符串或字符串向量，表示用于接收实时数据的流数据表的名字，**将使用这个名字创建新的持久化共享流数据表**。

*dbPath*： 可选参数。一个字符串，表示用于持久化存储数据的数据库的名字。若数据库不存在，将创建新数据库。

*tableNames* ：可选参数。一个字符串或字符串向量，表示用于持久化存储数据的分区表的名字。若分区表不存在，将创建新分区表。**若同名分区表已存在，则直接向该表写入**。

*options*：可选参数。一个字典标量，表示行情订阅的扩展参数。当前版本只支持以 “receivedTime” 和 “getAllFieldNames” 作为字典的键。receivedTime 表示是否显示接收时间，对应值为布尔类型标量。 getAllFieldNames 表示是否接受所有字段数据，对应值为布尔类型标量。详见后续的 ”行情数据表结构“章节以及 [NSQ 插件函数接口文档](https://docs.dolphindb.cn/zh/plugins/nsq/nsq.html#connect)。

*username*：可选参数。一个字符串，表示登录 NSQ 行情服务器的用户名。

*password*：可选参数。一个字符串，表示登录 NSQ 行情服务器用户名对应的密码。

**函数详情**

自动化接收和存储 NSQ 实时行情数据。对应行情市场和行情类型的实时数据会被接收到持久化共享流表，并根据用户需要，同时将数据持久化存储到分区表。 函数执行成功会返回流数据表的名字（如果 *saveToDfs* 为 true，还会返回数据库和分区表的名字），若执行不成功则返回 NULL。

```
streamTableNames = subscribeNsq(configFilePath, "snapshot", ["sh","sz"], merge=true)
streamTableNames, dbPath, tableNames = subscribeNsq(configFilePath, "orders", "sh", saveToDfs=true)
```

用户没有使用可选参数 *streamTableNames*、*dbPath* 和 *tableNames* 时，easyNSQ 模块默认使用以下名字：

| 行情类型 | 行情市场 | 流数据表 | 数据库 | 分区表 |
| --- | --- | --- | --- | --- |
| orders | sh | nsqStockOrdersSHStream | dfs://nsqStockOrders | ordersSH |
| orders | sz | nsqStockOrdersSZStream | dfs://nsqStockOrders | ordersSZ |
| orders | 合并存储 | nsqStockOrdersStream | dfs://nsqStockOrders | orders |
| trade | sh | nsqStockTradeSHStream | dfs://nsqStockTrade | tradeSH |
| trade | sz | nsqStockTradeSZStream | dfs://nsqStockTrade | tradeSZ |
| trade | 合并存储 | nsqStockTradeStream | dfs://nsqStockTrade | trade |
| snapshot | sh | nsqStockSnapshotSHStream | dfs://nsqStockSnapshot | snapshotSH |
| snapshot | sz | nsqStockSnapshotSZStream | dfs://nsqStockSnapshot | snapshotSZ |
| snapshot | 合并存储 | nsqStockSnapshotStream | dfs://nsqStockSnapshot | snapshot |

### 4.2 closeNsqConnection

**语法**

```
easyNSQ::closeNsqConnection()
```

**参数**

无

**函数详情**

断开与行情服务器的连接，本函数执行后会取消所有已建立的对实时行情数据的订阅。

函数执行成功返回 true，若有执行异常则会返回 false。

### 4.3 iniNsqEnv

**语法**

```
easyNSQ::iniNsqEnv([streamTableNames])
```

**参数**

*streamTableNames*：可选参数。一个字符串或字符串向量，表示要清理的流数据表。

**函数详情**

初始化流计算环境，清理指定的流数据表及其订阅。若用户没有使用可选参数 *streamTableNames*，则会根据 easyNSQ 模块默认使用的流表进行清理，请参考 `easyNSQ::subscribeNsq` 的函数详情说明。

**注意**：`iniNsqEnv` 函数在没有传入参数时，会根据 easyNSQ 模块默认使用的流表名字，对同名流表及其订阅进行清理。请用户注意这一行为可能会导致数据被误删除。

### 4.4 iniNsqDfs

**语法**

```
easyNSQ::iniNsqDfs([dbName], [tbNames])
```

**参数**

*dbName*： 可选参数。一个字符串，表示要清理的分区表的数据路径。

*tbNames* ：可选参数。一个字符串或字符串向量，表示要清理的分区表的表名。

**函数详情**

初始化环境，清理已指定的分区表。若用户没有使用可选参数 *dbName* 和 *tbNames*，则会根据 easyNSQ 模块默认使用的分区表进行清理，请参考 `easyNSQ::subscribeNsq` 的函数详情说明。

**注意**：`iniNsqDfs` 函数在没有传入参数时，会根据 easyNSQ 模块默认使用的数据库路径和分区表名字，对分区表进行清理。请用户注意这一行为可能会导致数据被误删除。

## 5. easyNSQ 模块使用示例

本章节为四个不同的使用场景提供了脚本示例，并在最后提供了脚本用于关闭 NSQ 连接和清理例子运行时创建的流表、分区表。

### 5.1 例1-接收深圳市场 snapshot 实时行情数据

```
// 加载插件
try{ loadPlugin("nsq") } catch(ex) { print(ex) }
go
// 调用模块
use DolphinDBModules::easyNSQ

configFilePath = "<your_path_to>/nsq_sdk_config.ini";

// 初始化化境并拉起订阅
iniNsqEnv()
streamTableNames = subscribeNsq(configFilePath, "snapshot", "sz")

// 检查订阅情况
nsq::getSubscriptionStatus()
select count(*) from objByName(streamTableNames[0])
select top 100 * from objByName(streamTableNames[0])

// 停止订阅
nsq::unsubscribe("snapshot", "sz")
nsq::getSubscriptionStatus()
```

### 5.2 例2-接收上海市场所有类型实时行情数据，并持久化存储

```
// 加载插件
try{ loadPlugin("nsq") } catch(ex) { print(ex) }
go
// 调用模块
use DolphinDBModules::easyNSQ

configFilePath = "<your_path_to>/nsq_sdk_config.ini";

// 数据接收选项（非必填）
nsq_data_option = dict(STRING, ANY)
nsq_data_option["receivedTime"]=true  // 在行情数据中增加一列接收时间
nsq_data_option["getAllFieldNames"]=true // 接受 nsq 原始行情中所有字段

// 初始化环境并拉起订阅
iniNsqEnv()
iniNsqDfs()
subscribeNsq(configFilePath, "orders", "sh", saveToDfs=true, options=nsq_data_option)
subscribeNsq(configFilePath, "trade", "sh", saveToDfs=true, options=nsq_data_option)
subscribeNsq(configFilePath, "snapshot", "sh", saveToDfs=true, options=nsq_data_option)

// 检查订阅情况
nsq::getSubscriptionStatus()
existsSubscriptionTopic(,"nsqStockOrdersSHStream","easyNSQ_saveToDfsTable")
existsSubscriptionTopic(,"nsqStockTradeSHStream","easyNSQ_saveToDfsTable")
existsSubscriptionTopic(,"nsqStockSnapshotSHStream","easyNSQ_saveToDfsTable")
select count(*) from objByName("nsqStockOrdersSHStream")
select count(*) from loadTable("dfs://nsqStockOrders", "ordersSH")
select count(*) from objByName("nsqStockTradeSHStream")
select count(*) from loadTable("dfs://nsqStockTrade", "tradeSH")
select count(*) from objByName("nsqStockSnapshotSHStream")
select count(*) from loadTable("dfs://nsqStockSnapshot", "snapshotSH")

// 仅停止 orders 行情数据的订阅
nsq::unsubscribe("orders", "sh")
nsq::getSubscriptionStatus()

// 停止所有订阅
closeNsqConnection()
nsq::getSubscriptionStatus()
```

### 5.3 例3-停止所有订阅后，重新接收上海市场 orders 数据

#### 保留之前持久化的数据

```
// 加载插件
try{ loadPlugin("nsq") } catch(ex) { print(ex) }
go
// 调用模块
use DolphinDBModules::easyNSQ

configFilePath = "<your_path_to>/nsq_sdk_config.ini";

// 数据接收选项（非必填）
nsq_data_option = dict(STRING, ANY)
nsq_data_option["receivedTime"]=true  // 在行情数据中增加一列接收时间
nsq_data_option["getAllFieldNames"]=true // 接受 nsq 原始行情中所有字段

// 初始化流环境并拉起订阅
iniNsqEnv("nsqStockOrdersSHStream")
streamTableNames, dbPath, tableNames = subscribeNsq(configFilePath, "orders", "sh", saveToDfs=true, options=nsq_data_option)

// 检查订阅情况
nsq::getSubscriptionStatus()
existsSubscriptionTopic(,streamTableNames[0],"easyNSQ_saveToDfsTable")
select count(*) from objByName(streamTableNames[0])
select count(*) from loadTable(dbPath, tableNames[0])

// 停止订阅
nsq::unsubscribe("orders", "sh")
```

#### 不保留之前持久化的数据

```
// 加载插件
try{ loadPlugin("nsq") } catch(ex) { print(ex) }
go
// 调用模块
use DolphinDBModules::easyNSQ

configFilePath = "<your_path_to>/nsq_sdk_config.ini";

// 数据接收选项（非必填）
nsq_data_option = dict(STRING, ANY)
nsq_data_option["receivedTime"]=true  // 在行情数据中增加一列接收时间
nsq_data_option["getAllFieldNames"]=true // 接受 nsq 原始行情中所有字段

// 初始化环境并拉起订阅
iniNsqEnv("nsqStockOrdersSHStream")
iniNsqDfs("dfs://nsqStockOrders", "ordersSH")
subscribeNsq(configFilePath, "orders", "sh", saveToDfs=true, options=nsq_data_option)

// 检查订阅情况
nsq::getSubscriptionStatus()
existsSubscriptionTopic(,"nsqStockOrdersSHStream","easyNSQ_saveToDfsTable")
select count(*) from objByName("nsqStockOrdersSHStream")
select count(*) from loadTable("dfs://nsqStockOrders", "ordersSH")

// 停止订阅
nsq::unsubscribe("orders", "sh")
```

### 5.4 例4-接收上海和深圳市场所有类型的实时行情数据，并持久化存储

#### 合并处理上海和深圳市场数据

```
// 加载插件
try{ loadPlugin("nsq") } catch(ex) { print(ex) }
go
// 调用模块
use DolphinDBModules::easyNSQ

configFilePath = "<your_path_to>/nsq_sdk_config.ini";
// nsq 账号（非必填）
nsq_username = "<your_nsq_username>";
nsq_password = "<your_nsq_password>";

// 数据接收选项（非必填）
nsq_data_option = dict(STRING, ANY)
nsq_data_option["receivedTime"]=true  // 在行情数据中增加一列接收时间
nsq_data_option["getAllFieldNames"]=true // 接受 nsq 原始行情中所有字段

// 初始化环境并拉起订阅
iniNsqEnv()
iniNsqDfs()
subscribeNsq(configFilePath, "orders", ["sh","sz"], merge=true, saveToDfs=true, options=nsq_data_option, username=nsq_username, password=nsq_password)
subscribeNsq(configFilePath, "trade", ["sh","sz"], merge=true, saveToDfs=true, options=nsq_data_option, username=nsq_username, password=nsq_password)
subscribeNsq(configFilePath, "snapshot", ["sh","sz"], merge=true, saveToDfs=true, options=nsq_data_option, username=nsq_username, password=nsq_password)

// 检查订阅情况
nsq::getSubscriptionStatus()
existsSubscriptionTopic(,"nsqStockOrdersStream","easyNSQ_saveToDfsTable")
existsSubscriptionTopic(,"nsqStockTradeStream","easyNSQ_saveToDfsTable")
existsSubscriptionTopic(,"nsqStockSnapshotStream","easyNSQ_saveToDfsTable")

// 停止订阅
closeNsqConnection()
```

#### 分开处理上海和深圳市场数据（用户自定义流表和分区表名字）

```
// 加载插件
try{ loadPlugin("nsq") } catch(ex) { print(ex) }
go
// 调用模块
use DolphinDBModules::easyNSQ

configFilePath = "<your_path_to>/nsq_sdk_config.ini";
// nsq 账号（非必填）
nsq_username = "<your_nsq_username>";
nsq_password = "<your_nsq_password>";

// 数据接收选项（非必填）
nsq_data_option = dict(STRING, ANY)
nsq_data_option["receivedTime"]=true  // 在行情数据中增加一列接收时间
nsq_data_option["getAllFieldNames"]=true // 接受 nsq 原始行情中所有字段

// 初始化环境并拉起订阅
iniNsqEnv(["myNsqOrdersSHStream", "myNsqOrdersSZStream", "myNsqTradeSHStream", "myNsqTradeSZStream","myNsqSnapshotSHStream", "myNsqSnapshotSZStream"])
iniNsqDfs("dfs://myNsqOrders", `myNsqOrdersSH`myNsqOrdersSZ)
iniNsqDfs("dfs://myNsqTrade", `myNsqTradeSH`myNsqTradeSZ)
iniNsqDfs("dfs://myNsqSnapshot", `myNsqSnapshotSH`myNsqSnapshotSZ)
subscribeNsq(configFilePath, "orders", ["sh","sz"], saveToDfs=true, streamTableNames=["myNsqOrdersSHStream", "myNsqOrdersSZStream"], dbPath="dfs://myNsqOrders", tableNames=["myNsqOrdersSH", "myNsqOrdersSZ"], options=nsq_data_option, username=nsq_username, password=nsq_password)
subscribeNsq(configFilePath, "trade", ["sh","sz"], saveToDfs=true, streamTableNames=["myNsqTradeSHStream", "myNsqTradeSZStream"], dbPath="dfs://myNsqTrade", tableNames=["myNsqTradeSH", "myNsqTradeSZ"], options=nsq_data_option, username=nsq_username, password=nsq_password)
subscribeNsq(configFilePath, "snapshot", ["sh","sz"], saveToDfs=true, streamTableNames=["myNsqSnapshotSHStream", "myNsqSnapshotSZStream"], dbPath="dfs://myNsqSnapshot", tableNames=["myNsqSnapshotSH", "myNsqSnapshotSZ"], options=nsq_data_option, username=nsq_username, password=nsq_password)

// 检查订阅情况
nsq::getSubscriptionStatus()
select * from getStreamingStat().subWorkers where topic like "%easyNSQ_saveToDfsTable%"

// 停止订阅
closeNsqConnection()
```

#### 关闭 NSQ 连接和清理以上例子运行时创建的流表和分区表

```
// 停止订阅和关闭 nsq 连接
closeNsqConnection()

// 清理流表和分区表
iniNsqEnv()
iniNsqDfs()
iniNsqEnv(["myNsqOrdersSHStream", "myNsqOrdersSZStream", "myNsqTradeSHStream", "myNsqTradeSZStream","myNsqSnapshotSHStream", "myNsqSnapshotSZStream"])
iniNsqDfs("dfs://myNsqOrders", `myNsqOrdersSH`myNsqOrdersSZ)
iniNsqDfs("dfs://myNsqTrade", `myNsqTradeSH`myNsqTradeSZ)
iniNsqDfs("dfs://myNsqSnapshot", `myNsqSnapshotSH`myNsqSnapshotSZ)
```

## 6. 设置节点启动时自动订阅 NSQ 行情数据

由于 DolphinDB 流数据表和流表的订阅只存在于内存中，在节点关闭后，先前创建的 DolphinDB 流数据表及其订阅会消失。所以每次节点启动时，都需要重新创建流数据表和发起订阅。如果每次重新启动后都要求用户进行手动操作，在使用上无疑是不便的。考虑到这一点，DolphinDB 实现了启动时自动执行用户指定脚本的功能。

DolphinDB 系统启动流程如下图所示：

图 6-1 DolphinDB 系统启动流程

![图 6-1 DolphinDB 系统启动流程](images/6.1.png)

* 用户启动脚本（*startup.dos*）

用户启动脚本是通过配置参数 *startup* 后才会执行，单机 single 模式在 *dolphindb.cfg* 中配置，集群模式在 *cluster.cfg* 中配置，可配置绝对路径或相对路径。若配置了相对路径或者没有指定目录，系统会依次搜索本地节点的 *home* 目录、工作目录和可执行文件所在目录。

以 Linux 单节点为例，在 *dolphindb.cfg* 添加如下的配置项：

```
startup=/DolphinDB/server/startup.dos
```

然后在 */DolphinDB/server/* 路径下创建 *startup.dos* 脚本文件即可完成配置。之后每次节点启动时，都会自动执行 */DolphinDB/server/startup.dos* 脚本文件中的代码。

假设用户希望接收上海和深证两个市场的 NSQ 行情数据、持久化存储，并对沪深行情数据做分开存储。用户的 *startup.dos* 应当如下：

```
// 登录数据库
login(`admin, `123456)
go
// 加载插件
try{ loadPlugin("nsq") } catch(ex) { print(ex) }
go
// 调用模块
use DolphinDBModules::easyNSQ
go

configFilePath = "<your_path_to>/nsq_sdk_config.ini";

// 初始化环境(不删除分区表)
iniNsqEnv()

// 拉起订阅
subscribeNsq(configFilePath, "orders", ["sh","sz"], saveToDfs=true)
subscribeNsq(configFilePath, "trade", ["sh","sz"], saveToDfs=true)
subscribeNsq(configFilePath, "snapshot", ["sh","sz"], saveToDfs=true)
```

## 7. 行情数据表结构

目前 NSQ 插件对上海和深圳市场的行情数据表结构做了统一处理，具体表结构如下：

### 7.1 逐笔委托（orders）

| name | type |
| --- | --- |
| ExchangeID | SYMBOL |
| InstrumentID | SYMBOL |
| TransFlag | INT |
| SeqNo | LONG |
| ChannelNo | INT |
| TradeDate | DATE |
| TransactTime | TIME |
| OrdPrice | DOUBLE |
| OrdVolume | LONG |
| OrdSide | CHAR |
| OrdType | CHAR |
| OrdNo | LONG |
| BizIndex | LONG |

* 开启 **receivedTime** 订阅选项，会在行情表中增加时间戳字段，表示插件接收消息的时刻。

| name | type |
| --- | --- |
| receivedTime | NANOTIMESTAMP |

### 7.2 逐笔成交（trade）

* 默认模式

| name | type |
| --- | --- |
| ExchangeID | SYMBOL |
| InstrumentID | SYMBOL |
| TransFlag | INT |
| SeqNo | LONG |
| ChannelNo | INT |
| TradeDate | DATE |
| TransactTime | TIME |
| TrdPrice | DOUBLE |
| TrdVolume | LONG |
| TrdMoney | DOUBLE |
| TrdBuyNo | LONG |
| TrdSellNo | LONG |
| TrdBSFlag | CHAR |
| BizIndex | LONG |

* 开启 **receivedTime** 订阅选项，会在行情表中增加时间戳字段，表示插件接收消息的时刻。

| name | type |
| --- | --- |
| receivedTime | NANOTIMESTAMP |

### 7.3 L2 快照（snapshot）

* 默认模式

| name | type | name | type | name | type |
| --- | --- | --- | --- | --- | --- |
| ExchangeID | SYMBOL | BidVolume0-9 | LONG | EtfSellBalance | DOUBLE |
| InstrumentID | SYMBOL | AskVolume0-9 | LONG | TotalWarrantExecVolume | LONG |
| LastPrice | DOUBLE | TradesNum | LONG | WarrantLowerPrice | DOUBLE |
| PreClosePrice | DOUBLE | InstrumentTradeStatus | CHAR | WarrantUpperPrice | DOUBLE |
| OpenPrice | DOUBLE | TotalBidVolume | LONG | CancelBuyNum | INT |
| HighPrice | DOUBLE | TotalAskVolume | LONG | CancelSellNum | INT |
| LowPrice | DOUBLE | MaBidPrice | DOUBLE | CancelBuyVolume | LONG |
| ClosePrice | DOUBLE | MaAskPrice | DOUBLE | CancelSellVolume | LONG |
| UpperLimitPrice | DOUBLE | MaBondBidPrice | DOUBLE | CancelBuyValue | DOUBLE |
| LowerLimitPrice | DOUBLE | MaBondAskPrice | DOUBLE | CancelSellValue | DOUBLE |
| TradeDate | DATE | YieldToMaturity | DOUBLE | TotalBuyNum | INT |
| UpdateTime | TIME | IOPV | DOUBLE | TotalSellNum | INT |
| TradeVolume | LONG | EtfBuycount | INT | DurationAfterBuy | INT |
| TradeBalance | DOUBLE | EtfSellCount | INT | DurationAfterSell | INT |
| AveragePrice | DOUBLE | EtfBuyVolume | LONG | BidOrdersNum | INT |
| BidPrice0-9 | DOUBLE | EtfBuyBalance | DOUBLE | AskOrdersNum | INT |
| AskPrice0-9 | DOUBLE | EtfSellVolume | LONG | PreIOPV | DOUBLE |

* 开启 **getAllFieldNames** 订阅选项，会在行情表中增加最优报价的50档委托等信息，如下所示。

| name | type |
| --- | --- |
| Bid1Count | INT |
| MaxBid1Count | INT |
| Ask1Count | INT |
| MaxAsk1Count | INT |
| Bid1Qty0-49 | LONG |
| Ask1Qty0-49 | LONG |

* 开启 **receivedTime** 订阅选项，会在行情表中增加时间戳字段，表示插件接收消息的时刻。

| name | type |
| --- | --- |
| receivedTime | NANOTIMESTAMP |

## 8. 附件

模块文件： [easyNSQ.dos](script/easyNSQ.dos)

startup脚本： [startup.dos](script/startup.dos)

使用示例：[example.txt](script/example.txt)

