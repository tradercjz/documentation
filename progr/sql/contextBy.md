# context by

context by 是 DolphinDB 的独有功能，是对标准 SQL 语句的拓展。使用 context by 子句可以简化对时间序列数据的操作。

传统的关系型数据库不支持时间序列数据处理。在关系型数据库管理系统 (RDBMS) 中，一张表由行的集合组成，行之间没有顺序。尽管可以使用如 min, max, avg
等聚合函数来对行进行分组，但是不能在分组内的行使用顺序敏感的聚合函数，比如 first, last 等，或者对顺序敏感的向量函数，如 cumsum, cummax,
ratios, deltas 等。

DolphinDB 支持时间序列数据处理。context by 子句使组内处理时间序列数据更加方便。

context by 与 group by 类似，都对数据进行分组。但是，用 group by 时，每一组返回一个标量值，而用 context by
时，每一组返回一个和组内元素数量相同的向量。group by 只能配合聚合函数使用，而 context by
既可以配合聚合函数使用，也可以与移动窗口函数或累积函数等其它函数结合使用。context by 常用于基于组更新的场景，请参考 [update](update.md) 语句的例子。context by 还可以和 having 子句一起使用，详情参考 [having](having.md)。

context by 通常与 [cumsum](../../funcs/c/cumsum.md),
[mavg](../../funcs/m/mavg.md) 等时间序列函数一起使用，每个分组中记录的顺序对结果有直接影响。可在
context by 语句后使用 csort 关键字排序。使用 context by 分组后，csort 在 select
从句的表达式执行之前，对每个组内的数据进行排序。可对多个列（包括计算列）使用 csort 关键字，在组内进行升序（asc）或降序（desc）排序，若 csort
后不指定排序关键字，则默认是升序。csort 关键字还可以和 top 关键字一起使用，用于获取每个分组中的最新记录。

下例展示了 group by 和 context by 的不同之处。

```
sym = `C`MS`MS`MS`IBM`IBM`C`C`C$SYMBOL
price= 49.6 29.46 29.52 30.02 174.97 175.23 50.76 50.32 51.29
qty = 2200 1900 2100 3200 6800 5400 1300 2500 8800
timestamp = [09:34:07,09:36:42,09:36:51,09:36:59,09:32:47,09:35:26,09:34:16,09:34:26,09:38:12]
t1 = table(timestamp, sym, qty, price);

t1;
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:34:07 | C | 2200 | 49.6 |
| 09:36:42 | MS | 1900 | 29.46 |
| 09:36:51 | MS | 2100 | 29.52 |
| 09:36:59 | MS | 3200 | 30.02 |
| 09:32:47 | IBM | 6800 | 174.97 |
| 09:35:26 | IBM | 5400 | 175.23 |
| 09:34:16 | C | 1300 | 50.76 |
| 09:34:26 | C | 2500 | 50.32 |
| 09:38:12 | C | 8800 | 51.29 |

```
select wavg(price,qty) as wvap, sum(qty) as totalqty from t1 group by sym;
```

| sym | wvap | totalqty |
| --- | --- | --- |
| C | 50.828378 | 14800 |
| IBM | 175.085082 | 12200 |
| MS | 29.726389 | 7200 |

```
select sym, price, qty, wavg(price,qty) as wvap, sum(qty) as totalqty from t1 context by sym;
```

| sym | price | qty | wvap | totalqty |
| --- | --- | --- | --- | --- |
| C | 49.6 | 2200 | 50.828378 | 14800 |
| C | 50.76 | 1300 | 50.828378 | 14800 |
| C | 50.32 | 2500 | 50.828378 | 14800 |
| C | 51.29 | 8800 | 50.828378 | 14800 |
| IBM | 174.97 | 6800 | 175.085082 | 12200 |
| IBM | 175.23 | 5400 | 175.085082 | 12200 |
| MS | 29.46 | 1900 | 29.726389 | 7200 |
| MS | 29.52 | 2100 | 29.726389 | 7200 |
| MS | 30.02 | 3200 | 29.726389 | 7200 |

计算每家公司的股票收益，我们不能使用 group by，但是可以使用 context by 和 [ratio](../operators/ratio.md) 函数。在使用 context by
之前，需要确保记录在每一组内已按时间排好序。

