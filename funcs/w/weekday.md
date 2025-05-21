# weekday

## 语法

`weekday(X, [startFromSunday=true])`

## 参数

**X** 是一个时间标量或向量。

**startFromSunday** 是一个布尔值，表示一周是否从星期日开始。默认值为 true。

## 详情

返回一个表示与 *X* 对应的一周中日期编号。

如果 *startFromSunday* =true，那么0表示星期日，1表示星期一，...，6表示星期六。如果 *startFromSunday*
=false，那么0表示星期一，1表示星期二，...，6表示星期日。

## 例子

```
weekday 2012.12.05;
// output
3

weekday(2012.12.05, false);
// output
2

weekday 2013.05.23T12:00:00;
// output
4

weekday(2014.01.11T23:04:28.113);
// output
6

weekday 2012.12.05 2012.12.06 2013.01.05;
// output
[3,4,6]
```

