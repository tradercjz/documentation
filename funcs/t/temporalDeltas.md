# temporalDeltas

别名：datetimeDeltas

## 语法

`temporalDeltas(X, [unit])`

## 参数

**X** 是一个时间类型的向量、矩阵，或包含时间类型列的表。

**unit** 可选参数，是一个字符串标量，指定时间单位。取值可以是：

* "d" 表示自然日
* "B" 表示工作日
* 一个交易日历标识，例如 "XNYS"，对应的交易日历文件必须保存在 *marketHolidayDir* 配置项指定的目录中。

注： 若指定 *unit*，*X* 必须是 DATE 类型。

## 详情

`temporalDeltas` 函数计算 *X* 中每个元素与前一个元素之间的时间差，NULL 值在计算中返回
NULL，且输出的第一个值总是 NULL。

* 若*X* 是向量，返回一个包含 *X* 中两个元素之差的向量。
* 若 *X* 是矩阵，在每列内进行上述计算，返回一个与 *X* 维度相同的矩阵。
* 若 *X* 是表，在每个时间类型列内进行上述计算，返回一个与 *X* 行数与列数都相同的表。

当提供 *unit* 参数时，时间差的计算将基于指定的时间单位（天、工作日或特定交易所的交易日）。

## 例子

```
timestamps = [2020.06.13T13:30:10.000, 2020.06.13T13:30:10.010, 2020.06.13T13:30:10.021, 2020.06.13T13:30:10.033, 2020.06.13T13:30:10.046]
temporalDeltas(timestamps)
// Output: [,10,11,12,13]
```

若指定 *unit* 参数，*X* 必须为日期（DATE）类型：

```
times = [2019.12.31, 2020.01.03, 2020.01.10, 2020.01.15, 2020.01.17]
temporalDeltas(times, "d");
// Output: [NULL, 3, 7, 5, 2]

temporalDeltas(times, "B");
// Output: [NULL, 3, 5, 3, 2]

temporalDeltas(times, "XNYS");
// Output: [NULL, 2, 5, 3, 2]

sym = `A`B`C`D`E
num = 5 4 3 2 1
t = table(times, sym, num)
temporalDeltas(t);

/*
times sym num
----- --- ---
      A   5
3     B   4
7     C   3
5     D   2
2     E   1
*/
```

