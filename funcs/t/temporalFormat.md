# temporalFormat

## 语法

`temporalFormat(X, format)`

别名：datetimeFormat

## 详情

把 DolphinDB 时序类型的数据转换成指定格式的字符串。详情请参考： [日期和时间的调整及格式](../../progr/data_mani/format_temp_obj.md)。

## 参数

**X** 是一个时间序列标量或向量。

**format** 是表示时间格式的字符串。

## 例子

```
temporalFormat(2018.02.14,"dd-MM-yyyy");
// output: 14-02-2018

temporalFormat(2018.02.14,"dd-MMM-yy");
// output: 14-FEB-18

temporalFormat(02:19:06,"HH.mm.ss");
// output: 02.19.06

temporalFormat(2018.02.06T13:30:10.001, "y-M-d-H-m-s-SSS");
// output: 2018-2-6-13-30-10-001

temporalFormat(14:19:06,"hhmmssaa");
// output: 021906PM
```

