# sql

## 语法

`sql(select, from, [where], [groupBy], [groupFlag],
[csort], [ascSort], [having], [orderBy], [ascOrder], [limit], [hint],
[exec=false], [map=false])`

## 参数

**select** 是表示选取的列的元代码。每列由函数 [sqlCol](sqlCol.md) 或 [sqlColAlias](sqlColAlias.md) 生成。若选择多列，使用元组表示。

**from** 选取数据的表对象或表名称。

**where** where 条件。如果有多个 where 条件，使用 ANY 向量来表示，每个元素对应一个条件的元代码。

**groupBy** group by 后面的关键字（列名）。如果有多个 group by 关键字，使用 ANY
向量来表示，每个元素对应一个列名的元代码。

**groupFlag** 1表示 group by，0表示 context by，2表示 pivot by。默认值为1。

**csort** csort 后面的关键字（列名）。只有当 *groupFlag*=0，即使用 context by 时，才能指定该参数。如果有多个
csort 关键字，使用元组来表示，每个元素对应一个列名的元代码。

**ascSort** 表示 csort 关键字按升序或降序排列的整型标量或向量。1表示升序，0表示降序。默认值为1。

**having** having 条件。如果有多个 having 条件，使用 ANY 向量来表示，每个元素对应一个条件的元代码。

**orderBy** order by 后面的关键字（列名）。如果有多个 order by 关键字，使用 ANY
向量来表示，每个元素对应一个列名的元代码。

**ascOrder** 表示 order by 后面的关键字按升序或降序排列的整型标量或向量。1表示升序，0表示降序。默认值为1。

**limit** 整数或整型数据对，表示从第一行开始选取的行数。如果指定了 *groupBy* 且
*groupFlag*=0，从每组的第一行开始选取 limit 行记录。它对应的是 SQL 中的 top 语句。

**hint** 常量。目前该参数可以是 HINT\_HASH、HINT\_SNAPSHOT 或 HINT\_KEEPORDER。HINT\_HASH 表示执行 group
by 查询时采用哈希算法，HINT\_SNAPSHOT 表示从快照引擎中查询数据，HINT\_KEEPORDER 表示执行context by
后的结果仍然按输入数据中的顺序排列。

**exec** 表示是否使用 exec 子句。默认值为 false。若设置为 true，可以生成一个标量或者一个向量，与 pivot by
共同使用，可以生成一个矩阵。

**map** 布尔类型的标量，表示是否使用 map 关键字，默认值为 false。

## 详情

动态生成 SQL 语句。使用函数 [eval](../e/eval.md) 执行生成的 SQL
语句。

## 例子

```
symbol = take(`GE,6) join take(`MSFT,6) join take(`F,6)
date=take(take(2017.01.03,2) join take(2017.01.04,4), 18)
price=31.82 31.69 31.92 31.8  31.75 31.76 63.12 62.58 63.12 62.77 61.86 62.3 12.46 12.59 13.24 13.41 13.36 13.17
volume=2300 3500 3700 2100 1200 4600 1800 3800 6400 4200 2300 6800 4200 5600 8900 2300 6300 9600
t1 = table(symbol, date, price, volume);

t1;
```

| symbol | date | price volume |
| --- | --- | --- |
| GE | 2017.01.03 | 31.82 2300 |
| GE | 2017.01.03 | 31.69 3500 |
| GE | 2017.01.04 | 31.92 3700 |
| GE | 2017.01.04 | 31.8 2100 |
| GE | 2017.01.04 | 31.75 1200 |
| GE | 2017.01.04 | 31.76 4600 |
| MSFT | 2017.01.03 | 63.12 1800 |
| MSFT | 2017.01.03 | 62.58 3800 |
| MSFT | 2017.01.04 | 63.12 6400 |
| MSFT | 2017.01.04 | 62.77 4200 |
| MSFT | 2017.01.04 | 61.86 2300 |
| MSFT | 2017.01.04 | 62.3 6800 |
| F | 2017.01.03 | 12.46 4200 |
| F | 2017.01.03 | 12.59 5600 |
| F | 2017.01.04 | 13.24 8900 |
| F | 2017.01.04 | 13.41 2300 |
| F | 2017.01.04 | 13.36 6300 |
| F | 2017.01.04 | 13.17 9600 |

```
x=5000
whereConditions = [<symbol=`MSFT>,<volume>x>]
havingCondition = <sum(volume)>200>;

sql(sqlCol("*"), t1);
//output:< select * from t1 >

sql(sqlCol("*"), t1, whereConditions);
//output:< select * from t1 where symbol == "MSFT",volume > x >

sql(select=sqlColAlias(<avg(price)>), from=t1, where=whereConditions, groupBy=sqlCol(`date));
//output:< select avg(price) as avg_price from t1 where symbol == "MSFT",volume > x group by date >

sql(select=sqlColAlias(<avg(price)>), from=t1, groupBy=[sqlCol(`date),sqlCol(`symbol)]);
//output:< select avg(price) as avg_price from t1 group by date,symbol >

