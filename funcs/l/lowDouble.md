# lowDouble

## 语法

`lowDouble(X)`

## 参数

**X** 是一个标量或向量，必须是16字节的数据类型。

## 详情

返回值为 *X* 的低位8字节的数据，为 DOUBLE 类型。

## 例子

```
x=1 2 3 4
y=4 3 2 1
points = point(x, y)
x1 = lowDouble(points)
```

输出返回：[1,2,3,4]

获取一个复数的实部（实数）：

```
a=complex(2, 5)
lowDouble(a)
```

输出返回：2

