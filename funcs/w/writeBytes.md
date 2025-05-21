# writeBytes

## 语法

`writeBytes(handle, bytes)`

## 详情

`writeBytes`
函数把整个缓冲区写入文件。缓冲区必须是一个字符标量或字符向量。如果操作成功，函数返回实际写入的字节数；否则，抛出一个 IOException。

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

