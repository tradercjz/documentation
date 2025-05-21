# loadText

## 语法

`loadText(filename, [delimiter], [schema], [skipRows=0], [arrayDelimiter], [containHeader],
[arrayMarker])`

## 参数

**filename** 字符串，表示数据文件的路径。仅支持 CSV 格式的文件。若传入其他格式文件，则无法保证数据准确性。

**delimiter** 字符串标量，表示数据文件中各列的分隔符。分隔符可以是一个或多个字符，默认是逗号（","）。

**schema** 表对象，用于指定各字段的数据类型。它可以包含以下四列（其中，name 和 type 这两列是必需的）

| 列名 | 含义 |
| --- | --- |
| name | 字符串，表示列名 |
| type | 字符串，表示各列的数据类型。暂不支持 BLOB, COMPLEX, POINT, DURATION 类型。 |
| format | 字符串，表示数据文件中日期或时间列的格式 |
| col | 整型，表示要加载的列的下标。该列的值必须是升序。 |

注： 若 type 为时间类型，则源数据的时间类型格式需要和 DolphinDB 时间类型数据格式一致。若原始数据的时间戳和
DolphinDB 时间类型不兼容，建议导入时先指定为字符串类型，再通过 [temporalParse](../t/temporalParse.md) 函数进行转换。

**skipRows** 0 到 1024 之间的整数，表示从文件头开始忽略的行数。它是一个可选参数。默认值为 0。

**arrayDelimiter** 数据文件中数组向量列的分隔符。默认是逗号。由于不支持自动识别数组向量，必须同步修改
*schema* 的 type 列修为数组向量类型。

**containHeader**
布尔值，表示数据文件是否包含标题行，默认为空。若不设置，则系统将会分析第一行数据并确定其是否为标题行。不同设置下，列名解析规则见详情描述。

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

将数据文件加载到 DolphinDB 的内存表中。`loadText`
使用单个线程加载数据，如果需要使用多个线程并行加载数据，请使用 [ploadText](../p/ploadText.md)
函数。

* 解析列名：

  + 不指定 *containHeader*
    时，导入文本文件时将以字符串格式读取第一行数据，并根据该数据解析列名。但需要注意，系统内部对第一行数据设置了读取上限，即不能超过
    256
    KB。解析时，如果文件中第一行的内容不包含以数字开头的数据，那么加载文件时系统会将第一行作为列名。如果文件第一行记录中某列记录以数字开头，那么加载文件时系统可能会使用col0,
    col1, ...等作为列名。
  + 指定 *containHeader* = true
    时，则系统将第一行数据视为标题行，并解析出列名。
  + 指定 *containHeader* = false 时，则系统将添加列名 col0,
    col1, ... 。
* 解析类型：

  + 当 DolphinDB
    加载数据文件时，会进行随机抽样，并基于样本决定每列的数据类型。这个方法不一定每次都能准确决定各列的数据类型。因此我们建议，在加载数据前，使用
    [extractTextSchema](../e/extractTextSchema.md) 函数查看 DolphinDB 识别每列的数据类型。
  + 当加载的数据文件中包含了表达时间、日期的数据时，满足分隔符要求的这部分数据（日期数据分隔符包含"-"、"/"和"."，时间数据分隔符为":"）会解析为相应的类型。例如，"12:34:56"解析为SECOND类型；"23.04.10"解析为DATE类型。对于不包含分隔符的数据，形如"yyMMdd"的数据同时满足0<=yy<=99，0<=MM<=12，1<=dd<=31，会被优先解析成DATE；形如"yyyyMMdd"的数据同时满足1900<=yyyy<=2100，0<=MM<=12，1<=dd<=31会被优先解析成DATE。
  + 如果 DolphinDB 识别的数据类型不符合预期，可以在 schema 的 type 列中指定数据类型。对于日期列或时间列，如果
    DolphinDB 识别的数据类型不符合预期，不仅需要在 schema 的 type 列指定时间类型，还需要在 format
    列中指定数据文件中日期或时间的格式（用字符串表示），如 "MM/dd/yyyy"。如何表示日期和时间格式请参考 [ParsingandFormatofTemporalVariables](../../progr/data_mani/format_temp_obj.md)。

