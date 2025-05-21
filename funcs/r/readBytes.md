# readBytes

## 语法

`readBytes(fileHandle, sizeInByte)`

## 参数

**fileHandle** 是文件句柄。

**sizeInByte** 是整数，用于指定读取的字节数。

## 详情

从句柄中读取给定数目的字节。如果文件到达结尾，或发生了 IO 错误，将抛出一个
IOException；否则返回一个包含了给定数目字节的缓冲区。因此，必须在调用函数之前知道要读取的确切的字节数。

## 例子

```
// 定义一个文件复制函数
def fileCopy(source, target){
s = file(source)
len = s.seek(0,TAIL)
s.seek(0,HEAD)
t = file(target,"w")
if(len==0) return
do{
  buf = s.readBytes(min(len,1024))
  t.writeBytes(buf)
  len -= buf.size()
}while(len)
};
fileCopy("test.txt","testcopy.txt");
```

