# any/all

## 用法

any 和 all 关键字用于 where 或 having 子句。

```
where/having col optr any(sub_query)
where/having col optr all(sub_query)
```

其中 optr 是比较运算符，sub\_query 是一个 SQL 查询或者向量。

any/all 关键字将比较运算符前的操作数（通常是某列的值）与子查询结果集或向量中的值一一比较：

* any：若存在满足条件的子查询结果或向量值，则返回 true，否则为 false。
* all：若所有子查询结果或向量值都满足比较条件，则返回 true，否则返回 false。

注：

* “= any“ 等价于 “in”；”= all” 等价于 “!= any”；
* SQL 的 any / all 谓词和内置函数 any / all
  功能类似但不同。前者用于值比较，后者用于判断布尔值。

下面以两个语句来说明区别：

* SQL 中的 any 谓词：

  ```
  x > any([n1,n2,n3])
  ```
* 内置 any 函数：

  ```
  any([x>n1, x>n2, x>n3])
  ```

## 例子

```
sym = `C`MS`MS`MS`IBM`IBM`C`C`C$SYMBOL
price= 49.6 29.46 29.52 30.02 174.97 175.23 50.76 50.32 51.29
qty = 2200 1900 2100 3200 6800 5400 1300 2500 8800
timestamp = [09:34:07,09:36:42,09:36:51,09:36:59,09:32:47,09:35:26,09:34:16,09:34:26,09:38:12]
t1 = table(timestamp, sym, qty, price);
t2 = table(`C`MS`IBM as sym, 1 0 1 as flag)

select * from t1 where sym = any(select sym from t2 where flag=1)
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:34:07 | C | 2,200 | 49.6 |
| 09:32:47 | IBM | 6,800 | 174.97 |
| 09:35:26 | IBM | 5,400 | 175.23 |
| 09:34:16 | C | 1,300 | 50.76 |
| 09:34:26 | C | 2,500 | 50.32 |
| 09:38:12 | C | 8,800 | 51.29 |

```
select * from t1 where sym != all(select sym from t2 where flag = 1)
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:36:42 | MS | 1,900 | 29.46 |
| 09:36:51 | MS | 2,100 | 29.52 |
| 09:36:59 | MS | 3,200 | 30.02 |

```
t3 = select wavg(price, qty) as wavg from t1 group by sym
select * from t1 where price >= all(select wavg from t3)
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:35:26 | IBM | 5,400 | 175.23 |

```
select * from t1 where price >= any(select wavg from t3)
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 09:34:07 | C | 2,200 | 49.6 |
| 09:36:59 | MS | 3,200 | 30.02 |
| 09:32:47 | IBM | 6,800 | 174.97 |
| 09:35:26 | IBM | 5,400 | 175.23 |
| 09:34:16 | C | 1,300 | 50.76 |
| 09:34:26 | C | 2,500 | 50.32 |
| 09:38:12 | C | 8,800 | 51.29 |

