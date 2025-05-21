# rowKurtosis

## 语法

`rowKurtosis(X, [biased=true])`

row 系列函数通用参数说明和计算规则请参考：[rowFunctions](../themes/rowFunctions.md)

## 参数

**biased** 是一个布尔值，表示是否为有偏估计。默认值为 true，表示为有偏估计。

## 详情

逐行计算 *X* 的峰度。

DolphinDB 使用以下公式计算峰度（当 *biased*=true 时）：

![kurtosisx](../../images/kurtosisx.png)

## 例子

```
m = [4.5 2.6 1.5 1.5 4.8, 5.9 4.9 2.0 4.0 6.3, 2 2 2 2 2, 2.1 3.4 4.2 5.5 2.3]
rowKurtosis(m);
// output
[1.336589711715856,1.839333299961742,2.248755164221374,1.437834622248661,1.341044189891083]

m=matrix([4.5 2.6 1.5, 1.5 4.8 5.9, 4.9 2.0 NULL, 4.3 NULL 3.5]);
rowKurtosis(m);
// output
[2.270290894661423,1.499999999999941,1.499999999999972]

t1=table(1..5 as x, 10..6 as y, 15..19 as z, take(3,5) as t);
rowKurtosis(t1);
// output
[1.417974225003112,1.676864,1.951167883478534,2.158698670898631,2.262015004030008]
```

相关函数：[kurtosis](../k/kurtosis.md)

