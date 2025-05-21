# tema

## 语法

`tema(X, window)`

TA-lib 系列函数参数说明和窗口计算规则请参考：[TAlib](../themes/TAlib.md)

## 详情

在给定长度（以元素个数衡量）的滑动窗口内，计算 *X* 的三重指数移动平均（Triple Exponential
Moving Average）。

其计算公式为：

![ema1](../../images/ema1.png)

![ema2](../../images/ema2.png)
![tema](../../images/tema.png)

## 例子

```
x=12.1 12.2 12.6 12.8 11.9 11.6 11.2
tema(x,3);
// output
[,,,,,,11.24444444444444]

x=matrix(12.1 12.2 12.6 12.8 11.9 11.6 11.2, 14 15 18 19 21 12 10)
tema(x,3);
```

| col1 | col2 |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
| 11.2444 | 10.6296 |

相关函数：[ema](../e/ema.md), [dema](../d/dema.md)

