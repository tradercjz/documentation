# pca

## 语法

`pca(ds, [colNames], [k], [normalize], [maxIter], [svdSolver],
[randomState])`

## 参数

**ds** 是一个或多个数据源，通常由 [sqlDS](../s/sqlDS.md) 函数生成。

**colNames** 是字符串向量，表示数据源中的列名。默认值是数据源中所有列的列名。

**k** 是一个正整数，表示需要计算的主成分的个数。默认值是数据源中的列数。

**normalize** 是一个布尔值，表示是否将数据减去均值再除以标准差。默认值为 false。

**maxIter** 是一个正整数，表示参数 *svdSolver* =randomized 时的迭代次数。若未指定，当 *k*
<0.1\*cols 时，*maxIter* = 7，否则 *maxIter* = 4。这里 cols 表示数据源中的列数。

**svdSolver** 是一个字符串，表示如何对数据源进行 svd 运算。它的取值可以是 "full", "randomized" 或
"auto"。*svdSolver* = "full" 适合 *k* 值与数据源的列数相近的情况；*svdSolver* =
"randomized" 适合 *k* 值与数据源的列数相差较大的情况。默认值为 "auto"，此时系统会自动判断使用 "full" 还是
"randomized"。

**randomState** 是一个整数，表示随机数种子，仅在参数 *svdSolver* ="randomized" 时起作用，默认为
int(time(now()))。

## 详情

对数据源中指定列中的数据进行主成分分析。返回的结果是一个字典，包含以下键：

* components：对应长度为 size( *colNames* )\**k* 的主成分分析矩阵。
* explainedVarianceRatio：对应长度为 *k* 的向量，包含前 *k* 个主成分分别解释的方差权重。
* singularValues：对应长度为 *k* 的向量，包含主成分方差(协方差矩阵特征值)。

## 例子

```
x = [7,1,1,0,5,2]
y = [0.7, 0.9, 0.01, 0.8, 0.09, 0.23]
t=table(x, y)
ds = sqlDS(<select * from t>);

pca(ds);

// output
components->
#0        #1
--------- ---------
-0.999883 0.015306
-0.015306 -0.999883
explainedVarianceRatio->[0.980301,0.019699]
singularValues->[6.110802,0.866243]
```

