# replayDS

## 语法

`replayDS(sqlObj, [dateColumn], [timeColumn],
[timeRepartitionSchema])`

## 详情

将一个 SQL 表达式，根据时间维度划分为多个数据源，作为 `replay`
函数的输入，逐一进行回放。时间维度既可以为 DFS 表的时间列的分区粒度，也可以是基于该分区粒度的进一步的划分（由参数 *timeColumn* 与
*timeRepartitionSchema* 决定）。返回一个由数据源列表（类型为 ANY VECTOR）。

若要回放 DFS 表中的数据，只能使用 `replayDS` 函数配合
`replay` 函数进行。

## 参数

**sqlObj** 表示 SQL 查询的元代码。SQL 查询的表对象是 DFS 表，且至少有一个分区列为时间类型。

**dateColumn** 列必须为 SQL 查询的表对象的时间类型列，一般为 DATE 类型，亦可为 MONTH
类型或其它时间类型。作为数据的排序依据。*dateColumn* 列必须为表的分区列之一，系统将根据 *dateColumn*
列的分区粒度划分数据源，如 dateColumn 列按天进行分区，则数据源也按天进行划分。

**timeColumn** 列必须为 SQL 查询的表对象的时间列，作为数据的排序依据。若
*dateColumn* 为 DATE 类型时，可以指定 *timeColumn* 为 SECOND, TIME 或 NANOTIME
类型的列作为第二排序列。此外，配合 *timeRepartitionSchema* 参数，*timeColumn*
列也可以作为数据源划分依据。

注：

* *dateColumn* 和 *timeColumn* 暂不支持 DATEHOUR 类型的时间列。
* 如果没有指定 *dateColumn*，原数据表的第一列将会作为 *dateColumn*。

**timeRepartitionSchema** 时间类型的向量。如果指定了
*timeColumn*，*timeRepartitionSchema* 可用于划分更小粒度的数据源。如果
*timeRepartitionSchema* 为 [t1, t2, t3]，均为 TIME 类型，则会将每天的数据进一步划分为 4
个数据源：[00:00:00.000,t1), [t1,t2), [t2,t3) 和 [t3,23:59:59.999)。

## 例子

在以下例子中：

1. 创建变量 n。
2. 创建一个包含 `IBM` 和 `GS` 的 join 表 sym，并重复该表内容。
3. 创建一个包含 2021.01.04 到 2021.01.06 的日期序列 date，并对其排序，用于模拟交易日。
4. 创建一个包含 09:30:00 到 15:59:59 的时间序列 time 用于模拟交易时间。
5. 创建一个包含随机数（范围在 0 到 100 之间）的交易量序列 volume。
6. 创建一个名为 t 的表，包含符号、日期、时间和交易量这四个字段。
7. 如果名为 "dfs://test\_stock" 的数据库存在，则删除该数据库。
8. 创建两个不同类型的数据库 db1 和 db2，分别为 RANGE 类型和 VALUE 类型，并将它们组合到 "dfs://test\_stock" 中。
9. 在数据库中创建一个分区表 trades，按 date 和 sym 分区。
10. 向 trades 表追加 t 表的内容。
11. 创建一个 replayDS 对象，从 trades 表中加载数据，并按日期维度和时间维度划分这些数据形成数据源列表 ds。
12. 输出 ds 的大小。

```
n=int(60*60*6.5)
sym = take(take(`IBM,n).join(take(`GS,n)), n*2*3)
date=take(2021.01.04..2021.01.06, n*2*3).sort!()
time=take(09:30:00..15:59:59,n*2*3)
volume = rand(100, n*2*3)
t=table(sym,date,time,volume)
if(existsDatabase("dfs://test_stock")){
dropDatabase("dfs://test_stock")
}
db1=database("",RANGE, 2021.01.04..2021.01.07)
db2=database("",VALUE,`IBM`GS)
db=database("dfs://test_stock",COMPO,[db1, db2])
trades=db.createPartitionedTable(t,`trades,`date`sym)
trades.append!(t);
ds = replayDS(sqlObj=<select * from loadTable(db, `trades)>, dateColumn=`date, timeColumn=`time)
ds.size();
```

返回：3。

接着，从数据库中加载名为 trades 表的所有数据，指定 *timeRepartitionSchema* 为 `[11:30:00,
14:00:00]`，按照指定的时间范围对每日数据进行重分区，重新计算数据源列表的大小：

```
ds = replayDS(sqlObj=<select * from loadTable(db, `trades)>, dateColumn=`date, timeColumn=`time, timeRepartitionSchema=[11:30:00, 14:00:00])
ds.size();
```

指定时间区间 `[11:30:00, 14:00:00]` 后，每天的数据被划分为三个更小的部分 [09:30:00,
11:30:00)、[11:30:00, 14:00:00] 和 [14:00, 15:59:59]。

因此，返回：9。

**相关信息**

* [replay](replay.html "replay")

