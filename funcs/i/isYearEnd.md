# isYearEnd

## 语法

`isYearEnd(X)`

## 参数

**X** 可以是 DATE, DATEHOUR, DATETIME, TIMESTAMP 或 NANOTIMESTAMP
类型的标量或向量。

## 详情

判断 *X* 是否为年末最后一天。

## 例子

```
isYearEnd(2012.12.31);
// output
true

isYearEnd([2012.12.30,2012.12.31]);
// output
[false,true]
```

相关函数：[isYearStart](isYearStart.md)

