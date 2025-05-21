# knn

## 语法

`knn(Y, X, type, nNeighbor, [power=2])`

## 参数

**Y** 是一个长度与X的行数相等的向量，表示X中每个样本对应的标签。

**X** 是一张表，表示训练集。表中的每一行表示一个样本，每一列表示一个特征。

**type** 是一个字符串。它的取值可以是 'regressor' 或 'classifier'。

**nNeighbor** 是一个正整数，表示 K 邻近算法的邻近节点个数。

**power** 是一个正整数，表示闵可夫斯基距离（Minkowski Distance）的参数。默认值是2，表示使用欧几里得距离（Euclidean
Distance）。如果 *power*=1，表示使用曼哈顿距离（Manhattan Distance）。

## 详情

通过 K 邻近算法（暴力搜索法）对表中的数据进行训练。返回的结果是一个字典，包含以下 key：

* nNeighbor：训练时所用的邻近节点个数
* modelName：模型的名称，为字符串 "KNN"
* model：内部模型
* power：训练时所用的闵可夫斯基距离
* type：字符串 "regressor" 或 "classifier"

## 例子

```
height = 158 158 158 160 160 163 163 160 163 165 165 165 168 168 168 170 170 170
weight = 58 59 63 59 60 60 61 64 64 61 62 65 62 63 66 63 64 68
t=table(height, weight)
labels=take(1,7) join take(2,11)
model = knn(labels,t,"classifier", 5);
```

