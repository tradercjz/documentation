# left join/left outer join

## 语法

### 左连接

```
lj(leftTable, rightTable, matchingCols, [rightMatchingCols], [leftFilter], [rightFilter])
```

### 兼容SQL的左连接语法

```
select column_name(s)
from leftTable left [outer] join rightTable
on leftTable.matchingCol=rightTable.rightMatchingCol and [filter]
```

### 左半连接

```
lsj(leftTable, rightTable, matchingCols, [rightMatchingCols], [leftFilter], [rightFilter])
```

### 兼容SQL的左半连接语法

```
select column_name(s)
from leftTable left semijoin rightTable
on leftTable.matchingCol=rightTable.rightMatchingCol and [filter]
```

**注意**：兼容 SQL 语法的 left join 与 left semijoin 不支持以下几点：

1. 如果有多个连接列，必须使用 and 连接。
2. 不能和 update 关键字一起使用。
3. 若 *leftTable* 不是分布式表，则其 *rightTable* 也不能是分布式表。

## 参数

* **leftTable** 和 **rightTable** 是连接的表。
* **matchingCols** 是表示连接列的字符串标量或向量。
* **rightMatchingCols** 是表示右表连接列的字符串标量或向量。当 *leftTable* 和
  *rightTable* 至少有一个连接列不同时，必须指定
  *rightMatchingCols*。返回结果中的连接列与左表的连接列名称相同。
* **filter**为条件表达式，作为连接时的过滤条件。暂时只支持通过 and 连接多个过滤条件，不支持 or。
* **leftFilter** 和 **rightFilter** 条件表达式，作为左右表字段的过滤条件。多个条件之间用 and 或 or
  连接。

## 详情

左连接(lj)返回左表中所有与右表匹配的记录。如果右表中没有匹配的记录，将会返回NULL。如果右表中有多条匹配记录，将会返回所有的匹配记录。因此，lj返回结果的行数有可能比左表的行数多。

左半连接(lsj)和左连接(lj)的唯一区别是，如果右表中有多条匹配记录，lsj将会取第一条的匹配记录。因此，lsj返回结果的行数与左表的行数相等。

## 例子

*例1. 两个表左连接，除了连接列之外没有其他相同列名：*

```
t1= table(1 2 3 3 as id, 7.8 4.6 5.1 0.1 as value)
t2 = table(5 3 1 as id,  300 500 800 as qty);
t1;
```

| id | value |
| --- | --- |
| 1 | 7.8 |
| 2 | 4.6 |
| 3 | 5.1 |
| 3 | 0.1 |

```
t2;
```

| id | qty |
| --- | --- |
| 5 | 300 |
| 3 | 500 |
| 1 | 800 |

