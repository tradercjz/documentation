# complex

## 语法

`complex(X, Y)`

## 参数

**X** 和 **Y** 是数值型的标量、数据对、向量或矩阵，支持的数据类型为 INTEGRAL
类（COMPRESSED、INT128 除外）和 FLOATING 类。

## 详情

创建复数 X+Y\*i。

复数类型的数据长度为16字节，其中低8位的数据存储于 *X* 中，高8位的数据存储于 *Y* 中。

## 例子

```
complex(2, 5)
// output: 2.0+5.0i

a=1.0 2.3
b=3 4
complex(a,b)

// output：[1+3i,2.3+4i]
```

