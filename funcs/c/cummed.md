# cummed

## 语法

`cummed(X)`

参数说明和窗口计算规则请参考：[累计窗口系列（cum 系列）](../themes/cumFunctions.md)

## 详情

计算 *X* 元素的累计中位数。

## 例子

```
x = [7,9,5,NULL,9]
cummed(x);
// output
[7,8,7,7,8]

m = matrix(6 5 7 8 1, 3 9 4 2 10);
m;
```

| #0 | #1 |
| --- | --- |
| 6 | 3 |
| 5 | 9 |
| 7 | 4 |
| 8 | 2 |
| 1 | 10 |

```
cummed(m);
```

| #0 | #1 |
| --- | --- |
| 6 | 3 |
| 5.5 | 6 |
| 6 | 4 |
| 6.5 | 3.5 |
| 6 | 4 |

相关函数：[cummax](cummax.md), [cummin](cummin.md), [med](../m/med.md)

