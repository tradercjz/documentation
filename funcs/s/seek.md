# seek

## 语法

`seek(handle, offset, [mode])`

## 参数

**handle** 必须是一个文件句柄。

**offset** 是一个整数。

**mode** 是 HEAD, CURRENT, TAIL 之一。默认的 *mode* 是 CURRENT。

## 详情

如果没有抛出异常，`seek` 函数将返回文件内部游标经计算后的位置。

当系统从一个文件中读取数据，或把数据写入一个文件中时，内部的游标将前进。用户可以通过 `seek`
函数手动操纵游标。

## 例子

```
// 编写一个返回文件长度的函数
def fileLength(f): file(f).seek(0, TAIL)
fileLength("test.txt");
// output
14

// 把内部游标移动到文件头部。
fin=file("test.txt")
fin.readLine();
// output
Hello World!

fin.seek(0, HEAD);
// output
0

fin.readLine();
// output
Hello World!
```

