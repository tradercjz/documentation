# isLeapYear

## 语法

`isLeapYear(X)`

## 参数

**X** 可以是 DATE, DATEHOUR, DATETIME, TIMESTAMP 或 NANOTIMESTAMP
类型的标量或向量。

## 详情

判断 *X* 是否为闰年。

## 例子

```
isLeapYear(2012.06.12T12:30:00);
// output
true

isLeapYear([2012.01.01,2013.01.01,2014.01.01,2015.01.01]);
// output
[true,false,false,false]
```

