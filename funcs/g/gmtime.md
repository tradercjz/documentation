# gmtime

## 语法

`gmtime(X)`

## 参数

**X** 可以是 DATATIME, TIMESTAMP, NANOTIMESTAMP 类型的标量或向量。

## 详情

把本地时间 *X* 转换成零时区时间，即格林尼治时间（GMT）。

## 例子

以下例子在美国东部时区执行：

```
gmtime(2018.01.22 10:20:26);

// output
2018.01.22T15:20:26

gmtime(2017.12.16T13:30:10.008);

// output
2017.12.16T18:30:10.008
```

