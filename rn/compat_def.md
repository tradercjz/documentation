# 版本兼容性说明

## DolphinDB 版本兼容性等级标准

本节对 DolphinDB 版本兼容性等级标准进行了定义和说明，用户可以参考各兼容性等级的要求，快速了解版本升级的潜在风险。为满足升级安全，DolphinDB 数据库服务器的最新版和稳定版升级至少满足向后兼容的要求。

注： 为了便于用户了解 DolphinDB
版本升级的兼容性情况，降低版本升级可能带来的业务中断、数据丢失等风险，DolphinDB 针对服务器、SDK 和插件等制定了版本兼容性等级标准。自1.30.17 和 2.00.5
版本起，DolphinDB 将在 release notes 中注明新发布版本的兼容性等级。如有不兼容之处，将在版本说明中详细说明并提供相应的解决方案。

* **向后兼容**（Backward Compatibility）：指新版本的软件可以兼容旧版本的软件，包括配置、数据和程序行为，即向过去兼容。
* **向前兼容**（Forward Compatibility）：指旧版本的软件可以兼容新版本的软件，包括配置、数据和程序行为，即向未来兼容。
* **版本回退**：指软件升级到新版本后，发现新版本运行有风险，又回退到升级前的版本。根据升级后数据库文件是否更新，又可以细分为三种情况：

  + **无条件回退**。新版本没有更新数据文件、日志文件和元数据的格式，无论升级后是否已经写入了数据，总是可以回退到旧版本。
  + **备份元数据后的回退**。数据文件格式没有发生变化，但元数据文件格式发生了变化。升级后重启的过程中，系统会对 edit log 做一次 checkpoint，生成新的元数据，但是回退到旧版本后，新格式的元数据文件将无法被读取。对此，我们可以通过在升级前备份元数据来解决这一问题。
  + **安全关机后的回退**。数据文件格式发生了变化。即使重启后用户没有主动写入数据，也有可能因为重放日志导致被动写入数据到数据库文件。这样回退到旧版本后无法读取数据。为解决这个问题，DolphinDB 从 1.30.17 和 2.00.5 版本开始支持安全关机，来确保关闭节点前 redo log 中的数据全部写入数据库文件。
* **滚动升级**：以传统方式升级集群版本，通常先把全部节点关闭，然后一次性把整个集群全部节点的版本升级为新版本。但是按照该方式升级时，业务会被中断。滚动升级是指可以逐一按节点进行版本升级，在单个节点升级为新版本，并确保其稳定运行后，再升级集群内的另一个节点，以此类推，直至整个集群内的所有节点完成升级。

  + 支持滚动升级，意味着内存中的数据格式，包括传输协议，序列化协议等需要完全兼容。
  + 滚动升级过程中，系统一直保持在线，除了新的版本要符合很高的兼容性标准外，集群部署方式必须是高可用的，即控制节点采用高可用部署，数据副本数至少为2，客户端采用高可用写入。
* **插件和 SDK 的兼容性**：插件和SDK的兼容性包括二进制兼容和代码的兼容。

  + 对于插件而言，二进制兼容指的是旧版的插件（动态库）可以在新版的数据库服务器上加载并运行。代码兼容性指原有的脚本可以不做任何修改在新版本的插件上运行。一个插件如果满足二进制兼容性，就可以在升级数据库服务器时选择不升级插件。
  + 对于 SDK（Python，C++，Java，C# 等）而言，二进制兼容性指旧版本的 SDK（通常为动态库的形式）兼容新版本的服务器。代码兼容性指 SDK 的接口兼容已有的客户端代码，客户端代码无需修改即可与新的 SDK 一起编译和链接。

## 兼容性要素

为了用户直观了解各版本所满足的兼容性标准，DolphinDB 将兼容性需求划分为了五个等级。每一等级的标准均向下兼容较低等级的标准。等级越高，兼容性要求越严格。

表 1. 各兼容性等级需要满足的兼容性要素

| 等级 | 配置 | 函数/脚本 | 存储数据 | 插件 | SDK | **滚动升级** | **版本回退** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **一级** | 兼容 | 可能删除声明 deprecation 超过一年的内置函数 | 向后兼容 | 代码可能不兼容 | 代码兼容 | 可能不支持 | 安全关机后回退 |
| **二级** | 兼容 | 兼容 | 向后兼容 | 代码兼容 | 代码兼容 | 可能不支持 | 安全关机后回退 |
| **三级** | 兼容 | 兼容 | 向前兼容 | 无需更新 | 无需更新 | 可能不支持 | 备份元数据后回退 |
| **四级** | 兼容 | 兼容 | 向前兼容 | 无需更新 | 无需更新 | 支持 | 备份元数据后回退 |
| **五级** | 兼容 | 兼容 | 向前兼容 | 无需更新 | 无需更新 | 支持 | 无条件回退 |

有关兼容性各个等级详细定义与标准，见以下各节。

