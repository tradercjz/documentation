# strpos

## 语法

`strpos(X, str)`

别名：strFind

## 参数

**X** 是在该字符串中搜索。它可以是标量或向量。

**str** 是被搜索的目标字符串。它必须是标量。

## 详情

检查 *X* 是否包含 *str*。如果是，返回 *str* 在 *X* 中的起始位置；
否则返回-1。

## 例子

```
strpos("abcdefg","cd");
// output
2

strpos("abcdefg","d");
// output
3

strpos("abcdefg","ah");
// output
-1
```

