# isMonthEnd

## 语法

`isMonthEnd(X)`

## 参数

**X** 可以是 DATE, DATEHOUR, DATETIME, TIMESTAMP 或 NANOTIMESTAMP
类型的标量或向量。

## 详情

判断 *X* 是否为月末最后一天。

## 例子

```
isMonthEnd(2012.05.31);
// output
true

isMonthEnd([2012.05.30,2012.05.31]);
// output
[false,true]
```

相关函数：[isMonthStart](isMonthStart.html)

