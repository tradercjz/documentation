# quantileSeries

## 语法

`quantileSeries(X, q, [interpolation='linear'])`

## 参数

**X** 是一个数值型向量。

**q** 是0到1之间的浮点型标量或向量。

**interpolation** 是一个字符串，表示当选中的分位点位于 i 和 j 之间时，采用的插值方法。它具有以下取值：

* 'linear': i+(j-1)\*fraction, fraction 是 size(X)\*q
  的小数部分
* 'lower':i
* 'higher': j
* 'nearest': i 和 j 之中最接近分位点的数据
* 'midpoint': (i+j)/2

如果没有指定 *interpolation*，默认采用 'linear'。

## 详情

计算 *X* 的分位数。

## 例子

```
a=[6, 47, 49, 15, 42, 41, 7, 39, 43, 40, 36];
quantileSeries(a,[0.25,0.5,0.75]);
// output
[25.5,40,42.5]

quantileSeries(a,[0.25,0.5,0.75], 'higher');
// output
[36,40,43]
```

相关函数：[quantile](quantile.md)

