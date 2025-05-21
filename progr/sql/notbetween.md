# notBetween/NOTBETWEEN

notBetween...and 是与 between…and 相反的操作，用于匹配指定范围（包括起始值和终止值）之外的所有值，其功能等同于
`notBetween` 函数、not between 语句。notBetween 支持内存表和分布式表。

## 语法

```
select col(s)
from table
where col notBetween value1 and value2
```

## 参数

**col(s)** 要选择的字段名称。一个或多个字段名称或 \*（表示所有列）。

**table** 要查询的表名称。

**col** 要查询的字段名称。

**value1, value2** 任何有效的表达式。*value1* 表示起始值，*value2*
表示终止值。*value1*，*value2* 和 *col* 的数据类型必须相同。

## 例子

查询 id 列值不在 2 和 4 之间的记录。

```
timeCols = 2024.11.14+1..6
symCols = `APPL`AMZN`IBM`IBM`AAPL`AMZN
priceCols = 1.8 2.3 3.7 3.1 4.2 2.8

t = table(timeCols as time, symCols as sym, priceCols as price);
select * from t where price notBetween 2 and 4

// 等价于 select * from t where price notBetween 2:4
// 亦等价于 select * from t where price not between 2 and 4
```

| time | sym | price |
| --- | --- | --- |
| 2024.11.15 | APPL | 1.8 |
| 2024.11.19 | AAPL | 4.2 |

查询 time 列日期不在 2024.11.16 和 2024.11.18 之间的所有记录

```
select * from t where time notBetween 2024.11.16 and 2024.11.18
```

| time | sym | price |
| --- | --- | --- |
| 2024.11.15 | APPL | 1.8 |
| 2024.11.19 | AAPL | 4.2 |
| 2024.11.20 | AMZN | 2.8 |

