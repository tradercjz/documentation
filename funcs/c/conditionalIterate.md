# conditionalIterate

## 语法

`conditionalIterate(cond, trueValue,
falseIterFunc)`

该函数只能用作响应式状态引擎 `metrics` 中的函数。

## 参数

**cond** 布尔表达式/返回值是布尔类型的函数。需要包含输入表中的字段，不支持常量/常量表达式。

**trueValue** 计算公式。计算结果将作为 *cond* 为 true 时的输出值。

**falseIterFunc** 用于进行迭代计算的函数。必须是一个单目函数，其唯一参数是 `conditionalIterate`
对应输出表中的字段。目前只支持以下函数（非单目函数以部分应用形式给出其他参数）：

* 滑动窗口函数：`tmove`, `tmavg`,
  `tmmax`, `tmmin`, `tmsum`,
  `mavg`, `mmax`, `mmin`,
  `mcount`, `msum`
* 累计窗口函数：`cumlastNot`,
  `cumfirstNot`
* 序列相关函数：`ffill`, `move`

若当前记录的 *cond* 为 true 时，触发 *trueValue* 的计算；若当前记录的
*cond* 为 false，则基于 `conditionalIterate` 的历史结果，调用
*falseIterFunc* 进行迭代计算。

注：

* 由于迭代是基于历史数据进行的，因此当前记录的输出是由输出表中的历史结果计算得到的。
* tm系列函数计算时，时间窗口由当前记录的时间戳确定。由于迭代不包含当前记录，因此实质上的，且计算窗口范围为 (T - window,
  T)。
* *trueValue* 和 *falseIterFunc*
  计算结果的类型需要兼容，且需要确保 *trueValue* 结果的精度和数据范围大于
  *falseIterFunc*。

## 详情

通过条件迭代实现因子中的递归逻辑。

假设该函数计算结果对应输出表的列为 factor，且迭代仅基于前一个值，对于第 k 条记录(k = 0, 1, 2 …)，其计算逻辑为：

* cond[k] == true：factor[k] = trueValue
* cond[k] == false：factor[k] = falseIterFunc(factor)[k-1]

注： 若 *falseIterFunc* 为窗口函数，则会基于前多个 factor
值进行计算。

## 例子

例1. 通过一个简单的例子，快速了解 `conditionalIterate`
函数的计算逻辑：

```
trade = table(take("A", 10) as sym,  take(1 3 6, 10) as val0,  take(10, 10) as val1)
trade
```

| sym | val0 | val1 |
| --- | --- | --- |
| A | 1 | 10 |
| A | 3 | 10 |
| A | 6 | 10 |
| A | 1 | 10 |
| A | 3 | 10 |
| A | 6 | 10 |
| A | 1 | 10 |
| A | 3 | 10 |
| A | 6 | 10 |
| A | 1 | 10 |

创建一个响应式状态引擎，并按 sym 列分组进行计算。组内的计算逻辑如下：

* 若满足 val0 > 5，若返回 true，则 *factor[k]=trueValue*，即以 val1 值作为输出。
* 若不满足 val0 > 5，则对应计算公式为
  factor[k]=falseIterFunc(factor)[k-1]。当 k=3 时，对应 val0=1，val1=10，factor=[NULL,
  NULL, 10]，带入公式计算即 msum([NULL, NULL, 10], 3)[2]=10；当 k=4 时，对应
  val0=3，val1=10，factor=[NULL, NULL, 10, 10]，带入公式计算即 msum([NULL, NULL, 10,
  10], 3)[3]=20，以此类推。

```
inputTable = streamTable(1:0, `sym`val0`val1, [SYMBOL, INT, INT])
outputTable = table(100:0, `sym`factor, [STRING, DOUBLE])
rse = createReactiveStateEngine(name="rsTest", metrics=<conditionalIterate(val0 > 5, val1, msum{, 3})>, dummyTable=inputTable, outputTable=outputTable, keyColumn="sym")
rse.append!(trade)
select * from outputTable
```

| sym | factor |
| --- | --- |
| A |  |
| A |  |
| A | 10 |
| A | 10 |
| A | 20 |
| A | 10 |
| A | 40 |
| A | 70 |
| A | 10 |
| A | 120 |

例2. 某因子在函数中算法逻辑如下：

```
def factor(TotalVolumeTrade, TotalValueTrade, HighPx, LowPx){
    factorValue = iif(TotalVolumeTrade < 1500000, pow(HighPx*LowPx, 0.5)-(TotalVolumeTrade/TotalValueTrade), mavg(factor(TotalVolumeTrade, TotalValueTrade, HighPx, LowPx), 3))
    return factorValue
}
```

该函数包含了一个递归操作。若需要在响应式状态引擎中实现上述逻辑，可以通过函数
`conditionalIterate` 实现。具体实现脚本如下：

```
@state
def factor1(TotalVolumeTrade, TotalValueTrade, HighPx, LowPx){
   factorValue = conditionalIterate(TotalVolumeTrade < 1500000, (pow(HighPx*LowPx, 0.5)-(TotalVolumeTrade/TotalValueTrade)), mavg{,3})
   return factorValue
}

SecurityID =  ["000001.SZ","000001.SZ","000001.SZ","000001.SZ","000001.SZ","000001.SZ","000001.SZ","000001.SZ","000001.SZ","000001.SZ"]$SYMBOL
Date = [2022.04.01,2022.04.01,2022.04.01,2022.04.01,2022.04.01,2022.04.01,2022.04.01,2022.04.01,2022.04.01,2022.04.01]
Time = [09:30:00.000,09:30:03.000,09:30:06.000,09:30:09.000,09:30:12.000,09:30:15.000,09:30:18.000,09:30:21.000,09:30:24.000,09:30:27.000]
TotalVolumeTrade = [844800,1035700,1240100,1304500,1457800,1522400,1550900,1663800,1692100,1767100]
TotalValueTrade = [12982101,15908020,19038479,20022525,22363886,23349799,23784950,25506625.75,25937850.75,27080561.75]
HighPx = [15.37,15.37,15.37,15.37,15.37,15.37,15.37,15.37,15.37,15.37]
LowPx = [15.3,15.3,15.29,15.28,15.24,15.24,15.24,15.22,15.22,15.22]
trade = table(SecurityID, Date, Time, TotalVolumeTrade, TotalValueTrade, HighPx, LowPx)

result = table(1:0, `SecurityID`Date`Time`Factor, `SYMBOL`DATE`TIME`DOUBLE)

factor=[<Date>,<Time>, <factor1(TotalVolumeTrade, TotalValueTrade, HighPx, LowPx)>]
rse = createReactiveStateEngine(name="rsTest", metrics=factor, dummyTable=trade, outputTable=result, keyColumn="SecurityID")
rse.append!(trade)

trade1 = select *,  (pow(HighPx*LowPx, 0.5)-(TotalVolumeTrade/TotalValueTrade)) as Factor0 from trade
select * from lj(trade1, result, `SecurityID`Date`Time)
dropStreamEngine("rsTest")
```

部分输出结果如图：

![](../../images/conditionalIterate_output.png)

对于上述蓝框部分的数据，触发 *trueValue* 计算逻辑，因此 Factor 的值等于 Factor0 的计算结果；红框部分的数据触发
*falseIterFunc* 计算逻辑，每条记录的 Factor 是输出表中该记录前三条 Factor 的平均值。

**相关信息**

* [stateIterate](../s/stateIterate.html "stateIterate")

