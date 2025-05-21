# cgroup by

使用cgroup by（cumulative group)子句可进行累计分组计算，第二组的记录包含第一个组的记录，第三个组的记录包含前两组的记录，以此类推。

若SQL语句使用cgroup by子句，其执行顺序如下：

1. 使用过滤条件（若有）
2. 根据cgroup by的列与group by的列（若有）
3. 对select子句中的项目进行分组计算
4. 根据order by的列（必须使用，且必须属于group by列或cgroup by列）对分组计算结果进行排序
5. 计算累计值。若使用group by，则在每个group by组内计算累计值。

**注意**：cgroup by子句必须与order by子句一同使用，以在执行累积计算前，将分组计算结果排序。

使用cgroup by的SQL语句只支持以下聚合函数：*sum, sum2, sum3, sum4, prod, max, min, first, last, count,
size, avg, std, var, skew, kurtosis, wsum, wavg, corr, covar, contextCount,
contextSum, contextSum2*.

## 例子

下例使用cgroup by计算交易量加权平均交易价格（volume weighted average price, 简称vwap）。

```
 t = table(`A`A`A`A`B`B`B`B as sym, 09:30:06 09:30:28 09:31:46 09:31:59 09:30:19 09:30:43 09:31:23 09:31:56 as time, 10 20 10 30 20 40 30 30 as volume, 10.05 10.06 10.07 10.05 20.12 20.13 20.14 20.15 as price);
t;
```

| sym | time | volume | price |
| --- | --- | --- | --- |
| A | 09:30:06 | 10 | 10.05 |
| A | 09:30:28 | 20 | 10.06 |
| A | 09:31:46 | 10 | 10.07 |
| A | 09:31:59 | 30 | 10.05 |
| B | 09:30:19 | 20 | 20.12 |
| B | 09:30:43 | 40 | 20.13 |
| B | 09:31:23 | 30 | 20.14 |
| B | 09:31:56 | 30 | 20.15 |

```

select wavg(price, volume) as vwap from t where sym=`A cgroup by minute(time) as minute order by minute;
```

| time | vwap |
| --- | --- |
| 09:30m | 10.056667 |
| 09:31m | 10.055714 |

cgroup by可以与group by配合使用：

```
 select wavg(price, volume) as vwap from t group by sym cgroup by minute(time) as minute order by minute;
```

| sym | minute | vwap |
| --- | --- | --- |
| A | 09:30m | 10.056667 |
| B | 09:30m | 20.126667 |
| A | 09:31m | 10.055714 |
| B | 09:31m | 20.135833 |

```
 select wavg(price, volume) as vwap from t group by sym cgroup by minute(time) as minute order by sym, minute;
```

| sym | minute | vwap |
| --- | --- | --- |
| A | 09:30m | 10.056667 |
| A | 09:31m | 10.055714 |
| B | 09:30m | 20.126667 |
| B | 09:31m | 20.135833 |

Copyright

**©2025 浙江智臾科技有限公司 浙ICP备18048711号-3**
