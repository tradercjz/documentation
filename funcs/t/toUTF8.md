# toUTF8

## 语法

`toUTF8(str, encode)`

## 参数

**str** 是一个字符串标量或向量。

**encode** 是一个字符串，表示 *str* 原来的编码名称。

## 详情

把字符串转换为 UTF8 编码。DolphinDB 对编码名称的大小写敏感，所有编码名称必须用小写表示。

因为 Windows 版本目前仅支持 gbk 和 utf-8 两种编码的相互转换，因此在 Windows
中，`toUTF8` 的第二个参数只能是 "gbk"。Linux 版本支持任意两种编码之间的转换。

## 例子

```
toUTF8("DolphinDB","gbk");
// output
DolphinDB

toUTF8(["hello","world"],"euc-cn");
// output
["hello","world"]
```

相关函数：[convertEncode](../c/convertEncode.html), [fromUTF8](../f/fromUTF8.html)

