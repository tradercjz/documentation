# textChunkDS

## 语法

`textChunkDS(filename, chunkSize, [delimiter], [schema], [skipRows=0], [arrayDelimiter], [containHeader],
[arrayMarker])`

## 参数

**filename** 一个字符串，表示文件的绝对路径。仅支持 CSV 格式的文件。若传入其他格式文件，则无法保证数据准确性。

**chunkSize** 1 到 2048 之间的整数，表示文件块的大小，单位是 MB。

**delimiter** 字符串标量，表示数据文件中各列的分隔符。分隔符可以是一个或多个字符，默认是逗号（","）。

**schema** 表对象，用于指定各字段的数据类型。具体请参考 [loadText](../l/loadText.md)
的 *schema* 参数。

**skipRows** 0 到 1024 之间的整数，表示从文件头开始忽略的行数。它是一个可选参数。默认值为 0。

**arrayDelimiter** 数据文件中数组向量列的分隔符。默认是逗号。由于不支持自动识别数组向量，必须同步修改
*schema* 的 type 列修为数组向量类型。

**containHeader** 布尔值，表示数据文件是否包含标题行，默认为空。具体请参考 [loadText](../l/loadText.md) 的 *containHeader* 参数。

**arrayMarker**  包含两个字符的字符串或或 CHAR
类型数据对，两个字符分别表示数组向量左右边界的标识符。默认标识符为双引号（"）。

* 不能包含空格、Tab(`\t`)
  和换行符(`\t`和`\n`)。
* 不能包含数字或字母。
* 如果其中一个为双引号(")，另一个也必须为双引号。
* 如果标识符为 `'`，`"` 或`\`
  ，需视情况添加转义符。例如 `arrayMarker="\"\""`。
* 如果 *delimiter* 是单个字符，则 *arrayMarker* 不能包含与其相同的字符。
* 如果 *delimiter* 是多个字符，则 *arrayMarker* 左边界不能与 *delimiter*的首个字符相同。

## 详情

将文件划分为多个数据源，每个数据源的大小为 *chunkSize*。如果需要将大文本文件加载到 DolphinDB, 可以使用
*textChunkDS* 函数将文本文件划分为多个小文件数据源，再通过 [mr](../m/mr.md) 函数写入到数据库中。与直接把大文本文件加载到数据库对比，这种方法占用的内存更少。

当 DolphinDB
加载数据文件时，会进行随机抽样，并基于样本决定每列的数据类型。这个方法不一定每次都能准确决定各列的数据类型。因此我们建议，在加载数据前，使用 [extractTextSchema](../e/extractTextSchema.md) 函数查看 DolphinDB
识别每列的数据类型。如果 DolphinDB 识别的数据类型不符合预期，可以在 *schema* 的 type 列中指定数据类型。对于日期列或时间列，如果
DolphinDB 识别的数据类型不符合预期，不仅需要在 *schema* 的 type 列指定时间类型，还需要在 format
列中指定数据文件中日期或时间的格式（用字符串表示），如 "MM/dd/yyyy"。如何表示日期和时间格式请参考 [日期和时间的调整及格式](../../progr/data_mani/format_temp_obj.md)。

## 例子

首先，通过以下脚本生成一个大约 3.2G 的文本文件：

```
n=30000000
workDir = "/home/DolphinDB"
if(!exists(workDir)) mkdir(workDir)
trades=table(rand(`IBM`MSFT`GM`C`FB`GOOG`V`F`XOM`AMZN`TSLA`PG`S,n) as sym, 2000.01.01+rand(365,n) as date, 10.0+rand(2.0,n) as price1, 100.0+rand(20.0,n) as price2, 1000.0+rand(200.0,n) as price3, 10000.0+rand(2000.0,n) as price4, 10000.0+rand(3000.0,n) as price5, 10000.0+rand(4000.0,n) as price6, rand(10,n) as qty1, rand(100,n) as qty2, rand(1000,n) as qty3, rand(10000,n) as qty4, rand(10000,n) as qty5, rand(10000,n) as qty6)
trades.saveText(workDir + "/trades.txt");
```

通过 `textChunkDS` 函数和 `mr`
函数将该文件导入到分布式数据库中：

```
db=database("dfs://db1",VALUE, `IBM`MSFT`GM`C`FB`GOOG`V`F`XOM`AMZN`TSLA`PG`S)
pt=db.createPartitionedTable(trades,`pt,`sym)
ds=textChunkDS(workDir + "/trades.txt",500)
mr(ds,append!{pt},,,false)
```

注： 每个小文件数据源可能包含相同分区的数据。DolphinDB 不允许多个线程同时对相同分区进行写入，因此要将
`mr` 函数 *parallel* 参数设置为 false，否则会抛出异常。

