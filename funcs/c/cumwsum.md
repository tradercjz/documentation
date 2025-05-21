# cumwsum

## 语法

`cumwsum(X, Y)`

参数说明和窗口计算规则请参考：[累计窗口系列（cum 系列）](../themes/cumFunctions.html)

## 详情

计算 *X* 和 *Y* 的累计内积。

## 例子

```
cumwsum(2.2 1.1 3.3, 4 5 6);
// output
[8.8,14.3,34.1]

cumwsum(1 NULL 1, 1 1 1);
// output
[1,1,2]
```

相关函数：[wsum](../w/wsum.html)

