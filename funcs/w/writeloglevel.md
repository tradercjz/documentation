# writeLogLevel

## 语法

`writeLogLevel(level,X1,[X2, X3,...,Xn])`

## 参数

**level** 日志等级，从低到高可选值为：DEBUG, INFO, WARNING, ERROR，分别对应数字 0,
1, 2, 3。

**X1**, **X2**, **X3** ... **Xn** 要写入日志文件的内容。每个 Xi
都是日志文件中的一行。支持以下数据类型：Logical, Integral, Temporal, Floating, Literal, Decimal。

## 详情

在日志文件中写入指定等级的日志。该命令只能由管理员调用。

注：

*level* 的等级必须等于或高于配置项 *logLevel* 或命令
`setLogLevel` 设置的等级，否则不会输出日志到文件中。

## 例子

```
writeLogLevel(INFO,111111111111,"This is an INFO message")
// Check the log file.
<INFO> :111111111111
<INFO> :This is an INFO message
```

