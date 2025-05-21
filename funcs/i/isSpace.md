# isSpace

## 语法

`isSpace(X)`

## 参数

**X** 是字符或字符串类型的标量、向量或表。

## 详情

判断 *X* 是否为空格类字符串。如果 *X* 中的字符都是空格、跳格符(\t)、回车符(\r)或换行符(\n)，该函数返回 true，反之，返回
false。对于空字符串（STRING 类型的 NULL 值），该函数返回 false。

## 例子

```
isSpace("hello world");
// output
false

isSpace(" \t ");
// output
true

isSpace(string());
// output
false
```

