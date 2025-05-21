# move

## 语法

`move(X, steps)`

## 参数

**X** 可以是向量、矩阵或表；

**steps** 是一个整数或一个 [duration](../d/duration.html)，表示移动多少位置或多少时间。

* 如果 *steps* 为正数，*X* 向右移动 *steps* 个位置；
* 如果 *steps* 为负数，*X* 向左移动 *steps* 个位置；
* 如果 *steps* 为 0，不改变 *X* 的位置；
* 如果 *steps* 为 DURATION，对应的 *X* 必须是行索引为时间类型的索引矩阵或者索引序列。

## 详情

`move` 是 [prev](../p/prev.html) 和
[next](../n/next.html) 的通用形式。

## 例子

```
x=3 9 5 1 4 9;
move(x,3);
// output
[,,,3,9,5]

move(x,-2);
// output
[5,1,4,9,,]

index = (second(08:20:00)+1..4) join 08:21:01 join 08:21:02
x = index.indexedSeries(x)
move(x,3s)
```

| label | col1 |
| --- | --- |
| 08:20:01 |  |
| 08:20:02 |  |
| 08:20:03 |  |
| 08:20:04 | 3 |
| 08:21:01 | 1 |
| 08:21:02 | 1 |

```
move(x,1m)
```

| label | col1 |
| --- | --- |
| 08:20:01 |  |
| 08:20:02 |  |
| 08:20:03 |  |
| 08:20:04 |  |
| 08:21:01 | 3 |
| 08:21:02 | 9 |

