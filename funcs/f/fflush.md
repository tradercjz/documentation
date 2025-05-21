# fflush

## 语法

`fflush(obj)`

## 参数

**obj** 是一个文件句柄。通常使用函数 [file](file.html)
打开一个文件获得一个文件句柄。

## 详情

将缓冲区中的数据写入操作系统的文件系统。该函数必须要用户登录后才能执行。

注：

1. 将数据写入文件，建议通过 [close](../c/close.html) 关闭该文件或通过 `fflush`
   强制将缓冲区的数据写入文件，否则可能丢失数据。
2. 该命令并没有将数据刷入磁盘，因此，发生意外宕机时可能会出现数据丢失。

## 例子

```
rows = 10
t=table(1..rows as id, 1..rows+100 as value)
f1=file("test.bin", "w")
f1.writeRecord(t)
// 没有关闭文件或者将缓冲区数据刷入文件。此时读取的文件并不包含新写入的数据
t1 = table(rows:0,`id`value,`INT`INT)
f=file('test.bin')
f.readRecord!(t1)
::readRecord!(f, t1) => Reach the end of a file or a buffer.

// 调用 fflush
f1.fflush()

t1 = table(rows:0,`id`value,`INT`INT)
f=file('test.bin')
f.readRecord!(t1)
10
```

