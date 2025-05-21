# highDouble

## 语法

`highDouble(X)`

## 参数

**X** 是一个标量或向量，必须是16字节的数据类型。

## 详情

返回值为 *X* 的高位8字节的数据，为 DOUBLE 类型。

## 例子

```
x=1 2 3 4
y=4 3 2 1
points = point(x, y)
x1 = highDouble(points)
// output
[4,3,2,1]
```

获取一个复数的虚部（虚数）

```
a=complex(2, 5)
highDouble(a)
// output
5
```

