# having

having子句总是跟在group by或者context by后，用来将结果进行过滤，只返回满足指定条件组结果。

* 如果having用在group by后，having只可与聚合函数一起使用，结果为符合聚合函数条件的每组产生一条记录。
* 如果having用在context by后，并且只与聚合函数一起使用，结果是符合聚合函数条件的分组，每组记录与输入数据中记录数一致。
* 如果having用在context by后，与非聚合函数一起使用，结果是符合指定条件的分组。

## 例子

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
select sum(qty) as totalqty from t1 group by sym having sum(qty)>10000;
```

| sym | totalqty |
| --- | --- |
| C | 14800 |
| IBM | 12200 |

```
select * from t1 context by sym having count(sym)>2 and sum(qty)>10000;
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:34:07 | C | 2200 | 49.6 |
| 09:34:16 | C | 1300 | 50.76 |
| 09:34:26 | C | 2500 | 50.32 |
| 09:38:12 | C | 8800 | 51.29 |

```
select * from t1 context by sym having rank(qty)>1;
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:34:26 | C | 2500 | 50.32 |
| 09:38:12 | C | 8800 | 51.29 |
| 09:36:59 | MS | 3200 | 30.02 |

```

select * from t1 context by sym having rank(qty)>1 and sum(qty)>10000;
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:34:26 | C | 2500 | 50.32 |
| 09:38:12 | C | 8800 | 51.29 |

在select语句中，对符合having条件的记录进行计算：

```
select *, min(qty) from t1 context by sym having rank(qty)>1;
```

| timestamp | sym | qty | price | min\_qty |
| --- | --- | --- | --- | --- |
| 09:34:26 | C | 2500 | 50.32 | 1300 |
| 09:38:12 | C | 8800 | 51.29 | 1300 |
| 09:36:59 | MS | 3200 | 30.02 | 1900 |

top语句可以与context by语句和having语句一起使用。

```
select top 2 * from t1 context by sym having sum(qty)>8000;
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:34:07 | C | 2200 | 49.6 |
| 09:34:16 | C | 1300 | 50.76 |
| 09:32:47 | IBM | 6800 | 174.97 |
| 09:35:26 | IBM | 5400 | 175.23 |

Copyright

**©2025 浙江智臾科技有限公司 浙ICP备18048711号-3**
