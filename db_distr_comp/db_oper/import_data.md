# 数据迁移方法

从外部数据源向向 DolphinDB 迁移时，可采取如下方法：

* 通过文本文件导入
* 通过 HDF5 插件导入
* 通过 ODBC 插件导入
* 通过 MySQL 插件导入

其中，HDF5, ODBC 与 MySQL 插件均可从 DolphinDB 官网下载。以下简介这四种导入方法：

## 文本文件

通过文本文件进行数据中转是较为通用的一种数据迁移方式。DolphinDB 提供了以下三个函数来加载文本文件：

* [loadText](../../funcs/l/loadText.md)：把文本文件加载到内存中
* [ploadText](../../funcs/p/ploadText.md)：以并行的方式把文本文件加载到内存中，它的速度比 `loadText` 要快
* [loadTextEx](../../funcs/l/loadTextEx.md)：把文本文件导入到 DolphinDB 数据库中

**导入内存**

使用 `loadText` 或
`ploadText`
函数时，需要先把数据加载到内存，然后再落盘到数据库。如果文本文件过大，可能会出现内存不足。因此这两个函数不能用于导入大于本地机器内存的文本文件。

若要把数据导入到数据库中，`loadText` 和
`ploadText` 需要与 `append!` 和
`tableInsert`
函数一起使用。

```
t = ploadText("/stockData/trades.csv")
db=database("dfs://stock",VALUE,2019.08.01..2019.08.10)
pt=db.createPartitionedTable(t,`pt,`timestamp)
pt.append!(t)
```

在下例中，原始数据是 2018 年 5 月至今的股票报价数据，每天一个
CSV 文件，保存在文件夹 */stockData* 下。按照下面的步骤，创建一个数据库并把数据导入。

创建组合分区类型(COMPO)的分布式数据库 *dfs://stockDB*
，根据日期进行值分区，根据股票代码进行范围分区。由于后续的数据都会导入到数据库，所以在创建数据库时我们扩大了日期的分区方案。

```
t = ploadText("/stockData/TAQ20180501.csv")
tmp = select count(*) as count from t group by sym order by sym;
buckets = cutPoints(tmp.sym, 128, tmp.count)

dateDomain = database("", VALUE, 2018.05.01..2030.07.01)
symDomain = database("", RANGE, buckets)
stockDB = database("dfs://stockDB", COMPO, [dateDomain, symDomain])
stockDB.createPartitionedTable(t, "quotes", `date`sym)
```

**导入数据库**

`loadTextEx`
可以避免文本文件过大时可能出现内存不足的问题。该函数将文本文件分为许多批次逐步载入内存并落盘到数据库，因可以导入超出本地机器内存的文本文件。

例如：

* 直接使用：

  ```
  db=database("dfs://stock",VALUE,2019.08.01..2019.08.10)
  loadTextEx(db,`pt,`timestamp,"/stockData/trades.csv")
  ```
* 利用 `loadTextEx` 函数，编写用户自定义函数 loadCsv
  把文件文件加载到数据库：

  ```
  def loadCsv(){
     fileDir='/stockData'
     filenames = exec filename from files(fileDir)
     db = database("dfs://stockDB")
     for(fname in filenames){
         jobId = fname.strReplace(".csv", "")
         submitJob(jobId, , loadTextEx{db, "quotes", `date`sym, fileDir+'/'+fname})
     }
  }
  loadCsv()
  ```

## HDF5 插件

HDF5 是一种在数据分析领域广泛使用的二进制数据文件格式。用户可通过 DolphinDB HDF5 插件提供的以下方法导入
HDF5 格式数据文件：

* hdf5::ls：列出HDF5文件中所有 group 和 dataset 对象
* hdf5::lsTable：列出HDF5文件中所有 dataset 对象
* hdf5::HDF5DS：返回HDF5文件中 dataset 的元数据
* hdf5::loadHDF5：将HDF5文件导入内存表
* hdf5::loadHDF5Ex：将HDF5文件导入分区表
* hdf5::extractHDF5Schema：从HDF5文件中提取表结构

用法如下：

下载HDF5 插件，再将插件部署到 */server/plugins* 目录下。使用以下脚本加载插件：

```
loadPlugin("plugins/hdf5/PluginHdf5.txt")
```

调用插件方法时需要在方法前面提供namespace，比如调用loadHdf5可以使用hdf5::loadHDF5。另一种写法是：

