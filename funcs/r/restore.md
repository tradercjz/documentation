# restore

## 语法

`restore(backupDir, dbPath, tableName, partition, [force=false],
[outputTable], [parallel=false], [snapshot=false], [keyPath])`

## 参数

**backupDir** 字符串，表示存放备份数据的目录。

**dbPath** 字符串，表示已备份的分布式数据库的路径。

**tableName** 字符串，表示已备份的表的名称。

**partition** 字符串，表示要恢复的分区的相对路径。分区路径可以包含通配符("%"和"?"), "?"表示单个字符，"%"表示0，1或多个字符。

* 若仅恢复某个分区，输入分区的相对路径或者"%/"+”分区名称”。举例：要恢复 "dfs://compoDB"
  下的分区 ”20170810/50\_100”，输入 "/compoDB/20170807/0\_50" 或者 "%/20170807/0\_50"。
  请注意：若使用 2.00.4 ~ 2.00.6 版本 server，对表级分区数据进行备份和恢复时，该参数必须指定路径到物理索引（可通过函数
  [listTables](../l/listTables.html) 获取），例如分区
  "/compoDB/20170807/0\_50" 下表的物理索引为8，则 *partition* 需指定为
  "/compoDB/20170807/0\_50/8"。
* 若需要恢复所有分区，直接输入"%"。但需注意，采用此方法可能会导致当前数据表的数据丢失。举例说明：若当前表有10个分区，备份只包含2个分区，若使用%恢复数据，则可能导致表中其他8个分区的数据丢失。

**force** 布尔值，表示是否强制恢复。默认值为 false，表示只有元数据与备份数据元数据不一致的分区，才会恢复。

**outputTable** 分布式表句柄，该表的结构必须与要恢复的表结构一致。如果没有指定
*outputTable*，恢复后的数据会存放到原表；如果指定了
*outputTable*，恢复后的数据会存放到该表中，而原数据表保持不变。

**parallel** 布尔值，表示是否对一个数据表下不同分区进行并行恢复。默认值为 false。

**snapshot** 仅在参数 *partition* = "%"
时有效。表示进行非首次恢复时，对于待恢复的数据库，若某些表或分区不在备份数据中，是否同步将数据库中对应的表/分区删除。 若设置为
true，则数据库将同步删除多余的表/分区；若设置为 false（默认值），则数据库不会删除多余的表/分区。

请注意：若 server 版本号低于3.00.1，则 *snapshot* 的默认值是 true，用户需要根据需求合理设置 *snapshot* 参数。

**keyPath** 字符串标量，指定恢复加密表备份的密钥路径。仅 Linux
系统支持该参数。恢复数据使用的密钥必须与备份时指定的密钥版本一致。注意恢复加密表时，备份表与目标表必须指定相同的加密方式（即建表时指定相同的
*encryptMode* 参数）。

## 详情

恢复指定分区的数据。返回一个字符串向量，包含恢复的分区的路径。该函数必须要用户登录后才能执行。

## 注意事项

* 恢复通过 SQL 元代码（即 [backup](../b/backup.html) 指定
  *sqlObj* 参数）备份的文件时，不能指定 *snapshot*，否则会报错。
* 指定 *outputTable* 时，恢复通过 SQL 元代码备份的文件，系统会在
  *outputTable* 中直接追加（append）备份数据；而恢复通过拷贝方式（即 `backup`
  指定 *dbPath* 参数）备份的文件时，系统只覆盖 *outputTable* 中数据不一致的分区。若不指定
  *outputTable*，则数据恢复至原表，恢复方式相同。
* 恢复时需要确保备份数据与待恢复数据库的引擎类型（engine）一致，且
  *partitionScheme*（VALUE 除外）也保持一致。当采用 VALUE
  分区时，须保证备份数据中的分区方案是待恢复数据库的分区方案的子集。例如：备份文件的分区方案是 database("dfs://xxx", VALUE,
  2017.08.07..2017.08.11)， 则待恢复数据库的 VALUE 分区范围必须不小于
  2017.08.07..2017.08.11。

## 例子

创建一个组合分区的数据库 dfs://compoDB：

```
n=1000000
ID=rand(100, n)
dates=2017.08.07..2017.08.11
date=rand(dates, n)
x=rand(10.0, n)
t=table(ID, date, x);

dbDate = database(, VALUE, 2017.08.07..2017.08.11)
dbID=database(, RANGE, 0 50 100);
db = database("dfs://compoDB", COMPO, [dbDate, dbID]);
pt = db.createPartitionedTable(t, `pt, `date`ID)
pt.append!(t);
```

备份表 pt 的所有数据：

```
backup("/home/DolphinDB/backup",<select * from loadTable("dfs://compoDB","pt")>,true);
// output
10
```

例1. 恢复所有数据到原表。

```
restore("/home/DolphinDB/backup","dfs://compoDB","pt","%",true);
// output
["dfs://compoDB/20170807/0_50/6F","dfs://compoDB/20170807/50_100/6F","dfs://compoDB/20170808/0_50/6F","dfs://compoDB/20170808/50_100/6F","dfs://compoDB/20170809/0_50/6F","dfs://compoDB/20170809/50_100/6F","dfs://compoDB/20170810/0_50/6F","dfs://compoDB/20170810/50_100/6F","dfs://compoDB/20170811/0_50/6F","dfs://compoDB/20170811/50_100/6F"]
```

例2. 恢复日期为2017.08.10的数据。

```
restore("/home/DolphinDB/backup","dfs://compoDB","pt","%20170810%",true)
// output
["dfs://compoDB/20170810/0_50/6F","dfs://compoDB/20170810/50_100/6F"]
```

例3. 在数据库 dfs://compoDB 中创建一个与表 pt 结构相同的表 temp，把 pt 的数据恢复到表
temp。请注意，采用此方法可能导致表中数据丢失。

```
temp=db.createPartitionedTable(t, `pt, `date`ID);

restore("/home/DolphinDB/backup","dfs://compoDB","pt","%",true,temp);
// output
["dfs://compoDB/20170807/0_50/6F","dfs://compoDB/20170807/50_100/6F","dfs://compoDB/20170808/0_50/6F","dfs://compoDB/20170808/50_100/6F","dfs://compoDB/20170809/0_50/6F","dfs://compoDB/20170809/50_100/6F","dfs://compoDB/20170810/0_50/6F","dfs://compoDB/20170810/50_100/6F","dfs://compoDB/20170811/0_50/6F","dfs://compoDB/20170811/50_100/6F"]

select count(*) from temp;
```

| count |
| --- |
| 1000000 |

相关函数：[restoreDB](restoreDB.html), [restoreTable](restoreTable.html), [migrate](../m/migrate.html), [backup](../b/backup.html)

