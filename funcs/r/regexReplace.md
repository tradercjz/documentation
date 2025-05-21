# regexReplace

## 语法

`regexReplace(str, pattern, replacement,
[offset])`

## 参数

**str** 是一个字符串或字符串向量。

**pattern** 是一个字符串，表示搜索的模式字符串（[正则表达式](../../progr/objs/expr.html)）。模式字符串可以包含字面量字符、元字符或两者的组合。

**replacement** 是字符串标量，表示替换的字符串。

**offset** 是一个非负整数，默认值为0。它是一个可选参数，表示从 *str* 的第 *offset*
个位置开始搜索。*str* 的第一个位置为0。

## 详情

从 *str* 的第 *offset* 个位置开始搜索与 *pattern* 匹配的字符串，如果找到匹配字符串，则把匹配字符串替换成
*replacement*，然后返回替换后的字符串。

## 例子

```
regexReplace("abc234 ff456", "[a-z]", "z");
// output
zzz234 zz456

regexReplace("abc234 ff456", "[a-z]+", "zzz");
// output
zzz234 zzz456

regexReplace("abc234 ff456", "[0-9]+", "zzz");
// output
abczzz ffzzz
```

