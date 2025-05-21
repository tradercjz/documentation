# kmeans

## 语法

`kmeans(X, k, [maxIter=300], [randomSeed], [init='random'])`

## 参数

**X** 是一个表，表示训练集。

**k** 是一个正整数，表示要生成的聚类数。

**maxIter** 是一个正整数，表示质心更新的最大迭代次数。默认值是300。

**randomSeed** 是一个整数，表示质心初始化时随机算法的种子。默认值为 NULL。

**init** 可以是一个字符串或者一个矩阵，表示初始值的选择方式。默认值是 'random'。

* 若 *init* 是一个字符串，则可选参数为 'random' 或
  'k-means++'。'random' 表示根据 *randomSeed* 随机生成，'kmeans++' 表示根据
  kmeans++ 算法生成。
* 若 *init* 是一个矩阵，表示自定义的质心。其列数与表 *X* 需保持一致，行数为
  *k*。

## 详情

对训练集执行 K-Means 聚类。返回的结果是一个字典，包含以下 key：

* centers：一个 *k* 行 m 列的矩阵（m 是 *X* 的列数），包含各个类的质心坐标。
* predict：一个聚类模型预测函数，数据类型是 FUNCTIONDEF。
* modelName：字符串 'KMeans'。
* model：保存的模型，数据类型为 RESOURCE，用于预测。
* labels：一个向量，表示 *X* 中每一行数据对应的聚类的类标签。

## 例子

使用模拟数据训练一个 K-Means 模型：

```
t = table(100:0, `x0`x1, [DOUBLE, DOUBLE])
x0 = norm(1.0, 1.0, 50)
x1 = norm(1.0, 1.5, 50)
insert into t values (x0, x1)
x0 = norm(2.0, 1.0, 50)
x1 = norm(-1.0, 1.5, 50)
insert into t values (x0, x1)
x0 = norm(-1.0, 1.0, 50)
x1 = norm(-3.0, 1.5, 50)
insert into t values (x0, x1);

model = kmeans(t, 3);
model;

// output
centers->

#0        #1
--------- ---------
-1.048027 -3.809539
1.110899  1.24216
1.677974  -1.19158

predict->kmeansPredict
modelName->KMeans
model->KMeans
labels->[2,2,2,2,2,2,3,2,3,2,...]
```

