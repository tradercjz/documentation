# brentq

## 语法

`brentq(f, a, b, [xtol], [rtol], [maxIter],
[funcDataParam])`

## 参数

**f** 是一个返回值为一个数值的函数。函数在 [a, b] 内连续且 f(a) 与 f(b) 的正负号需要相反。

**a** 是一个数值标量，指定区间的左边界。

**b** 是一个数值标量，指定区间的右边界。

**xtol** 是一个数值标量，用于指定求解结果的精度，默认值为 2e-12。

**rtol** 是一个数值标量，用于指定求解结果的精度，默认值为 4 倍的 DOUBLE 类型的机器精度。

**maxIter** 是一个整形标量，指定 Brent 的最大迭代次数，默认值为 100 。

**funcDataParam** 是一个向量，指定函数 f 的其他参数。

## 详情

使用 Brent 方法在一个给定区间 [a, b] 内求出函数 f(x) 的一个根 x0，使得 f(x0)=0 ，求解精度满足 `|x-x0| <=
(xtol + rtol* |x0| )`，其中 x 是精确根，x0 为计算结果。

返回值为长度为2的向量 res：

* res[0] 是一个字符串标量，表示求解状态。共有三种求解状态：
  + CONVERGED， 表示得到符合预期的解；
  + SIGNERR，表示 f(a) 与 f(b) 同号，不满足正负号相反的要求；
  + CONVERR，表示达到最大迭代次数
* res[1] 是一个数值标量，表示求得的根。

## 例子

求解 f(x) = x^2 - 1 在 [-2,0], [0,2] 的根

```
def f(x) {
    return (pow(x, 2) - 1)
}

root1 = brentq(f, -2, 0)
root2 = brentq(f, 0, 2)
print("root1 : ", root1)
print("root2 : ", root2)
```

返回如下：

```
root1 :
("CONVERGED",-1)
root2 :
("CONVERGED",1)
```

求解带有额外参数的函数 f(x,b) 在 [0,2] 的根：

```
def f(x, b) {
    return (pow(x, 2) - b)
}
root = brentq(f, 0, 2, 2e-12, 1e-9, 100, [2])
print("root : ", root)
```

返回如下：

```
root :
("CONVERGED",1.414213562373136)
```

