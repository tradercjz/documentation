# 数据导入方法

DolphinDB 针对各种类型的数据文件和数据源提供了便捷的导入导出工具，利用这些工具，可以完成即时或定时的数据加载、清洗和导入导出任务。

## 内置函数

DolphinDB 提供了多种内置函数进行文本文件、二进制、JSON
文件的数据导入与导出。在数据导入的过程中，用户通过对相关的参数进行设置，可进行数据类型匹配等预处理。

### 文本文件导入

| **函数** | **说明** |
| --- | --- |
| `loadText` | 将文本文件导入为内存表。 |
| `ploadText` | 将文本文件并行导入为分区内存表，与 `loadText` 函数相比速度更快。`ploadText` 充分利用了多核 CPU 来并行载入文件，可快速载入 16MB 或以上的较大文件。 |
| `loadTextEx` | 将文本文件导入数据库中，包括分布式数据库或内存数据库。该函数将文本文件分为许多批次逐步载入内存并落盘到数据库，避免文本文件过大时可能出现内存不足的问题。支持通过传入自定义函数，在入库前对数据进行预处理。 |
| `textChunkDS` | 将文本文件划分为多个小数据源，并将划分后的数据通过分布式计算框架下的 map-reduce 函数导入数据库。 |

### 二进制、JSON 文件导入

| **导入类型** | **函数** | **说明** |
| --- | --- | --- |
| 二进制文件 | `readRecord!` | 将二进制文件转换为 DolphinDB 数据对象。 |
| `loadRecord` | 将二进制文件转换为 DolphinDB 数据对象，并支持处理字符串类型的数据。 |
| JSON 文件 | `fromJson`, `fromStdJson` | 将 JSON 格式的字符串转换为 DolphinDB 对象。 |

### 数据导出

| **导出类型** | **函数** | **说明** |
| --- | --- | --- |
| 文本文件 | `saveText` | 可以将任意变量或表对象保存为文本文件。 |
| `saveTextFile` | 通过追加或覆盖将字符串保存到文本文件中。 |
| 二进制文件 | `writeRecord` | 将 DolphinDB 对象（例如表或元组）转换为二进制文件并返回向文件写入的行数。 |
| `saveAsNpy` | 将 DolphinDB 向量或矩阵保存为 NumPy 支持的 *.npy* 二进制文件。 |
| JSON 文件 | `toJson`, `toStdJson` | 将 DolphinDB 对象转换为 JSON 字符串。 |

## 插件及工具

DolphinDB 还提供了一系列用于数据导入/迁移的插件。

### 数据库插件

使用数据库迁移插件的主要优点在于可以直接调用现成的接口，脚本简单易上手。DolphinDB 提供了一系列专门针对第三方数据库的数据迁移插件，如对
MySQL，kdb+，MongoDB 有专门的插件， SQL Server，Oracle，ClickHouse，SQLite 等可通过 ODBC
插件进行连接和导入。

| **插件名** | **功能描述** |
| --- | --- |
| odbc | 通过 ODBC 读取其他数据源的数据，包括来自 MySQL, Oracle, SQL Server 等大多数数据库的数据 |
| mysql | 连接 MySQL 并读取数据 |
| HBase | 通过 Thrift 连接 HBase，读取数据 |
| kdb | 通过连接 kdb+ 数据库或直接读取磁盘上的 kdb+ 数据文件以导入数据 |
| mongodb | 连接 MongoDB，读取数据 |

### 数据文件读取插件

通过插件从数据文件中导入数据的优点在于操作简单、稳定，适合大量数据迁移。

| **插件名** | **功能描述** |
| --- | --- |
| Arrow | 序列化支持 Apache Arrow 格式 |
| aws | 读取和写入 AWS S3 的网络文件 |
| feather | 读取、写入 Apache Feather 文件 |
| hdfs | 读取和写入 Hadoop 的 HDFS 文件 |
| hdf5 | 读取和写入 HDF5 文件 |
| mat | 读取、写入 MATLAB 文件 |
| mseed | 读取和写入 miniSEED 文件 |
| orc | 读取、写入 ORC 文件 |
| parquet | 读取和写入 Apache Parquet 文件 |
| zip | 解压 ZIP 文件 |
| zlib | 压缩、解压 gz 文件 |

### 消息中间件、行情插件

通过对接消息中间件及行情服务的插件，可以将实时数据写入 DolphinDB。

| **插件** | **类别** | **功能描述** |
| --- | --- | --- |
| zmq | 消息发布和订阅 | 发送、接收 ZeroMQ 消息 |
| mqtt | 发布和订阅 MQTT 消息 |
| kafka | 发布或订阅 Kafka 流服务 |
| insight | 行情接收 | 接收华泰 Insight 实时行情 |
| AmdQuote | 接收华锐 Amd 实时行情数据 |
| nsq | 读取恒生 NSQ 实时行情数据 |

### 其他导入工具

DolphinDB 也提供了基于离线数据同步工具 DataX 的 dolphindbwriter 插件，可满足从不同数据源向 DolphinDB
导入数据、同步增量数据的功能，具有可拓展、通用性强的优势。

此外，用户也可通过 DolphinDB C++ API，Python API，Java API 等 API 所提供的接口导入数据，详情请见相关 API
文档。

