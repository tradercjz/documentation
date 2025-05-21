# writeLog

## 语法

`writeLog(X1, [X2, X3....Xn])`

## 参数

**X1**, **X2**, **X3** ... **Xn** 是要写入日志文件的字符串。每个字符串都是日志文件中的一行。

## 详情

在日志文件中写入日志。该函数必须要用户登录后才能执行。

## 例子

```
writeLog("This is a message written into the log file.")
writeLog("line1.","line2.","line3");

// Check the log file.
// output
Sun Aug 06 16:41:05 2017 <INFO> :This is a message written into the log file.
Sun Aug 06 16:50:35 2017 <INFO> :line1.
Sun Aug 06 16:50:35 2017 <INFO> :line2.
Sun Aug 06 16:50:35 2017 <INFO> :line3
```

