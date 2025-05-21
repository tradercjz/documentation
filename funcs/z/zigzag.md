# zigzag

## 语法

`zigzag(HL, [change=10], [percent=true], [retrace=false],
[lastExtreme=true])`

## 参数

**HL** 数值向量或者包含两列的数值矩阵。

**change** 极值波动的最小阈值。

**percent** 布尔值，表示 *change* 是否是一个百分数。

**retrace** 是一个布尔值，默认为 false。

* true：*change* 当前值相对于前一次波动的回撤。
* false：*change* 当前值相对于两端极值点间的变化。

注：

当 *percent*=false 时， *retrace* 的 true 值将不生效。

**lastExtreme** 布尔值，表示有多个连续且值相同的极值点时，是否输出最后一个极值点，默认为 true。

## 详情

`zigzag` 主要用于过滤掉 *HL* 中较小波动的值，只有满足条件的极值点会被输出。

若 *HL* 是向量，返回一个与 *HL* 长度相同的向量；若 *HL* 是矩阵，返回与 *HL* 行数相同的向量。

## 例子

```
t = table(1.1 2.3 4.45 3.67 4.9 as `low, 1.3 2.8 4.9 3.73 6.28 as `high)
HL = matrix(t[`low], t[`high])
zz = zigzag(HL, change=10, percent=true, retrace=false, lastExtreme=true)
zz;
```

| 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| 1.2 |  | 4.45 | 3.73 | 4.9 |

```
HL = 1.2 3 3.1 14 14.5 14.7 25.0 17.8 19 10
zz = zigzag(HL, change=10, percent=true, retrace=false, lastExtreme=true)
zz;
```

| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.2 |  |  |  |  |  | 25 |  |  | 10 |

