# inner join

## 语法

等值连接，又称内连接。

```
select column_name(s) from leftTable inner join rightTable on leftTable.matchingCol=rightTable.rightMatchingCol
```

或

```
select column_name(s)
from table1 inner join table2
on table1.column_name=table2.column_name and [filter]
```

## 参数

**filter** 为条件表达式，作为连接时的过滤条件。暂时只支持通过 and 连接多个过滤条件，不支持 or。

## 详情

返回与连接列匹配的行。该函数返回结果与 [equijoin](equijoin.md)
相同。

**注意**：

1. 如果有多个连接列，必须使用 and 连接。
2. 不能和 update 关键字一起使用。

## 例子

例1. 两个表等值连接，除了连接列外没有其他名称相同的列

```
t1= table(1 2 3 3 as id, 7.8 4.6 5.1 0.1 as value)
t2 = table(5 3 1 as id, 300 500 800 as qty);
select id, value, qty from t1 inner join t2 on t1.id=t2.id
```

| id | value | qty |
| --- | --- | --- |
| 1 | 7.8 | 800 |
| 3 | 5.1 | 500 |
| 3 | 0.1 | 500 |

```
select id, value, qty from t1 inner join t2 on t1.id=t2.id where id=3
```

| id | value | qty |
| --- | --- | --- |
| 3 | 5.1 | 500 |
| 3 | 0.1 | 500 |

例2. 等值连接两张表，它们含有相同名字的列，但是不以它作为连接列：

```
t3 = table(1 2 3 3 as id, 7.8 4.6 5.1 0.1 as value, 64 73 52 66 as x);
t4 = table(5 3 1 as id,  300 500 800 as qty, 44 66 88 as x) ;
select id, value, qty, x from t3 inner join t4 on t3.id=t4.id
```

| id | value | qty | x |
| --- | --- | --- | --- |
| 1 | 7.8 | 800 | 64 |
| 3 | 5.1 | 500 | 52 |
| 3 | 0.1 | 500 | 66 |

若不指定value与qty来自何表，系统首先会在左表中定位这两个列，如果左表没有这两个列，系统会在右表定位。

```
select id, value, qty, t4.x from t3 inner join t4 on t3.id=t4.id
```

| id | value | qty | x |
| --- | --- | --- | --- |
| 1 | 7.8 | 800 | 88 |
| 3 | 5.1 | 500 | 52 |
| 3 | 0.1 | 500 | 66 |

例3. 多个连接列：

```
select id, value, qty, x from t3 inner join t4 on t3.id=t4.id and t3.x=t4.x
```

| id | value | qty | x |
| --- | --- | --- | --- |
| 3 | 0.1 | 500 | 66 |

例4. 分布式表连接：

```
dbName1="dfs://sql_inner_join"
if(existsDatabase(dbName1)){
  dropDatabase(dbName1)
}
db1=database(dbName1, RANGE, 1 30 70 101)
t1=table("A"+string(1..100) as sym, 1..100 as val)
pt1=db1.createPartitionedTable(t1, `pt1, `val).append!(t1)
t2=table("A"+string(1..20) as sym, 1..20 as val)
pt2=db1.createPartitionedTable(t2, `pt2, `val).append!(t2)

select * from pt1 inner join pt2 on pt1.val=pt2.val
```

| sym | val | pt2\_sym |
| --- | --- | --- |
| A1 | 1 | A1 |
| A2 | 2 | A2 |
| A3 | 3 | A3 |
| A4 | 4 | A4 |
| A5 | 5 | A5 |
| A6 | 6 | A6 |
| A7 | 7 | A7 |
| A8 | 8 | A8 |
| A9 | 9 | A9 |
| A10 | 10 | A10 |
| A11 | 11 | A11 |
| A12 | 12 | A12 |
| A13 | 13 | A13 |
| A14 | 14 | A14 |
| A15 | 15 | A15 |
| A16 | 16 | A16 |
| A17 | 17 | A17 |
| A18 | 18 | A18 |
| A19 | 19 | A19 |
| A20 | 20 | A20 |

例5. 指定 *filter*

```
t1= table(1 2 3 3 6 8 as id, 7.8 4.6 5.1 0.1 0.5 1.2 as value)
t2 = table(5 3 1 2 6 8 as id, 300 500 800 400 600 700 as qty);
select * from t1 inner join t2 on t1.id=t2.id and t1.id>=3
```

| id | value | qty |
| --- | --- | --- |
| 3 | 5.1 | 500 |
| 3 | 0.1 | 500 |
| 6 | 0.5 | 600 |
| 8 | 1.2 | 700 |

