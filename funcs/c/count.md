# count

## 语法

`count(X)`

## 参数

**X** 可以是标量、向量、矩阵或表。

## 详情

[size](../s/size.md) 和 `count`
不同。`size` 返回向量/矩阵中元素的个数，而 `count` 返回向量/矩阵中非 NULL
的元素个数。`count` 可以用在 SQL 查询中，而 `size`
不可以。对于表而言，`size` 和 `count` 都返回行数。参见相关函数 [size](../s/size.md)。

`count` 用于 SQL 查询时，有如下三种常见用法：

* `select count(*) from pt` ：返回 pt 表中的数据条数。
* `select count(1) from pt` ：若 pt 为空表，则返回1；否则返回 pt
  表中数据涉及到的分区数量。
* `select count(colName) from pt` ：返回列 colName 中的非空数据的个数。

## 例子

```
count(3 NULL 5 6);
// output
3
size(3 NULL 5 6);
// output
4

m=1 2 3 NULL 4 5$2:3;
m;
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 1 | 3 | 4 |
| 2 |  | 5 |

```
count(m);
// output
5
size(m);
// output
6

t = table(1 NULL 3 as id, 3 NULL 9 as qty);
t;
```

| id | qty |
| --- | --- |
| 1 | 3 |
|  |  |
| 3 | 9 |

```
count(t);
// output
3
size(t);
// output
3
```

```
data = table(2023.10.01 + take(0..9,100) as date, take(['A','B','C','D'],100) as sym, 1..100 as val)

db = database("dfs://demo",VALUE,2023.10.01..2023.10.10)
pt = db.createPartitionedTable(data,`pt,`date)//创建一个分区表

pt.append!(data)  //向表中插入数据

select count(*) from pt;//返回数据条数
```

| count |
| --- |
| 100 |

```
select count(1) from pt;//返回分区数
```

| count |
| --- |
| 10 |