如果只需加载数据文件中的部分列，需要在 schema 的 col 列中指定要加载的列的下标。

由于 DolphinDB 的字符串采用 UTF-8 编码，加载的文件必须是 UTF-8 编码。

由于 DolphinDB 中列名仅可使用中文或英文字母、数字或下划线
(\_)，且必须以中文或英文字母开头，若数据文件中的列名不符合要求，系统会依据以下规则自动调整列名：

* 若数据中列名存在中文或英文字母、数字或下划线之外的字符，将其转换为下划线。
* 若数据中列名第一个字符不是中文或英文字母，添加 "c" 作为该列名首字符。

以下是数据文件中不合规列名以及自动转换的列名的例子：

| 数据文件中列名 | 自动转换的列名 |
| --- | --- |
| 1\_test | c1\_test |
| test-a! | test\_a\_ |
| [test] | c\_test\_ |

注： 从 2.00.10
版本开始，`loadText` 支持加载一条记录中包含多个换行符的数据文件。

## 例子

首先，使用以下脚本生成模拟的数据文件：

```
n=10
sym=rand(`AAPL`ORCL`MS`SUN,n)
permno=take(10001,n)
date=rand(2019.06.01..2019.06.10,n)
open=rand(100.0,n)
high=rand(200.0,n)
close=rand(200.0,n)
pre_close=rand(200.0,n)
change=rand(100.0,n)
vol=rand(10000,n)
amount=rand(100000.0,n)
t=table(sym,permno,date,open,high,close,pre_close,change,vol,amount)
saveText(t,"/home/DolphinDB/Data/stock.csv");
```

## 例 1. 直接加载数据文件

```
tt=loadText("/home/DolphinDB/Data/stock.csv");
// output
tt;
```

| sym | permno | date | open | high | close | pre\_close | change | vol | amount |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MS | 10001 | 2019.06.06 | 90.346594 | 80.530542 | 96.474428 | 146.305659 | 0.720236 | 1045 | 90494.568297 |
| AAPL | 10001 | 2019.06.07 | 91.165315 | 8.482074 | 85.514922 | 16.259077 | 76.797829 | 7646 | 91623.485996 |
| AAPL | 10001 | 2019.06.03 | 45.361885 | 14.077451 | 149.848419 | 89.110375 | 45.499145 | 9555 | 98171.601654 |
| MS | 10001 | 2019.06.04 | 8.98688 | 0.591778 | 155.54643 | 132.423187 | 69.95799 | 1202 | 3512.927634 |
| MS | 10001 | 2019.06.07 | 62.866173 | 33.465237 | 174.20712 | 102.695818 | 74.580523 | 3524 | 61943.64517 |
| MS | 10001 | 2019.06.09 | 32.819915 | 13.319577 | 136.729618 | 63.980405 | 60.66375 | 7078 | 85138.216568 |
| MS | 10001 | 2019.06.07 | 90.210866 | 22.728777 | 150.212291 | 59.454705 | 73.916303 | 5306 | 19883.845607 |
| AAPL | 10001 | 2019.06.06 | 83.752686 | 71.3501 | 98.211979 | 145.60098 | 94.428343 | 8852 | 9236.020781 |
| ORCL | 10001 | 2019.06.01 | 81.64719 | 129.702202 | 182.784373 | 117.575967 | 74.84595 | 2942 | 43394.871242 |
| AAPL | 10001 | 2019.06.02 | 10.068382 | 80.875383 | 181.674585 | 138.783821 | 25.298267 | 1088 | 82981.043775 |

```
schema(tt).colDefs;
```

| name | typeString | typeInt | comment |
| --- | --- | --- | --- |
| sym | SYMBOL | 17 |  |
| permno | INT | 4 |  |
| date | DATE | 6 |  |
| open | DOUBLE | 16 |  |
| high | DOUBLE | 16 |  |
| close | DOUBLE | 16 |  |
| pre\_close | DOUBLE | 16 |  |
| change | DOUBLE | 16 |  |
| vol | INT | 4 |  |
| amount | DOUBLE | 16 |  |

## 例 2. 指定某列的数据类型来加载数据文件

