# equi join

## 语法

* *等值连接*

  ```
  ej(leftTable, rightTable, matchingCols, [rightMatchingCols], [leftFilter], [rightFilter])
  ```

  兼容SQL的语法

  ```
  select *
  from leftTable
  [inner] join rightTable on t1.matchingCol=t2.rightMatchingCol
  [where leftFilter and rightFilter]
  ```
* *有序等值连接：*

  ```
  sej(leftTable, rightTable, matchingCols, [rightMatchingCols], [leftFilter], [rightFilter])
  ```

  兼容SQL的语法

  ```
  select *
  from leftTable
  [inner] join rightTable on leftTable.matchingCol=rightTable.rightMatchingCol
  [where leftFilter and rightFilter]
  order by matchingCol
  ```

## 参数

* **leftTable** 和 **rightTable** 是连接的表。
* **matchingCols** 是表示连接列的字符串标量或向量。
* **rightMatchingCols** 是表示右表连接列的字符串标量或向量。当 *leftTable* 和
  *rightTable* 至少有一个连接列不同时，必须指定
  *rightMatchingCols*。返回结果中的连接列与左表的连接列名称相同。
* **leftFilter** 和 **rightFilter** 条件表达式，作为左右表字段的过滤条件。多个条件之间用 and 或 or
  连接。注意：若 *leftTable* / *rightTable* 指定为维度表或分区表，不支持指定
  *leftFilter*, *rightFilter*。

## 详情

返回与连接列匹配的行。有序等值连接 sej 的结果表会根据连接字段进行排序。

## 例子

例1. 两个表等值连接，除了连接列外没有其他名称相同的列

```
t1= table(1 2 3 3 as id, 7.8 4.6 5.1 0.1 as value)
t2 = table(5 3 1 as id, 300 500 800 as qty);
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
ej(t1, t2,`id);
```

等价于

```
select * from t1 inner join t2 on t1.id=t2.id
```

| id | value | qty |
| --- | --- | --- |
| 1 | 7.8 | 800 |
| 3 | 5.1 | 500 |
| 3 | 0.1 | 500 |

```
 ej(t2, t1,`id);
```

等价于

```
select * from t2 inner join t1 on t2.id=t1.id
```

| id | qty | value |
| --- | --- | --- |
| 3 | 500 | 5.1 |
| 3 | 500 | 0.1 |
| 1 | 800 | 7.8 |

```
ej(t1, t2,`id,, t1.id==3);
```

等价于

```
select * from t1 inner join t2 on t1.id=t2.id  where t1.id=3
```

| id | value | qty |
| --- | --- | --- |
| 3 | 5.1 | 500 |
| 3 | 0.1 | 500 |

例2. 等值连接两张表，它们含有相同名字的列，但是不以它作为连接列：

```
t1 = table(1 2 3 3 as id, 7.8 4.6 5.1 0.1 as value, 4 3 2 1 as x);
t1;
```

| id | value | x |
| --- | --- | --- |
| 1 | 7.8 | 4 |
| 2 | 4.6 | 3 |
| 3 | 5.1 | 2 |
| 3 | 0.1 | 1 |

```
t2 = table(5 3 1 as id,  300 500 800 as qty, 44 66 88 as x) ;
t2;
```

| id | qty | x |
| --- | --- | --- |
| 5 | 300 | 44 |
| 3 | 500 | 66 |
| 1 | 800 | 88 |

```
select id, value, qty, x from ej(t1, t2, `id);
```

等价于

```
select id, value, qty, x from t1 inner join t2 on t1.id=t2.id
```

| id | value | qty | x |
| --- | --- | --- | --- |
| 1 | 7.8 | 800 | 4 |
| 3 | 5.1 | 500 | 2 |
| 3 | 0.1 | 500 | 1 |

我们无需指定value和qty来自哪个表。系统首先会在左表中定位这两个列，如果左表没有这两个列，系统会在右表定位。

```
select id, value, qty, t2.x from ej(t1, t2, `id);
```

等价于

```
select id, value, qty, t2.x from t1 inner join t2 on t1.id=t2.id
```

| id | value | qty | x |
| --- | --- | --- | --- |
| 1 | 7.8 | 800 | 88 |
| 3 | 5.1 | 500 | 66 |
| 3 | 0.1 | 500 | 66 |

```
ej(t1, t2, `id);
```

等价于

```
select * from t1 inner join t2 on t1.id=t2.id
```

| id | value | x | qty | t2\_x |
| --- | --- | --- | --- | --- |
| 1 | 7.8 | 4 | 800 | 88 |
| 3 | 5.1 | 2 | 500 | 66 |
| 3 | 0.1 | 1 | 500 | 66 |

ej选择了t1和t2中的两个x，然后将t2中的x重命名成t2\_x。

例3. 多个连接列：

```
t1=table(1 1 2 2 3 3 as x, 1 2 2 3 3 4 as y, 1..6 as a);
t2=table(0 1 1 2 2 3 as x, 1 2 3 3 4 5 as y, 11..16 as b);
t1;
```

| x | y | z |
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
ej(t1, t2, `x`y);
// x, y是连接列
```

等价于

```
select * from t1 inner join t2 on t1.x=t2.x and t1.y=t2.y
```

| x | y | a | b |
| --- | --- | --- | --- |
| 1 | 2 | 2 | 12 |
| 2 | 3 | 4 | 14 |

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
ej(t1, t2, `x`y, `x2`y2);
// t1.x, t1.y t2.x2, t2.y2是连接列
```

等价于

```
select * from t1 inner join t2 on t1.x=t2.x2 and t1.y=t2.y2
```

| x | y | a | b |
| --- | --- | --- | --- |
| 1 | 2 | 2 | 12 |
| 2 | 3 | 4 | 14 |

例4. 连接表时，可以使用表的别名：

```
table1=table(1 1 2 2 3 3 as x, 1 2 2 3 3 4 as y, 1..6 as a, 21..26 as c)
table2=table(0 1 1 2 2 3 as x, 1 2 3 3 4 5 as y, 4..9 as a, 11..16 as b);
select * from ej(table1 as t1, table2 as t2, `x`y) where t2.a<7;
```

| x | y | a | c | t2\_a | b |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 22 | 5 | 12 |

在自连接时，必须使用表的别名：

```
t = table(`A`A`A`A`B`B`B`B as id, 1 3 6 9 1 9 12 17 as time, 1 2 6 3 5 9 4 0 as x)
select * from ej(t as a, t as b, `id) where a.time=b.time+3;
```

等价于

```
select * from t as a inner join t as b on a.id=b.id where a.time=b.time+3
```

| id | time | x | b\_time | b\_x |
| --- | --- | --- | --- | --- |
| A | 6 | 6 | 3 | 2 |
| A | 9 | 3 | 6 | 6 |
| B | 12 | 4 | 9 | 9 |

例5. 指定 *leftFilter* 和 *rightFilter*

```
t1= table(1 2 3 3 as id1, 7.8 4.6 5.1 0.1 as value)
t2 = table(5 3 1 as id2, 300 500 800 as qty);
select * from ej(t1, t2, `id1, `id2, t1.value>1 and t1.value<6, t2.qty>300)
```

等价于

```
select * from t1 inner join t2 on t1.id1=t2.id2 where t1.value>1 and t1.value<6 and t2.qty>300
```

| id1 | value | qty |
| --- | --- | --- |
| 3 | 5.1 | 500 |

