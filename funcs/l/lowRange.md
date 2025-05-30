# lowRange

## 语法

`lowRange(X)`

## 参数

**X** 向量/元组/矩阵/表。

## 详情

对于 *X* 中的每个元素 *Xi*，统计 *Xi* 左侧相邻且连续大于它的元素个数。

该函数常用于统计一个序列的当前值是前多少周期（日或分钟等）内的最小值。例如某只股票创几日新低等。

## 例子

```
lowRange([13.5, 13.6, 13.4, 13.3, 13.5, 13.9, 13.1, 20.1, 20.2, 20.3])
// output
[0,0,2,3,0,0,6,0,0,0]

m = matrix(1.5 2.6 3.2 1.4 2.5 2.2 3.7 2.0, 1.6 2.3 4.2 5.6 4.1 3.2 4.4 6.9)
lowRange(m)
```

| #0 | #1 |
| --- | --- |
| 0 | 0 |
| 0 | 0 |
| 0 | 0 |
| 3 | 0 |
| 0 | 2 |
| 1 | 3 |
| 0 | 0 |
| 3 | 0 |

```
// 模拟股票 A 8天的股价,使用 lowRange 计算股票 A 当日股价创几日新低
trades = table(take(`A, 8) as sym,  2022.01.01 + 1..8 as date, 39.70 39.72 39.80 39.78 39.83 39.92 40.00 40.03 as price)
select *, lowRange(price) from trades
```

| id | date | price | lowRange\_price |
| --- | --- | --- | --- |
| A | 2022.01.02 | 39.7 | 0 |
| A | 2022.01.03 | 39.72 | 0 |
| A | 2022.01.04 | 39.8 | 0 |
| A | 2022.01.05 | 39.78 | 1 |
| A | 2022.01.06 | 39.83 | 0 |
| A | 2022.01.07 | 39.92 | 0 |
| A | 2022.01.08 | 40 | 0 |
| A | 2022.01.09 | 40.03 | 0 |

**相关信息**

* [topRange](../t/topRange.html "topRange")

