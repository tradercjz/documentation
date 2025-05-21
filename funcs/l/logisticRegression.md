# logisticRegression

## 语法

`logisticRegression(ds, yColName, xColNames, [intercept=true], [initTheta],
[tolerance=1e-3], [maxIter=500], [regularizationCoeff=1.0])`

## 参数

**ds** 是数据源，通常是由 [sqlDS](../s/sqlDS.html) 生成。

**yColName** 是字符串，表示数据源中作为因变量（所属分类）的列名。

**xColNames** 是字符串标量或向量，表示数据源中作为自变量的列名。

**intercept** 是布尔值，表示是否包含回归中的截距。默认值为True，系统会自动给自变量添加一列，该列的值全为1，用于生成截距。

**initTheta** 是迭代的初始参数向量。默认是长度为 *xColNames.size()+intercept* 的零向量。

**tolerance** 是迭代中止的边界差值 。如果在两次相邻迭代中，参数的对数似然函数的梯度的绝对值最大分量的差小于
*tolerance*，迭代中止。默认值是0.001。

**maxIter** 是正整数，表示最大的迭代次数。当迭代次数达到 *maxIter* 时，迭代中止。默认值是500.

**regularizationCoeff** 是正数，表示正则项系数。默认值是1.0。

## 详情

计算数据源中 *xColNames* 和 *yColName* 逻辑回归的结果。返回结果是一个字典，包含以下
key：*iterations*, *modelName*, *coefficients*, *tolerance*,
*logLikelihood*, *xColNames* 和 *intercept*。其中，*iterations*
是实际迭代的次数；*modelName* 是 “Logistic Regression”；*coefficients*
是向量，表示模型参数的估计值；*logLikelihood* 是最终的对数似然值。

生成的模型可以作为 *predict* 函数的输入。

## 例子

以下例子把两个不同中心的正态分布标记为两类，然后计算逻辑回归模型。

```
t = table(100:0, `y`x0`x1, [INT,DOUBLE,DOUBLE])
y = take(0, 50)
x0 = norm(-1.0, 1.0, 50)
x1 = norm(-1.0, 1.0, 50)
insert into t values (y, x0, x1)
y = take(1, 50)
x0 = norm(1.0, 1.0, 50)
x1 = norm(1.0, 1.0, 50)
insert into t values (y, x0, x1)

model = logisticRegression(sqlDS(<select * from t>), `y, `x0`x1);

// output
modelName->Logistic Regression
logLikelihood->-23.269132
intercept->true
coefficients->[1.377971,1.914001,-0.305114]
xColNames->[x0,x1]
iterations->7
tolerance->0.001
```

把模型用于预测：

```
predict(model, t);
```

保存模型到磁盘：

```
saveModel(model, "C:/DolphinDB/data/logisticModel.txt");
```

加载一个保存的模型：

```
loadModel("C:/DolphinDB/data/logisticModel.txt");
```

