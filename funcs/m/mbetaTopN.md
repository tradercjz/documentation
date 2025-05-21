# mbetaTopN

## 语法

`mbetaTopN(X, Y, S, window, top, [ascending=true],
[tiesMethod='oldest'])`

参数说明和窗口计算规则请参考：[mTopN](../themes/TopN.md)

## 详情

在给定长度（以元素个数衡量）的滑动窗口内，根据 *ascending* 指定的排序方式将 *X* 和 *Y* 按照 *S*
进行稳定排序后，取前 *top* 个元素，然后计算 *Y* 在 *X* 上的回归系数的最小二乘估计。

## 例子

```
x = NULL 3 8 4 0
y = 2 3 1 7 3
s = 5 NULL 8 9 4
mbetaTopN(x, y, s, 3, 2)
// output
[ , , , -0.66, -4]

s2=2021.01.01 2021.02.03 2021.01.23 2021.04.06 2021.12.29
mbetaTopN(x, y, s2, 3, 2)
// output
[ , , , -2.5, -0.6667]

x1 = matrix(x, 4 3 6 2 3)
y1=matrix(3 7 9 3 2, y)
s1=matrix(2 3 1 7 3, s)

mbetaTopN(x, y1, s1, 3, 2)
```

| col1 | col2 |
| --- | --- |
|  |  |
|  |  |
|  |  |
| 2.5 | -2.5 |
| 1.1429 | -4 |

```
mbetaTopN(x1, y1, s, 3, 2)
```

| col1 | col2 |
| --- | --- |
|  |  |
|  | -1 |
|  | -1 |
| 2.5 | -1.5 |
| 1.1429 | -1.5 |

```
n = 3000
ids = 1..3000
dates = take(2021.01.01..2021.10.01,n)
prices = rand(1000,n)
vals = rand(1000,n)
t = table(ids as id,dates as date,prices as price,vals as val)
dbName = "dfs://test_mbetaTopN_2"
if(existsDatabase(dbName))dropDB(dbName)
db = database(dbName,VALUE,1..5000)
pt = db.createPartitionedTable(t,"pt",`id).append!(t)
select mbetaTopN(price, val, id, 10, 5, true) from pt where date>2021.05.01
```

相关函数：[mbeta](mbeta.md)

