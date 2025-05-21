# linearInterpolateFit

## 语法

`linearInterpolateFit(X, Y, [fillValue], [sorted=false])`

## 详情

为一组点集进行线性插值，支持内插（interpolate）和外插（extrapolate）两种模式。内插用于估计已知数据点之间的未知值，而外插则用于估计已知数据点范围之外的未知值。

## 参数

**X** 数值向量，表示用于插值的点的 x 坐标。注意：

* X 的长度至少为 2，即至少需要两个已知数据点才能进行插值。
* X中的值必须是唯一的且不可包含 NULL 值。

**Y** 数值向量，表示用于插值的点的 y 坐标。注意：*Y* 和 *X* 的长度必须一致，且不包含 NULL 值。

**fillValue** 可选参数，表示位于已知数据点范围之外的预测数据的赋值方式。支持以下两种方式：

* 形如 `(below, above)` 的数值类型数据对，below 和 above 分别表示当预测数据小于 X
  的最小值或大于 X 的最大值时的赋值。具体含义如下，Xmin 和 Xmax 分别表示输入参数
  *X* 向量中的最小值和最大值。

  + 当预测数据 Xnew < Xmin，将其赋值为 below；
  + 当预测数据 Xnew > Xmax，将其赋值为 above。
* 字符串 “extrapolate”，表示进行外插赋值，为默认值。

**sorted** 可选参数，布尔值标量，表示输入参数 X 是否有序递增。

* 如果为 true，则 *X* 必须是递增序列。
* 如果为 false，函数内部会对 *X* 进行排序，并相应调整 *Y* 的顺序。默认为 false。

## 返回值

返回一个字典，字典有以下成员：

* modelName：字符串类型，表示模型名称，值为 “linearInterpolate”。
* sortedX：Double 类型向量，表示对输入 *X* 进行升序排序后的向量。
* sortedY：Double 类型向量，表示与 *sortedX* 所对应的 y 值。
* fillValue：表示外插方式，即输入的 *fillValue* 参数值。
* predict：模型的预测函数，`predict` 函数将返回在新 X 点处的线性插值结果。可通过
  `model.predict(X)` 或 `predict(model, X)`
  进行调用。其中：

  + model：字典类型，即 `linearInterpolateFit` 的输出。
  + X： 数值向量，表示需要求值的点的 x 坐标。

## 例子

通过自定义函数 linspace 创建一组点集，对其进行线性插值。

```
def linspace(start, end, num, endpoint=true){
	if(endpoint) return end$DOUBLE\(num-1), start + end$DOUBLE\(num-1)*0..(num-1)
	else return start + (end-start)$DOUBLE\(num)*0..(num-1)
}
x = 0..9
y = exp(-x/3.0)
model = linearInterpolateFit(x, y, sorted=true)

/*Output
sortedX->[0.0,1.000000000000,2.000000000000,3.000000000000,4.000000000000,5.000000000000,6.000000000000,7.000000000000,8.000000000000,9.000000000000]
modelName->linearInterpolate
predict->linearInterpolatePredict
fillValue->extrapolate
sortedY->[1.000000000000,0.716531310573,0.513417119032,0.367879441171,0.263597138115,0.188875602837,0.135335283236,0.096971967864,0.069483451222,0.049787068367]
*/

// 使用新 X 值进行预测
xnew = linspace(0,9,15,false)
model.predict(xnew)

//Output：[1,0.829918786344274,0.67590847226555,0.554039957340832,0.455202047888132,0.367879441171442,0.305310059338013,0.248652831060094,0.203819909893195,0.167459474997182,0.135335283236613,0.112317294013288,0.091474264536084,0.074981154551122,0.061604898080826]
```

