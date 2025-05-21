# delete

delete 语句用于删除表中的记录。

delete 语句不仅可用于内存表，也可用于 DFS 表（分布式表与维度表）。请注意，对分布式表使用 delete 语句时，系统把要删除记录所在的分区整体删除后更新；对维度表使用
delete 语句时，系统将该表删除后更新。因此对 DFS 表使用 delete
语句仅适用于低频删除任务，例如分钟级删除任务，不适用于高频删除任务，例如毫秒级删除任务。

删除采取了多版本的方式，并且支持事务。系统会创建一个新的版本以存储新的数据。提交事务之前，其他 SQL
语句仍然访问旧版本的数据。若删除涉及多个分区，只要其中某一个分区删除失败，系统会回滚所有分区的修改。

在 2.00.1 及以上版本中，delete 支持 map 子句，即支持将 delete 语句在每个分区内分别执行。若 where
子句中使用结果与次序有关的函数，如： isDuplicated, first, firstNot 等，且涉及到多个分区，则必须使用 map 关键字。

自 3.00.0 版本起，支持 catalog 结构。

## 语法

方法一

```
 delete from table_name
    where condition(s);
```

如果没有使用 where 条件，删除表中所有记录。

方法二

```
delete table_name
  from table_joiner(table_names)
  [where condition(s)];
```

结合 join 子句删除数据时：

* 支持 ej 和 lj
* 要删除的表必须作为 join 的左表
* 如果没有指定 where 条件，将删除表左表中所有与右表连接成功的数据
* 对于嵌套 join 的情况，只允许最外层 join 中包含分布式表
* 对于内存表 join 分区表的情况，需要将右表（分区表）加载到内存，故使用前应合理评估内存用量，避免 OOM
* 当分区表所在数据库的 *chunkGranularity* 为 “CHUNK” 时，分区表仅可作为左表，即此时不允许两个分布式表
  join。
* 不支持两个不同数据库的表之间 join。

## 例子

### 对内存表进行删除操作

```
t = table(1 1 1 2 2 2 3 3 3 3 as id, 1..10 as x);
t;
```

| id | x |
| --- | --- |
| 1 | 1 |
| 1 | 2 |
| 1 | 3 |
| 2 | 4 |
| 2 | 5 |
| 2 | 6 |
| 3 | 7 |
| 3 | 8 |
| 3 | 9 |
| 3 | 10 |

```
delete from t where id=1;
t;
```

| id | x |
| --- | --- |
| 2 | 4 |
| 2 | 5 |
| 2 | 6 |
| 3 | 7 |
| 3 | 8 |
| 3 | 9 |
| 3 | 10 |

```
delete from t where id=3, x>8;
t;
```

| id | x |
| --- | --- |
| 2 | 4 |
| 2 | 5 |
| 2 | 6 |
| 3 | 7 |
| 3 | 8 |

```
delete from t;
t;
```

| id | x |
| --- | --- |
|  |  |

### 对分布式表进行删除操作

```
login(`admin, `123456)
n=1000000
ID=rand(10, n)
x=rand(1.0, n)
t=table(ID, x)
db=database("dfs://rangedb124", RANGE,  0 5 10)
pt=db.createPartitionedTable(t, `pt, `ID)
pt.append!(t)
```

```
select count(*) from pt;

1000000

delete from pt where ID=5;
select count(*) from pt;
```

### 删除分布式表数据且where条件与数据行次序相关

删除分布式表数据，且 where 过滤条件与数据行的次序有关，必须使用 map 子句，在分区内分别执行。

```
n=10000
ID=take(0..4, n)
date=take(2017.08.07..2017.11.11, n)
ts=rand(timestamp(1..n),n)
int=take(1..50,n)
str=rand(string(1..n),n)
sym=rand(symbol(string(1..n)),n)
x=rand(10.0, n)
t=table(ID, date,ts,int,str,sym, x)
if(existsDatabase("dfs://compoDB")){
    dropDatabase("dfs://compoDB")
}
db = database("dfs://compoDB", VALUE,2017.08M..2017.10M)
pt = db.createPartitionedTable(t, `pt, `date)
pt.append!(t);
delete from pt where isDuplicated([ID,int])=false map;
```

## delete 语句结合 join 子句进行删除操作

```
t1 = table(1..5 as id, [1,2,2,1,1] as flag)
```

| id | flag |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 2 |
| 4 | 1 |
| 5 | 1 |

```
t2 = table(3..7 as id, [100,200,100,150,100] as profit)
```

| id | profit |
| --- | --- |
| 3 | 100 |
| 4 | 200 |
| 5 | 100 |
| 6 | 150 |
| 7 | 100 |

```
delete t2 from ej(t2, t1, `id) where flag=1
t2
```

| id | profit |
| --- | --- |
| 3 | 100 |
| 6 | 150 |
| 7 | 100 |

