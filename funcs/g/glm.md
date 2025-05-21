# glm

## 语法

`glm(ds, yColName, xColNames, [family], [link], [tolerance=1e-6],
[maxIter=100])`

## 参数

**ds** 是数据源，通常由 [sqlDS](../s/sqlDS.md) 函数生成。

**yColName** 是字符串，表示数据源中作为因变量的列名。

**xColNames** 是字符串标量或向量，表示数据源中作为自变量的列名。

**family** 是字符串标量，表示指数族分布的类型。它的取值可以是 gaussian, poisson, gamma, inverseGaussian,
binomial。

**link** 是字符串标量，表示 *link* 函数的类型。对于不同取值的 *family*, *link*
的默认值如下表所示。

**tolerance** 是浮点数，表示迭代中止的边界差值。如果相邻两次迭代的对数似然函数值的差值小于
*tolerance*，则停止迭代。默认值为0.000001。

**maxIter** 是正整数，表示最大的迭代次数。默认值为100。

*family* 参数对 *link* 参数、因变量的限制如下：

| *family* 的取值 | *link* 可选值 | 默认的 *link* 取值 | 因变量的取值 |
| --- | --- | --- | --- |
| gaussian | identity, inverse, log | identity | DOUBLE 类型 |
| poisson | log, sqrt, identity | log | 非负整数 |
| gamma | inverse, identity, log | inverse | 大于等于0 |
| inverseGaussian | inverseOfSquare, inverse, identity, log | inverseOfSquare | 大于等于0 |
| binomial | logit, probit | logit | 0或1 |

## 详情

训练广义线性模型。返回结果是一个字典，包含以下 key：coefficients, link, tolerance, family,
xColNames, tolerance, modelName, residualDeviance, iterations 和
dispersion。其中，coefficients 是一张表，包括计算得到的自变量系数值、每个系数的标准误差、t 值、p 值；modelName 为
"Generalized Linear Model"；iterations 是实际迭代次数；dispersion 是模型的规范系数。

## 例子

下面的例子使用模拟数据训练一个广义线性模型：

```
x1 = rand(100.0, 100)
x2 = rand(100.0, 100)
b0 = 6
b1 = 1
b2 = -2
err = norm(0, 10, 100)
y = b0 + b1 * x1 + b2 * x2 + err
t = table(x1, x2, y)
model = glm(sqlDS(<select * from t>), `y, `x1`x2, `gaussian, `identity);
model;

// output
coefficients->

beta     stdError tstat      pvalue
-------- -------- ---------- --------
1.027483 0.032631 31.487543  0
-1.99913 0.03517  -56.842186 0
5.260677 2.513633 2.092858   0.038972

link->identity
tolerance->1.0E-6
family->gaussian
xColNames->["x1","x2"]
modelName->Generalized Linear Model
residualDeviance->8873.158697
iterations->5
dispersion->91.475863
```

把模型用于预测：

```
predict(model, t);
```

把模型保存到磁盘：

```
saveModel(model, "C:/DolphinDB/Data/GLMModel.txt");
```

把模型加载到内存中：

```
loadModel("C:/DolphinDB/Data/GLMModel.txt");
```

