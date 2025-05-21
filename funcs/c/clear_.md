# clear!

## 语法

`clear!(X)`

## 参数

**X** 可以是向量、矩阵、集合、字典、内存表。

## 详情

函数 `clear!` 用来清除 *X* 中的所有内容。对 *X*
执行该函数后，*X* 仍然存在，保持原有的数据类型，可以追加新的数据。

## 例子

```
x=1 2 3;
clear!(x);

// output
[]
typestr x;

// output
FAST INT VECTOR
size x;

// output
0
x.append!(1..6);

// output
[1,2,3,4,5,6]

y=set(8 9 4 6);
y.clear!();

// output
set()

x=1..3;
y=4..6;
z=dict(x,y);
z;

// output
3->6
1->4
2->5
z.clear!();

t = table(1 2 3 as id, 1.0 2.0 3.0 as value)
t.clear!()
```

