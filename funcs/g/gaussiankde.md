# gaussianKde

## 语法

`gaussianKde(X,[weights],[bwMethod="scott"])`

## 详情

使用核密度估计方法中的高斯核来估计随机变量的概率密度。

生成的模型可以作为 `gaussianKdePredict` 函数的输入。

## 参数

**X** 数值向量、矩阵、元组或表类型，表示给定的数据集合。*X* 的每一行表示一个数据点，元素数量至少为 2（即数据点的维度至少为
2），各数据点的维度保持一致，且 *X* 的行数须大于列数。暂时不支持分布式表。

**weights** 数值向量类型，可选参数，表示每一个数据点的权重，默认每个数据点的权重相同。向量中数值必须非负且不全为0；且向量大小须和 *X*
的行数相同。

**bwMethod** 数值标量，字符串标量或函数名类型，可选参数，表示带宽的生成方式。默认值为”scott”。

* 若传入数值标量，则表示带宽的大小。
* 若传入字符串标量类型，可选值为”scott”和”silverman”。
* 若传入函数，表示用于计算带宽的函数，其输入值为已传入的参数 *X*，执行后得到带宽的值。注意：返回值须为数值标量。

## 返回值

返回一个字典，字典的内容有：

* X：浮点型向量或矩阵，表示输入的数据集合 *X*。
* cov：浮点型矩阵，表示的是通过 *weights*、*X* 和带宽生成的协方差矩阵的 cholesky 分解矩阵。
* weights：浮点型向量，表示对应的权重。
* predict：函数指针，表示对应的预测函数。其使用方法为
  `model.gaussianKdePredict(model,X)`，详情见
  gaussianKdePredict。
* bandwidth：浮点型标量，表示的生成的带宽。

## 例子

下例传入指定的 [*trainset.txt*](../data/trainset.txt)，使用高斯核估计来预测数据的概率密度。

```
trainData = loadText("trainset.txt"," ");
model = gaussianKde(trainData)
model
/* Output
X->
#0      #1
0.1460  -0.1659
-1.3717 -1.6650
-1.6957 -1.1680
-0.7976 0.6081
0.1088  2.5113
-0.0724 -0.8210
-1.7548 -0.3485
1.1202  0.9004
1.0234  0.7907
-0.4256 0.7169

predict->gaussianKdePredict
cov->
#0     #1
0.7040 0.0
0.4921 0.6700

weights->[0.1000,0.1000,0.1000,0.1000,0.1000,0.1000,0.1000,0.1000,0.1000,0.1000]
bandwidth->0.6812
*/
```

承接上例，传入 [*testset.txt*](../data/testset.txt)
文件，`gaussianKde` 可与 `gaussianKdePredict`
函数结合使用，生成其对应的预测结果。

```
testData = loadText("testset.txt"," ");
model.predict(testData)
/* Output
->[0.0623,0.0730,0.0336,0.0030,0.0001,0.0552....]
*/
```

相关函数：[gaussianKdePredict](gaussiankdepredict.md)