sql(select=(sqlCol(`symbol),sqlCol(`date),sqlColAlias(<cumsum(volume)>, `cumVol)), from=t1, groupBy=sqlCol(`date`symbol), groupFlag=0);
//output:< select symbol,date,cumsum(volume) as cumVol from t1 context by date,symbol >

sql(select=(sqlCol(`symbol),sqlCol(`date),sqlColAlias(<cumsum(volume)>, `cumVol)), from=t1, where=whereConditions, groupBy=sqlCol(`date), groupFlag=0);
//output:< select symbol,date,cumsum(volume) as cumVol from t1 where symbol == "MSFT",volume > x context by date >

sql(select=(sqlCol(`symbol),sqlCol(`date),sqlColAlias(<cumsum(volume)>, `cumVol)), from=t1, where=whereConditions, groupBy=sqlCol(`date), groupFlag=0, csort=sqlCol(`volume), ascSort=0);
//output:< select symbol,date,cumsum(volume) as cumVol from t1 where symbol == "MSFT",volume > x context by date csort volume desc >

sql(select=(sqlCol(`symbol),sqlCol(`date),sqlColAlias(<cumsum(volume)>, `cumVol)), from=t1, where=whereConditions, groupBy=sqlCol(`date), groupFlag=0, having=havingCondition);
//output:< select symbol,date,cumsum(volume) as cumVol from t1 where symbol == "MSFT",volume > x context by date having sum(volume) > 200 >

sql(select=sqlCol("*"), from=t1, where=whereConditions, orderBy=sqlCol(`date), ascOrder=0);
//output:< select * from t1 where symbol == "MSFT",volume > x order by date desc >

sql(select=sqlCol("*"), from=t1, limit=1);
//output:< select top 1 * from t1 >

sql(select=sqlCol("*"), from=t1, groupBy=sqlCol(`symbol), groupFlag=0, limit=1);
//output:< select top 1 * from t1 context by symbol >

sql(select=(sqlCol(`symbol),sqlCol(`date),sqlColAlias(<cumsum(volume)>, `cumVol)), from=t1, groupBy=sqlCol(`date`symbol), groupFlag=0, hint=HINT_KEEPORDER);
//output:< select [128] symbol,date,cumsum(volume) as cumVol from t1 context by date,symbol >

whereConditions1 = <symbol=`MSFT or volume>x>
sql(select=sqlCol("*"), from=t1, where=whereConditions1, orderBy=sqlCol(`date), ascOrder=0);
//output:< select * from t14059d76a00000000 where symbol == "MSFT" or volume > x order by date desc >
sql(select=sqlCol("*"), from=t1, where=whereConditions, orderBy=sqlCol(`date), ascOrder=0, map=true);
//output:< select [256] * from t17092a30500000000 where symbol == "MSFT",volume > x order by date desc map >
```

可以定义一个函数使用 `sql` 函数来动态生成 SQL 语句。

```
def f1(t, sym, x){
whereConditions=[<symbol=sym>,<volume>x>]
return sql(sqlCol("*"),t,whereConditions).eval()
};

f1(t1, `MSFT, 5000);
```

| symbol | date | price volume |
| --- | --- | --- |
| MSFT | 2017.01.04 | 63.12 6400 |
| MSFT | 2017.01.04 | 62.3 6800 |

```
f1(t1, `F, 9000);
```

| symbol | date | price volume |
| --- | --- | --- |
| F | 2017.01.04 | 13.17 9600 |

```
def f2(t, sym, colNames, filterColumn, filterValue){
 whereConditions=[<symbol=sym>,expr(sqlCol(filterColumn),>,filterValue)]
    return sql(sqlCol(colNames),t,whereConditions).eval()
};
```

```
f2(t1,`GE, `symbol`date`volume, `volume, 3000);
```

| symbol | date | volume |
| --- | --- | --- |
| GE | 2017.01.03 | 3500 |
| GE | 2017.01.04 | 3700 |
| GE | 2017.01.04 | 4600 |

```
f2(t1,`F, `symbol`date`volume,`price,13.2);
```

| symbol | date | volume |
| --- | --- | --- |
| F | 2017.01.04 | 8900 |
| F | 2017.01.04 | 2300 |
| F | 2017.01.04 | 6300 |

设置参数 *exec*=true，配合 pivot by 语句，生成一个矩阵：

```
date = 2020.09.21 + 0 0 0 0 1 1 1 1
sym = `MS`MS`GS`GS`MS`MS`GS`GS$SYMBOL
factorNum = 1 2 1 2 1 2 1 2
factorValue = 1.2 -3.4 -2.5 6.3 1.1 -3.2 -2.1 5.6
t = table(date, sym, factorNum, factorValue);
sql(select=sqlCol(`factorValue), from=t, groupBy=[sqlCol(`date), sqlCol(`sym)], groupFlag=2, exec=true)

//output:< exec factorValue from t pivot by date,sym >
```

