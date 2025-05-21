# localtime

## 语法

`localtime(X)`

## 详情

把零时区时间 *X* 转换成本地时间。

## 参数

**X** 可以是 DATETIME, TIMESTAMP, NANOTIMESTAMP
类型的标量、向量或表，表示零时区时间。

## 例子

以下例子在美国东部时区执行：

```
localtime(2018.01.22T15:20:26);
// output
2018.01.22T10:20:26

localtime(2017.12.16T18:30:10.001);
// output
2017.12.16T13:30:10.001
```

