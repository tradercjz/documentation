# concatDateTime

## 语法

`concatDateTime(date, time)`

别名：`concatDT`

## 参数

**date** 可以是 DATE 类型的标量或向量。

**time** 可以是 SECOND、TIME 或 NANOTIME 类型的标量或向量。

如果 *date* 和 *time* 都是向量，它们的长度必须相同。

## 详情

合并日期和时间。如果 *time* 是 SECOND 类型，返回的结果是 DATETIME 类型；如果
*time* 是 TIME 类型，返回的结果是 TIMESTAMP 类型；如果 *time* 是 NANOTIME，返回的结果是
NANOTIMESTAMP 类型。

## 例子

```
concatDateTime(2019.06.15,13:25:10);
// output
2019.06.15T13:25:10

concatDateTime(2019.06.15,[13:25:10, 13:25:12, 13:25:13]);
// output
[2019.06.15T13:25:10,2019.06.15T13:25:12,2019.06.15T13:25:13]

date=[2019.06.18, 2019.06.20, 2019.06.21, 2019.06.19, 2019.06.18, 2019.06.20]
time = [09:34:07,09:36:42,09:36:51,09:36:59,09:32:47,09:35:26]
sym = `C`MS`MS`MS`IBM`IBM$SYMBOL
price= 49.6 29.46 29.52 30.02 174.97 175.23
qty = 2200 1900 2100 3200 6800 5400
t = table(date, time, sym, qty, price);

select concatDateTime(date,time) as datetime, sym, qty, price from t;
```

| datetime | sym | qty | price |
| --- | --- | --- | --- |
| 2019.06.18T09:34:07 | C | 2200 | 49.6 |
| 2019.06.20T09:36:42 | MS | 1900 | 29.46 |
| 2019.06.21T09:36:51 | MS | 2100 | 29.52 |
| 2019.06.19T09:36:59 | MS | 3200 | 30.02 |
| 2019.06.18T09:32:47 | IBM | 6800 | 174.97 |
| 2019.06.20T09:35:26 | IBM | 5400 | 175.23 |

