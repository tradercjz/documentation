# cumvar

## 语法

`cumvar(X)`

参数说明和窗口计算规则请参考：[累计窗口系列（cum 系列）](../themes/cumFunctions.md)

## 详情

计算 *X* 元素的累计方差。

## 例子

```
x=[2,3,4];
cumvar(x);
// output
[,0.5,1]

m=matrix(0.15 0.08 0.03 -0.14 -0.09, 0.2 -0.12 -0.16 0.08 0.16);
m;
```

| #0 | #1 |
| --- | --- |
| 0.15 | 0.2 |
| 0.08 | -0.12 |
| 0.03 | -0.16 |
| -0.14 | 0.08 |
| -0.09 | 0.16 |

```
cumvar(m);
```

| #0 | #1 |
| --- | --- |
|  |  |
| 0.0024 | 0.0512 |
| 0.0036 | 0.0389 |
| 0.0152 | 0.0288 |
| 0.0143 | 0.0267 |

相关函数：[cummax](cummax.md), [cummin](cummin.md), [cumprod](cumprod.md), [cumPositiveStreak](cumPositiveStreak.md), [cumsum](cumsum.md), [cumavg](cumavg.md), [cumstd](cumstd.md)

