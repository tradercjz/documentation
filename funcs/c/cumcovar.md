# cumcovar

## 语法

`cumcovar(X,Y)`

参数说明和窗口计算规则请参考：[累计窗口系列（cum 系列）](../themes/cumFunctions.html)

## 详情

累积计算 *X* 和 *Y* 的协方（covariance）。

## 例子

```
x = 7 4 5 8 9
y = 1 7 8 9 0
cumcovar(x, y);
// output
[,-9,-5.166667,-1,-4.5]
```

相关函数：[covar](covar.html)

