# panel

## 语法

`panel(row, col, metrics, [rowLabel], [colLabel], [parallel=false])`

## 参数

**row** 是一个向量，其中每个元素对应结果矩阵中的一行。

**col** 是一个向量，其中每个元素对应结果矩阵中的一列。

**metrics** 是一个或多个指标列。每个指标列产生一个矩阵。

**rowLabel** 是一个向量，为结果矩阵的行标签。必须升序排列，而且没有重复值。结果中仅包括 *rowLabel* 中指定的行。

**colLabel** 是一个向量，为结果矩阵的列标签。必须升序排列，而且没有重复值。结果中仅包括 *colLabel* 中指定的列。

**parallel** 是一个布尔值，表示是否并行计算。默认值为 false。

## 详情

将指标列按给定行与列维度进行透视操作，生成一个或多个矩阵。每一个矩阵对应一个指标列（metrics）。

`panel` 函数同 [pivotBy](../../progr/sql/pivotBy.md)
语句类似，将数据表中的数据按照两个维度重新排列。两者的不同之处在于，SQL 中，exec... pivot by... 只能指定一个指标列， 生成一个矩阵，而
`panel` 函数可以指定一个或多个指标列，生成一个或多个矩阵。

## 例子

```
t = table(1 1 2 2 2 3 3 as id, 2020.09.01 + 1 3 1 2 3 2 3 as date, 1..7 as value);
t;
```

| id | date | value |
| --- | --- | --- |
| 1 | 2020.09.02 | 1 |
| 1 | 2020.09.04 | 2 |
| 2 | 2020.09.02 | 3 |
| 2 | 2020.09.03 | 4 |
| 2 | 2020.09.04 | 5 |
| 3 | 2020.09.03 | 6 |
| 3 | 2020.09.04 | 7 |

`panel` 面板数据生成的表中，指定的 *row* 和 *col*
会自动按升序排序。

```
panel(t.date, t.id, t.value);
```

|  | 1 | 2 | 3 |
| --- | --- | --- | --- |
| 2020.09.02 | 1 | 3 |  |
| 2020.09.03 |  | 4 | 6 |
| 2020.09.04 | 2 | 5 | 7 |

```
panel(t.date, t.id, t.value, 2020.09.02 2020.09.03, 1 2);
```

|  | 1 | 2 |
| --- | --- | --- |
| 2020.09.02 | 1 | 3 |
| 2020.09.03 |  | 4 |

```
panel(t.date, t.id, [t.value, t.value>0], 2020.09.02 2020.09.03, 1 2);
```

|  | 1 | 2 |
| --- | --- | --- |
| 2020.09.02 | 1 | 3 |
| 2020.09.03 |  | 4 |

|  | 1 | 2 |
| --- | --- | --- |
| 2020.09.02 | 1 | 1 |
| 2020.09.03 |  | 1 |

利用`panel` 生成的矩阵，计算每只股票的累积最大股价。

```
syms = "sym"+string(1..2)
dates = 2021.12.07..2021.12.11
t = table(loop(take{, size(syms)}, dates).flatten() as trade_date,  take(syms, size(syms)*size(dates)) as code, rand(1000, (size(syms)*size(dates))) as volume)
volume = panel(t.trade_date, t.code, t.volume, dates)
cummax(volume)
```

