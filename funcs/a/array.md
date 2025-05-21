# array

## 语法

`array(dataType|template, [initialSize], [capacity], [defaultValue])`

## 参数

**dataType** 是向量的数据类型。

**template** 是一个已有向量。这个已有向量的数据类型决定了新向量的数据类型。

**initialSize** 是正整数，表示向量的初始长度，即该向量新建时的元素数量。

**capacity**
是正整数，表示向量的容量，即该向量新建时系统为该向量分配的内存（以元素数为单位）。当元素数超过capacity时，系统会自动扩充容量。系统首先会分配当前容量1.2~2倍的内存，然后复制数据到新的内存空间，最后释放原来的内存。

**defaultValue** 是向量的默认值。若指定，则只能是标量。若不指定：对于多数数据类型，默认值是 0；对于字符串和符号（Symbol），默认值是
NULL。

## 详情

返回一个向量。

## 例子

```
x=array(INT, 10, 100, 1)
// 初始长度是 10；容量是 100；默认值是 1。
x
// output
[1,1,1,1,1,1,1,1,1,1]

x=array(INT, 0)
// 初始化一个空向量
x
// output
[]
x.append!(1..10)
// output
[1,2,3,4,5,6,7,8,9,10]

y=array(x)
y
// output
[0,0,0,0,0,0,0,0,0,0]

syms=array(SYMBOL, 0, 100)
// 一个空的符号向量，容量是 100.
typestr syms
// output
FAST SYMBOL VECTOR
```

