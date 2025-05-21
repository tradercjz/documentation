# cdfNormal

## 语法

`cdfNormal(mean, stdev, X)`

## 参数

**mean** 是正态分布的均值。

**stdev** 是正态分布的标准差。

**X** 是数值型标量或向量。

## 详情

返回均值为 *mean*，标准差为 *stdev* 的正态分布的累计密度函数的值。

## 例子

```
cdfNormal(0,1,-2.33);
// output
0.009903

cdfNormal(10, 20, -30);
// output
0.02275
```