```
select sym, timestamp, price, eachPre(\,price)-1.0 as ret from t1 context by sym;
```

| sym | timestamp | price | ret |
| --- | --- | --- | --- |
| C | 09:34:07 | 49.6 |  |
| C | 09:34:16 | 50.76 | 0.023387 |
| C | 09:34:26 | 50.32 | -0.008668 |
| C | 09:38:12 | 51.29 | 0.019277 |
| IBM | 09:32:47 | 174.97 |  |
| IBM | 09:35:26 | 175.23 | 0.001486 |
| MS | 09:36:42 | 29.46 |  |
| MS | 09:36:51 | 29.52 | 0.002037 |
| MS | 09:36:59 | 30.02 | 0.016938 |

可以使用 [contextby](../../funcs/ho_funcs/contextby.md)
高阶函数来达到同样的效果，但是结果是一个向量而不是表。

```
contextby(eachPre{ratio}, t1.price, t1.sym);
// output
[,,1.002037,1.016938,,1.001486,1.023387,0.991332,1.019277]
```

这里用了一个部分应用 `eachPre{ratio}`。详情参考 [PartialApplication](../partial_app.md)。

对每个股票，计算每分钟累计交易量：

```
select *, cumsum(qty) from t1 context by sym, timestamp.minute();
```

| timestamp | sym | qty | price | cumsum\_qty |
| --- | --- | --- | --- | --- |
| 09:34:07 | C | 2200 | 49.6 | 2200 |
| 09:34:16 | C | 1300 | 50.76 | 3500 |
| 09:34:26 | C | 2500 | 50.32 | 6000 |
| 09:38:12 | C | 8800 | 51.29 | 8800 |
| 09:32:47 | IBM | 6800 | 174.97 | 6800 |
| 09:35:26 | IBM | 5400 | 175.23 | 5400 |
| 09:36:42 | MS | 1900 | 29.46 | 1900 |
| 09:36:51 | MS | 2100 | 29.52 | 4000 |
| 09:36:59 | MS | 3200 | 30.02 | 7200 |

和 top 子句一起使用：

