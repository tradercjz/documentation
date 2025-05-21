# EFH

盛立极速行情系统（EFH）是以FPGA硬件技术处理交易所原始行情及行情发布的低延迟系统。为对接盛立 EFH 行情服务软件，DolphinDB 开发了 EFH 插件。通过插件可以将上交所和深交所的 Level-2 实时行情接入 DolphinDB。

## 安装插件

### 版本要求

* DolphinDB Server: 2.00.10 及更高版本，支持 Linux x86-64。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请自行选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("EFH")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("EFH")
   ```

## 接口说明

### createHandle

**语法**

```
EFH::createHandle(filePath, name, [option])
```

**详情**

创建 EFH 句柄。

返回一个 EFH 句柄，用于订阅、取消订阅、连接和关闭。EFH 连接句柄不能重名。

**参数**

**filePath** STRING 类型标量，表示 EFH 行情配置文件路径。

**警告**：如果使用 efvi 模式，且配置的网卡不适配，在 `connect` 时可能会导致盛立的 SDK crash，在使用前务必确保配置文件中的网卡信息正确。

**name** STRING 类型标量，指定给该 EFH 句柄的名称。

**option** 一个字典, 类型为 (STRING, BOOL)，可选参数。其键支持 "outputRecvTime"，"outputElapsed"。其中：

* "outputRecvTime" 表示是否获取插件收到行情数据的时间戳。其指定为 dict (["outputRecvTime"], [true]) 时，`getSchema`获取的表结构中将包含插件收到行情数据的时间戳列。
* "outputElapsed" 表示是否获取 EFH 插件 接收数据处理的时延。其指定为 dict (["outputElapsed"], [true]) 时，`getSchema`获取的表结构中将包含插件收到行情数据的时延列时延的定义："EFH 回调函数返回数据" 到 "准备写入到共享流表前" 这段时间。

### getSchema

**语法**

```
EFH::getSchema(handle, market, dataType)
```

**详情**

获取行情数据的表结构。

返回一个表，包含三列：name，typeString 和 typeInt，分别表示该行情表各个字段的名称，类型名和类型枚举值。可以通过该表来创建具有相同结构的共享流表。

如果在 `createHandle`中指定了 *option*，在返回的 schema 中会增加对应的列：

* 如果指定了 *outputRecvTime* 为 true，则会增加一个 NANOTIMESTAMP 类型列 receivedTime。
* 如果指定了 *outputElapsed* 为 true，则会增加一个 LONG 类型列 perPenetrationTime。

**参数**

**handle** `createHandle` 返回的连接句柄。

**market** STRING 类型标量，需要订阅的的市场名称，可以为 "EFH\_SSE\_LEV2" 表示上交所，"EFH\_SZE\_LEV2" 表示深交所。

**dataType** STRING 类型标量，表示行情数据类型：

* 深交所可取以下值："afterClose"，"snapshot"，"order"，"execution"，"index"，"tree"，"ibrTree"，"turnover"，"bondSnapshot"，"bondOrder"，"bondExecution"。
* 上交所可取以下值："snapshot"，"order"，"execution"，"index"，"tree"，"option"，"bondSnapshot"，"bondTick"，"mergeTick"。

### subscribe

**语法**

```
EFH::subscribe(handle, outputTable, market, dataType)
```

**详情**

订阅具体的行情数据。

**注意：** EFH 插件是在连接建立前进行订阅，连接建立后无法进行订阅。

**参数**

**handle** `createHandle` 返回的连接句柄。

**outputTable** 一个共享流表，作为行情数据输出的目标表。流表的结构必须与 `getSchema` 返回的结构相同。

**market** STRING 类型标量，需要订阅的的市场名称，可以为 "EFH\_SSE\_LEV2" 表示上交所，"EFH\_SZE\_LEV2" 表示深交所。

**dataType** STRING 类型标量，表示行情数据类型：

* 深交所可取以下值："afterClose"，"snapshot"，"order"，"execution"，"index"，"tree"，"ibrTree"，"turnover"，"bondSnapshot"，"bondOrder"，"bondExecution"。
* 上交所可取以下值："snapshot"，"order"，"execution"，"index"，"tree"，"option"，"bondSnapshot"，"bondTick"，"mergeTick"。

### unsubscribe

**语法**

```
EFH::unsubscribe(handle, market, dataType)
```

**详情**

取消订阅具体的行情数据。

**参数**

**handle** `createHandle` 返回的连接句柄。

**market** STRING 类型标量，需要订阅的的市场名称，可以为 "EFH\_SSE\_LEV2" 表示上交所，"EFH\_SZE\_LEV2" 表示深交所。

**dataType** STRING 类型标量，表示行情数据类型：

* 深交所可取以下值："afterClose"，"snapshot"，"order"，"execution"，"index"，"tree"，"ibrTree"，"turnover"，"bondSnapshot"，"bondOrder"，"bondExecution"。
* 上交所可取以下值："snapshot"，"order"，"execution"，"index"，"tree"，"option"，"bondSnapshot"，"bondTick"，"mergeTick"。

### connect

**语法**

```
EFH::connect(handle)
```

**详情**

建立与 EFH 行情服务器之间的连接，开始接收行情数据。

**参数**

**handle** `createHandle` 返回的连接句柄。

### close

**语法**

```
EFH::close(handle)
```

**详情**

关闭一个 EFH 连接句柄，在 close 之后还可以通过接口 `getStatus` 查看状态。

**参数**

**handle** `createHandle` 返回的连接句柄

### delete

**语法**

```
EFH::delete(handle)
```

**详情**

删除一个 EFH 连接句柄，在 delete 之后将无法再次连接。

**参数**

**handle** `createHandle` 返回的连接句柄

### getHandle

**语法**

```
EFH::getHandle(name)
```

**详情**

通过句柄名称，获取已经创建的 EFH 句柄。

**参数**

**name** STRING 类型标量，指定给该 EFH 句柄的名称

### getStatus

**语法**

```
EFH::getStatus(handle)
```

**详情**

获取对应 EFH 句柄已订阅数据的状态信息。

返回一个表格，包含各种已订阅数据的状态信息，不包含未订阅过的数据类型

| 列名 | 含义 | 类型 |
| --- | --- | --- |
| **topicType** | 订阅的名称 | STRING |
| **channelNo** | OrderTransaction 分 channel 订阅时的 channel 号 | INT |
| **startTime** | 订阅开始的时间 | NANOTIMESTAMP |
| **endTime** | 订阅结束的时间 | NANOTIMESTAMP |
| **firstMsgTime** | 第一条消息收到的时间 | NANOTIMESTAMP |
| **lastMsgTime** | 最后一条消息收到的时间 | NANOTIMESTAMP |
| **processedMsgCount** | 已经处理的消息数 | LONG |
| **lastErrMsg** | 最后一条错误信息 | STRING |
| **failedMsgCount** | 处理失败的消息数 | LONG |
| **lastFailedTimestamp** | 最后一条错误消息发生的时间 | NANOTIMESTAMP |
| **subscribeInfo** | 该订阅涉及的市场和投资品类型 | STRING |

**参数**

**handle** `createHandle` 返回的连接句柄。

### getHandleStatus

**语法**

```
EFH::getHandleStatus()
```

**详情**

获取本节点所有 EFH 句柄的状态信息。

返回一个表格，包含各个 handle 的信息

| 列名 | 含义 | 类型 |
| --- | --- | --- |
| handleName | 创建 handle 时指定的名称 | STRING |
| configPath | 配置文件的路径 | STRING |
| createTime | 创建 handle 的时间 | DATETIME |
| startTime | 建立连接的时间 | BOOL |
| endTime | 关闭连接的时间 | BOOL |

**参数**

无

## 使用示例

```
// 建立 handle
handle = EFH::createHandle("config.ini", "handle0", dict(["outputRecvTime", "outputElapsed"], [true, true]));

// 订阅上交所的股票快照
schema = EFH::getSchema(handle, `EFH_SSE_LEV2, `snapshot);
snapshot_sh_s = streamTable(10000:0, schema[`name], schema[`typeString]);
share snapshot_sh_s as snapshot_sh_s1;
EFH::subscribe(handle, snapshot_sh_s1, "EFH_SSE_LEV2", "snapshot");

// 获取已有的 handle
handle = EFH::getHandle("handle0");

// 建立连接
EFH::connect(handle)

// 查看订阅状态
EFH::getStatus(handle)

// 查看 handle 状态
EFH::gethandleStatus(handle)

// 关闭连接
EFH::close(handle)

// 取消已有的订阅（非必要）
EFH::unsubscribe(handle, "EFH_SSE_LEV2", "snapshot");

// 移除 handle
EFH::delete(handle)
```

