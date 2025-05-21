# saveModel

## 语法

`saveModel(model, location)`

## 参数

**model** 需要保存的模型，一般是字典，由 [randomForestClassifier](../r/randomForestClassifier.md), [randomForestRegressor](../r/randomForestRegressor.md) 等机器学习函数生成。

**location** 字符串，表示服务器端输出文件的绝对路径或相对路径。

## 详情

把模型保存到本地文件中，返回表示保存结果的布尔值。

## 例子

```
x1 = rand(100.0, 100)
x2 = rand(100.0, 100)
b0 = 6
b1 = 1
b2 = -2
err = norm(0, 10, 100)
y = b0 + b1 * x1 + b2 * x2 + err
t = table(x1, x2, y)
model = randomForestRegressor(sqlDS(<select * from t>), `y, `x1`x2)
saveModel(model, "/home/DolphinDB/Data/regressionModel.txt");
```

