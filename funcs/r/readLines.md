# readLines

## 语法

`readLines(handle, [length=1024])`

## 参数

**handle** 是文件句柄。

**length** 是从文件中读取的行数。默认的读取行数是1024。

## 详情

从文件中读取指定行数。如果到达文件尾部或者已经读取指定行数后，函数将返回。

## 例子

```
 timer(10){
 x=rand(`IBM`MSFT`GOOG`YHOO`ORCL,10240)
 eachRight(writeLine, file("test.txt","w"),x)
 fin = file("test.txt")
 do{
    y=fin.readLine()
 } while(!y.isVoid())
 fin.close()
 };
// output
Time elapsed: 277.548 ms ms

 timer(10){
 x=rand(`IBM`MSFT`GOOG`YHOO`ORCL,10240)
 file("test.txt","w").writeLines(x)
 fin = file("test.txt")
 do{
    y=fin.readLines(1024)
 } while(y.size()==1024)
  fin.close()
 };
// output
Time elapsed: 28.003 ms
```

