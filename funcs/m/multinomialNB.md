# multinomialNB

## 语法

`multinomialNB(Y, X, [varSmoothing=1.0])`

## 参数

**Y** 是一个长度与 *X* 的行数相等的向量，表示 *X* 中每个样本对应的标签。

**X** 是一个表，表示训练集。表中每一行表示一个样本，每一列表示一个特征。

**varSmoothing** 是0到1之间的浮点数，表示平滑系数。

## 详情

使用多项式朴素贝叶斯（Multinomial Naive Bayes）算法对数据进行分类训练。返回的结果是一个字典，包含以下key：

* modelName：模型名称，为字符串 "MultinomialNB"
* model：multinomialNB 的内部模型
* varSmoothing：训练时使用的平滑系数

## 例子

本例所用数据集 iris.data 可从 <https://archive.ics.uci.edu/ml/datasets/iris> 下载。

```
DATA_DIR = "C:/DolphinDB/Data"
t = loadText(DATA_DIR+"/iris.data")
t.rename!(`col0`col1`col2`col3`col4, `sepalLength`sepalWidth`petalLength`petalWidth`class)
t[`classType] = take(0, t.size())
update t set classType = 1 where class = "Iris-versicolor"
update t set classType = 2 where class = "Iris-virginica"

training = select sepalLength, sepalWidth, petalLength, petalWidth from t
labels = t.classType

model = multinomialNB(labels, training);

predict(model, training);
```

