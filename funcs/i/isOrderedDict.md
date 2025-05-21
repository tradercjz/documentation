# isOrderedDict

## 语法

`isOrderedDict(X)`

## 参数

**X**：一个字典对象。

## 详情

判断 *X* 是否为一个有序字典：

* 如果是，返回 *true*；
* 如果不是， *false*。

## 例子

```
x=1 5 3
y=4.5 7.8 4.3
z=dict(x,y);
isOrderedDict(z)
// output
false

z1=dict(x,y,true);
isOrderedDict(z1)
// output
true
```

