# writeRecord

## 语法

`writeRecord(handle, object, [offset=0], [length])`

## 参数

**handle** 是二进制文件句柄。

**object** 是一个表或一个由多个等长向量组成的元组。

**offset** 表示写入的起始位置。

**length** 是向文件写入的行数。

## 详情

`writeRecord` 函数把 DolphinDB
对象（例如表或元组）转换为二进制文件。函数将返回向文件写入的行数。

## 例子

```
t=table(1..10000 as id, 1..10000+100 as value);

f1=file("C:/DolphinDB/a.bin", "w");        // 创建一个用于写入记录的文件句柄
f1.writeRecord(t);
// output
10000

f2=file("C:/DolphinDB/b.bin", "w");
f2.writeRecord(t, 100, 1000);
// output
1000

f3=file("C:/DolphinDB/c.bin", "w");
f3.writeRecord(t, 100, 10000);
// output
The optional argument length is invalid.
```

