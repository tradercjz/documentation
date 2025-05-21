# elasticNetCV

## 语法

`elasticNetCV(ds, yColName, xColNames, [alpha=[0.01,0.1,1.0]], [l1Ratio=0.5],
[intercept=true], [normalize=false], [maxIter=1000], [tolerance=0.0001],
[positive=false])`

## 详情

使用五折交叉验证方法进行弹性网络回归（ElasticNet），输出最优参数对应的模型。结果为一个字典，包含以下 key：

* modelName：模型名称。elasticNetCV 方法对应的模型名为 "elasticNetCV"。
* coefficients：模型的回归系数。
* intercept：截距。
* dual\_gap：表示优化结束时的对偶间隙。
* tolerance：迭代中止的边界差值。
* iterations：迭代次数
* xColNames：数据源中自变量的列名。
* predict：用于预测的函数。
* alpha：交叉验证选择的惩罚量。

## 参数

**alpha** 是浮点型标量或向量，表示乘以L1范数惩罚项的系数。默认值是 [0.01, 0.1, 1.0]。

注： 除 *alphas* 参数外，其它参数都和 [elasticNet](elasticNet.md)
的参数相同，参数描述可参考 [elasticNet](elasticNet.md)。这里仅说明 *alphas* 参数。

## 例子

```
y = [225.720746,-76.195841,63.089878,139.44561,-65.548346,2.037451,22.403987,-0.678415,37.884102,37.308288]
x0 = [2.240893,-0.854096,0.400157,1.454274,-0.977278,-0.205158,0.121675,-0.151357,0.333674,0.410599]
x1 = [0.978738,0.313068,1.764052,0.144044,1.867558,1.494079,0.761038,0.950088,0.443863,-0.103219]
t = table(y, x0, x1);

elasticNetCV(t, `y, `x0`x1);
```

返回如下：

```
dual_gap->0.0037
modelName->elasticNetCV
intercept->0.5416
alpha->0.0100
coefficients->[93.8331,13.9105]
predict->coordinateDescentPredict
xColNames->[x0,x1]
tolerance->0.0001
iterations->5
```

