# highLong

## 语法

`highLong(X)`

## 参数

**X** 是一个标量、向量、表、数据对或者字典，且必须为16字节的数据类型（支持 UUID、IPADDR、INT128、COMPLEX、POINT）。

## 详情

返回值为 *X* 的高位8字节的数据，为 LONG 类型。

## 例子

```
x =ipaddr("192.168.1.13")
x1 = highLong(x)
print(x1)
//output: 0

x=1 2 3 4
y=4 3 2 1
points = point(x, y)
x1 = highLong(points)
//output:[4616189618054758400,4613937818241073152,4611686018427387904,4607182418800017408]
```

**相关信息**

* [lowLong](../l/lowlong.html "lowLong")

