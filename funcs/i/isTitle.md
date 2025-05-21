# isTitle

## 语法

`isTitle(X)`

## 参数

**X** 可以是字符串标量或向量。

## 详情

判断字符串中每个单词的第一个字母是否为大写，其他字母都为小写。对于不包含字母的字符串和空字符串，该函数返回 false。

## 例子

```
isTitle("Hello World");
// output
true

isTitle("Hello world");
// output
false

isTitle(["Hello","468","  "]);
// output
[true,false,false]

isTitle("1And1");
// output
true
```

相关函数：[isLower](isLower.md), [isUpper](isUpper.md)