```
select top 2 * from t1 context by sym;
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:34:07 | C | 2200 | 49.6 |
| 09:34:16 | C | 1300 | 50.76 |
| 09:32:47 | IBM | 6800 | 174.97 |
| 09:35:26 | IBM | 5400 | 175.23 |
| 09:36:42 | MS | 1900 | 29.46 |
| 09:36:51 | MS | 2100 | 29.52 |

和 top 子句一起使用时，不允许在 top 子句中指定一个范围：

```
select top 2:3 * from t1 context by sym;
// output
Syntax Error: [line #2] When top clause uses together with context clause in SQL query, can't specify a range in top clause
```

context by 与 csort、top 子句一起使用，获取每只股票时间最近两条记录：

```
select top 2 * from t1 context by sym csort timestamp desc;
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:38:12 | C | 8800 | 51.29 |
| 09:34:26 | C | 2500 | 50.32 |
| 09:35:26 | IBM | 5400 | 175.23 |
| 09:32:47 | IBM | 6800 | 174.97 |
| 09:36:59 | MS | 3200 | 30.02 |
| 09:36:51 | MS | 2100 | 29.52 |

context by 与 limit 一起使用能够获取表中每个分组前 n 条记录或最后 n 条记录。如果 limit 后面为正数，表示取前 n 条记录；如果 limit
后面为负数，表示取最后 n 条记录。例如，获取每只股票的前 2 条记录：

```
select * from t1 context by sym limit 2;
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:34:07 | C | 2200 | 49.6 |
| 09:36:42 | MS | 1900 | 29.46 |
| 09:36:51 | MS | 2100 | 29.52 |
| 09:32:47 | IBM | 6800 | 174.97 |
| 09:35:26 | IBM | 5400 | 175.23 |
| 09:34:16 | C | 1300 | 50.76 |

获取每只股票最后两条记录：

```
select * from t1 context by sym limit -2;
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:36:51 | MS | 2100 | 29.52 |
| 09:36:59 | MS | 3200 | 30.02 |
| 09:32:47 | IBM | 6800 | 174.97 |
| 09:35:26 | IBM | 5400 | 175.23 |
| 09:34:26 | C | 2500 | 50.32 |
| 09:38:12 | C | 8800 | 51.29 |

context by 与 csort, limit 一起使用能够获取表中每个分组排序后的前 n 条记录或最后 n 条记录：

```
select * from t1 context by sym csort qty limit -2;
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:34:26 | C | 2500 | 50.32 |
| 09:38:12 | C | 8800 | 51.29 |
| 09:35:26 | IBM | 5400 | 175.23 |
| 09:32:47 | IBM | 6800 | 174.97 |
| 09:36:51 | MS | 2100 | 29.52 |
| 09:36:59 | MS | 3200 | 30.02 |

从每个股票价格对数量的回归模型，计算价格的拟合值。

```
select *, ols(price, qty)[0]+ols(price, qty)[1]*qty as fittedPrice from t1 context by sym;
```

| timestamp | sym | qty | price | fittedPrice |
| --- | --- | --- | --- | --- |
| 09:34:07 | C | 2200 | 49.6 | 50.282221 |
| 09:34:16 | C | 1300 | 50.76 | 50.156053 |
| 09:34:26 | C | 2500 | 50.32 | 50.324277 |
| 09:38:12 | C | 8800 | 51.29 | 51.207449 |
| 09:32:47 | IBM | 6800 | 174.97 | 174.97 |
| 09:35:26 | IBM | 5400 | 175.23 | 175.23 |
| 09:36:42 | MS | 1900 | 29.46 | 29.447279 |
| 09:36:51 | MS | 2100 | 29.52 | 29.535034 |
| 09:36:59 | MS | 3200 | 30.02 | 30.017687 |

context by 和 order by 配合使用。order by 的字段必须是 context by 结果表中的字段。

```
select *, ols(price, qty)[0]+ols(price, qty)[1]*qty as fittedPrice from t1 context by sym order by timestamp;
```

| timestamp | sym | qty | price | fittedPrice |
| --- | --- | --- | --- | --- |
| 09:32:47 | IBM | 6800 | 174.97 | 174.97 |
| 09:34:07 | C | 2200 | 49.6 | 50.075318 |
| 09:34:16 | C | 1300 | 50.76 | 49.911222 |
| 09:34:26 | C | 2500 | 50.32 | 50.130017 |
| 09:35:26 | IBM | 5400 | 175.23 | 175.23 |
| 09:36:42 | MS | 1900 | 29.46 | 29.447279 |
| 09:36:51 | MS | 2100 | 29.52 | 29.535034 |
| 09:36:59 | MS | 3200 | 30.02 | 30.017687 |
| 09:38:12 | C | 8800 | 51.29 | 51.278686 |

请注意，以上例子仅用于展示，股票价格对交易量的回归没有经济意义。

context by 与 contextby 函数的区别主要有以下三个方面：

1. contextby 生成一个向量，而 context by 在 select 语句中使用中，结果为数据表。
2. contextby 只能使用一个列进行分组，而 context by 子句可以使用多个列进行分组。
3. contextby 每次调用都只对一个列进行计算，因此如果要对多列进行计算，contextby 效率不高。使用 context by
   可以一次性完成分组，再同时对多列进行计算。

## 提高性能的技巧

在使用 context by 之前，若对数据按照 context by 的列进行排序，可加快 context by 的运行速度。

```
n=1000000
ID=rand(100, n)
x=rand(10.0, n)
ta=table(ID, x)
tb=select * from ta order by ID;
```

```
timer select (NULL \:P x)-1 as ret from ta context by ID;
// output
Time elapsed: 4.018 ms

timer select (NULL \:P x)-1 as ret from tb context by ID;
// output
Time elapsed: 2.991 ms
```

在特定条件下使用 context by 子句时，系统内部进行了查询优化：

若要查询分区表中某些组的最新数据，可使用 context by 配合 csort，limit。在满足以下条件时，对 context by + csort + limit
场景，系统对查询语句的性能进行了优化：

1. 在 where 子句中对 context by 列进行了条件过滤。
2. csort 指定的列必须是分区列，且该列的分区方式是 VALUE 或 RANGE。
3. context by 与 csort 只能指定单列。
4. context by 指定的列也需要一起输出（通过 select 语句指定该列）。

可以通过添加 [hint\_explain](hint_explain.md)
关键字查询执行计划来判断是否进行了优化。

Copyright

**©2025 浙江智臾科技有限公司 浙ICP备18048711号-3**
