# between

between...and 用于匹配指定范围内的所有值，包括起始值和终止值，其功能等同于 between 函数。

## 语法

```
select col(s)
from table
where col [not] between value1 and value2
```

## 例子

```
t = table(`APPL`AMZN`IBM`IBM`AAPL`AMZN as sym, 1.8 2.3 3.7 3.1 4.2 2.8 as price);
select * from t where price between 2 and 4
// 等价于 select * from t where price between 2:4
```

| sym | price |
| --- | --- |
| AMZN | 2.3 |
| IBM | 3.7 |
| IBM | 3.1 |
| AMZN | 2.8 |

```
select * from t where sym between `A and `H
```

| sym | price |
| --- | --- |
| APPL | 1.8 |
| AMZN | 2.3 |
| APPL | 4.2 |
| AMZN | 2.8 |

