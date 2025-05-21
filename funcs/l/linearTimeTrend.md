# linearTimeTrend

## 语法

`linearTimeTrend(X, window)`

TA-lib 系列函数参数说明和窗口计算规则请参考: [TA-lib 系列](../themes/TAlib.html)

## 详情

计算滑动线性回归，返回一个 tuple 类，包含两列，分别是 alpha 和 beta，对应 talib 中的 linearreg\_intercept（线性回归截距）和
linearreg\_slope（线性回归斜率指标）。

## 例子

```
x = 3 3 5 7 8 9 10 11 15 13 12 11 10
print linearTimeTrend(x,3)
// output
([,,2.666666666666666,3,5.166666666666667,7,8,9,9.5,12,14.833333333333333,13,12],[,,1,2,1.5,1,1,1,2.5,1,-1.5,-1,-1])
```

```
n = 10
t = table(09:00:00 + 1..n as time, rand(`A`B, n) as sym, rand(100.0, n) as val1, rand(1000..2000, n) as val2)
select time, sym, linearTimeTrend(val1, 3) as `alpha`beta from t
```

| time | sym | alpha | beta |
| --- | --- | --- | --- |
| 09:00:01 | B |  |  |
| 09:00:02 | A |  |  |
| 09:00:03 | A | 85.0844 | -30.0688 |
| 09:00:04 | B | 49.3461 | 7.3621 |
| 09:00:05 | B | 30.4248 | 28.3589 |
| 09:00:06 | A | 83.106 | -7.7515 |
| 09:00:07 | B | 78.4412 | -17.7575 |
| 09:00:08 | A | 56.8575 | 4.4732 |
| 09:00:09 | A | 53.8492 | -6.0653 |
| 09:00:10 | A | 61.7888 | -4.5586 |

