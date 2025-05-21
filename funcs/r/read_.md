# read!

## 语法

`read!(handle, holder, [offset=0], [length=1])`

## 参数

**handle** 是文件句柄。

**holder** 是用于保存读取的数据的变量。

**offset** 表示数据保存至 *holder* 的起始位置。

**length** 是读取的数据点数量。

## 详情

从文件句柄中读取指定数目的数据点，并从指定位置开始，把读取结果保存至 *holder* 表示的变量中。读入的数据和
*holder* 具有相同的数据类型。函数将返回实际读入的数据点的个数。

[readBytes](readBytes.html) 函数总是返回一个新的 CHAR
向量。创建一个新的向量缓冲区时会花费一定时间。为了提高性能，可以创建一个缓冲区，并重复利用。`read!`函数就是使用这样的方式提高速度。

使用 `read!`
的另一个好处是，用户不需要知道确切的读取字节数。函数在文件到达结尾时返回，并给出读取的字节数。如果返回的字节数小于预期，表明文件已经到达结尾。

## 例子

```
// 用 read! 和 write 函数定义一个复制函数

def fileCopy(source, target){
s = file(source)
t = file(target,"w")
buf = array(CHAR,1024)
do{
  numByte = s.read!(buf,0,1024)
  t.write(buf,0, numByte)
}while(numByte==1024)
}
fileCopy("test.txt","testcopy.txt");
```

