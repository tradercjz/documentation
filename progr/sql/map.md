# map

使用 map 关键字，SQL 语句会在每个分区内分别执行，然后输出每个分区的执行结果。

适合使用 map 关键字的场景：

* 场景一：需要在每个分区内进行查询的场景（见 例子 1）
* 场景二：分组查询计算提升性能（见 例子 2）

对分组数据进行查询和计算时，通常先在各个分区单独计算，然后将结果进行进一步计算以保证最终结果的正确性。如果分区的粒度大于分组的粒度，从而可以确保数据的查询和计算不会跨分区进行，则可添加
map 关键字，避免进一步计算的开销，从而提升查询性能。

注： SQL where 子句中一般不允许使用聚合函数或序列相关函数，原因在于：

* 若允许则会进行全表扫描计算，无法进行分区剪枝。
* 但若使用 map 关键字，则允许在 where
  子句中使用聚合函数或序列相关函数，在每个分区内部进行指定计算以过滤记录。（见 例子 3）

## 例子

### 分区计算

```
t = table(0..9 as id, take(1 2 3, 10) as qty)
db=database("dfs://rangedb", RANGE, 0 5 10)
pt = db.createPartitionedTable(t, `pt, `id)
pt.append!(t);

select * from pt;
```

| id | qty |
| --- | --- |
| 0 | 1 |
| 1 | 2 |
| 2 | 3 |
| 3 | 1 |
| 4 | 2 |
| 5 | 3 |
| 6 | 1 |
| 7 | 2 |
| 8 | 3 |
| 9 | 1 |

```
select first(id), count(*) from pt map;
```

| first\_id | count |
| --- | --- |
| 0 | 5 |
| 5 | 5 |

### 合理使用 map 关键字

合理使用 map 关键字有助于在分组查询和计算时提升性能：

```
t = table(2022.01.01T00:00:00 + rand(10000000, 10000) as dateTime, rand(1000, 10000) as qty)
if(existsDatabase("dfs://valuedb")) dropDatabase("dfs://valuedb")
db=database("dfs://valuedb", VALUE, 2022.02.01..2022.02.05)
pt = db.createPartitionedTable(t, `pt, `dateTime)
pt.append!(t)

timer(1000) select count(*) from pt group by bar(dateTime, 60)

Time elapsed: 4010.31 ms

timer(1000) select count(*) from pt group by bar(dateTime, 60) map

Time elapsed: 3607.331 ms
```

### 跨分区查询

跨分区查询时，指定 map 关键字，以支持在 where 子句中使用聚合函数或者序列相关函数进行条件过滤

```
t = table(0..9 as id, take(1 2 3, 10) as qty)
db=database("dfs://rangedb", RANGE, 0 5 10)
pt = db.createPartitionedTable(t, `pt, `id)
pt.append!(t);

select * from pt where isDuplicated([id,qty]) = false map;
```

| id | qty |
| --- | --- |
| 0 | 1 |
| 1 | 2 |
| 2 | 3 |
| 3 | 1 |
| 4 | 2 |
| 5 | 3 |
| 6 | 1 |
| 7 | 2 |
| 8 | 3 |
| 9 | 1 |

