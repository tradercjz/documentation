# fromUTF8

## 语法

`fromUTF8(str, encode)`

## 参数

**str** 是一个字符串标量或向量。

**encode** 是一个字符串，表示 *str* 的目标编码名称。

## 详情

把 UTF8 编码的字符串转换为其他编码。DolphinDB 对编码名称的大小写敏感，所有编码名称必须用小写表示。

因为 Windows 版本目前仅支持 gbk 和 utf-8 两种编码的相互转换，因此在 Windows
中，`fromUTF8` 的第二个参数只能是 "gbk"。Linux 版本支持任意两种编码之间的转换。

## 例子

```
fromUTF8("DolphinDB","gbk");
```

输出返回：DolphinDB

```
fromUTF8(["hello","world"],"euc-cn");
```

输出返回：["hello","world"]

相关函数：[convertEncode](../c/convertEncode.md), [toUTF8](../t/toUTF8.md)

