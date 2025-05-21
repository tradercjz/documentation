# substru

## 语法

`substru(X, offset, [length])`

## 参数

**X** 是 Unicode 编码的字符串。它可以是标量或向量。

**offset** 是一个非负整数。

**length** 是一个正整数。

## 详情

从 *X* 的指定位置开始截取指定长度的字符串。*X* 的第一个字符的位置为0。 如果 *length* 超过了 *X*
的长度，则到 *X* 的尾部结束。

## 例子

```
substru("这是测试字符串",0,4)
// output
这是测试

substru("这是测试字符串",4,3)
// output
字符

substru("这是测试字符串",2)
// output
测试字符串

substru("这是测试字符串",2,10)
// output
测试字符串
```

相关函数：[substr](substr.md)

