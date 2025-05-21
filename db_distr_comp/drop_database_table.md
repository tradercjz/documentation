# 删除库表

删除库表前请确认具有必要的权限。更多关于权限信息请参考：[用户权限管理](../tutorials/ACL_and_Security.md)。

## 删除数据库

DolphinDB 支持使用 [DROP DATABASE](../progr/sql/drop.html#%E5%88%A0%E9%99%A4%E5%88%86%E5%B8%83%E5%BC%8F%E6%95%B0%E6%8D%AE%E5%BA%93) 语句和 [dropDatabase](../funcs/d/dropDatabase.md) 函数两种方式删除数据库。

注： 数据库删除后，库中所有数据会一并删除，此操作不可逆，须谨慎操作。

例如，删除已经存在的分布式数据库 dfs://demo。

```
db = database("dfs://demo", VALUE, 1..5)

// 使用 SQL DROP DATABASE 语句
drop database "dfs://demo"

// 使用 dropDatabase 函数
dropDatabase("dfs://demo")
```

## 删除分布式表

DolphinDB 支持使用 [DROP TABLE](../progr/sql/drop.html#%E5%88%A0%E9%99%A4%E5%88%86%E5%B8%83%E5%BC%8F%E8%A1%A8%E6%88%96%E7%BB%B4%E5%BA%A6%E8%A1%A8) 语句和 [dropTable](../funcs/d/dropTable.md)
函数两种方式删除分布式表。

注： 表删除后，表中所有数据会一并删除，此操作不可逆，须谨慎操作。

例如，删除数据库 dfs://demo 中的表 demoTable

```
db = database("dfs://demo", VALUE, 1..5)
schemaTb = table(1:0,`id`name`val,[INT,SYMBOL,DOUBLE])
pt = db.createPartitionedTable(schemaTb,`demoTable,`id)

// 使用 SQL DROP TABLE 语句
drop table "dfs://demo"."demoTable"

// 使用 dropTable 函数
dropTable(db,"demoTable")
```

## 删除内存表

DolphinDB 支持使用 SQL [DROP TABLE](../progr/sql/drop.html#%E5%88%A0%E9%99%A4%E5%88%86%E5%B8%83%E5%BC%8F%E8%A1%A8%E6%88%96%E7%BB%B4%E5%BA%A6%E8%A1%A8) 语句或 [undef](../funcs/u/undef.md) 函数删除。

例如，删除表
t：

```
t = table(1:0,`id`name`val,[INT,SYMBOL,DOUBLE])

// 使用 SQL DROP TABLE 语句
drop table t

// 使用 undef 函数
undef("t")
```

对于共享内存表，可通过指定参数 *objType*=SHARED 使用 `undef` 函数删除：

```
share table(1:0,`id`name`val,[INT,SYMBOL,DOUBLE]) as t
undef(obj="t", objType=SHARED)
```

对于流数据表，可通过 [dropStreamTable](../funcs/d/dropStreamTable.md)
函数删除：

```
t = streamTable(1:0,`id`name`val,[INT,SYMBOL,DOUBLE])
dropStreamTable("t")
```

