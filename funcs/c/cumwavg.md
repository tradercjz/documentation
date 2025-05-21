# cumwavg

## 语法

`cumwavg(X, Y)`

参数说明和窗口计算规则请参考：[累计窗口系列（cum 系列）](../themes/cumFunctions.html)

## 详情

以 *Y* 为权重，计算 *X* 的累计加权平均。

## 例子

```
cumwavg(2.2 1.1 3.3, 4 5 6);
// output
[2.2,1.588889,2.273333]

cumwavg(1 NULL 1, 1 1 1);
// output
[1,1,1]
```

相关函数：[wavg](../w/wavg.html)

