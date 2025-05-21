# regexCount

## 语法

`regexCount(str, pattern, [offset=0])`

## 参数

**str** 是一个字符串或字符串向量。

**pattern** 是一个字符串，表示搜索的模式字符串（[正则表达式](../../progr/objs/expr.html)）。模式字符串可以包含字面量字符、元字符或两者的组合。

**offset** 是一个非负整数，默认值为0。它是一个可选参数，表示从 *str* 的第 *offset*
个位置开始搜索。*str* 的第一个位置为0。

## 详情

从 *str* 的第 *offset* 个位置开始搜索，返回与 *pattern* 匹配的字符串在 *str*
中出现的次数。

## 例子

```
regexCount("1231hsdU777_ DW#122ddd", "[0-9]+");
// output
3

regexCount("1231hsdU777_ DW#122ddd", "[0-9]+$");
// output
0

regexCount("1231hsdU777_ DW#122ddd", "^[0-9]+");
// output
1

regexCount("abc234 ff456", "[a-z]", 3);
// output
2
```

