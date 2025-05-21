# kurtosis

## 语法

`kurtosis(X, [biased=true])`

## 参数

**X** 是一个向量、矩阵或表。

**biased** 是一个布尔值，表示是否为有偏估计。默认值为 true，表示为有偏估计。

## 详情

计算 *X* 的峰度。`kurtosis` 函数在计算时会忽略 NULL 值。

* 若 *biased*=true，表示结果为有偏估计，计算公式为：

![k1](../../images/k1.png)

* 若 *biased*=false，表示结果为无偏估计，计算公式为：

![k0](../../images/k0.png)

* 若 *X* 为矩阵，计算每列的峰度，返回一个向量。
* 若 *X* 为表，计算每列的峰度，返回一个表。

`kurtosis` 函数也支持校正偏差查询分区表和分布式表。

DolphinDB 的 `kurtosis` 默认情况（当 *biased*=true
时）存在偏差，而 pandas 和 Excel 的 kurt 默认为无偏估计，且减去了正态分布的峰度3。参考下面例子，可以使 DolphinDB 的峰度计算结果与
pandas 和 excel 的结果保持一致：

```
python
m = [1111, 323, 43, 51]
df = pandas.DataFrame(m)
y = df.kurt()
// output
2.504252

dolphindb
m=matrix(1111 323 43 51)
kurtosis(m, false) - 3
// output
2.5043
```

## 例子

下面的例子使用了 [norm](../n/norm.md)
函数生成数据，每次生成的数据都会有细微差别，因此每次计算的结果会有所偏差。

```
x=norm(0, 1, 1000000);
kurtosis(x);
// output
3.000249

x[0]=100;
kurtosis(x);
// output
100.626722

m=matrix(1..10, 1 2 3 4 5 6 7 8 9 100);
m;
```

| #0 | #1 |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |
| 4 | 4 |
| 5 | 5 |
| 6 | 6 |
| 7 | 7 |
| 8 | 8 |
| 9 | 9 |
| 10 | 100 |

```
kurtosis(m);
// output
[1.775757575757576,7.997552566718839]
```

