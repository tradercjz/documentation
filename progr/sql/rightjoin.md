# right join/right outer join

## 语法

### 右连接

```
SELECT column_name(s)
FROM leftTable RIGHT [OUTER] JOIN rightTable
ON leftTable.matchingCol=rightTable.rightMatchingCol and [filter]
```

注： 目前 RIGHT JOIN 不支持以下几点：

1. 暂不支持同时连接两个以上的表。
2. 如果有多个连接列，必须使用 AND 连接。
3. 不能和 UPDATE 关键字一起使用。

## 参数

**filter**为条件表达式，作为连接时的过滤条件。暂时只支持通过 AND 连接多个过滤条件，不支持 OR。

## 详情

右连接返回右表中所有与左表匹配的记录。如果左表中没有匹配的记录，将会返回NULL。如果左表中有多条匹配记录，将会返回所有的匹配记录。因此，右连接返回结果的行数有可能比右表的行数多。

## 例子

*例1. 两个表右连接，除了连接列之外没有其他相同列名：*

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
SELECT id, value, qty FROM t1 RIGHT OUTER JOIN t2 ON t1.id=t2.id
//等价于 SELECT id, value, qty FROM t1 RIGHT JOIN t2 ON t1.id=t2.id
```

| id | value | qty |
| --- | --- | --- |
|  |  | 300 |
| 3 | 5.1 | 500 |
| 3 | 0.1 | 500 |
| 1 | 7.8 | 800 |

我们无需指定value和qty来自哪个表。系统首先会在左表中定位这两个列，如果左表没有这两个列，系统会在右表定位。

```
SELECT id, value, qty FROM t2 RIGHT JOIN t1 ON t2.id=t1.id
```

| id | value | qty |
| --- | --- | --- |
| 1 | 7.8 | 800 |
|  | 4.6 |  |
| 3 | 5.1 | 500 |
| 3 | 0.1 | 800 |

例2. 两个表右连接，它们具有相同列名，但是不作为连接列：

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
SELECT id, value, qty, x FROM t1 RIGHT JOIN t2 ON t1.id=t2.id
```

| id | value | qty | x |
| --- | --- | --- | --- |
|  |  | 300 |  |
| 3 | 5.1 | 500 | 2 |
| 3 | 0.1 | 500 | 1 |
| 1 | 7.8 | 800 | 4 |

```
SELECT id, value, qty, t1.x FROM t1 RIGHT JOIN t2 ON t1.id=t2.id
```

| id | value | qty | x |
| --- | --- | --- | --- |
|  |  | 300 |  |
| 3 | 5.1 | 500 | 2 |
| 3 | 0.1 | 500 | 1 |
| 1 | 7.8 | 800 | 4 |

如果左表(t1)和右表(t2)有除连接列以外其他相同的字段名(x)，我们从右表(t2)中选择字段名为x的数据时，需要指定x所在的表：t2.x。

```
SELECT  * FROM t1 RIGHT JOIN t2 ON t1.id=t2.id
```

| value | x | id | qty | t2\_x |
| --- | --- | --- | --- | --- |
|  |  | 5 | 300 | 44 |
| 5.1 | 2 | 3 | 500 | 66 |
| 0.1 | 1 | 3 | 500 | 66 |
| 7.8 | 4 | 1 | 800 | 88 |

在上面的例子中，从t1和t2选择字段名为x的数据，并且把结果中t2的x字段重命名为t2\_x。

*例3. 多个连接列：*

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
SELECT * FROM t1 RIGHT JOIN t2 ON t1.x=t2.x AND t1.y=t2.y
// x, y是连接列
```

| a | x | y | b |
| --- | --- | --- | --- |
|  | 0 | 1 | 11 |
| 2 | 1 | 2 | 12 |
|  | 1 | 3 | 13 |
| 4 | 2 | 3 | 14 |
|  | 2 | 4 | 15 |
|  | 3 | 5 | 16 |

```
t2.rename!(`x`y, `x2`y2);
t2
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
SELECT * FROM t1 RIGHT JOIN t2 ON t1.x=t2.x2 AND t1.y=t2.y2
// t1.x, t1.y t2.x2, t2.y2是连接列
```

| a | x2 | y2 | b |
| --- | --- | --- | --- |
|  | 0 | 1 | 11 |
| 2 | 1 | 2 | 12 |
|  | 1 | 3 | 13 |
| 4 | 2 | 3 | 14 |
|  | 2 | 4 | 15 |
|  | 3 | 5 | 16 |

*例4. 指定过滤条件*

```
t1= table(1 2 3 3 as id1, 7.8 4.6 5.1 0.1 as value)
t2 = table(5 3 1 as id2, 300 500 800 as qty);
SELECT * FROM t1 RIGHT JOIN t2 ON t1.id1=t2.id2 AND t1.value>1 AND t1.value<6 AND t2.qty>300
```

| value | id2 | qty |
| --- | --- | --- |
|  | 5 | 300 |
| 5.1 | 3 | 500 |
|  | 1 | 800 |