例如，我们想要把 permno 列的数据类型转换成 SYMBOL，可以用 [extractTextSchema](../e/extractTextSchema.md)
函数获取输入文件的结构，在导入数据前修改该列的数据类型，并指定 `loadText` 函数的 *schema* 参数。

```
schema=extractTextSchema("/home/DolphinDB/Data/stock.csv");
update schema set type=`SYMBOL where name=`permno;
tt=loadText("/home/DolphinDB/Data/stock.csv",,schema);
schema(tt).colDefs;
```

| name | typeString | typeInt | comment |
| --- | --- | --- | --- |
| sym | SYMBOL | 17 |  |
| permno | SYMBOL | 17 |  |
| date | DATE | 6 |  |
| open | DOUBLE | 16 |  |
| high | DOUBLE | 16 |  |
| close | DOUBLE | 16 |  |
| pre\_close | DOUBLE | 16 |  |
| change | DOUBLE | 16 |  |
| vol | INT | 4 |  |
| amount | DOUBLE | 16 |  |

用户也可以指定所有数据类型：

```
schematable=table(`sym`permno`date`open`high`close`pre_close`change`vol`amount as name,`SYMBOL`SYMBOL`DATE`DOUBLE`DOUBLE`DOUBLE`DOUBLE`DOUBLE`INT`DOUBLE as type)
tt=loadText("/home/DolphinDB/Data/stock.csv",,schematable)
schema(tt).colDefs;
```

| name | typeString | typeInt | comment |
| --- | --- | --- | --- |
| sym | SYMBOL | 17 |  |
| permno | SYMBOL | 17 |  |
| date | DATE | 6 |  |
| open | DOUBLE | 16 |  |
| high | DOUBLE | 16 |  |
| close | DOUBLE | 16 |  |
| pre\_close | DOUBLE | 16 |  |
| change | DOUBLE | 16 |  |
| vol | INT | 4 |  |
| amount | DOUBLE | 16 |  |

## 例 3. 只加载部分列

例如，只需加载 sym, date, open, high, close, vol, amount 这 7
列。注意，加载数据时，不能改变各列的先后顺序。如果需要调整列的顺序，可以将数据文件加载后，再使用`reorderColumns!`函数。

