# dict

## 语法

`dict(keyObj, valueObj, [ordered=false])`

或

`dict(keyType, valueType, [ordered=false])`

## 参数

对于第一种情形，**keyObj** 是表示键的向量，**valueObj** 是表示值的向量。

对于第二种情形，**keyType** 是字典键的数据类型，**valueType**
是字典值的数据类型。系统支持以下键的数据类型：Literal、Integral（COMPRESS 除外）、Floating 和 Temporal。字典中的值不支持
COMPLEX，POINT 类别。

**ordered** 一个布尔值，默认为 false，表示创建一个无序字典。当 *ordered* = true
时，创建一个有序字典。无序字典在输出或进行遍历时，其键值对不保留输入时的顺序；有序字典在输出或进行遍历时，键值对的顺序与输入顺序保持一致。

## 详情

返回一个无序字典或有序字典对象。

## 例子

```
x=1 6 3
y=4.5 7.8 4.3
z=dict(x,y);
z;
// output
3->4.3
1->4.5
6->7.8

z=dict(INT,DOUBLE);
z[5]=7.9;
z;
// output
5->7.9

z[3]=6;
z;
// output
3->6
5->7.9

dt=dict([`test], [1]);
dt;
// output
test->1

// 创建有序字典
z=dict(x,y,true)
z;
// output
1->4.5
6->7.8
3->4.3

// y 为 DECIMAL32 类型的向量，将 y 作为 value 值创建有序字典 z
x=1 3 2
y = decimal32(1.23 3 3.14, 3)
z=dict(x,y,true);
z;
// output
1->1.230
3->3.000
2->3.140
```

获取键和值:

```
x=1 6 3
y=4.5 7.8 4.3
z=dict(x,y);
z.keys();
// output
[3,1,6]

z.values();
// output
[4.3,4.5,7.8]
```

相关函数：[array](../a/array.md), [matrix](../m/matrix.md)， [dictUpdate!](dictUpdate_.md), [syncDict](../s/syncDict.md)

