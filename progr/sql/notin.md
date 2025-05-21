# notIn/NOTIN

notIn 是与 in 相反的操作，用于确定指定的值是否与子查询或列表中的值不匹配，其功能等同于 `notIn` 函数、not in
语句。notIn 支持内存表和分布式表。

## 语法

```
select col(s)
from table
where col notIn (value1, value2, ...)
```

或

```
select col(s)
from table
where col notIn (subquery)
```

## 参数

**参数**

* **col(s)** 要选择的字段名称。一个或多个多个字段名称或 \*（表示所有列）。
* **table** 要查询的表名称。
* **col** 要查询的字段名称。
* **value1, value2, ...** 要查询的值，可以为1个或多个值。
* **subquery** 包含某列结果集的子查询。 该列必须与 *col* 具有相同的数据类型。

## 例子

查询 sym 列值不等于 APPL 和 AMZN 的记录。

```
t = table(`APPL`AMZN`IBM`IBM`APPL`AMZN as sym, 1.8 2.3 3.7 3.1 4.2 2.8 as price);
select * from t where sym notIn (`APPL, `AMZN)
// 等价于 select * from t where sym not in (`APPL, `AMZN)
```

| sym | price |
| --- | --- |
| IBM | 3.7 |
| IBM | 3.1 |

```
t1=table(`APPL`AMZN`IBM`IBM`APPL`AMZN as sym, 200 500 300 350 240 580 as vol);
select * from t where sym notIn (select sym from t1 where sym=`IBM)
```

| sym | price |
| --- | --- |
| APPL | 1.8 |
| AMZN | 2.3 |
| APPL | 4.2 |
| AMZN | 2.8 |

