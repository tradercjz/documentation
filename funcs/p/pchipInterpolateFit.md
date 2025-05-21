# pchipInterpolateFit

## 语法

`pchipInterpolateFit(X, Y, [extrapolate=true])`

## 参数

**X** 数值型向量，表示用于插值的点的 x 坐标（自变量）。*X* 必须严格递增，且至少包含两个元素。

**Y** 与 *X* 等长的数值型向量，表示用于插值的点的 y 坐标（因变量）。

**extrapolate** 可选参数，布尔标量，表示当预测点超出已知数据范围时是否进行外插。默认为 true。

## 详情

对一组数值向量 *X* 和 *Y* 进行分段三次 Hermite 多项式插值（PCHIP）。

**返回值**：返回一个字典，包含以下键值对：

* modelName：字符串“PchipInterpolate”，表示模型名称。
* X：DOUBLE 向量，表示输入参数 *X*。
* extrapolate：BOOL 标量，即输入参数 *extrapolate*。
* coeffs：数值型向量，表示根据输入数据点拟合得到的多项式系数。
* predict：模型的预测函数，可以通过 `model.predict(X)` 或 `predict(model,
  X)` 调用，其中：
  + model：字典，即当前函数 `pchipInterpolateFit`的返回。
  + X：数值型向量，表示需要求值的点的 x 坐标，`predict` 函数将返回在 *X*
    点处的插值结果。

## 例子

对 x 和 y 进行进行分段三次 Hermite 多项式插值。

```
def linspace(start, end, num, endpoint=true){
	if(endpoint) return end$DOUBLE\(num-1), start + end$DOUBLE\(num-1)*0..(num-1)
	else return start + end$DOUBLE\(num-1)*0..(num-1)
}

x_observed = linspace(0.0, 10.0, 11)[1]
y_observed = sin(x_observed)

model = pchipInterpolateFit(x_observed, y_observed)
model;

/* output:
modelName->PchipInterpolate
X->[0,1,2,3,4,5,6,7,8,9,10]
coeffs->#0                 #1                 #2                 #3
------------------ ------------------ ------------------ ------------------
-0.32911446845195  -0.057707802943105 1.228293256202952  0
-0.01011863907468  -0.047589163868426 0.125534244960891  0.841470984807897
0.708356730424705  -1.476534149190519 0                  0.909297426825682
0.637878921149598  -0.707803317410469 -0.827998107106924 0.141120008059867
0.074275580231352  0.053570618892506  -0.329967978479069 -0.756802495307928
-0.571482233207003 1.250991009671215  0                  -0.958924274663138
-0.594663658922633 0.743530436118926  0.787535319721422  -0.279415498198926
-0.174138080617811 0.015904513331029  0.490605215191374  0.656986598718789
0.434603140426252  -1.011842901807877 0                  0.989358246623382
0.046813296419378  -0.283076510213506 -0.719876382336998 0.412118485241757

extrapolate->true
predict->cubicHermiteSplinePredict
*/
```

**相关函数：**[predict](predict.html)
[cubicHermiteSplineFit](../c/cubichermitesplinefit.html)

