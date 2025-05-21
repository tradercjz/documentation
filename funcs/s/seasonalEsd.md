# seasonalEsd

## 语法

`seasonalEsd(data, period, [hybrid], [maxAnomalies], [alpha])`

## 参数

**data** 是一个数值向量，表示时间序列。

**period** 是一个大于1的整数，表示时间序列的周期。

**hybrid** 是一个布尔值，表示是否用中位数和绝对中位差代替 Grubb's test 中 zscore
计算的平均值和标准差。如果 *hybrid* 为 true，算法更具鲁棒性。默认值为 false。

**maxAnomalies** 是一个正整数或(0, 0.5)之间的浮点数。默认值为0.1。

* 如果 *maxAnomalies* 是正整数，且 *maxAnomalies* 必须小于
  data 长度的一半，函数最多检测 *maxAnomalies* 个异常点。
* 如果 *maxAnomalies* 是(0, 0.5)之间的浮点数，函数最多检测
  int(size(data) \* *maxAnomalies* ) 个异常点。

**alpha** 是一个正数，表示显著度。*alpha* 越大，数据越有可能被判断为异常点。

## 详情

使用 S-ESD(Seasonal Extreme Studentized Deviate)
算法对周期性的时间序列进行异常检测。返回结果是包含了异常值的表，该表有两列，index 列记录原始数据中异常值的下标，anoms 列记录异常值。

## 例子

定时执行一个函数：

```
n = 100
trend = 6 * sin(1..n \ 200)
seasonal = sin(pi / 6 * 1..n)
residual = rand(1.0, n) - 0.5
data = trend + seasonal + residual
data[20 50 70] += 20;

seasonalEsd(data, 12);
```

| index | anoms |
| --- | --- |
| 50 | 22.6365 |
| 70 | 21.141346 |
| 20 | 19.174165 |

相关函数：[stl](stl.html), [esd](../e/esd.html)

