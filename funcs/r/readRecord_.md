# readRecord!

## 语法

`readRecord!(handle, holder, [offset=0], [length])`

## 参数

**handle** 是文件句柄。

**holder** 是用于保存读取的数据的变量。

**offset** 表示数据保存至 *holder* 的起始位置。

**length** 是从文件中读取的行数。

## 详情

`readRecord!` 函数将二进制文件转换为 DolphinDB 数据对象。DolphinDB
也提供了 [writeRecord](../w/writeRecord.html) 函数，用于将 DolphinDB
数据对象转换为二进制文件，以供其它程序使用。 二进制文件基于行，且每行包含的记录有相同的数据类型和固定的长度。例如，如果一个二进制文件包含了 5
个数据域，分别具有下述数据类型（长度）：char(1), boolean(1), short(2), int(4), long(8), 和 double(8)， 那么
`readRecord!` 函数将把每行视为 24 个字节。类似地，`writeRecord`
函数把 DolphinDB 对象（例如表或元组）转换为具有上述格式的二进制文件。

## 例子

```
// 创建一个文件句柄，用于读取记录。二进制文件 a.bin 包含了 1000 条记录。
f=file("c:/DB/a.bin")
t=table(1000:0, `PERMNO`PRC`VOL`SHROUT, `int`double`int`double)
f.readRecord!(t);
// output
1000

// 类似地，我们可以将一个二进制文件读入一个 DolphinDB 元组对象
f=file("c:/DB/a.bin")
t=loop(array, [int, double, int, double], 0, 500)
// 创建具有 4 个数组元素的元组 t。每一个数组的长度是 500
 f.readRecord!(t, 0, 500);
// 读取前 500 行
// output
500
```

