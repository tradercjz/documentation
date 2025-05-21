# isLower

## 语法

`isLower(X)`

## 参数

**X** 是字符或字符串类型的标量、向量或表。

## 详情

判断字符串中的字母是否全部为小写。对于空字符串，该函数返回 false。

## 例子

```
isLower("this is string example....wow!!!");
// output
true

isLower("THIS is string example....wow!!!");
// output
false

isLower("123456abc");
// output
true

isLower("123");
// output
false

isLower(["  ",string()]);
// output
[false,false]
```

相关函数：[isUpper](isUpper.md), [isTitle](isTitle.md)

