# cumcorr

## 语法

`cumcorr(X,Y)`

参数说明和窗口计算规则请参考: [累计窗口系列（cum 系列）](../themes/cumFunctions.html)

## 参数

**X** 和 **Y** 是向量、矩阵或表。

## 详情

累计计算 *X* 和 *Y* 之间的相关性（correlation）。

## 例子

```
x = 7 4 5 8 9
y = 1 7 8 9 0
cumcorr(x, y);

// output
[,-1,-0.893405,-0.1524,-0.518751]
```

相关函数：[corr](corr.html)

