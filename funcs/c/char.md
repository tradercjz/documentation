# char

## 语法

`char(X)`

## 详情

把输入转换为 CHAR 数据类型。

## 参数

**X** 可以是任意数据类型。

## 例子

```
x=char();
x;
```

返回：null

```
typestr x;
```

返回：CHAR

```
a=char(99);
a;
```

返回：'c'

```
typestr a;
```

返回：CHAR

```
char(a+5);
```

返回：'h'

```
char("990");
```

返回：`Failed to convert the string to CHAR`

注： `char` 函数会把输入的字符串识别为 ASCII 码，超出 ASCII
码范围的输入字符无法转换。