```
use hdf5
loadHdf5(filePath,tableName)
```

若要导入包含一个Dataset candle\_201801的文件candle\_201801.h5，可使用以下脚本：

```
dataFilePath = "/home/data/candle_201801.h5"
datasetName = "candle_201801"
tmpTB = hdf5::loadHDF5(dataFilePath,datasetName)
```

如果需要指定数据类型导入可以使用hdf5::extractHDF5Schema，脚本如下：

```
dataFilePath = "/home/data/candle_201801.h5"
datasetName = "candle_201801"
schema=hdf5::extractHDF5Schema(dataFilePath,datasetName)
update schema set type=`LONG where name=`volume
tt=hdf5::loadHDF5(dataFilePath,datasetName,schema)
```

如果HDF5文件超过服务器内存，可以使用hdf5::loadHDF5Ex载入数据。

```
dataFilePath = "/home/data/candle_201801.h5"
datasetName = "candle_201801"
dfsPath = "dfs://dataImportHDF5DB"
db=database(dfsPath,VALUE,2018.01.01..2018.01.31)
hdf5::loadHDF5Ex(db, "cycle", "tradingDay", dataFilePath,datasetName)
```

更多关于 HDF5 插件的内容，参考：[HDF5 插件](../../plugins/hdf5/hdf5.md)。

## ODBC 插件

用户可通过 ODBC 插件提供的接口连接第三方数据库后迁移数据至 DolphinDB。

ODBC 插件提供了以下四个方法用于操作第三方数据源数据：

* odbc::connect：创建连接。
* odbc::close： 关闭连接。
* odbc::query：根据给定的SQL语句查询数据并将结果返回到DolphinDB的内存表。
* odbc::execute：在第三方数据库内执行给定的SQL语句，不返回结果。

在使用ODBC 插件之前，需要安装ODBC驱动程序。

下面的例子使用ODBC 插件连接以下SQL Server：

* IP地址：172.18.0.15
* 连接用户名：sa
* 密码：123456
* 数据库名称： SZ\_TAQ

下载插件解压并拷贝 plugins/odbc 目录下所有文件到 DolphinDB server/plugins/odbc
目录下，通过下面的脚本完成插件初始化：

```
loadPlugin("plugins/odbc/odbc.cfg")
conn=odbc::connect("Driver=ODBC Driver 17 for SQL Server;Server=172.18.0.15;Database=SZ_TAQ;Uid=sa;Pwd=123456;")
```

创建 DolphinDB 分布式数据库dfs://dataImportODBC。使用SQL
Server中的数据表结构作为DolphinDB数据表的模板，在dfs://dataImportODBC中创建数据库cycle。

```
tb = odbc::query(conn,"select top 1 * from candle_201801")
db=database("dfs://dataImportODBC",VALUE,2018.01.01..2018.01.31)
db.createPartitionedTable(tb, "cycle", "tradingDay")
```

从SQL Server中导入数据并保存入cycle表中：

```
tb = database("dfs://dataImportODBC").loadTable("cycle")
data = odbc::query(conn,"select * from candle_201801")
tb.append!(data);
```

更多关于 ODBC 插件的内容，参考：[ODBC 插件](../../plugins/odbc/odbc.md)。

## MySQL 插件

MySQL 插件导入数据的速度比ODBC接口要快，并且不需要配置数据源，使用更加便捷。

MySQL插件提供了以下接口函数：

* mysql::connect：创建连接
* mysql::showTables：列出MySQL数据库中的所有表
* mysql::extractSchema：获取MySQL数据表的结构
* mysql::load：把MySQL数据加载到DolphinDB的内存表
* mysql::loadEx：把MySQL中的数据加载到DolphinDB的分区表

下载插件解压并拷贝 plugins\mysql 目录下所有文件到DolphinDB server的 plugins/mysql
目录下，通过下面的脚本完成插件初始化：

```
loadPlugin("plugins/PluginMySQL.txt")
```

连接本地MySQL服务器中的employees数据库：

```
conn=connect("127.0.0.1",3306,"root","123456","employees")
```

确定分区类型和分区方案，创建数据库，用于保存MySQL数据：

```
db=database("dfs://mysql",VALUE,`F`M)
```

导入数据：

```
pt=loadEx(conn,db,"pt","gender","employees")
```

更多关于 MySQL 插件的内容，参考：[MySQL
插件](../../plugins/mysql/mysql.md)。

