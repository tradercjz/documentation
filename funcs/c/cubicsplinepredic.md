# cubicSplinePredict

## 语法

`cubicSplinePredict(model, x)`

## 详情

根据 *model* 给出的三次样条曲线，预测 x 对应的 y。

## 参数

**model** 是一个字典，包含两个 key：c 和 x，其中 c 的值是三次样条函数的分段多项式的系数，x 的值是分段多项式的分段点，c 的长度=（x
的长度-1）\*4。c 和 x 的值均不可包含空值。*model* 可由 `cubicSpline` 函数生成。

**x** 是一个数值型标量或向量要预测的自变量。

## 例子

```
n = 10
x = 0..(n-1)
y = sin(x)
model = cubicSpline(x, y, bc_type="not-a-knot")

newx = [-0.5, 0.5, 0.7, 1.2, 4.5, 8.9, 9.3]
ret = cubicSplinePredict(model, newx)
```

返回：

```
[-0.632383304169291,0.501747281896522,0.658837295715183,0.924963051153032,-0.974025627606784,0.515113155358425,0.03881591118089]
```

**相关信息**

* [cubicSpline](cubicspline.html "cubicSpline")

