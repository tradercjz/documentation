# md5

## 语法

`md5(X)`

## 参数

**X** 是一个字符串标量或向量。

## 详情

根据 MD5 算法，对字符串进行哈希，生成 INT128 类型的数据。

## 例子

```
a=md5(`e`f);
a;
// output
[e1671797c52e15f763380b45e841ec32,8fa14cdd754f91cc6554c9e71929cce7]

typestr(a);
// output
INT128
```

