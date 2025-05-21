# mwsumTopN

## 语法

`mwsumTopN(X, Y, S, window, top, [ascending=true],
[tiesMethod='oldest'])`

参数说明和窗口计算规则请参考：[mTopN](../themes/TopN.html)

## 详情

在给定长度（以元素个数衡量）的滑动窗口内，根据 *ascending* 指定的排序方式将 *X* 和 *Y* 按照 *S*
进行稳定排序后，取前 *top* 个元素，然后计算 *Y* 和 *X* 的内积。

## 例子

```
x = NULL 3 8 4 0 7 4
y = 2 3 1 7 3 6 1
s = 5 NULL 8 9 9 4 4

mwsumTopN(x, y, s, 4, 3)
// output
[,,8,36,36,78,74]

s2=2021.01.01 2021.02.03 2021.01.23 2021.04.06 2021.12.29 2021.04.16 2021.10.29
mwsumTopN(x, y, s2, 3, 2)
// output
[ , 9, 8, 17, 36, 70, 46]

x1 = matrix(x, 4 3 6 2 3 1 3)
y1=matrix(3 7 9 3 2 4 6, y)
s1=matrix(2 3 1 7 3 NULL 1, s)

mwsumTopN(x1,y1,s1,4,3)
```

| #1 | #2 |
| --- | --- |
|  | 8 |
| 21 | 8 |
| 93 | 14 |
| 93 | 28 |
| 93 | 29 |
| 84 | 26 |
| 36 | 23 |

```
mwsumTopN(x1, y1, s, 4, 3)
```

| #1 | #2 |
| --- | --- |
|  | 8 |
|  | 8 |
| 72 | 14 |
| 84 | 28 |
| 84 | 29 |
| 112 | 26 |
| 64 | 23 |

```
n = 3000
ids = 1..3000
dates = take(2021.01.01..2021.10.01,n)
prices = rand(1000,n)
vals = rand(1000,n)
t = table(ids as id,dates as date,prices as price,vals as val)
dbName = "dfs://test_mwsumTopN_2"
if(existsDatabase(dbName))dropDB(dbName)
db = database(dbName,VALUE,1..5000)
pt = db.createPartitionedTable(t,"pt",`id).append!(t)
select mwsumTopN(price, val, id, 10, 5, true) from pt where date>2021.05.01
```

相关函数：[mwsum](mwsum.html)

