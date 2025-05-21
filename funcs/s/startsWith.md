# startsWith

## 语法

`startsWith(X, str)`

## 参数

**X** 是在该字符串中搜索。它可以是标量或向量。

**str** 是被搜索的目标字符串。它必须是标量。

## 详情

检查 *X* 是否以 *str* 开头。如果是，返回 true； 否则返回 false。

## 例子

```
str1="US product"
str2="UK product"
if (startsWith(str1, "US")) print "str1 is a US product."
else print "str1 is not a US product."
if (startsWith(str2, "US")) print "str2 is a US product."
else print "str2 is not a US product.";

// output
str1 is a US product.
str2 is not a US product.
```

