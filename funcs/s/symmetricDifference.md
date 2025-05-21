# symmetricDifference

## 语法

`symmetricDifference(X, Y)` 或
`X^Y`

## 参数

**X** 和 **Y** 是集合。

## 详情

返回两个集合的并集减去两个集合的交集。

## 例子

```
x=set([5,3,4])
y=set(8 9 4 6);

y^x;
// output
set(5,8,3,9,6)

x^y;
// output
set(8,5,3,6,9)
```

