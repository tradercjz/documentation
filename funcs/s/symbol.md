# symbol

## 语法

`symbol(X)`

## 详情

把输入转换为一个符号向量。

## 参数

**X** 是字符串或符号的向量。

## 例子

```
x=`XOM`y;
typestr(x);
```

返回：STRING VECTOR

```
y=symbol(x);
y;
```

返回：["XOM","y"]

```
typestr(y);
```

返回：FAST SYMBOL VECTOR

