# isort

## 语法

`isort(X, [ascending=true])`

## 参数

**X** 是一个向量或一个由多个等长向量组成的元组。

**ascending** 是布尔值标量或向量，表示按升序排序还是按降序排序。默认值为 true（按升序排序）。

## 详情

和 [sort!](../s/sort_.md) 返回一个排序后的数组不同，*isort*
返回排序后的每个元素在原始向量中的索引。

X[isort X] 等价于 sort(X)。

## 例子

```
x = 4 1 3 2;
y = isort(x);
y;
// output
[1,3,2,0]
// 对于排序后的 x: [1 2 3 4]，第一个元素 1 在原始的 x 中的位置是 1，第二个元素 2 在原始 x 中的位置是 3，... 以此类推。
x[y];
// output
[1,2,3,4]
// 等价于 sort(x)

z=isort(x, false);
z;
// output
[0,2,3,1]
x[z];
// output
[4,3,2,1]

x=2 2 1 1
y=2 1 1 2
isort([x,y]);
// output
[2,3,1,0]
isort([x,y],[0,0]);
// output
[0,1,3,2]
```

基于表的单列排序：

```
t2 = table(4 2 3 1 as x, 9 6 7 3 as y);
t2;
```

| x | y |
| --- | --- |
| 4 | 9 |
| 2 | 6 |
| 3 | 7 |
| 1 | 3 |

```
t2[isort(t2.x)];
```

| x | y |
| --- | --- |
| 1 | 3 |
| 2 | 6 |
| 3 | 7 |
| 4 | 9 |

```
t2[isort(t2.x, false)];
```

| x | y |
| --- | --- |
| 4 | 9 |
| 3 | 7 |
| 2 | 6 |
| 1 | 3 |

基于表的多列排序：

```
a=5 5 5 3 3 8 7 7;
b=`MSFT`GOOG`IBM`YHOO`X`YHOO`C`ORCL;
t=table(a,b);
t;
```

| a | b |
| --- | --- |
| 5 | MSFT |
| 5 | GOOG |
| 5 | IBM |
| 3 | YHOO |
| 3 | X |
| 8 | YHOO |
| 7 | C |
| 7 | ORCL |

```
t[isort([a,b], false true)];
// 先基于 a 降序排序，再基于 b 升序排序
```

| a | b |
| --- | --- |
| 8 | YHOO |
| 7 | C |
| 7 | ORCL |
| 5 | GOOG |
| 5 | IBM |
| 5 | MSFT |
| 3 | X |
| 3 | YHOO |

```
t[isort([a,b], false)];
// 等价于 t[isort([a,b], false false)];
```

| a | b |
| --- | --- |
| 8 | YHOO |
| 7 | ORCL |
| 7 | C |
| 5 | MSFT |
| 5 | IBM |
| 5 | GOOG |
| 3 | YHOO |
| 3 | X |

