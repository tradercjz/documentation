# eval

## 语法

`eval(expr)`

## 参数

**expr** 是元代码。

## 详情

解析给定的元代码。

## 例子

```
eval(<1+2>);
// output
3

eval(<1+2+3=10>);
// output
0

eval(expr(6,<,8));
// output
1

eval(expr(sum, 1 2 3));
// output
6

a=6; b=9;
eval(expr(<a>,+,<b>));
// output
15
```

