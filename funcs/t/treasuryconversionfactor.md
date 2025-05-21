# treasuryConversionFactor

## 语法

`treasuryConversionFactor(contractCoupon, deliverableCoupon,
monthsToNextCoupon, remainingPayments, frequency)`

## 详情

本函数基于[中金所国债转换因子和应计利息计算公式](http://www.cffex.com.cn/5tf/)对转换因子进行估值计算。成功执行后将返回转换因子的估值，是一个 DOUBLE 类型的标量或向量。

## 参数

**contractCoupon** 数值型类型标量或向量，非负数，表示国债合约票面利率。

**deliverableCoupon** 数值型标量或向量，非负数，表示可交割国债的票面利率。

**monthsToNextCoupon** 整数类型标量或向量，非负数，表示交割月到下一付息月的月份数。

**remainingPayments** 整数类型标量或向量，非负数，表示剩余付息次数。

**frequency** 表示可交割国债每年的付息频率，支持两种输入类型：

* INT 类型标量或向量，正数，表示可交割国债每年的付息次数。例如，*frequency* = 1 表示每年付息 1
  次，即按年支付；*frequency* = 2 表示每年付息 2 次，即按半年期支付。
* DURATION 标量或向量：表示可交割国债每隔多久进行一次付息。例如，*frequency* = duration(`3M)，表示每隔 3
  个月付息一次，即按季度支付。

| 可选值 | 含义 |
| --- | --- |
| 1 / 1y | 表示每年付息1次 |
| 2 / 6M | 表示每年付息2次 / 每6个月付息1次 |
| 3 / 4M | 表示每年付息3次 / 每4个月付息1次 |
| 4 / 3M | 表示每年付息4次 / 每3个月付息1次 |
| 6 / 2M | 表示每年付息6次 / 每2个月付息1次 |
| 12 / 1M | 表示每年付息12次 / 每月付息1次 |
| 13 / 4w | 表示每年付息13次 / 每4周付息1次 |
| 26 / 2w | 表示每年付息26次 / 每2周付息1次 |
| 52 / 1w | 表示每年付息52次 / 每周付息1次 |
| 365 / 1d | 表示每年付息365次 / 每天付息1次 |

注意：在调用此函数时，必须保证所有提供的向量参数长度相同。若参数向量长度不一致，函数将会报错。

## 例子

假设 5 年期国债合约票面利率为 3%，交割月到下一付息月的月份数为 2，剩余付息次数为 1，可交割国债的票面利率为 3.2%，付息频率为
4，该种情况下对转换因子进行估值计算。

```
treasuryConversionFactor(contractCoupon=0.03, deliverableCoupon=0.032, monthsToNextCoupon=2, remainingPayments=1, frequency=4)
// Output：1.000324624767048
```

