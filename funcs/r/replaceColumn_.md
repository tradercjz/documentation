# replaceColumn!

## 语法

`replaceColumn!(table, colName, newCol)`

## 参数

**table** 非共享内存表或分布式表（仅支持 OLAP 引擎）。

**colName** 字符串，表示要替换列的列名。当 *table*
是内存表时，*colName* 也可以是字符串向量，表示多列的列名。

**newCol** 表示用于替换的列值。当 *table* 是内存表时，当 *colName* 为标量时，*newCol*是一个长度与 *table* 行数相同的向量；当 *colName* 为向量时，*newCol* 是一个元组，其元素个数与
*colName* 一致，且每一个元素是一个长度与 *table* 行数相同的向量。当 *table* 是 OLAP
分布式表时，newCol 仅用于提供目标数据类型。

## 详情

* 当 *table* 为内存表时：

  + 使用向量替换 *table* 中指定列。替换后，指定列的数据类型与向量的数据类型一致。支持替换多列（请注意该操作目前不保证原子性，即在遇到一些系统错误时可能出现部分列替换失败的情况）。
  + `replaceColumn!` 与 SQL 中的 [update](../../progr/sql/update.html)
    语句的区别在于，前者可以修改列的值或数据类型，而后者只能修改列的值。
* 当 *table* 为 OLAP 分布式表时，`replaceColumn!`
  仅修改列的数据类型，并遵循以下规则：
  + SYMBOL 类型不支持转换，即不能将 SYMBOL 转换为其他类型，其他类型也不能转换为 SYMBOL。
  + 除 SYMBOL 外，同类别的数据类型间支持相互转换。
  + INTEGRAL 和 FLOATING 类型支持相互转换。
  + INTEGRAL, FLOATING, LITERAL, TEMPORAL 类型支持转换为 STRING 类型。

## 例子

```
sym = `C`MS`MS`MS`IBM`IBM`C`C`C
price= 49.6 29.46 29.52 30.02 174.97 175.23 50.76 50.32 51.29
qty = 2200 1900 2100 3200 6800 5400 1300 2500 8800
timestamp = [09:34:07,09:36:42,09:36:51,09:36:59,09:32:47,09:35:26,09:34:16,09:34:26,09:38:12]
t = table(timestamp, sym, qty, price)
schema(t).colDefs;
```

输出返回：

| name | typeString | typeInt | extra | comment |
| --- | --- | --- | --- | --- |
| timestamp | SECOND | 10 |  |  |
| sym | STRING | 18 |  |  |
| qty | INT | 4 |  |  |
| price | DOUBLE | 16 |  |  |

把 sym 列的数据类型修改为 SYMBOL 类型：

```
syms=symbol(exec sym from t)
replaceColumn!(t,`sym,syms);
schema(t).colDefs;
```

输出返回：

| name | typeString | typeInt | extra | comment |
| --- | --- | --- | --- | --- |
| timestamp | SECOND | 10 |  |  |
| sym | SYMBOL | 17 |  |  |
| qty | INT | 4 |  |  |
| price | DOUBLE | 16 |  |  |

对 price 列和 timestamp
列进行替换：

```
newPrice =round(t.qty)
newTimestamp = minute(t.timestamp)
replaceColumn!(t, `price`timestamp, (newPrice,newTimestamp))
schema(t).colDefs;
```

输出返回：

| name | typeString | typeInt | extra | comment |
| --- | --- | --- | --- | --- |
| timestamp | MINUTE | 9 |  |  |
| sym | SYMBOL | 17 |  |  |
| qty | INT | 4 |  |  |
| price | INT | 4 |  |  |

```
login("admin","123456")
if(existsDatabase("dfs://replaceColumn")){
  dropDatabase("dfs://replaceColumn")
}
n=10
month=take(2012.06.13..2012.06.13, n);
x=rand(1.0, n);
t=table(month, x);
db=database("dfs://replaceColumn", VALUE, 2012.06.13..2012.06.23)
pt = db.createPartitionedTable(t, `pt, `month);
pt.append!(t);
schema(pt).colDefs
```

输出返回：

| name | typeString | typeInt | extra | comment |
| --- | --- | --- | --- | --- |
| month | DATE | 6 |  |  |
| x | DOUBLE | 16 |  |  |

```
newCols=array(INT,0)
replaceColumn!(loadTable("dfs://replaceColumn",`pt), `x, newCols)
schema(pt).colDefs
```

输出返回：

| name | typeString | typeInt | extra | comment |
| --- | --- | --- | --- | --- |
| month | DATE | 6 |  |  |
| x | INT | 4 |  |  |

