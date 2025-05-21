# in

in 谓词用在 where 子句中，可以指定一个或多个值。通过 in 可以简写多个 or 条件。

## 语法

```
select col(s)
from table
where col [not] in (value1, value2, ...)
```

或

```
select col(s)
from table
where col [not] in (subquery)
```

## 参数

* `col(s)` 要选择的字段名称。可以为多个字段名称或 \*（表示所有列）。
* `table` 要查询的表名称。
* `col` 要查询的字段名称。
* `value1, value2, ...` 要查询的值，可以为多个值。

## 例子

```
t = table(`APPL`AMZN`IBM`IBM`APPL`AMZN as sym, 1.8 2.3 3.7 3.1 4.2 2.8 as price);
select * from t where sym in (`APPL, `AMZN)
// select * from t where sym=`APPL or sym=`AMZN
```

| sym | price |
| --- | --- |
| APPL | 1.8 |
| AMZN | 2.3 |
| APPL | 4.2 |
| AMZN | 2.8 |

```
t1=table(`APPL`AMZN`IBM`IBM`APPL`AMZN as sym, 200 500 300 350 240 580 as vol);
select * from t where sym in (select sym from t1 where sym=`IBM)
```

| sym | price |
| --- | --- |
| IBM | 3.7 |
| IBM | 3.1 |

