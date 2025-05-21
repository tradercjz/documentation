# copy

## 语法

`copy(obj)`

## 参数

**obj** 可以是任意数据类型。

## 详情

返回 *obj* 的浅拷贝。即复制最外层结构，内部子对象仍与原对象共享引用。

`copy`（浅拷贝）和 `deepCopy`（深拷贝）的区别主要体现在嵌套结构（如元组或 ANY
类型字典）中：

* 使用 `copy` 时，子对象的引用会被共享（即子对象的地址保持不变）。
* 使用 `deepCopy` 时，所有子对象都会被递归复制，引用也会完全分离。

## 例子

例1. 拷贝向量

```
x = 1 2 3
a = x.copy()
b = x.deepCopy();

print constantDesc(x[0]).address  // 000000000dd3d640
print constantDesc(a[0]).address  // 000000000cb5a4c0
print constantDesc(b[0]).address  // 000000000de92c20
```

例2. 拷贝元组

```
x = ([[1, 2], [3, 4]], "a")
a = x.copy()
b = x.deepCopy();

print constantDesc(x[0]).address  // 000000000c7ce880
print constantDesc(a[0]).address  // 000000000c7ce880
print constantDesc(b[0]).address  // 000000000c89be00
```

例3. 拷贝 ANY 字典

```
y = dict(`A`B`C, (1 2, 3 4, 5 6))
c = y.copy()
d = y.deepCopy();

print constantDesc(y[`A]).address  // 000000000c88c450
print constantDesc(c[`A]).address  // 000000000c88c450
print constantDesc(d[`A]).address  // 000000000c7cde00
```

相关函数：[asis](../a/asIs.html), [deepCopy](../d/deepCopy.html)

