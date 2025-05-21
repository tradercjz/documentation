# pwlfPredict

## 语法

`pwlfPredict(model, X, [beta], [breaks])`

## 详情

本函数须结合函数 [piecewiseLinFit](piecewiselinfit.md)
共同使用，即使用 `piecewiseLinFit` 拟合后的连续分段线性回归模型来对输入的数据点进行预测。

## 参数

**model** 字典类型，由 `piecewiseLinFit` 函数返回的分段线性回归模型。

**X** 数值向量，表示需要预测的数据点的 x 坐标。注意：不可传入 NULL 值。

**beta** 可选参数，数值向量，表示分段线性回归模型的参数。注意：不可传入 NULL 值。

**breaks** 可选参数，数值向量，表示每段线段终点处的 x 坐标，每段线段的终点又被称为每段线段的断点。注意：不可传入 NULL 值。

## 返回值

浮点数向量，表示模型的预测值。

## 例子

本例先自定义参数条件，使用 `piecewiseLinFit` 拟合生成连续分段线性回归模型；再传入预测的数据点的 x 坐标
`xHat`，最后使用 `pwlfPredict` 计算模型的预测值。

```
def linspace(start, end, num, endpoint=true){
	if(endpoint) return end$DOUBLE\(num-1), start + end$DOUBLE\(num-1)*0..(num-1)
	else return start + end$DOUBLE\(num-1)*0..(num-1)
}
X = linspace(0.0, 1.0, 10)[1]
Y = [0.41703981, 0.80028691, 0.12593987, 0.58373723, 0.77572962, 0.41156172, 0.72300284, 0.32559528, 0.21812564, 0.41776427]
model = piecewiseLinFit(X, Y, 3)
xHat = linspace(0.0, 1.0, 20)[1]
pwlfPredict(model, xHat)
/*
output:
[0.593305499919518 0.524360777381737 0.455416054843957 0.386471332306177 0.317526609768396 0.368043438179296 0.529813781212159 0.691584124245021 0.69295837868457  0.655502915538459 0.618047452392347 0.580591989246236 0.543136526100125 0.505681062954014 0.468225599807903 0.430770136661792 0.393314673515681 0.35585921036957  0.318403747223459 0.280948284077348]
*/
```

相关函数：[piecewiseLinFit](piecewiselinfit.md)

