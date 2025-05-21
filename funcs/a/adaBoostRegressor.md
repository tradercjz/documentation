# adaBoostRegressor

## 语法

`adaBoostRegressor(ds, yColName, xColNames,
[maxFeatures=0], [numTrees=10], [numBins=32], [maxDepth=10],
[minImpurityDecrease=0.0], [learningRate=0.1], [loss='linear'],
[randomSeed])`

## 参数

**ds** 是数据源，通常用 `sqlDS` 函数生成。

**yColName** 是字符串，表示数据源中作为因变量（所属分类）的列名。

**xColNames** 是字符串标量或向量，表示数据源中作为自变量的列名。

**numClasses** 是正整数，表示分类数目。y列的取值必须是[0, numClasses)之间的整数。

**maxFeatures** 是一个整数或浮点数，表示一次分裂节点选取的特征个数或比例。默认值是0。

* 如果 *maxFeatures* 为正整数，则在一次分裂时选取
  *maxFeatures* 个特征。
* 如果 *maxFeatures* =0 ，则在一次分裂时选取全部特征。
* 如果 *maxFeatures* 是一个0和1之间的浮点数，则在一次分裂时选取
  int(特征列数量\*maxFeatures)个特征。

**numTrees** 是正整数，表示产生树的最大个数，即停止提升时的最大迭代次数。如果能够完美训练，学习会提前中止。默认值为10。

**numBins** 是正整数，表示离散化连续特征时的桶数。默认值为32。增加 *numBins*
会使算法考虑更多的分裂节点的决策值，产生更好的分裂结果，但也会提高计算量和通讯量。

**maxDepth** 是正整数，表示树的最大深度。默认值为10。

**minImpurityDecrease** 是浮点数，如果分裂产生的基尼指数纯度减少值大于或等于这个值，节点会继续分裂。

**learningRate** 是正浮点数，表示迭代过程中的每个分类器对下一个分类器的样本权重的影响。

**algorithm** 是一个字符串，表示所使用的算法，可以取值 "SAMME.R" 或 "SAMME"。默认值为 "SAMME.R"。

**loss** 是一个字符串，表示在提升迭代时，更新样本权重时所用的损失函数，可以取值 "linear", "square" 或
"exponential"。默认值为 "linear"。

**randomSeed** 是随机数生成器使用的种子。

## 详情

进行 AdaBoost 回归。返回结果是字典，包含以下 key：numClasses, minImpurityDecrease,
maxDepth, numBins, numTrees, maxFeatures, model, modelName, xColNames, learningRate,
loss. 其中 model 是一个元组，保存了训练生成的树；modelName 为 "AdaBoost Regressor"。

生成的模型可以作为 `predict` 函数的输入

## 例子

用模拟数据训练一个 AdaBoost 分类模型

```
n=10
x1 = rand(1.0, n)
x2 = rand(1.0, n)
b0 = 1
b1 = 1
b2 = -2
err = norm(0, 0.2, n)
y = b0 + b1 * x1 + b2 * x2 + err
t = table(y, x1, x2)
model = adaBoostRegressor(sqlDS(<select * from t>), `y, `x1`x2);
```

把模型用于预测

```
t1 = table(0 0.4 0.7 1 as x1, 0.9 0.2 0.1 0 as x2)
predict(model, t1);
```

保存模型到磁盘及加载保存的模型

```
saveModel(model, "C:/DolphinDB/data/regressionModel.bin")
loadModel("C:/DolphinDB/data/regressionModel.bin");
```

相关函数：[adaBoostClassifier](adaBoostClassifier.html),
[randomForestClassifier](../r/randomForestClassifier.html), [randomForestRegressor](../r/randomForestRegressor.html)

