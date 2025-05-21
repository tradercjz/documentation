# group by

关键字会自动加入到结果集中，用户可以不在select语句中指定该列。生成的表的顺序为：group by中select未指定的字段排列在前，select指定的字段排列在后。

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
| 09:35:26 | IBM | 5400 | 175.2 |
| 09:34:16 | C | 1300 | 50.76 |
| 09:34:26 | C | 2500 | 50.32 |
| 09:38:12 | C | 8800 | 51.29 |

```
select count(sym) as counts from t1 group by sym;
```

| sym | counts |
| --- | --- |
| C | 4 |
| MS | 3 |
| IBM | 2 |

和 top 子句一起使用：

```
select top 2:3 count(sym) as counts from t1 group by sym;
```

| sym | counts |
| --- | --- |
| IBM | 2 |

```
select max(price), sym from t1 group by sym, minute(timestamp)
```

| minute\_timestamp | max\_price | sym |
| --- | --- | --- |
| 09:34m | 50.76 | C |
| 09:36m | 30.02 | MS |
| 09:32m | 174.97 | IBM |
| 09:35m | 175.23 | IBM |
| 09:38m | 51.29 | C |

```
select avg(qty) from t1 group by sym;
```

| sym | avg\_qty |
| --- | --- |
| C | 3700 |
| MS | 2400 |
| IBM | 6100 |

```
select wavg(price, qty) as vwap, sum(qty) from t1 group by sym;
```

| sym | vwap | sum\_qty |
| --- | --- | --- |
| C | 50.828378 | 14800 |
| IBM | 175.085082 | 12200 |
| MS | 29.726389 | 7200 |

```
select wsum(price, qty) as dollarVolume, sum(qty) from t1 group by minute(timestamp) as ts;
```

| ts | dollarVolume | sum\_qty |
| --- | --- | --- |
| 09:32m | 1.189796e+006 | 6800 |
| 09:34m | 300908 | 6000 |
| 09:35m | 946242 | 5400 |
| 09:36m | 214030 | 7200 |
| 09:38m | 451352 | 8800 |

```
select sum(qty) from t1 group by sym, timestamp.minute() as minute;
```

| sym | minute | sum\_qty |
| --- | --- | --- |
| C | 09:34m | 6000 |
| C | 09:38m | 8800 |
| IBM | 09:32m | 6800 |
| IBM | 09:35m | 5400 |
| MS | 09:36m | 7200 |

group by和order by配合使用。order by的字段必须是group by结果表中的字段。

```
select sum(qty) from t1 group by sym, timestamp.minute() as minute order by minute;
```

| sym | minute | sum\_qty |
| --- | --- | --- |
| IBM | 09:32m | 6800 |
| C | 09:34m | 6000 |
| IBM | 09:35m | 5400 |
| MS | 09:36m | 7200 |
| C | 09:38m | 8800 |

在上述例子中，每个分组的函数结果都是标量。在其他情况下，函数可能输出向量或者字典，而不是输出标量。比如，[stat](../../funcs/s/stat.html) 函数输出字典； [ols](../../funcs/o/ols.html) 输出一个系数向量或一个含有参数估计如t-stat,
R²的字典等。为了在多列中输出结果，需要将向量或字典输出转换成多个标量值。换而言之，需要将一个合成列转换成多个列。我们可以通过as关键字和一个代表列名的常量字符串向量来完成这项工作。

```
y=1..15
factor1=3.2 1.2 5.9 6.9 11.1 9.6 1.4 7.3 2.0 0.1 6.1 2.9 6.3 8.4 5.6
factor2=1.7 1.3 4.2 6.8 9.2 1.3 1.4 7.8 7.9 9.9 9.3 4.6 7.8 2.4 8.7
id=take(1 2 3, 15).sort();
t=table(id, y, factor1, factor2);

t;
```

| id | y | factor1 | factor2 |
| --- | --- | --- | --- |
| 1 | 1 | 3.2 | 1.7 |
| 1 | 2 | 1.2 | 1.3 |
| 1 | 3 | 5.9 | 4.2 |
| 1 | 4 | 6.9 | 6.8 |
| 1 | 5 | 11.1 | 9.2 |
| 2 | 6 | 9.6 | 1.3 |
| 2 | 7 | 1.4 | 1.4 |
| 2 | 8 | 7.3 | 7.8 |
| 2 | 9 | 2 | 7.9 |
| 2 | 10 | 0.1 | 9.9 |
| 3 | 11 | 6.1 | 9.3 |
| 3 | 12 | 2.9 | 4.6 |
| 3 | 13 | 6.3 | 7.8 |
| 3 | 14 | 8.4 | 2.4 |
| 3 | 15 | 5.6 | 8.7 |

```
select ols(y,(factor1,factor2),true,0) as `int`factor1`factor2 from t group by id;
```

| id | int | factor1 | factor2 |
| --- | --- | --- | --- |
| 1 | 1.063991 | -0.258685 | 0.732795 |
| 2 | 6.886877 | -0.148325 | 0.303584 |
| 3 | 11.833867 | 0.272352 | -0.065526 |

```
select ols(y,(factor1,factor2),true,2).Coefficient.tstat[1:] as `t1`t2 from t group by id;
```

| id | t1 | t2 |
| --- | --- | --- |
| 1 | -0.891868 | 2.253451 |
| 2 | -5.73315 | 11.433117 |
| 3 | 0.510866 | -0.183903 |

若想要忽略函数的一些输出元素，可将列名留空。

```
select ols(y,(factor1,factor2),true,2).Coefficient.beta as ``factor1`factor2 from t group by id;
```

| id | factor1 | factor2 |
| --- | --- | --- |
| 1 | -0.258685 | 0.732795 |
| 2 | -0.148325 | 0.303584 |
| 3 | 0.272352 | -0.065526 |

若想要自定义输出格式，可以写一个简单的包装函数。下面例子中，输出包含了系数估计和R²：

```
def myols(y,x) {
  r=ols(y,x,true,2)
  return r.Coefficient.beta join r.RegressionStat.statistics[0]
}

select myols(y,(factor1,factor2)) as `int`factor1`factor2`R2 from t group by id;
```

| id | int | factor1 | factor2 | R2 |
| --- | --- | --- | --- | --- |
| 1 | 1.063991 | -0.258685 | 0.732795 | 0.946056 |
| 2 | 6.886877 | -0.148325 | 0.303584 | 0.992413 |
| 3 | 11.833867 | 0.272352 | -0.065526 | 0.144837 |

Copyright

**©2025 浙江智臾科技有限公司 浙ICP备18048711号-3**
