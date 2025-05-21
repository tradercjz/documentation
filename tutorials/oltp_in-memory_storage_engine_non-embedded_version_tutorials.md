# OLTP 内存存储引擎（非嵌入式版）使用教程

## 1. 背景

在一些数据库应用场景中，例如金融行业的交易系统，其主要工作负载来源于对关系表的高频度、高并发的更新和查询操作。这样的应用场景要求数据的读写和计算能够具有低延迟、高并发的特征，同时保证极高的数据一致性，并提供 ACID 事务的支持，是典型的在线事务处理（OLTP）场景。传统的存储引擎由于其架构的设计出发点是将数据存储在磁盘上，在面对上述场景要求时，软硬件层面面临巨大挑战，无法很好地满足上述苛刻的性能要求。而在这些场景中，往往需要维护的数据量实际上没有那么大，那么，能否把所有的数据都维护在内存里呢？这样就可以减少读写磁盘的带宽，能够大大降低数据库的延迟和提升数据库的并发度。

基于这个想法，DolphinDB 设计并实现了一款纯自研的内存 OLTP 数据库，它有以下特点：

* 将所有数据都存储在内存中，省去磁盘 I/O 的开销；
* 以行存的形式来组织数据，主要适用于 OLTP 的场景；
* 支持创建 B+ 树索引 (主键索引和二级索引) 来应对高频度、高并发的更新和查询操作；
* 支持事务，默认为 snapshot isolation；
* 实现 Write-Ahead-Logging 和 checkpoint 机制以保证数据的持久化和恢复；
* 为加速重启时的恢复过程，实现了并行恢复机制。

下文将介绍 OLTP 的使用方式。

注： 需要在配置文件里加上 `enableIMOLTPEngine=true` 来开启 OLTP 引擎。

## 2. DDL

### 2.1 建库

