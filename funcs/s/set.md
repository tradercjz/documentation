# set

## 语法

`set(X)`

## 参数

**X** 是一个向量。

## 详情

返回向量 *X* 对应的集合对象。

## 例子

`set` 函数返回一个集合。

```
x=set(4 5 5 2 3 11 6);
x;
// output
set(6,11,3,2,5,4)

x.intersection(set([2,5,9]));
// output
set(2,5)
```

与此不同，[distinct](../d/distinct.html) 函数返回一个向量。

```
distinct(4 5 5 2 3 11 6);
// output
[6,11,3,2,5,4]
```

