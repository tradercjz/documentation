# cross join

## 语法

```
cj(leftTable, rightTable)
```

## 参数

**leftTable** 和 **rightTable** 是连接的表。

在DolphinDB中，该语句的使用兼容 SQL 的语法：

```
select column_name(s) from leftTable cross join rightTable
```

## 详情

交叉连接函数返回两张表的笛卡尔积的结果集。如果左表有n行，右表有m行，那么笛卡尔积结果集含有n\*m行。

## 例子

```
a = table(2010 2011 2012 as year)
b = table(`IBM`C`AAPL as Ticker);
a;
```

| year |
| --- |
| 2010 |
| 2011 |
| 2012 |

```
b;
```

| Ticker |
| --- |
| IBM |
| C |
| AAPL |

```
cj(a,b);
```

| year | Ticker |
| --- | --- |
| 2010 | IBM |
| 2010 | C |
| 2010 | AAPL |
| 2011 | IBM |
| 2011 | C |
| 2011 | AAPL |
| 2012 | IBM |
| 2012 | C |
| 2012 | AAPL |

```
select * from cj(a,b) where year>2010;
// 等价于 select * from a cross join b where year>2010
```

| year | Ticker |
| --- | --- |
| 2011 | IBM |
| 2011 | C |
| 2011 | AAPL |
| 2012 | IBM |
| 2012 | C |
| 2012 | AAPL |

相反, [join](../operators/join.html)
只是简单地合并两张表的列。

```
join(a,b);
```

| year | Ticker |
| --- | --- |
| 2010 | IBM |
| 2011 | C |
| 2012 | AAPL |

