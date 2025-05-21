# substr

## 语法

`substr(X, offset, [length])`

## 参数

**X** 是一个字符串。它可以是标量或向量。

**offset** 是一个非负整数。

**length** 是一个正整数。

## 详情

从 *X* 的指定位置开始截取指定长度的字符串。*X* 的第一个字符的位置为0。如果 *length* 超过了 *X*
的长度，则到 *X* 的尾部结束。

## 例子

```
substr("This is a test", 0, 4);
// output
This

substr("This is a test", 5, 2);
// output
is

substr("This is a test", 5);
// output
is a test

substr("This is a test", 8, 100);
// output
a test
```

