# kroghInterpolateFit

## 语法

`kroghInterpolateFit(X, Y, [der=0])`

## 详情

对一组点集进行多项式插值，该多项式通过点集中所有的点对 (X, Y)。并且可以额外指定在每个点 X 处的多个导数值：用户通过重复 X 值并将导数值指定为连续的 Y
值来实现：

* 当 X 只出现一次时，Y 为多项式 f(x) 的值。
* 当 X 出现多次时，则第一个 Y 是 f(X) 的值，第二个为对应的 X 的一阶导数值，第三个为对应的 X 的二阶导数值，依此类推。比如对于输入 X =
  [0,0,1,1], Y= [1,0,2,3], 有 Y[0]=f(0)，Y[1]=f'(0)，Y[2]=f(1)，Y[3]=f'(1)。

另外，本函数可结合 [predict](../p/predict.md)
函数先后使用，针对生成的模型进行预测。

## 参数

**X** 数值向量，表示用于插值的点的 x 坐标，必须是递增序列。注意：X 中不可包含 NULL 值。

**Y** 数值向量，表示用于插值的点的 y 坐标。注意：Y 和 X 的长度必须一致，且 Y 中不可包含 NULL 值。

**der** 可选参数，非负整数，表示要求的导数阶数。*der*=0 时计算多项式函数本身的值。其默认值为 0。

## 返回值

返回一个字典，字典有以下成员：

* modelName：字符串类型，表示模型名称，值为“kroghInterpolate”。
* X：数值向量，表示用于插值的点的x坐标，即输入 X。
* der：非负整数，即输入 der。
* coeffs：数值向量，表示根据输入数据点拟合得到的多项式系数。
* predict：模型的预测函数。其使用方法为 `model.predict(X)`，或者通过 [predict](../p/predict.md) 函数进行调用：`predict(model,
  X)`。其参数为：

  + model：字典类型，即 kroghInterpolateFit 的输出。
  + X： 数值向量，表示需要求值的点的 x 坐标，`predict` 函数将返回在 X
    点处的多项式估值。

## 例子

以正弦函数为例进行多项式插值，计算 x
点处的多项式估值。

```
x = 0 1 2 3 4 5
y = sin(x)
model = kroghInterpolateFit(x,y)
model

/*
output:
X->[0,1,2,3,4,5]
der->0
predict->kroghInterpolateFitPredict
modelName->kroghInterpolate
coeffs->[0.0,0.841470984807,-0.386822271395,-0.010393219665,0.032025753923,-0.005411092181,0.0]
*/
```

根据生成的模型，自定义函数
`linspace`，并传入相关参数，进一步预测模型。

```
def linspace(start, end, num, endpoint=true){
	if(endpoint) return end$DOUBLE\(num-1), start + end$DOUBLE\(num-1)*0..(num-1)
	else return start + end$DOUBLE\(num-1)*0..(num-1)
}
xx = linspace(0.0, 5.0, 10)[1]
model.predict(xx)

/*
output:
[0,0.515119011157387,0.898231239576709,0.998548648650381,0.793484053410063,0.354287125066207,-0.188319604452395,-0.678504737959061,-0.969692008469677,-0.958924274663139]
*/
```

相关函数：[predict,](../p/predict.md)
[kroghinterpolate](kroghinterpolate.md)

