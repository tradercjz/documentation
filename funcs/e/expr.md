# expr

## 语法

`expr(args...)`

## 参数

**args** 可以是对象、运算符或元代码。元代码是由"<"和">"包围的对象和/或表达式。参数的最小数量为2。

## 详情

函数 `expr` 从对象、运算符或其他元代码生成元代码。

## 例子

```
expr(6,<,8);
// output
< 6 < 8 >

expr(sum, 1 2 3);
// output
< sum [1,2,3] >

a=6;
expr(a,+,1);
// output
< 6 + 1 >

expr(<a>,+,1);
// output
< a + 1 >

expr(<a>,+,<b>);
// output
< a + b >

expr(a+7,*,8);
// output
< 13 * 8 >

expr(<a+7>,*,8);
// output
< (a + 7) * 8 >

expr(not, < a >);
// output
< ! a >
```

