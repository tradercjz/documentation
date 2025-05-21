# ploadText

## 语法

`ploadText(filename, [delimiter], [schema], [skipRows=0], [arrayDelimiter], [containHeader],
[arrayMarker])`

## 参数

参数与 [loadText](../l/loadText.md) 相同。

## 详情

将数据文件并行加载到内存中。当文件大于 16MB 时，`ploadText`
返回一个顺序分区的内存表；否则返回一个普通内存表。

注：

* `ploadText`
  返回的分区表数据均匀分配到各个分区，且每个分区中的数据量介于8MB与16MB之间。
* 与 [loadText](../l/loadText.md)
  函数相比，进行并行加载时，`ploadText` 速度更快。
* 从 2.00.10 版本开始，`loadText`
  支持加载一条记录中包含多个换行符的数据文件。

## 例子

```
n=1000000
timestamp=09:30:00+rand(18000,n)
ID=rand(100,n)
qty=100*(1+rand(100,n))
price=5.0+rand(100.0,n)
t1 = table(timestamp,ID,qty,price)
saveText(t1, "C:/DolphinDB/Data/t1.txt");

timer tt1=loadText("C:/DolphinDB/Data/t1.txt");
// output
Time elapsed: 437.236 ms

timer tt2=ploadText("C:/DolphinDB/Data/t1.txt");
// output
Time elapsed: 241.126 ms

typestr(tt2);
// output
SEGMENTED IN-MEMORY TABLE
```

更多例子请参考 [loadText](../l/loadText.md)。

