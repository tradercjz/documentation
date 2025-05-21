# sqlCol

## 语法

`sqlCol(colName, [func], [alias], [qualifier])`

## 参数

**colName** 是一个字符串标量或向量，表示列名。

**func** 是一个一元函数。

**alias** 是一个字符串标量或向量，表示选择列或计算结果列的别名。

**qualifier** 是一个字符串标量，表示表名。多表连接时，可以通过该参数指定含有相同名字的非连接列属于哪个表。

## 详情

生成表示选择某些列或对某些列进行计算的元代码。一般与函数 [sql](sql.html) 和
[eval](../e/eval.html) 共同使用，用于动态生成 SQL 语句。

## 例子

```
t = table(`GME`AMC`KOSS as symbol, 325 13.26 64 as price);
colName="symbol";
sql(select=sqlCol(colName), from=t).eval();
```

| symbol |
| --- |
| GME |
| AMC |
| KOSS |

```
colName="price";
sql(select=sqlCol(colName, max, `maxPrice), from=t).eval();
```

| maxPrice |
| --- |
| 325 |

```
t1 = table(1 2 3 3 as id, 7.8 4.6 5.1 0.1 as value, 4 3 2 1 as x);
t2 = table(5 3 1 as id,  300 500 800 as qty, 44 66 88 as x) ;
sql(select=(sqlCol(`id),sqlCol(colName=`x, alias="t1_x", qualifier="t1"),sqlCol(colName=`x, alias="t2_x", qualifier=`t2)), from=<ej(t1,t2,`id)>).eval()
```

| id | t1\_x | t2\_x |
| --- | --- | --- |
| 1 | 4 | 88 |
| 3 | 2 | 66 |
| 3 | 1 | 66 |

