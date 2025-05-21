# mcorrTopN

## 语法

`mcorrTopN(X, Y, S, window, top, [ascending=true],
[tiesMethod='oldest'])`

参数说明和窗口计算规则请参考：[mTopN](../themes/TopN.html)

## 详情

在给定长度（以元素个数衡量）的滑动窗口内，根据 *ascending* 指定的排序方式将 *X* 和 *Y* 按照 *S*
进行稳定排序后，取前 *top* 个元素，然后计算 *Y* 和 *X* 的相关性。

## 例子

```
a =  2 5 3 1 9
b = 2 3 1 7 13
s = 6 8 4 2 7

mcorrTopN(a, b, s, 4, 3)
// output
[ , 1, 0.6547, -0.9333, 0.7206]

s2=2021.01.01 2021.02.03 2021.01.23 2021.04.06 2021.12.29
mcorrTopN(a, b, s2, 4, 3)
// output
[ , 1, 0.6547, 0.6547, -0.6547]

a1 = matrix(a, 4 3 6 2 3)
b1=matrix(3 7 9 3 2, b)
s1=matrix(2 3 1 7 3, s)
mcorrTopN(a, b1, s1, 4, 3)
```

| col1 | col2 |
| --- | --- |
|  |  |
| 1 | 1 |
| 0.5 | 0.6547 |
| 0.5 | -0.9333 |
| -0.9986 | 0.7206 |

```
mcorrTopN(a1, b1, s, 4, 3)
```

| col1 | col2 |
| --- | --- |
|  |  |
| 1 | -1 |
| 0.5 | -0.982 |
| 0.866 | -0.9333 |
| -0.4018 | -0.7206 |

```
mcorrTopN(a1, b1, s1, 4, 3)
```

| col1 | col2 |
| --- | --- |
|  |  |
| 1 | -1 |
| 0.5 | -0.982 |
| 0.5 | -0.9333 |
| -0.9986 | -0.7206 |

```
n = 3000
ids = 1..3000
dates = take(2021.01.01..2021.10.01,n)
prices = rand(1000,n)
vals = rand(1000,n)
t = table(ids as id,dates as date,prices as price,vals as val)
dbName = "dfs://test_mcorrTopN_2"
if(existsDatabase(dbName))dropDB(dbName)
db = database(dbName,VALUE,1..5000)
pt = db.createPartitionedTable(t,"pt",`id).append!(t)
select mcorrTopN(price, val, id, 10, 5, true) from pt where date>2021.05.01
```

相关函数：[mcorr](mcorr.html)

