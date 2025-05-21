# ema

## 语法

`ema(X, window, warmup=false)`

TA-lib 系列函数参数说明和窗口计算规则请参考：[TA-lib 系列](../themes/TAlib.html)

## 参数

**warmup** 布尔值，默认为 false，即计算结果的前 *window*-1 个元素为空值。若为
true，则结果的前 *window*-1 元素将由详情给出的公式计算得出。

## 详情

在给定长度（以元素个数衡量）的滑动窗口内，计算 *X* 的指数移动平均（Exponential Moving
Average）。

其计算公式为：

* *warmup*=false：

![EMA_k](../../images/ema_k.png)

* *warmup*=true:

![EMA_ktrue](../../images/ema_ktrue.png)

其中：![EMA_k1](../../images/EMA_k1.png)为第k个指数移动平均值，![n](../../images/n.png)为移动窗口长度，![xk](../../images/xk.png)为向量 ![x](../../images/x.png)中第 k 个元素。

## 例子

```
x=12.1 12.2 12.6 12.8 11.9 11.6 11.2
ema(x,3);
// output
[,,12.3,12.55,12.225,11.9125,11.55625]

ema(x,3, warmup=true)
// output
[12.1,12.2,12.4667,12.6333,12.2667,11.9333,11.5667]

x=matrix(12.1 12.2 12.6 12.8 11.9 11.6 11.2, 14 15 18 19 21 12 10)
ema(x,3);
```

| #0 | #1 |
| --- | --- |
|  |  |
|  |  |
| 12.30 | 15.666667 |
| 12.55 | 17.333333 |
| 12.225 | 19.166667 |
| 11.9125 | 15.583333 |
| 11.55625 | 12.791667 |

相关函数：[gema](../g/gema.html), [wilder](../w/wilder.html), [dema](../d/dema.html), [tema](../t/tema.html)

