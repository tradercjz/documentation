# isQuarterStart

## 语法

`isQuarterStart(X)`

## 参数

**X** 可以是 DATE, DATEHOUR, DATETIME, TIMESTAMP 或 NANOTIMESTAMP
类型的标量或向量。

## 详情

判断 *X* 是否为季度第一天。

## 例子

```
isQuarterStart(2012.04.01);
// output
true

isQuarterStart([2012.04.01,2012.05.01]);
// output
[true,false]
```

相关函数：[isQuarterEnd](isQuarterEnd.md)

