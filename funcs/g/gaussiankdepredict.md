# gaussianKdePredict

## 语法

`gaussianKdePredict(model,X)`

## 详情

[gaussianKde](gaussiankde.md)
对应的预测函数。使用其生成的模型对数据进行预测。

## 参数

**model** 字典类型，表示 `gaussianKde` 生成的字典。

**X** 数值向量、矩阵、元组或表类型，表示需要预测的数据。其维度必须和 `gaussianKde` 的数据集合的维度相同。

## 返回值

函数返回一个浮点型向量，大小和 *X* 的行数相同，表示 *X* 中每个数据点的预测结果。

## 例子

下例中先使用 `gaussianKde` 生成模型。传入指定的 [*trainset.txt*](../data/trainset.txt)，使用高斯核估计来预测数据的概率密度。然后调用 `predict`
函数，通过模型和传入的 [*testset.txt*](../data/testset.txt)
文件生成对应的预测结果。

```
trainData = loadText("trainset.txt"," ");
testData = loadText("testset.txt"," ");
model = gaussianKde(trainData)
gaussianKdePredict(model, testData)
/*
->[0.0623,0.0730,0.0336,0.0030,0.0001,0.0552....]
*/
```

相关函数：[gaussianKde](gaussiankde.md)