```
select id, value, qty from lj(t1, t2, `id);
//等价于  select id, value, qty from t1 left join t2 on t1.id=t2.id
```

| id | value | qty |
| --- | --- | --- |
| 1 | 7.8 | 800 |
| 2 | 4.6 |  |
| 3 | 5.1 | 500 |
| 3 | 0.1 | 500 |

我们无需指定value和qty来自哪个表。系统首先会在左表中定位这两个列，如果左表没有这两个列，系统会在右表定位。

```
select id, value, qty from lj(t2, t1, `id);
//等价于  select id, value, qty from t2 left join t1 on t2.id=t1.id
```

| id | value | qty |
| --- | --- | --- |
| 5 |  | 300 |
| 3 | 5.1 | 500 |
| 3 | 0.1 | 500 |
| 1 | 7.8 | 800 |

```
select id, value, qty from lsj(t2, t1, `id);
//等价于  select  id, value, qty from t2 left semijoin t1 on t2.id=t1.id
```

| id | value | qty |
| --- | --- | --- |
| 5 |  | 300 |
| 3 | 5.1 | 500 |
| 1 | 7.8 | 800 |

通过上面的例子，我们可以看到lj和lsj的区别。lj返回了右表中所有id=3的记录，lsj只返回了右表中第一条id=3的记录。

*例2. 两个表左连接，它们具有相同列名，但是不作为连接列：*

```
t1 = table(1 2 3 3 as id, 7.8 4.6 5.1 0.1 as value, 4 3 2 1 as x)
t2 = table(5 3 1 as id,  300 500 800 as qty, 44 66 88 as x);
t1;
```

| id | value | x |
| --- | --- | --- |
| 1 | 7.8 | 4 |
| 2 | 4.6 | 3 |
| 3 | 5.1 | 2 |
| 3 | 0.1 | 1 |

```
t2;
```

| id | qty | x |
| --- | --- | --- |
| 5 | 300 | 44 |
| 3 | 500 | 66 |
| 1 | 800 | 88 |

```
select id, value, qty, x from lj(t1, t2, `id);
//等价于  select  id, value, qty, x from t1 left join t2 on t1.id=t2.id
```

| id | value | qty | x |
| --- | --- | --- | --- |
| 1 | 7.8 | 800 | 4 |
| 2 | 4.6 |  | 3 |
| 3 | 5.1 | 500 | 2 |
| 3 | 0.1 | 500 | 1 |

```
select id, value, qty, t2.x from lj(t1, t2, `id);
//等价于  select  id, value, qty, t2.x from t1 left join t2 on t1.id=t2.id
```

| id | value | qty | x |
| --- | --- | --- | --- |
| 1 | 7.8 | 800 | 88 |
| 2 | 4.6 |  |  |
| 3 | 5.1 | 500 | 66 |
| 3 | 0.1 | 500 | 66 |

如果左表(t1)和右表(t2)有除连接列以外其他相同的字段名(x)，我们从右表(t2)中选择字段名为x的数据时，需要指定x所在的表：t2.x。

```
lj(t1, t2, `id);
```

| id | value | x | qty | t2\_x |
| --- | --- | --- | --- | --- |
| 1 | 7.8 | 4 | 800 | 88 |
| 2 | 4.6 | 3 |  |  |
| 3 | 5.1 | 2 | 500 | 66 |
| 3 | 0.1 | 1 | 500 | 66 |

在上面的例子中，从t1和t2选择字段名为x的数据，并且把结果中t2的x字段重命名为t2\_x。

*例3. 多个连接列：*

```
t1=table(1 1 2 2 3 3 as x, 1 2 2 3 3 4 as y, 1..6 as a);
t2=table(0 1 1 2 2 3 as x, 1 2 3 3 4 5 as y, 11..16 as b);
t1;
```

| x | y | a |
| --- | --- | --- |
| 1 | 1 | 1 |
| 1 | 2 | 2 |
| 2 | 2 | 3 |
| 2 | 3 | 4 |
| 3 | 3 | 5 |
| 3 | 4 | 6 |

```
t2;
```

| x | y | b |
| --- | --- | --- |
| 0 | 1 | 11 |
| 1 | 2 | 12 |
| 1 | 3 | 13 |
| 2 | 3 | 14 |
| 2 | 4 | 15 |
| 3 | 5 | 16 |

```
lj(t1, t2, `x`y);
// x, y是连接列
```

| x | y | a | b |
| --- | --- | --- | --- |
| 1 | 1 | 1 |  |
| 1 | 2 | 2 | 12 |
| 2 | 2 | 3 |  |
| 2 | 3 | 4 | 14 |
| 3 | 3 | 5 |  |
| 3 | 4 | 6 |  |

```
t2.rename!(`x`y, `x2`y2);
```

| x2 | y2 | b |
| --- | --- | --- |
| 0 | 1 | 11 |
| 1 | 2 | 12 |
| 1 | 3 | 13 |
| 2 | 3 | 14 |
| 2 | 4 | 15 |
| 3 | 5 | 16 |

```
lj(t1, t2, `x`y, `x2`y2);
// t1.x, t1.y t2.x2, t2.y2是连接列
```

| x | y | a | b |
| --- | --- | --- | --- |
| 1 | 1 | 1 |  |
| 1 | 2 | 2 | 12 |
| 2 | 2 | 3 |  |
| 2 | 3 | 4 | 14 |
| 3 | 3 | 5 |  |
| 3 | 4 | 6 |  |

*例4. 指定过滤条件*

```
t1= table(1 2 3 3 as id1, 7.8 4.6 5.1 0.1 as value)
t2 = table(5 3 1 as id2, 300 500 800 as qty);
select * from lj(t1, t2, `id1, `id2, t1.value>1 and t1.value<6, t2.qty>300)
```

| id1 | value | qty |
| --- | --- | --- |
| 1 | 7.8 |  |
| 2 | 4.6 |  |
| 3 | 5.1 | 500 |
| 3 | 0.1 |  |

```
t1= table(1 2 3 3 6 8 as id, 7.8 4.6 5.1 0.1 0.5 1.2 as value)
t2 = table(5 3 1 2 6 8 as id, 300 500 800 400 600 700 as qty);
select * from t1 left join t2 on t1.id=t2.id and t2.qty>=550
```

| id | value | qty |
| --- | --- | --- |
| 1 | 7.8 | 800 |
| 2 | 4.6 |  |
| 3 | 5.1 |  |
| 3 | 0.1 |  |
| 6 | 0.5 | 600 |
| 8 | 1.2 | 700 |

