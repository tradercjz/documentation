# upsert!

## 语法

`upsert!(obj, newData, [ignoreNull=false], [keyColNames],
[sortColumns])`

## 参数

**obj** 是一个索引内存表、键值内存表，或者 DFS 表（分布式表或维度表）。

**newData** 是一个内存表。

**ignoreNull** 是一个布尔值，表示若 *newData* 中某元素为 NULL 值，是否对目标表中的相应数据进行更新。默认值为
false。

**keyColNames** 是一个字符串标量或向量。由于 DFS 表没有键值列，对 DFS
表进行更新时，将该参数指定的列和分区列一起视为键值列。

**sortColumns**
是一个字符串标量或向量。设置该参数，更新的分区内的所有数据会根据指定的列进行排序。排序在每个分区内部进行，不会跨分区排序。

注：

* 仅 OLAP 引擎下使用 `upsert!` 时，才支持设置
  *sortColumns*。
* 要设置 *sortColumns*， *obj* 必须为分布式表。
* 仅对同一个分区内的数据 按照 *sortColumns* 进行排序，不同分区之间的数据不会进行排序。
* *obj* 为一个空表时，设置 *sortColumns* 无效，即更新后不对新插入的数据进行排序。
* 在 PKEY 引擎下不支持设置 *ignoreNull*,
  *keyColNames*, *sortColumns*。

## 详情

将新数据写入索引内存表、键值内存表，或者 DFS 表。若新数据的主键值已存在，更新该主键值的数据；否则添加数据。

注：

* 调用该函数时，需要保证 *newData* 和 *obj*
  两表各列的顺序一致，否则可能产生错误结果或报错。
* 若 *keyColNames* 指定的列存在重复值，对重复值进行
  `upsert!` 操作，仅会更新第一个值所在行，其余值所在行不会更新。

## 例子

对键值内存表使用 `upsert!`

```
sym=`A`B`C
date=take(2021.01.06, 3)
x=1 2 3
y=5 6 7
t=keyedTable(`sym`date, sym, date, x, y)
t;
```

| sym | date | x | y |
| --- | --- | --- | --- |
| A | 2021.01.06 | 1 | 5 |
| B | 2021.01.06 | 2 | 6 |
| C | 2021.01.06 | 3 | 7 |

如果对应列的数据类型一致，就会输出结果。

```
newData = table(`A`B`C`D as sym1, take(2021.01.06, 4) as date1, NULL NULL 300 400 as x1, NULL 600 700 800 as y1);
newData;
```

| sym | date | x1 | y1 |
| --- | --- | --- | --- |
| A | 2021.01.06 |  |  |
| B | 2021.01.06 |  | 600 |
| C | 2021.01.06 | 300 | 700 |
| D | 2021.01.06 | 400 | 800 |

```
upsert!(t, newData, ignoreNull=true)
t;
```

| sym | date | x | y |
| --- | --- | --- | --- |
| A | 2021.01.06 | 1 | 5 |
| B | 2021.01.06 | 2 | 600 |
| C | 2021.01.06 | 300 | 700 |
| D | 2021.01.06 | 400 | 800 |

以上为将 *ignoreNull* 设为 true 时的情况。此时，若新数据中有元素值为 NULL，不对目标数据表的相应的元素进行更新操作。

以下为将 *ignoreNull* 设为 false（默认值）时的情况，不管新数据中值是否为 NULL，均进行更新操作。

```
sym=`A`B`C
date=take(2021.01.06, 3)
x=1 2 3
y=5 6 7
t=keyedTable(`sym`date, sym, date, x, y)
upsert!(t, newData)
t;
```

| sym | date | x | y |
| --- | --- | --- | --- |
| A | 2021.01.06 |  |  |
| B | 2021.01.06 |  | 600 |
| C | 2021.01.06 | 300 | 700 |
| D | 2021.01.06 | 400 | 800 |

对 DFS 表使用 `upsert!`：

```
ID=0 1 2 2
x=0.1*0..3
t=table(ID, x)
db=database("dfs://rangedb128", VALUE,  0..10)
pt=db.createPartitionedTable(t, `pt, `ID)
pt.append!(t)
select * from pt;
```

| ID | x |
| --- | --- |
| 0 | 0 |
| 1 | 0.1 |
| 2 | 0.2 |
| 2 | 0.3 |

```
t1=table(1 as ID, 111 as x)
upsert!(pt, t1, keyColNames=`ID)
select * from pt;
```

| ID | x |
| --- | --- |
| 0 | 0 |
| 1 | 111 |
| 2 | 0.2 |
| 2 | 0.3 |

```
t1=table(2 as ID, 222 as x)
upsert!(pt, t1, keyColNames=`ID)
select * from pt;
```

| ID | x |
| --- | --- |
| 0 | 0 |
| 1 | 111 |
| 2 | 222 |
| 2 | 0.3 |

对 DFS 表使用 `upsert!` 更新数据，设置 *ignoreNull* = true，当新数据中有数据值为 NULL,
则不对目标数据表的相应的元素进行更新操作。

```
if(existsDatabase("dfs://valuedemo")) {
  dropDatabase("dfs://valuedemo")
}
db = database("dfs://valuedemo", VALUE, 1..10)
t = table(take(1..10, 100) as id, 1..100 as id2, 100..1 as value)
pt = db.createPartitionedTable(t, "pt", `id).append!(t)
t2 = table( 1 2 as id, 1 2 as id2, 1 NULL as value)
upsert!(pt, t2, true, "id2")
```

```
if(existsDatabase("dfs://upsert")) {
  dropDatabase("dfs://upsert")
}
sym=`A`B`C`A`D`B`A
date=take(2021.12.10,3) join take(2021.12.09, 3) join 2021.12.10
price=8.3 7.2 3.7 4.5 6.3 8.4 7.6
val=10 19 13 9 19 16 10
t=table(sym, date, price, val)
db=database("dfs://upsert", VALUE,  `A`B`C)
pt=db.createPartitionedTable(t, `pt, `sym)
pt.append!(t)
t1=table(`A`B`E as sym, take(2021.12.09, 3) as date, 11.1 10.5 6.9 as price, 12 9 11 as val)
upsert!(pt, t1, keyColNames=`sym, sortColumns=`date`val)
select * from pt
```

| sym | date | price | val |
| --- | --- | --- | --- |
| A | 2021.12.09 | 4.5 | 9 |
| A | 2021.12.09 | 11.1 | 12 |
| A | 2021.12.10 | 7.6 | 10 |
| B | 2021.12.09 | 10.5 | 9 |
| B | 2021.12.09 | 8.4 | 16 |
| C | 2021.12.10 | 3.7 | 13 |
| D | 2021.12.09 | 6.3 | 19 |
| E | 2021.12.09 | 6.9 | 11 |

