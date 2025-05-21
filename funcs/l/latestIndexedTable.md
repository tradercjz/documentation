# latestIndexedTable

## 语法

`latestIndexedTable(keyColumns, timeColumn, [X1], [X2], .....)`

或

`latestIndexedTable(keyColumns, timeColumn, capacity:size, colNames,
colTypes)`

或

`latestIndexedTable(keyColumns, timeColumn, table)`

## 参数

在 [indexedTable](../i/indexedTable.md) 的基础上，增加了
*timeColumn* 参数。

**timeColumn** 字符串，表示时间列，可以为整型或时间类型。

## 详情

该函数用于创建索引内存表，包含一个主键。主键可由一个或多个字段组成。其相较于 indexedTable，除主键外，还包含一个时间列，用于判断是否更新记录。

向表中添加新记录时，系统自动检查新记录的主键值。如果新记录的主键值与已有记录的主键值相同，且新记录的时间戳大于等于已有记录的时间戳，则更新表中对应的记录，否则不更新。因为在写入数据时会判断时间列，对相同主键的记录进行去重，所以`latestIndexedTable`写入性能较`indexedTable`差，但查询性能不受影响。

注：

* 不允许对主键进行更新操作。

优化查询 latestIndexedTable 的方法和相关案例请参照函数 indexedTable。

## 例子

例1. 创建索引表

第一种写法：

```
sym=`A`B`C`D`E
id=5 4 3 2 1
val=52 64 25 48 71
timeCol = 2022.12.07T00:00:00.001+0..4
t=latestIndexedTable(`sym`id,`timeCol,sym,id,timeCol,val)
t;
```

输出返回：

| sym | id | timeCol | val |
| --- | --- | --- | --- |
| A | 5 | 2022.12.07T00:00:00.001 | 52 |
| B | 4 | 2022.12.07T00:00:00.002 | 64 |
| C | 3 | 2022.12.07T00:00:00.003 | 25 |
| D | 2 | 2022.12.07T00:00:00.004 | 48 |
| E | 1 | 2022.12.07T00:00:00.005 | 71 |

第二种写法：

```
t=latestIndexedTable(`sym`id,`timeCol, 1:0,`sym`id`timeCol`val,[SYMBOL,INT,TIMESTAMP, INT])
insert into t values(`A`B`C`D`E,5 4 3 2 1,2022.12.07T00:00:00.001+0..4,52 64 25 48 71);
```

第三种写法：

```
tmp=table(sym, id, timeCol, val)
t=latestIndexedTable(`sym`id, `timeCol, tmp);
```

例2. 更新内存表

插入新记录，并且新记录中的主键值与表中主键值重复，根据时间列来确定保留哪条记录：

```
insert into t values(`A`A`E,5 5 1, 2022.12.07T00:00:00.001 2022.12.07T00:00:00.007 2022.12.07T00:00:00.003, 44 66 28);
t;
```

输出返回：

| sym | id | timeCol | val |
| --- | --- | --- | --- |
| A | 5 | 2022.12.07T00:00:00.007 | 66 |
| B | 4 | 2022.12.07T00:00:00.002 | 64 |
| C | 3 | 2022.12.07T00:00:00.003 | 25 |
| D | 2 | 2022.12.07T00:00:00.004 | 48 |
| E | 1 | 2022.12.07T00:00:00.005 | 71 |

相关函数：[keyedTable](../k/keyedTable.md), [indexedTable](../i/indexedTable.md), [latestKeyedTable](latestKeyedTable.md)

