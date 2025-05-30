# limit

limit 子句可使用整型标量或代表整型标量的变量，以限制返回记录的数量，亦可与context by子句一同使用，以限制结果中每组记录的数量。

limit子句和top子句功能类似。两者的区别在于：

* top子句中的整型常量不能为负数。在与context
  by子句一同使用时，limit子句标量值可以为负整数，返回每个组最后指定数目的记录。其他情况limit子句标量值为非负整数。
* 可使用limit子句从某行开始选择一定数量的行。

```
sym = `C`MS`MS`MS`IBM`IBM`C`C`C$SYMBOL
price= 49.6 29.46 29.52 30.02 174.97 175.23 50.76 50.32 51.29
qty = 2200 1900 2100 3200 6800 5400 1300 2500 8800
timestamp = [09:34:07,09:36:42,09:36:51,09:36:59,09:32:47,09:35:26,09:34:16,09:34:26,09:38:12]
t = table(timestamp, sym, qty, price);
t;
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
| 09:38:12 | C | 8800 | 51.2 |

```
select * from t limit 2;
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:34:07 | C | 2200 | 49.6 |
| 09:36:42 | MS | 1900 | 29.46 |

```
select * from t limit 2, 5;
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:36:51 | MS | 2100 | 29.52 |
| 09:36:59 | MS | 3200 | 30.02 |
| 09:32:47 | IBM | 6800 | 174.97 |
| 09:35:26 | IBM | 5400 | 175.23 |
| 09:34:16 | C | 1300 | 50.76 |

```
rowOffset = 2
rowCount = 5
select * from t limit rowOffset, rowCount;
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:36:51 | MS | 2100 | 29.52 |
| 09:36:59 | MS | 3200 | 30.02 |
| 09:32:47 | IBM | 6800 | 174.97 |
| 09:35:26 | IBM | 5400 | 175.23 |
| 09:34:16 | C | 1300 | 50.76 |

```
select * from t context by sym order by qty limit -1;
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:36:59 | MS | 3200 | 30.02 |
| 09:35:26 | IBM | 5400 | 175.23 |
| 09:38:12 | C | 8800 | 51.29 |

Copyright

**©2025 浙江智臾科技有限公司 浙ICP备18048711号-3**
