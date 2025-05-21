# olsEx

## 语法

`olsEx(ds, Y, X, [intercept=true], [mode=0])`

## 参数

**ds** 是存储在元组中的数据源集合。它通常是由 [sqlDS](../s/sqlDS.md) 函数生成。

**Y** 是一个字符串，表示 *ds* 表中因变量的列名。

**X** 是字符串标量或向量，表示 *ds* 表中自变量的列名。

**intercept** 是一个布尔变量，指示是否包含回归中的截距。默认值是 true。当它为 true 时，系统自动给
*X* 添加一列 "1" 以生成截距。

**mode** 是一个整数，默认值为 0，取以下 3 个值之一

* 0：输出一个系数估计向量
* 1：输出一个具有系数估计，标准差，t统计量和p值的表
* 2：输出一个具有 ANOVA（方差分析）、RegressionStat（回归统计）和
  Cofficient（系数）的字典，具体含义见下表：

键 ANOVA 对应值：

| Source of Variance | 自由度（Degree of freedom） | 平方和（Sum of Square） | 均方差（Mean of square） | F 统计量 | Significance |
| --- | --- | --- | --- | --- | --- |
| Regression（回归） | 变量个数（p） | 回归平方和（SSR） | 回归均方差（MSR=SSR/R） | MSR 对 MSE 的比值 | 显著性，即统计出的P值 |
| Residual（残差） | 残差自由度（n-p-1） | 残差平方和（SSE） | 残差均方差（MSE=MSE/E） |  |  |
| Total | 样本自由度 |  |  |  |  |
| 不包括常数项（n-1） | 总离差平方和（SST） |  |  |  |  |

键RegressionStat对应值：

| item | 统计值 |
| --- | --- |
| R2 | R 决定系数，描述回归曲线对真实数据点拟合程度的统计量。范围在 [0,1]之间，越接近1 ，说明对y的解释能力越强，拟合越好。 |
| AdjustedR2 | 经自由度修正后的决定系数，通过样本数量与模型数量对 R-squared 进行修正。 |
| StdError | 回归残差标准误差，残差经自由度修正后的标准差。 |
| Observations | 观察样本个数。 |

键Coefficient对应值：

| 元素 | 说明 |
| --- | --- |
| factor | 自变量名称 |
| beta | 回归系数估计值 |
| stdError | 回归系数标准误差。标准差越大，回归系数的估计值越不靠谱。 |
| tstat | T 统计值，衡量系数的统计显著性。 |

## 详情

返回对 *X* 和 *Y* 计算普通最小二乘回归的结果。*X* 和 *Y*
是分布式表中的列。

注：

* 该函数会将 *X* 和 *Y* 中的空值替换为0后进行计算。
* 因为`olsEX` 不支持输出残差，可以通过 [residual](../r/residual.md) 获取残差。

## 例子

```
n=10000
ID=rand(100, n)
dates=2017.08.07..2017.08.11
date=rand(dates, n)
vol=rand(1..10 join int(), n)
price=rand(100,n)
t=table(ID, date, vol,price)
saveText(t, "/home/DolphinDB/Data/t.txt");
if(existsDatabase("dfs://rangedb")){
  dropDatabase("dfs://rangedb")
}
db = database(directory="dfs://rangedb", partitionType=RANGE, partitionScheme=0 51 101)
USPrices=loadTextEx(dbHandle=db,tableName=`USPrices, partitionColumns=`ID, filename="/home/DolphinDB/Data/t.txt");

ds=sqlDS(<select vol as VS, price as SBA from USPrices where vol>5>)
rs=olsEx(ds, `VS, `SBA, true, 2)
rs;

// output
RegressionStat->
item         statistics
------------ ----------
R2           0.000848
AdjustedR2   0.000628
StdError     1.404645
Observations 4535

ANOVA->
Breakdown  DF   SS          MS       F        Significance
---------- ---- ----------- -------- -------- ------------
Regression 1    7.592565    7.592565 3.848178 0.049861
Residual   4533 8943.739298 1.973029
Total      4534 8951.331863

Coefficient->
factor    beta     stdError tstat      pvalue
--------- -------- -------- ---------- --------
intercept 7.953084 0.04185  190.039423 0
SBA       0.001422 0.000725 1.961677   0.049861
```

