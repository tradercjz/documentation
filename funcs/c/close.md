# close

## 语法

`close(X)`

## 参数

**X** 是一个文件句柄或远程连接。

## 详情

关闭一个已打开的文件或远程连接。该函数必须要用户登录后才能执行。

## 例子

```
fout.writeLine("hello world!");
// output
1
fout.close();
fin = file("test3.txt");
print fin.readLine();
hello world!
fin.close();
```

