# isValley

## 语法

`isValley(X, [strict=true])`

## 参数

**X** 数值型向量/矩阵/表。

**strict** 布尔值，表示是否取严格的谷值点。默认值为 true。

* 若 *strict* = true，相邻元素不为空且严格大于该元素
* 若 *strict* = false，相邻元素不为空且大于等于该元素

## 详情

若 *X* 为向量，计算 *X* 中的每个元素是否为谷值点，若是则返回 true，否则返回 false。

若 *X* 为矩阵，在每列进行上述计算，返回值一个同 X 维度相同的矩阵。若 *X* 为表，则只对数值型的列进行上述计算。

## 例子

```
v = [3.1, 2.2, 2.2, 2.2, 1.3, 2.1, 1.2]
isValley(v)
// output
[false,false,false,false,true,false,false]

v = [3.1, 2.2, 2.2, 2.2, 2.6, 1, 1.2]
isValley(v)
// output
[false,false,false,false,false,true,false]
isValley(v, false)
// output
[false,true,true,true,false,true,false]

// 矩阵在每列单独计算
m = matrix(5.3 5.8 5.6 NULL 5.7 1.2, 4.5 3.5 4.6 2.8 3.9 NULL)
isValley(m)
```

| #0 | #1 |
| --- | --- |
| false | false |
| false | true |
| false | false |
| false | true |
| false | false |
| false | false |

```
// 表只在数值列进行计算
t = table(`01`01`00`01`02`00 as id, 388.3 390.6 390.8 390.6 390.3 391.5 as price)
isValley(t)
```

| id | price |
| --- | --- |
| 01 | false |
| 01 | false |
| 00 | false |
| 01 | false |
| 02 | true |
| 00 | false |

相关函数：[isPeak](isPeak.html)