使用 [database](https://docs.dolphindb.cn/zh/funcs/d/database.html) 函数来创建 OLTP 数据库，语法与创建 OLAP/TSDB 数据库一样，但是有以下注意事项：

* *directory* 必须以 `oltp://` 开头。
* *engine* 必须为 `IMOLTP`。
* OLTP 目前只支持单机版本，分区方式可以任意填写。

```
dbName = "oltp://test_imoltp"
db = database(dbName, VALUE, 1..100, , "IMOLTP")
```

### 2.2 建表

使用 [createIMOLTPTable](https://docs.dolphindb.cn/zh/funcs/c/createIMOLTPTable.html) 函数来创建 OLTP 表，语法如下：

```
createIMOLTPTable(dbHandle, table, tableName, primaryKey, [secondaryKey], [uniqueFlag])
```

*primaryKey* 用来指定主键索引的键。主键索引有且只有一个，每个 OLTP 表都必须指定。主键索引是 unique 的，插入数据时会检查是否满足唯一性约束（即不能插入重复元素），若违反则报错。主键可以包含多个字段（字段即为列名）。

*secondaryKey* 用来指定二级索引的键。二级索引可选，并且每个 OLTP 表可以创建多个二级索引。二级索引有 unique 和 non-unique 两种，两者的区别在于 unique 索引需要满足唯一性约束，而 non-unique 索引没有这个限制。由 *uniqueFlag* 来指定二级索引是否是 unique 的。二级索引的键同样可以包含多个字段。

```
// pt1 以 id 为主键，没有二级索引
pt1 = db.createIMOLTPTable(
    table(1:0, ["id", "val1", "val2", "sym"], [LONG, INT, LONG, STRING]),
    "test_table_1",
    primaryKey=`id
)

// pt2 以 id,sym 为主键，有一个 unique 二级索引：以 val2,sym 为键
pt2 = db.createIMOLTPTable(
    table(1:0, ["id", "val1", "val2", "sym"], [LONG, INT, LONG, STRING]),
    "test_table_2",
    primaryKey=`id`sym,
    secondaryKey=`val2`sym,
    uniqueFlag=true
)

// pt3 以 id 为主键，有一个非 unique 二级索引：以 val1 为键；一个 unique 二级索引：以 sym 为键
pt3 = db.createIMOLTPTable(
    table(1:0, ["id", "val1", "val2", "sym"], [LONG, INT, LONG, STRING]),
    "test_table_3",
    primaryKey=`id,
    secondaryKey=[`val1, `sym],
    uniqueFlag=[false, true]
)
```

通常来说，对于查询效率：主键索引优于二级索引优于非索引，如果查询时不能利用任何索引，则只能进行全表扫描。合理地创建二级索引可以提升查询的效率，但是相应地会降低写入的效率，因为写入时 (insert/delete/update) 需要修改相应的索引。

### 2.3 删库/删表

使用 [dropTable](https://docs.dolphindb.cn/zh/funcs/d/dropTable.html) 和 [dropDatabase](https://docs.dolphindb.cn/zh/funcs/d/dropDatabase.html) 来删表删库，使用方式与 OLAP/TSDB 没有区别。

```
db.dropTable("test_table_1")

if (existsDatabase(dbName)) {
    dropDatabase(dbName)
}
```

## 3. DML

后文的例子假设已经执行过下面的脚本来建库建表：

```
dbName = "oltp://test_imoltp"
tableName = "test_table"

if (existsDatabase(dbName)) {
    dropDatabase(dbName)
}

db = database(dbName, VALUE, 1..100, , "IMOLTP")

// pt 以 id 为主键，没有二级索引
pt = db.createIMOLTPTable(
    table(1:0, ["id", "val1", "val2", "sym"], [LONG, INT, LONG, STRING]),
    tableName,
    primaryKey=`id
)
```

### 3.1 写入数据

写入数据可以用 [append!](https://docs.dolphindb.cn/zh/funcs/a/append%21.html) 和 [insert into](https://docs.dolphindb.cn/zh/progr/sql/insertInto.html)，使用方式与 OLAP/TSDB 一样。

```
pt = loadTable("oltp://test_imoltp", "test_table")

id = 1..100
val1 = id * 10
val2 = rand(10000, size(id))
sym = take(`aaa`bbb`ccc`ddd`eee, size(id))
pt.append!(table(id, val1, val2, sym))

insert into pt values(200, 2000, 1111, `xxx)
insert into pt values(201, 2010, 2222, `yyy)
insert into pt values(211..220, (211..220)*10, take(9527, 10), take(`xxx`yyy`zzz, 10))

insert into pt(id, sym) values(1000, `aaa)
insert into pt(id, sym, val1) values(1001, `bbb, 10010)
```

### 3.2 查询数据

使用 SQL 来查询数据。where 条件非常重要，如果一次查询无法利用索引，那么性能会大幅降低。

```
pt = loadTable("oltp://test_imoltp", "test_table")

select * from pt where id = 10  // 点查，用主键索引
select * from pt where id > 100, id < 200  // 范围查询，用主键索引

select * from pt where val1 = 1000  // 全表扫描，无法利用索引
```

### 3.3 更新数据

使用 SQL 来更新数据。

```
pt = loadTable("oltp://test_imoltp", "test_table")

update pt set val1 = 100 where id = 1
update pt set val1 = id + val1 where id < 10
```

### 3.4 删除数据

使用 SQL 来删除数据。

```
pt = loadTable("oltp://test_imoltp", "test_table")

delete from pt where id = 1
delete from pt where id >= 100, id <= 110
```

## 4. 事务

使用 [transaction](https://docs.dolphindb.cn/zh/progr/statements/transaction.html) 语句块可以在一个事务内执行多条 DML 语句，在一个事务范围内，所有的 DML 操作都会一起成功或一起失败。若一个事务执行的时候有异常抛出，会自动撤销本次事务的所有更改。

```
pt = loadTable("oltp://test_imoltp", "test_table")

delete from pt

transaction {
    insert into pt values(0, 0, 0, `aaa)
    insert into pt values(1, 1, 1, `bbb)
    insert into pt values(2, 2, 2, `ccc)
    commit  // 提交事务（可以省略）
}
assert (exec id from pt order by id) == [0,1,2]

transaction {
    insert into pt values(3, 3, 3, `ddd)
    insert into pt values(4, 4, 4, `eee)
    delete from pt where id = 1
    update pt set id = 10 where id = 0

    assert (exec id from pt order by id) == [2,3,4,10]
    rollback  // 强制回滚事务，撤销所有修改
}
assert (exec id from pt order by id) == [0,1,2]
```

`commit` 表示提交本次事务的所有更改，`rollback` 表示撤销本次事务的所有更改。不需要显式地写 `commit`，出了 transaction 语句块的作用域时会自动 commit。

注：
若不显式地使用 `transaction` 语句块，则每一句 SQL 都是一个事务。

重要：
DDL 语句（即建表，删表等）不能放在 `transaction` 语句块里面，因为 DDL 目前不支持事务。

## 5. 配置参数

目前 OLTP 有以下配置参数可以设置：

* *enableIMOLTPEngine*，bool 类型。表示是否开启 OLTP 引擎。默认为 false。
* *enableIMOLTPRedo*，bool 类型。表示是否开启 WAL（Write-Ahead-Log），开启之后才能保证数据不会丢失。默认为 true。
* *IMOLTPRedoFilePath*，string 类型。表示 redo 文件（即 WAL 文件）的路径（注意不是目录），可以为绝对路径或者相对路径。当为相对路径时，相对于 home 目录下的 `IMOLTP` 目录。默认为 home 目录下的 `IMOLTP/im_oltp.redo`。
* *IMOLTPSyncOnTxnCommit*，bool 类型。只在 *enableIMOLTPRedo* 为 true 时（即开启了 WAL）有意义。默认为 false。详细解释见下文。
* *enableIMOLTPCheckpoint*，bool 类型。表示是否开启 checkpoint。默认为 true。
* *IMOLTPCheckpointFilePath*，string 类型。表示 checkpoint 文件的路径（注意不是目录），可以为绝对路径或者相对路径。当为相对路径时，相对于 home 目录下的 `IMOLTP` 目录。默认为 home 目录下的 `IMOLTP/im_oltp.ckp`。
* *IMOLTPCheckpointThreshold*，long 类型，单位为 MiB。 表示：如果 redo 文件里面的 log 大小达到该阈值后，会触发一次 checkpoint。默认为 100 MiB。
* *IMOLTPCheckpointInterval*，long 类型，单位为秒。表示每隔 # 秒之后强制做一次 checkpoint。默认为 60 秒。

注：

关于 *IMOLTPSyncOnTxnCommit* 的含义：

在开启 WAL 后，事务对数据进行修改之前，会先写日志到持久化存储。系统重启时会回放 redo 文件里的日志，恢复到重启之前的状态。

如果 *IMOLTPSyncOnTxnCommit* 为 false，事务 commit 成功之后，保证日志写到了操作系统的缓存里，但是不保证日志已经写到了持久化存储上。因此，如果进程崩溃, 数据不会丢失, 但是当操作系统崩溃（机器掉电）, 可能会有数据丢失。

如果 *IMOLTPSyncOnTxnCommit* 为 true，在事务 commit 成功之后，保证日志已经写到了持久化存储上，即使操作系统崩溃，数据也不会丢失。(但是如果存储设备故障, 还是可能有数据丢失)。

如果需要持久化数据，并且对数据的一致性要求较高，绝对无法忍受数据丢失，推荐把 *enableIMOLTPRedo* 和 *IMOLTPSyncOnTxnCommit* 都设置为 true。这种模式下，（写入）性能较差。

如果需要持久化数据，并且可以容忍操作系统崩溃（比如机器掉电等小概率事件）导致的数据丢失，推荐把 *enableIMOLTPRedo* 设置为 true， 把 *IMOLTPSyncOnTxnCommit* 设置为 false。这种模式下，（写入）性能较好。默认为这种配置。

## 6. 内置函数 `triggerCheckpointForIMOLTP`

当开启了 checkpoint 时（即 *enableIMOLTPCheckpoint* 配置为 true ），系统会在达到以下两个条件之一时自动触发 checkpoint：

* redo 文件里面的 log 大小达到阈值（*IMOLTPCheckpointThreshold* MiB）；
* 或者，距离上一次 checkpoint 过去了 *IMOLTPCheckpointInterval* 秒。

用户也可以手动调用 `triggerCheckpointForIMOLTP` 函数来触发 checkpoint。函数语法如下：

```
triggerCheckpointForIMOLTP([force=false], [sync=false])
```

参数：

* *force*，bool 类型，可选。表示是否强制做 checkpoint。如果为 false，并且当前并没有达到做 checkpoint 的条件（即 redo 文件里的 log 大小没有达到 `IMOLTPCheckpointThreshold`），则忽略这次请求。默认为 false。
* *sync*，bool 类型，可选。表示是否异步。如果为 false，则该函数请求一次异步的 checkpoint，并不会等到请求完成再返回；否则该函数会等到请求完成（注意不一定做了 checkpoint）再返回。默认为 false。

## 7. 总结

DolphinDB 推出的OLTP 内存数据库适用于高并发、低延迟的在线事务处理场景。该数据库将数据存储在内存中，支持 B+ 树索引、事务、Write-Ahead-Logging 和 checkpoint 机制。事务通过 transaction 语句块实现，保证了操作的原子性。

用户还可以通过配置参数的配置以及内置函数 `triggerCheckpointForIMOLTP` 的使用，手动触发 checkpoint。

总体而言，DolphinDB 的 OLTP 引擎适用于对数据一致性和性能要求较高的场景。

