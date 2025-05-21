# 错误代码

DolphinDB 数据库错误代码列表用于解释 DolphinDB Server（以下简称 Server）的不同类型错误。每个错误代码对应特定的系统状态或不当操作。

错误代码由三部分构成：`S + <与模块相关的错误类别码> + <类别内编码>`

以 S00004 为例：

* S：Server
* 00：错误类别，此处指系统错误类别，见下表第一行
* 004：错误类别下的 004 错误

表 1. 错误代码类别

| 模块 | 错误类别 | 说明 |
| --- | --- | --- |
| 系统 | 00 | 网络错误、磁盘错误、文件操作错误、内存错误等通用系统错误 |
| 存储 | 01 | DFS、OLAP、TSDB、事务、Raft 基础模块、Recovery、Redo log、cacheEngine、backup/restore、异步复制等相关错误 |
| SQL | 02 | SQL 相关错误 |
| 流数据 | 03 | 流计算、流计算引擎、流数据引擎解释器相关错误 |
| 管理 | 04 | 与数据库管理操作、权限管理、函数视图、集群管理相关错误 |
| 通用 | 05 | 难以归类的错误。例如：与基础数据结构相关的错误 |
| DolphinDB 解释器 | 06 | 语法错误和语法解析相关错误 |

部分报错信息中包含类似 "with error 13" 的信息。这里的 13 是 DolphinDB 的报错码。下表列举了 DolphinDB
报错码对应的报错信息：

表 2. DolphinDB 报错码

| 报错码 | 说明 |
| --- | --- |
| 1 | Socket is disconnected/closed or file is closed. |
| 2 | In non-blocking socket mode, there is no data ready for retrieval yet. |
| 3 | Out of memory, no disk space, or no buffer for sending data in non-blocking socket mode. |
| 4 | String size exceeds 64K or code size exceeds 1 MB during serialization over network. |
| 5 | In non-blocking socket mode, a program is in pending connection mode. |
| 6 | Invalid message format. |
| 7 | Reach the end of a file or a buffer. |
| 8 | File is readable but not writable. |
| 9 | File is writable but not readable. |
| 10 | A file doesn't exist or the socket destination is not reachable. |
| 11 | The database file is corrupted. |
| 12 | Not the leader node of the RAFT protocol. |
| 13 | Unknown IO error. |

Copyright

**©2025 浙江智臾科技有限公司 浙ICP备18048711号-3**
