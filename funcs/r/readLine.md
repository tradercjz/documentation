# readLine

## 语法

`readLine(handle)`

## 参数

**handle** 是文件句柄。

## 详情

从给定的文件中读取一行。返回的行不包括换行符。如果文件结束，函数会返回一个 NULL 对象，可以用 [isNull](../i/isNull.html) 函数测试。

## 例子

```
x=`IBM`MSFT`GOOG`YHOO`ORCL;
eachRight(writeLine, file("test.txt","w"), x);

// output
[1,1,1,1,1]

fin = file("test.txt")
do{
x=fin.readLine()
if(x.isNull()) break
print x
}while(true);

// output
IBM
MSFT
GOOG
YHOO
ORCL
```

