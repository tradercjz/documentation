# bucket

## 语法

`bucket(vector, dataRange, bucketNum, [includeOutbound=false])`

## 参数

**vector** 一个数值或时间向量。

**dataRange** 一对表示数据范围的值，包括下限，不包括上限。

**bucketNum** 桶的数量。当 *dataRange* 是整型数据对时，它的范围大小必须是 *bucketNum* 的整数倍。

**includeOutbound** 一个可选的布尔值，表明是否包括小于下限的值，以及大于或等于上限的值。默认值为 false。

## 详情

返回一个和 *vector* 相同长度的向量，表明根据 *dataRange* 和
*bucketNum* 所给出的分类规则，每一个元素应该属于哪个桶。

例如，*dataRange* 是 0:10，*bucketNum* 是 2，则两个桶分别是 [0, 5) 和
[5, 10)，桶的编号分别为0和1。如果 *includeOutbound* 为true，这个例子会产生 4 个桶，即 <0, [0, 5),
[5,10) 和 >=10。如果 *includeOutbound* 为false，任何小于下限或大于等于上限的值会返回 NULL。

## 例子

```
bucket(9 23 54 36 46 12, 12:54, 2);
// output
[,0,,1,1,0]

bucket(9 23 54 36 46 12, 12:54, 2, 1);
// output
[0,1,3,2,2,1]
```

