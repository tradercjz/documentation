# isDuplicated

## 语法

`isDuplicated(X, [keep=FIRST])`

## 参数

**X** 是一个向量或包含多个等长向量的元组。

**keep** 是一个常量，表示系统处理多个重复值的方式。它的取值可以是 FIRST, LAST 或 NONE。它是一个可选参数，默认值为 FIRST。

## 详情

判断向量中是否包含重复值。如果 *X* 是一个向量，返回的结果是一个与 *X* 长度相同的布尔向量。如果
*X* 是一个元组，返回的结果是一个与 *X* 中每个元素等长的布尔向量。

如果输入向量中有多个重复值，

* *keep* 的取值为 FIRST 表示，返回结果中第一个重复值对应位置的值为
  false，其他重复值对应位置的值为 true。
* *keep* 的取值为 LAST 表示，返回结果中最后一个重复值对应位置的值为
  false，其他重复值对应位置的值为 true。
* *keep* 的取值为 NONE 表示，返回结果中所有重复值对应位置的值都为 true。

## 例子

下面通过一个例子说明 *keep* 参数不同取值的区别。

```
v = [1,3,1,-6,NULL,2,NULL,1]
isDuplicated(v,FIRST);
//output:[false,false,true,false,false,false,true,true]
// 1在向量 v 中出现了三次，所在的位置是第0、第2和第7位，由于 isDuplicated 的第二个参数为 FIRST，因此返回结果中第0位为 false，第2和第7位为 true。

v = [1,3,1,-6,NULL,2,NULL,1]
isDuplicated(v,LAST);
//output:[true,false,true,false,true,false,false,false]
// 1在向量 v 中出现了三次，所在的位置是第0、第2和第7位，由于 isDuplicated 的第二个参数为 LAST，因此返回结果中第7位为 false，第0和第1位为 true。

v = [1,3,1,-6,NULL,2,NULL,1]
isDuplicated(v,NONE);
//output:[true,false,true,false,true,false,true,true]
// 1在向量 v 中出现了三次，所在的位置是第0、第2和第7位，由于 isDuplicated 的第二个参数为 NONE，因此返回结果中第0、第1位和第7位都为 true。
```

`isDuplicated` 函数可以去除表中的重复记录。

```
t=table(1 2 4 8 4 2 7 1 as id, 10 20 40 80 40 20 70 10 as val);
t;
```

| id | val |
| --- | --- |
| 1 | 10 |
| 2 | 20 |
| 4 | 40 |
| 8 | 80 |
| 4 | 40 |
| 2 | 20 |
| 7 | 70 |
| 1 | 10 |

```
select * from t where isDuplicated([id,val],FIRST)=false;
// 保留第一条重复的记录，去除表中其他重复的记录
```

| id | val |
| --- | --- |
| 1 | 10 |
| 2 | 20 |
| 4 | 40 |
| 8 | 80 |
| 7 | 70 |

下例展示 `isDuplicated` 判断 BLOB 类型数据。

```
a=[blob("s1"), blob("s2")]
isDuplicated(a)
//output: [false, false]

a1=[blob("s1"), blob("s2"), blob("s1"), blob("s2")]
isDuplicated(a1)
//output: [false, false, true, true]
```

