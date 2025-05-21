# tableUpsert

## 语法

`tableUpsert(obj, newData, [ignoreNull=false], [keyColNames],
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

返回值：LONG 类型数据对，第一个元素表示新插入的记录数，第二个元素表示更新的记录数。

将新数据写入索引内存表、键值内存表，或者 DFS 表。若新数据的主键值已存在，更新该主键值的数据；否则添加数据。

`tableUpsert` 与 `upsert!` 的用法一致，区别在于
`tableUpsert` 会返回操作行数，而 `upsert!`
进行了就地修改，用于链式操作。

注：

* 调用该函数时，需要保证 *newData* 和 *obj*
  两表各列的顺序一致，否则可能产生错误结果或报错。
* 若 *keyColNames* 指定的列存在重复值，对重复值进行
  `upsert!` 操作，仅会更新第一个值所在行，其余值所在行不会更新。

## 例子

对键值内存表使用
`tableUpsert`：

```
sym=`A`B`C
date=take(2021.01.06, 3)
x=1 2 3
y=5 6 7
t=keyedTable(`sym`date, sym, date, x, y)
newData = table(`A`B`C`D as sym1, take(2021.01.06, 4) as date1, NULL NULL 300 400 as x1, NULL 600 700 800 as y1);
tableUpsert(t, newData, ignoreNull=true)
// output
1:2
```

对索引内存表使用
`tableUpsert`：

```
sym=`A`B`C
date=take(2021.01.06, 3)
x=1 2 3
y=5 6 7
t=indexedTable(`sym`date, sym, date, x, y)
newData = table(`A`B`C`D as sym1, take(2021.01.06, 4) as date1, NULL NULL 300 400 as x1, NULL 600 700 800 as y1);
tableUpsert(t, newData, ignoreNull=true)
// output
1:2
```

对 DFS 表使用
`tableUpsert`：

```
ID=0 1 2 2
x=0.1*0..3
t=table(ID, x)
db=database("dfs://rangedb128", VALUE,  0..10)
pt=db.createPartitionedTable(t, `pt, `ID)
pt.append!(t)
t1=table(1 as ID, 111 as x)
tableUpsert(pt, t1, keyColNames=`ID)
// output
0:1
```

