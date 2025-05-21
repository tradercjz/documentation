# decimalMultiply

## 语法

`decimalMultiply(X, Y, scale)`

## 参数

**X / Y** 标量或向量，其中至少有一个必须为 DECIMAL 类型。

**scale** 非负整型标量，表示计算结果保留的小数位数。

## 详情

DECIMAL 类型的乘法运算，相较于 `mul` 函数或运算符
\*，该函数可以指定计算结果保留的小数位数。

注：

* 在以下情况下，*scale* 参数将会失效，返回值类型为 DECIMAL：

  + 只有一个参数是 DECIMAL 类型（小数位数是 S），且指定的
    *scale* 值不等于 S。
  + X 和 Y 都是 DECIMAL 类型（小数位数分别是 S1 和 S2），且指定的
    *scale* 值小于 min(S1, S2) 或大于 S1+S2。
* 当其中一个参数是浮点数时，scale 参数将会失效，并且返回值类型为 DOUBLE。

当 *scale* 参数失效时，该函数的计算结果等同于 X \* Y。

## 返回值

DECIMAL 或 DOUBLE 类型。

## 例子

```
a = decimal32(`1.235, 3);
b = decimal32(`7.5689, 4);
c=decimalMultiply(a, b, 5)
// output
9.34759

typestr(c)
// output
DECIMAL32

decimalMultiply(a, b, 2)   // scale 小于min(3,4)，函数结果等于 a*b
// output
9.3475915

b=float(`7.5689)
c=decimalMultiply(a, b, 5)   // b 是浮点数， 函数结果等于 a*b，且数据类型是 DOUBLE。
// output
9.3475916337

typestr(c)
// output
DOUBLE
```

乘法运算（\*）和 decimalMultiply 的计算结果如果溢出，会自动转换为更高精度的类型。如果无法进行转换，则会抛出异常。

```
x = decimal32(1\7, 8)
y = decimal32(1\6, 8)
z = x * y
z
// output
0.0238095223809524
typestr z
// output
DECIMAL64

z = decimalMultiply(x, y, 8)
z
// output
0.02380952
typestr z
// output
DECIMAL64

x = decimal128(1\7, 35)
y = decimal128(1\6, 35)
x*y
// output
x * y => Scale out of bound (valid range: [0, 38], but get: 70)

decimalMultiply(x, y, 35)
// output
decimalMultiply(x, y, 35) => Decimal math overflow
```

*X* 和 *Y* 中至少有一个是向量。

```

x = [decimal32(3.213312, 3), decimal32(3.1435332, 3), decimal32(3.54321, 3)]
y = 2.1
decimalMultiply(x, y, 5)
// output
[6.7473,6.6003,7.440300000000001]

x = [decimal32(3.213312, 3), decimal32(3.1435332, 3), decimal32(3.54321, 3)]
y = [decimal64(4.312412, 3), decimal64(4.53231, 3), decimal64(4.31258, 3)]
decimalMultiply(x, y, 5)
// output
[13.85445,14.24407,15.27741]
```

