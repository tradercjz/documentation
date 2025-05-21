# esd

## 语法

`esd(data, [hybrid], [maxAnomalies], [alpha])`

## 参数

**data** 是一个数值向量。

**hybrid** 是一个布尔值，表示是否用中位数和绝对中位差代替 Grubb's test 中 zscore
计算的平均值和标准差。如果 *hybrid* 为 true，算法更具鲁棒性。默认值为 false。

**maxAnomalies** 是一个正整数或(0, 0.5)之间的浮点数。默认值为0.1。

* 如果 *maxAnomalies* 是正整数，*maxAnomalies* 必须小于
  *data* 长度的一半，函数最多检测 *maxAnomalies* 个异常点。
* 如果 *maxAnomalies* 是(0, 0.5)之间的浮点数，函数最多检测
  int(size(data) \* maxAnomalies) 个异常点。

**alpha** 是一个正数，表示检验的显著度。*alpha* 越大，数据越有可能被判断为异常点。

## 详情

使用 ESD (Extreme Studentized Deviate)
算法对时间序列进行异常检测。返回的结果是一个包含异常值的表，该表有两列，index 列记录原始数据中异常值的下标，anoms 列记录异常值。

## 例子

```
n = 1000
ts = rand(10.0, n)
ts[500 600 700 999] += 20
esd(ts);
```

| index | anoms |
| --- | --- |
| 600 | 29.815742 |
| 700 | 25.517493 |
| 500 | 25.17515 |
| 999 | 24.748516 |

相关函数：[stl](../s/stl.html), [seasonalEsd](../s/seasonalEsd.html)

