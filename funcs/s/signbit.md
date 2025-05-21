# signbit

## 语法

`signbit(X)`

## 参数

**X**：一个整型或者浮点型的标量。

## 详情

获取输入数据的符号位。

返回值：负号返回 ture；正号返回 false。

## 例子

```
signbit('a')
false

signbit(-21)
true

signbit(-2.1)
true

b=complex(10,-5)//创建一个复数
b
10.0-5.0i
signbit(highDouble(b)) //判断虚部符号
true

signbit(lowDouble(b))  //判断实部符号
false
```

