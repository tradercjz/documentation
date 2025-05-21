# rdp

## 语法

`rdp(pointList, epsilon)`

## 参数

**pointList** 是一个 POINT 类型向量，且不能包含空元素。

**epsilon** 是一个非负的 DOUBLE 类型的标量，表示压缩阈值。

## 详情

使用 RDP(Ramer-Douglas-Peucker) 矢量压缩算法对 POINT 类型向量进行压缩。

## 例子

```
pt = point(1 2 3 4, 1 2 3 4)
rdp(pt, 0.1)
// output
[(1.0, 1.0), (4.0, 4.0)]
​
pt = point(1 2 3 4, 1 3 3 4)
rdp(pt, 0.1)
// output
[(1.0, 1.0), (2.0, 3.0), (3.0, 3.0), (4.0, 4.0)]

temp = array(POINT,0)
n=90000
x_data = rand(10.0,n)
y_data = rand(10.0,n)
index=0
do{
temp.append!(point(x_data[index], y_data[index]))
index += 1
}while(index<n)
s=rdp(temp, 0.8)
print(s.size())
// output
82002
print(temp.size())
// output
90000
```

