# case

case 是一个控制流语句，用于 SQL 的条件判断语句，其作用与 if-else 语句相似。

case 语句至少包含一组 when…then… 语句，当满足 when 条件，则返回 then 结果，否则返回 else 后的表达式结果；若没有指定
else，则返回空值。case 语句多个条件的返回结果类型必须一致。case when 语句支持在分布式查询中使用。

## 语法

```
case
    when condition_1 then expression_1
    [when condition_2 then expression_2]
    ...
    [when condition_n then expression_n]
    [else expression_end]
end
```

从 2.00.10 版本开始，不再要求 when 和 then 必须在同一行。

## 例子

```
t = table(`st0`st1`st2`st4`st5`st6 as sym, 80 200 150 220 130 190 as vol)
select sym, case
	when vol < 100 then -1
	when vol < 200 then 0
	else 1
end as flag
from t
```

| sym | flag |
| --- | --- |
| st0 | -1 |
| st1 | 1 |
| st2 | 0 |
| st4 | 1 |
| st5 | 0 |
| st6 | 0 |

```
t = table(2022.01.01 2022.01.01 2022.01.01 2022.01.01 2022.01.01 2022.01.01 as date, `a`a`b`b`a`b as id, 300 290 302 296 304 320 as val)
select date, case when t.id == `a then val end as `GroupA, case when t.id == `b then val end as `GroupB from t
```

| date | GroupA | GroupB |
| --- | --- | --- |
| 2022.01.01 | 300 |  |
| 2022.01.01 | 290 |  |
| 2022.01.01 |  | 302 |
| 2022.01.01 |  | 296 |
| 2022.01.01 | 304 |  |
| 2022.01.01 |  | 320 |

```
select sum(val) as total from t group by case when t.val < 300 then 0 else 1 end as flag
```

| flag | total |
| --- | --- |
| 1 | 1,226 |
| 0 | 586 |

支持在 case 语句中使用分析函数

```
t = table([2023.06M,2023.07M,2023.08M,2023.07M,2023.07M,2023.06M,2023.08M,2023.06M,2023.08M] as month, ["A","A","B","B","C","C","A","B","C"] as flag, [1200,1500,1200,1300,1400,1400,1400,1000,1300] as val)
t
```

| month | flag | val |
| --- | --- | --- |
| 2023.06M | A | 1,200 |
| 2023.07M | A | 1,500 |
| 2023.08M | B | 1,200 |
| 2023.07M | B | 1,300 |
| 2023.07M | C | 1,400 |
| 2023.06M | C | 1,400 |
| 2023.08M | A | 1,400 |
| 2023.06M | B | 1,000 |
| 2023.08M | C | 1,300 |

当 flag 为 A 时，按月分组计算 val 的偏差；当 flag 不为 A 时，按月分组计算 val 的标准差。

```
select month,flag,(case when flag = "A"
then (val - avg(val)over(partition by month))
else std(val)over(partition by month) end) as value
from t
```

| month | flag | value |
| --- | --- | --- |
| 2023.06M | A | 0 |
| 2023.07M | A | 100 |
| 2023.08M | B | 100 |
| 2023.07M | B | 100 |
| 2023.07M | C | 100 |
| 2023.06M | C | 200 |
| 2023.08M | A | 100 |
| 2023.06M | B | 200 |
| 2023.08M | C | 100 |

