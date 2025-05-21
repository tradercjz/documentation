# makeCall

## 语法

`makeCall(F, args...)`

## 参数

**F** 是一个函数。

**args** 是 *F* 需要的参数。

## 详情

它使用指定参数调用一个函数并生成脚本。高阶函数 [call](../ho_funcs/call.html) 与
`makeCall` 的区别是，`makeCall` 不执行脚本。

## 例子

在下列例子中，我们创建了 `generateReport`
函数。它能够以指定格式显示表的某些列。

```
def generateReport(tbl, colNames, colFormat): sql(sqlColAlias(each(makeCall{format},sqlCol(colNames),colFormat),colNames), tbl).eval();

t = table(1..100 as id, (1..100 + 2018.01.01) as date, rand(100.0, 100) as price, rand(10000, 100) as qty, rand(`A`B`C`D`E`F`G, 100) as city);
t;
```

| id | date | price | qty | city |
| --- | --- | --- | --- | --- |
| 1 | 2018.01.02 | 77.9896 | 375 | A |
| 2 | 2018.01.03 | 8.1332 | 7864 | F |
| 3 | 2018.01.04 | 56.7185 | 4912 | B |
| 4 | 2018.01.05 | 72.4173 | 534 | E |
| 5 | 2018.01.06 | 8.2019 | 31 | B |
| 6 | 2018.01.07 | 74.7275 | 4139 | A |
| 7 | 2018.01.08 | 7.5421 | 2725 | D |
| 8 | 2018.01.09 | 59.1689 | 3095 | C |
| 9 | 2018.01.10 | 55.8454 | 5443 | D |
| 10 | 2018.01.11 | 32.1285 | 6998 | G |
| ... |  |  |  |  |

```
generateReport(t, ["id", "date","price","qty"], ["0", "MM/dd/yyyy", "0.00", "#,###"]);
```

| id | date | price | qty |
| --- | --- | --- | --- |
| 1 | 01/02/2018 | 77.99 | 375 |
| 2 | 01/03/2018 | 8.13 | 7,864 |
| 3 | 01/04/2018 | 56.72 | 4,912 |
| 4 | 01/05/2018 | 72.42 | 534 |
| 5 | 01/06/2018 | 8.20 | 31 |
| 6 | 1/07/2018 | 74.73 | 4,139 |
| 7 | 01/08/2018 | 7.54 | 2,725 |
| 8 | 01/09/2018 | 59.17 | 3,095 |
| 9 | 01/10/2018 | 55.85 | 5,443 |
| 10 | 01/11/2018 | 32.13 | 6,988 |
| ... |  |  |  |

与之等效的 SQL 脚本是：

```
def generateReportSQL(tbl, colNames, colFormat): sql(sqlColAlias(each(makeCall{format},sqlCol(colNames),colFormat),colNames), tbl)
generateReportSQL(t, ["id", "date","price","qty"], ["0", "MM/dd/yyyy", "0.00", "#,###"]);
// output
< select format(id, "0") as id,format(date, "MM/dd/yyyy") as date,format(price, "0.00") as price,format(qty, "#,###") as qty from t >
```

