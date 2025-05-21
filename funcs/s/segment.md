# segment

## 语法

`segment(X, [segmentOffset=true])`

## 参数

**X** 是一个向量。

**segmentOffset** 是一个布尔值。默认值为 true。

## 详情

将向量分组，连续的相同元素为一组。返回的结果是与 *X* 等长的向量。

如果 *segmentOffset* 为 true，返回的结果是每组第一个元素在 *X* 中的下标。

如果 *segmentOffset* 为 false，返回的结果表示每个元素位于第几组。组号从0开始编号。

## 例子

```
x = 1 1 2 4 4 5 2 5 NULL NULL
segment(x);
// output
[0,0,2,3,3,5,6,7,8,8]

segment(x, false);
// output
[0,0,1,2,2,3,4,5,6,6]

x = 1 2 1 2 1 2 1 2 1 2 1 2;
y = 0 0 1 1 1 2 2 1 1 3 3 2;
t = table(x,y);
select *, cumsum(x) from t context by segment(y);
```

| y | x | cumsum\_x |
| --- | --- | --- |
| 0 | 1 | 1 |
| 0 | 2 | 3 |
| 1 | 1 | 1 |
| 1 | 2 | 3 |
| 1 | 1 | 4 |
| 2 | 2 | 2 |
| 2 | 1 | 3 |
| 1 | 2 | 2 |
| 1 | 1 | 3 |
| 3 | 2 | 2 |
| 3 | 1 | 3 |
| 2 | 2 | 2 |

