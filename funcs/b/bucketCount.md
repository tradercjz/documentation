# bucketCount

## 语法

`bucketCount(vector, dataRange, bucketNum,
[includeOutbound=false])`

## 参数

**vector** 一个数值或时间向量。

**dataRange** 一对表示数据范围的值，包括下限，不包括上限。

**bucketNum** 桶的数量。当 *dataRange* 是整型数据对时，它的范围大小必须是 *bucketNum* 的整数倍。

**includeOutbound** 一个可选的布尔值，表明是否包括小于下限的值，和大于等于上限的值。默认值为 false。

## 详情

函数 `bucketCount` 有和 [bucket](bucket.html) 相同的参数，但是返回每个桶中元素的计数。

## 例子

```
bucketCount(9 23 54 36 46 12, 12:54, 2);
// output
[2,2]

bucketCount(9 23 54 36 46 12, 12:54, 2, 1);
// output
[1,2,2,1]
```

