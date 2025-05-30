# 四级兼容性标准

四级兼容性标准在三级兼容性标准的基础上，要求新版本能够有条件回退到旧版本，并支持滚动升级，即 DolphinDB 集群可以逐一按节点进行升级，一个节点更新版本并稳定运行后，再升级集群内另一个节点。在升级过程中，如果出现异常，也可快速回退到旧版本，大幅降低升级风险。

支持滚动升级，内存中的数据格式、传输协议等需要完全兼容。

**具体要求包括：**

1. 兼容旧版本的配置；
2. 兼容旧版本的函数和脚本；
3. 兼容旧版本的存储数据，包括分布式表数据，持久化的流数据表数据，定时任务，函数视图和用户权限数据等；
4. 插件和 SDK 满足二进制兼容性，即插件和 SDK 不需要升级也能继续运行；
5. 支持有条件回退。若新版本的存储数据未写入，版本能回退到旧版本继续运行。
6. 兼容旧版本的内存数据，包括内存表的数据，矩阵、向量等变量的数据，以及传输协议等，确保集群的各节点能滚动升级。

Copyright

**©2025 浙江智臾科技有限公司 浙ICP备18048711号-3**
