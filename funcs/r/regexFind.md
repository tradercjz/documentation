# regexFind

## 语法

`regexFind(str, pattern, [offset])`

## 参数

**str** 是一个字符串或字符串向量。

**pattern** 是一个字符串，表示搜索的模式字符串（[正则表达式](../../progr/objs/expr.html)）。模式字符串可以包含字面量字符、元字符或两者的组合。

**offset** 是一个非负整数，默认值为0。它是一个可选参数，表示从 *str* 的第 *offset*
个位置开始搜索。*str* 的第一个位置为0。

## 详情

从 *str* 的第 *offset* 个位置开始搜索与 *pattern* 匹配的字符串，如果在 *str*
中找到匹配字符串，则返回 *str* 中第一个匹配字符串的位置；如果没有找到，则返回-1。

## 例子

```
regexFind("1231hsdU777_ DW#122ddd", "[a-z]+");
// output
4

regexFind("1231hsdU777_ DW#122ddd", "[0-9]+");
// output
0

regexFind("1231hsdU777_ DW#122ddd", "[0-9]+", 4);
// output
8
```

相关函数：[regexFindStr](regexfindstr.html)

