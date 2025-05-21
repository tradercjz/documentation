# stateIterate

## 语法

`stateIterate(X, initial, initialWindow, iterateFunc,
combineCoeff)`

该函数只能用作响应式状态引擎 *metrics* 中的函数。

## 参数

**X** 输入表中的字段或其应用向量函数的计算结果。

**initial** 数据形式同 *X*，作为 *initialWindow* 内数据的输出结果。

**initialWindow** 正整数，表示初始化窗口的长度。其确定的窗口范围为[0, initialWindow)。

**iterateFunc** 用于迭代计算的函数。必须是一个单目函数，其唯一参数是 `stateIterate`
对应输出表中的字段。目前只支持以下函数（非单目函数以部分应用形式给出其他参数）：

* 滑动窗口函数：`tmove`, `tmavg`,
  `tmmax`, `tmmin`,
  `tmsum`, `mavg`,
  `mmax`, `mmin`, `mcount`,
  `msum`
* 累计窗口函数：`cumlastNot`,
  `cumfirstNot`
* 序列相关函数：`ffill`,
  `move`

注：

* 由于迭代是基于历史数据进行的，因此当前记录的输出是基于输出表中的历史结果和 *X*
  计算得到的。
* tm 系列函数计算时，时间窗口由当前记录的时间戳确定。且计算窗口范围为 (T - window, T)。

**combineCoeff** 长度为 2 的向量，作为 *iterateFunc* 迭代结果和 *X* 的关联系数。

## 详情

通过线性迭代实现线性递归。

假设该函数计算结果对应输出表的列为 factor，且迭代仅基于前一个值，对于第 k 条记录(k = 0, 1, 2 …)，其计算逻辑为：

* k < *initialWindow*：factor[k] = initial[k]
* k >= *initialWindow*：factor[k] = combineCoeff[0] \*
  X[k] + combineCoeff[1] \* iterateFunc(factor)[k-1]。

注意：若 `iterateFunc` 为窗口函数，则会基于前多个 factor 值进行计算。

## 例子

```
trade = table(take("A", 6) join take("B", 6) as sym,  1..12 as val0,  take(10, 12) as val1)
trade;
```

| sym | val0 | val1 |
| --- | --- | --- |
| A | 1 | 10 |
| A | 2 | 10 |
| A | 3 | 10 |
| A | 4 | 10 |
| A | 5 | 10 |
| A | 6 | 10 |
| B | 7 | 10 |
| B | 8 | 10 |
| B | 9 | 10 |
| B | 10 | 10 |
| B | 11 | 10 |
| B | 12 | 10 |

定义一个响应式状态引擎，并按 sym 列分组进行计算。组内的计算逻辑如下：

* 前 *initialWindow* 行记录，计算公式为 factor[k]=initial[k]，因此
  factor[0], factor[1], factor[2] 均将 val1 列的值直接作为 factor 列的输出。
* 之后的记录，对应计算公式为 factor[k]=0.5\*val0[k]+0.5\*msum(factor,
  3)[k-1]。以计算 sym=`A，val0=4 这条记录为例，此时 factor 列仅有前 3 条数据的输出，即 factor=[10, 10,
  10]，k=3，带入计算公式即 0.5\*4+0.5\*msum([10, 10, 10], 3)[2]=17。同理 sym=`A，val0=5
  这条记录带入计算公式即 0.5\*5+0.5\*msum([10, 10, 10, 17], 3)[3]=21，以此类推。

```
inputTable = streamTable(1:0, `sym`val0`val1, [SYMBOL, INT, INT])
outputTable = table(100:0, `sym`factor, [STRING, DOUBLE])
engine = createReactiveStateEngine(name="rsTest", metrics=<[stateIterate(val0, val1, 3, msum{, 3}, [0.5, 0.5])]>, dummyTable=inputTable, outputTable=outputTable, keyColumn=["sym"], keepOrder=true)

engine.append!(trade)
select * from outputTable
```

| sym | factor |
| --- | --- |
| A | 10 |
| A | 10 |
| A | 10 |
| A | 17 |
| A | 21 |
| A | 27 |
| B | 10 |
| B | 10 |
| B | 10 |
| B | 20 |
| B | 25.5 |
| B | 33.75 |

相关函数：[conditionalIterate](../c/conditionalIterate.html)

