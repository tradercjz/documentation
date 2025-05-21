# isAlpha

## 语法

`isAlpha(X)`

## 参数

**X** 是字符或字符串类型的标量、向量或表。

## 详情

判断 *X* 是否只包含字母。如果 *X* 中的所有字符都是字母，该函数返回 true，反之，返回 false。对于空字符串（STRING 类型的
NULL 值），该函数返回 false。

## 例子

```
isAlpha("hello");
// output
true

isAlpha("hello world");
// output
false

isAlpha("1And1");
// output
false

isAlpha(string());
// output
false
```

