# rpad

## 语法

`rpad(str, length, [pattern])`

## 参数

**str** 是一个字符串或字符串向量。它表示目标字符串。

**length** 是一个非负整数。它表示返回字符串的长度。如果 *length* 小于 *str*
的长度，`rpad` 会把 *str* 截断成长度为 *length* 的字符串。

**pattern** 是一个填充字符串。它是一个可选参数。如果没有指定，则在 *str* 的右边填充空格。

## 详情

在字符串的右边填充特定字符串。

## 例子

```
rpad("Hello",2);
// output
He

rpad(`Hello, 10);
// output
Hello

rpad(`Hello, 12, `0);
// output
Hello0000000
```