```
schema=extractTextSchema("/home/DolphinDB/Data/stock.csv");
schema=select * from schema where name in `sym`date`open`high`close`vol`amount
schema[`col]=[0,2,3,4,5,8,9]

tt=loadText("/home/DolphinDB/Data/stock.csv",,schema);
tt;
```

| sym | date | open | high | close | vol | amount |
| --- | --- | --- | --- | --- | --- | --- |
| SUN | 2019.06.10 | 18.675316 | 72.754005 | 136.463909 | 1376 | 31371.319038 |
| AAPL | 2019.06.05 | 42.098717 | 196.873587 | 41.513899 | 3632 | 9950.864129 |
| ORCL | 2019.06.05 | 62.223474 | 197.099027 | 123.785675 | 3069 | 38035.800937 |
| SUN | 2019.06.03 | 0.18163 | 50.669866 | 4.652098 | 6213 | 1842.198893 |
| SUN | 2019.06.06 | 32.54134 | 67.012502 | 130.312294 | 4891 | 55744.156823 |
| SUN | 2019.06.07 | 56.899091 | 81.709825 | 61.786176 | 1133 | 69057.849515 |
| AAPL | 2019.06.08 | 77.026838 | 38.504431 | 22.68496 | 3672 | 34420.187073 |
| ORCL | 2019.06.07 | 62.752656 | 39.33621 | 48.483091 | 4382 | 41601.601639 |
| AAPL | 2019.06.02 | 8.5487 | 17.623418 | 141.88325 | 8092 | 15449.159988 |
| AAPL | 2019.06.02 | 26.178685 | 197.320455 | 110.52407 | 5541 | 14616.820449 |

## 例 4. 加载文件时，忽略数据文件的前 2 行。

示例文件的第一行为列名，因此忽略前 2 行后，总的数据条数为 9。

```
re=loadText(filename="/home/DolphinDB/Data/stock.csv",skipRows=2)
select count(*) from re;
```

| count |
| --- |
| 9 |

## 例 5. 指定时间类型的格式来加载数据文件

生成本例所需的数据文件：

```
time=["20190623145457","20190623155423","20190623163025"]
sym=`AAPL`MS`IBM
qty=2200 5400 8670
price=54.78 59.64 65.23
t=table(time,sym,qty,price)
saveText(t,"/home/DolphinDB/Data/t2.csv");
```

加载数据前，使用 [extractTextSchema](../e/extractTextSchema.md) 函数获取该数据文件的结构：

```
extractTextSchema("/home/DolphinDB/Data/t2.csv");
```

| name | type |
| --- | --- |
| time | LONG |
| sym | SYMBOL |
| qty | INT |
| price | DOUBLE |

由于 time 列的时间格式与 DolphinDB 中的时间格式不同，如果直接加载该文件，time 列的数据将会被识别为长整型。为了能够正确加载该文件 time
列的数据，需要指定 time 列的数据类型为 DATETIME，并且指定该列的格式为 "yyyyMMddHHmmss"。

```
schema=extractTextSchema("/home/DolphinDB/Data/t2.csv")
update schema set type = "DATETIME" where name = "time"
schema[`format]=["yyyyMMddHHmmss",,,];

loadText("/home/DolphinDB/Data/t2.csv",,schema);
```

| time | sym | qty | price |
| --- | --- | --- | --- |
| 2019.06.23T14:54:57 | AAPL | 2200 | 54.78 |
| 2019.06.23T15:54:23 | MS | 5400 | 59.64 |
| 2019.06.23T16:30:25 | IBM | 8670 | 65.23 |

## 例 6. 加载包含数组向量列的数据

使用以下脚本模拟生成一个 csv 文本文件：

```
bid = array(DOUBLE[], 0, 20).append!([1.4799 1.479 1.4787, 1.4796 1.479 1.4784, 1.4791 1.479 1.4784])
ask = array(DOUBLE[], 0, 20).append!([1.4821 1.4825 1.4828, 1.4818 1.482 1.4821, 1.4814 1.4818 1.482])
TradeDate = 2022.01.01 + 1..3
SecurityID = rand(`APPL`AMZN`IBM, 3)
t = table(SecurityID as `sid, TradeDate as `date, bid as `bid, ask as `ask)
t;
saveText(t,filename="/home/DolphinDB/Data/t.csv",delimiter=',',append=true)
```

saveText在保存数组向量到 csv 文件时，把原数据中的`[ ]` 替换为了 `"
"`，文件内容如下：

```
sid,date,bid,ask
APPL,2022.01.02,"1.4799,1.479,1.4787","1.4821,1.4825,1.4828"
IBM,2022.01.03,"1.4796,1.479,1.4784","1.4818,1.482,1.4821"
APPL,2022.01.04,"1.4791,1.479,1.4784","1.4814,1.4818,1.482"
```

然后调用 loadText 导入该文件：

```
path = "/home/DolphinDB/Data/t.csv"
schema=extractTextSchema(path);
update schema set type = "DOUBLE[]" where name="bid" or name ="ask"
t = loadText(path, schema=schema, arrayDelimiter=",")
t;
```

| sid | date | bid | ask |
| --- | --- | --- | --- |
| AMZN | 2022.01.02 | [1.4799,1.479,1.4787] | [1.4821,1.4825,1.4828] |
| AMZN | 2022.01.03 | [1.4796,1.479,1.4784] | [1.4818,1.482,1.4821] |
| IBM | 2022.01.04 | [1.4791,1.479,1.4784] | [1.4814,1.4818,1.482] |

通过 saveText 导出 csv 文件时，数组向量的边界标识默认为双引号（”），本例中 t.csv 的内容如下

当数组向量的边界标识不为双引号时，可以通过设置参数 arrayMarker 导入，例如当 t.csv 的内容如下时

```
sid,date,bid,ask
APPL,2022.01.02,[1.4799,1.479,1.4787],[1.4821,1.4825,1.4828]
IBM,2022.01.03,[1.4796,1.479,1.4784],[1.4818,1.482,1.4821]
APPL,2022.01.04,[1.4791,1.479,1.4784],[1.4814,1.4818,1.482]
```

通过以下脚本导入

```
path = "/home/DolphinDB/Data/t.csv"
schema=extractTextSchema(path);
update schema set type = "DOUBLE[]" where name="bid" or name ="ask"
t = loadText(path, schema=schema, arrayDelimiter=",",arrayMarker="[]")
t;
```

## 例 7. 批量导入小文件

在现实场景中，数据供应商会将一只股票数据保存到一个文件中，这种场景的特点是文件数量比较多，但单个文件比较小。如果将文件一个个导入，则效率会比较低。为提高导入效率，可以考虑将多个小文件批量合并后再导入。

数据文件：[smallDataset.zip](../../tutorials/data/smallDataset.zip)

```
db = database("dfs://k_day_level")
colName = `securityid`tradetime`open`close`high`low`vol`val`vwap
colType = [SYMBOL,TIMESTAMP,DOUBLE,DOUBLE,DOUBLE,DOUBLE,INT,DOUBLE,DOUBLE]
tbSchema = table(1:0, colName, colType)
if(existsDatabase("dfs://k_day_level")){
	dropDatabase("dfs://k_day_level")
}
database(directory = 'dfs://k_day_level', partitionType = RANGE, partitionScheme =[2000.01M,2001.01M,2002.01M,2003.01M,2004.01M,2005.01M,2006.01M,2007.01M,2008.01M,2009.01M,2010.01M,2011.01M,2012.01M,2013.01M,2014.01M,2015.01M,2016.01M,2017.01M,2018.01M,2019.01M,2020.01M,2021.01M,2022.01M,2023.01M,2024.01M]$7, engine= `OLAP, atomic = `TRANS)
db.createPartitionedTable(table=tbSchema,tableName=`k_day,partitionColumns=`tradetime)

//2. 导入数据文件
batchNum=1000
dir = "/home/data/smallDataset/"
allFiles = files(dir).filename
i = 0
s = allFiles.size()
do{
    files =allFiles[i:min(i+batchNum, s)]
    data = each(loadText, dir + files).unionAll(false)
    loadTable("dfs://k_day_level","k_day").append!(data)
    i = i + batchNum
}while(i < s)

select top 10* from loadTable("dfs://k_day_level","k_day")
```

| securityid | tradetime | open | close | high | low | vol | val | vwap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sz000001 | 2010.01.01T00:00:00.000 | 35.9484 | 35.4385 | 36.3261 | 35.9569 | 10,732 | 380,325.7701 | 35.4385 |
| sz000002 | 2010.01.01T00:00:00.000 | 5.4374 | 7.2864 | 5.4665 | 3.8142 | 45,577 | 332,092.5668 | 7.2864 |
| sz000003 | 2010.01.01T00:00:00.000 | 8.4177 | 10.5074 | 8.7004 | 7.577 | 96,865 | 1,017,794.5994 | 10.5074 |
| sz000004 | 2010.01.01T00:00:00.000 | 78.7732 | 76.4809 | 79.1491 | 78.4188 | 67,520 | 5,163,993.091 | 76.4809 |
| sz000005 | 2010.01.01T00:00:00.000 | 23.5196 | 25.8487 | 23.9986 | 23.9379 | 1,156 | 29,881.1144 | 25.8487 |
| sz000006 | 2010.01.01T00:00:00.000 | 75.3909 | 73.9721 | 75.5661 | 74.8373 | 70,337 | 5,202,974.0605 | 73.9721 |
| sz000007 | 2010.01.01T00:00:00.000 | 21.9932 | 22.7951 | 22.5291 | 21.218 | 76,912 | 1,753,219.9525 | 22.7951 |
| sz000008 | 2010.01.01T00:00:00.000 | 21.0682 | 21.5055 | 21.6914 | 20.733 | 9,320 | 200,431.077 | 21.5055 |
| sz000009 | 2010.01.01T00:00:00.000 | 77.2482 | 75.6649 | 78.2001 | 76.9927 | 13,538 | 1,024,351.3968 | 75.6649 |
| sz000010 | 2010.01.01T00:00:00.000 | 54.2793 | 55.6466 | 54.3281 | 53.6054 | 31,924 | 1,776,461.4488 | 55.6466 |

