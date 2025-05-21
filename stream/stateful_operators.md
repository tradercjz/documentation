# 有状态算子

有状态算子是指在处理流数据时，需要维护状态的算子。这种算子的输出不仅依赖于当前输入，还依赖于先前的状态或历史记录。在处理完当前输入后，有状态算子会更新其内部状态，并将其用于后续的计算。因此，相同的输入在不同的状态下可能会产生不同的输出。

![](images/stateful_operators_1.png)

## 有状态算子

在 DolphinDB 的部分流计算引擎中，例如状态引擎、时序聚合引擎、window join
引擎，可以使用内置有状态算子。内置的有状态算子经过系统优化，实现了增量计算，可以提高计算性能。在状态引擎中，还可以使用自定义状态算子，以满足用户复杂的流计算需求。

**内置有状态算子**

以下内置函数可以作为响应式状态引擎的有状态算子：

* 累计窗口函数：[cumavg](../funcs/c/cumavg.md), [cumsum](../funcs/c/cumsum.md), [cumprod](../funcs/c/cumprod.md), [cumcount](../funcs/c/cumcount.md), [cummin](../funcs/c/cummin.md), [cummax](../funcs/c/cummax.md), [cumvar](../funcs/c/cumvar.md), [cumvarp](../funcs/c/cumvarp.md), [cumstd](../funcs/c/cumstd.md), [cumstdp](../funcs/c/cumstdp.md), [cumcorr](../funcs/c/cumcorr.md), [cumcovar](../funcs/c/cumcovar.md), [cumbeta](../funcs/c/cumbeta.md), [cumwsum](../funcs/c/cumwsum.md), [cumwavg](../funcs/c/cumwavg.md), [cumfirstNot](../funcs/c/cumfirstNot.md),
  [cumlastNot](../funcs/c/cumlastNot.md), [cummed](../funcs/c/cummed.md), [cumpercentile](../funcs/c/cumpercentile.md), [cumnunique](../funcs/c/cumnunique.md),
  [cumPositiveStreak](../funcs/c/cumPositiveStreak.md), [cummdd](../funcs/c/cummdd.md)
* 滑动窗口函数：[ema](../funcs/c/../e/ema.md), [mavg](../funcs/c/../m/mavg.md), [msum](../funcs/c/../m/msum.md), [mcount](../funcs/c/../m/mcount.md), [mprod](../funcs/c/../m/mprod.md), [mvar](../funcs/c/../m/mvar.md), [mvarp](../funcs/c/../m/mvarp.md), [mstd](../funcs/c/../m/mstd.md), [mstdp](../funcs/c/../m/mstdp.md), [mskew](../funcs/c/../m/mskew.md), [mkurtosis](../funcs/c/../m/mkurtosis.md), [mmin](../funcs/c/../m/mmin.md), [mmax](../funcs/c/../m/mmax.md), [mimin](../funcs/c/../m/mimin.md), [mimax](../funcs/c/../m/mimax.md), [mmed](../funcs/c/../m/mmed.md), [mpercentile](../funcs/c/../m/mpercentile.md), [mrank](../funcs/c/../m/mrank.md), [mcorr](../funcs/c/../m/mcorr.md), [mcovar](../funcs/c/../m/mcovar.md), [mbeta](../funcs/c/../m/mbeta.md), [mwsum](../funcs/c/../m/mwsum.md), [mwavg](../funcs/c/../m/mwavg.md), [mmad](../funcs/c/../m/mmad.md), [mfirst](../funcs/c/../m/mfirst.md), [mlast](../funcs/c/../m/mlast.md), [mslr](../funcs/c/../m/mslr.md), [tmove](../funcs/c/../t/tmove.md), [tmfirst](../funcs/c/../t/tmfirst.md), [tmlast](../funcs/c/../t/tmlast.md), [tmsum](../funcs/c/../t/tmsum.md), [tmsum2](../funcs/c/../t/tmsum2.md), [tmavg](../funcs/c/../t/tmavg.md), [tmcount](../funcs/c/../t/tmcount.md), [tmvar](../funcs/c/../t/tmvar.md), [tmvarp](../funcs/c/../t/tmvarp.md), [tmstd](../funcs/c/../t/tmstd.md), [tmstdp](../funcs/c/../t/tmstdp.md), [tmprod](../funcs/c/../t/tmprod.md), [tmskew](../funcs/c/../t/tmskew.md), [tmkurtosis](../funcs/c/../t/tmkurtosis.md), [tmmin](../funcs/c/../t/tmmin.md), [tmmax](../funcs/c/../t/tmmax.md), [tmmed](../funcs/c/../t/tmmed.md), [tmpercentile](../funcs/c/../t/tmpercentile.md),
  [tmrank](../funcs/c/../t/tmrank.md), [tmcovar](../funcs/c/../t/tmcovar.md), [tmbeta](../funcs/c/../t/tmbeta.md), [tmcorr](../funcs/c/../t/tmcorr.md), [tmwavg](../funcs/c/../t/tmwavg.md), [tmwsum](../funcs/c/../t/tmwsum.md), [tmoving](../funcs/c/../ho_funcs/tmoving.md), [moving](../funcs/c/../ho_funcs/moving.md), [sma](../funcs/c/../s/sma.md), [wma](../funcs/c/../w/wma.md), [dema](../funcs/c/../d/dema.md), [tema](../funcs/c/../t/tema.md),
  [trima](../funcs/c/../t/trima.md), [linearTimeTrend](../funcs/c/../l/linearTimeTrend.md), [talib](../funcs/c/../ho_funcs/talib.md), [t3](../funcs/c/../t/t3.md), [ma](../funcs/c/../m/ma.md), [gema](../funcs/c/../g/gema.md), [wilder](../funcs/c/../w/wilder.md), [mmaxPositiveStreak](../funcs/c/../m/mmaxPositiveStreak.md), [movingWindowData](../funcs/c/../m/movingWindowData.md), [tmovingWindowData](../funcs/c/../t/tmovingWindowData.md)
* 行计算函数： [rowMin](../funcs/c/../r/rowMin.md), [rowMax](../funcs/c/../r/rowMax.md), [rowAnd](../funcs/c/../r/rowAnd.md), [rowOr](../funcs/c/../r/rowOr.md), [rowXor](../funcs/c/../r/rowXor.md), [rowProd](../funcs/c/../r/rowProd.md), [rowSum](../funcs/c/../r/rowSum.md), [rowSum2](../funcs/c/../r/rowSum2.md), [rowSize](../funcs/c/../r/rowSize.md), [rowCount](../funcs/c/../r/rowCount.md), [rowAvg](../funcs/c/../r/rowAvg.md), [rowKurtosis](../funcs/c/../r/rowKurtosis.md), [rowSkew](../funcs/c/../r/rowSkew.md), [rowVar](../funcs/c/../r/rowVar.md), [rowVarp](../funcs/c/../r/rowVarp.md), [rowStd](../funcs/c/../r/rowStd.md), [rowStdp](../funcs/c/../r/rowStdp.md)
* 序列相关函数：[deltas](../funcs/c/../d/deltas.md), [ratios](../funcs/c/../r/ratios.md), [ffill](../funcs/c/../f/ffill.md), [move](../funcs/c/../m/move.md), [prev](../funcs/c/../p/prev.md), [iterate](../funcs/c/../i/iterate.md), [ewmMean](../funcs/c/../e/ewmMean.md), [ewmVar](../funcs/c/../e/ewmVar.md), [ewmStd](../funcs/c/../e/ewmStd.md), [ewmCov](../funcs/c/../e/ewmCov.md), [ewmCorr](../funcs/c/../e/ewmCorr.md), [prevState](../funcs/c/../p/prevState.md), [percentChange](../funcs/c/../p/percentChange.md)
* topN相关函数：[msumTopN](../funcs/c/../m/msumTopN.md), [mavgTopN](../funcs/c/../m/mavgTopN.md), [mstdpTopN](../funcs/c/../m/mstdpTopN.md), [mstdTopN](../funcs/c/../m/mstdTopN.md), [mvarpTopN](../funcs/c/../m/mvarpTopN.md), [mvarTopN](../funcs/c/../m/mvarTopN.md), [mcorrTopN](../funcs/c/../m/mcorrTopN.md), [mbetaTopN](../funcs/c/../m/mbetaTopN.md), [mcovarTopN](../funcs/c/../m/mcovarTopN.md), [mwsumTopN](../funcs/c/../m/mwsumTopN.md), [cumsumTopN](../funcs/c/cumsumTopN.md), [cumwsumTopN](../funcs/c/cumwsumTopN.md), [cumvarTopN](../funcs/c/cumvarTopN.md), [cumvarpTopN](../funcs/c/cumvarpTopN.md), [cumstdTopN](../funcs/c/cumstdTopN.md), [cumstdpTopN](../funcs/c/cumstdpTopN.md), [cumcorrTopN](../funcs/c/cumcorrTopN.md), [cumbetaTopN](../funcs/c/cumbetaTopN.md), [cumavgTopN](../funcs/c/../m/mstdpTopN.md), [msumTopN](../funcs/c/../m/msumTopN.md), [mavgTopN](../funcs/c/../m/mavgTopN.md), [mstdpTopN](../funcs/c/../m/mstdpTopN.md), [mstdTopN](../funcs/c/../m/mstdTopN.md), [mvarpTopN](../funcs/c/../m/mvarpTopN.md), [mvarTopN](../funcs/c/../m/mvarTopN.md), [mcorrTopN](../funcs/c/../m/mcorrTopN.md), [mbetaTopN](../funcs/c/../m/mbetaTopN.md), [mcovarTopN](../funcs/c/../m/mcovarTopN.md), [mwsumTopN](../funcs/c/../m/mwsumTopN.md), [cumsumTopN](../funcs/c/cumsumTopN.md), [cumwsumTopN](../funcs/c/cumwsumTopN.md), [cumvarTopN](../funcs/c/cumvarTopN.md), [cumvarpTopN](../funcs/c/cumvarpTopN.md), [cumstdTopN](../funcs/c/cumstdTopN.md), [cumstdpTopN](../funcs/c/cumstdpTopN.md), [cumcorrTopN](../funcs/c/cumcorrTopN.md), [cumbetaTopN](../funcs/c/cumbetaTopN.md), [cumavgTopN](../funcs/c/cumavgTopN.md), [cumskewTopN](../funcs/c/cumskewTopN.md), [cumkurtosisTopN](../funcs/c/cumkurtosisTopN.md), [mskewTopN](../funcs/c/../m/mskewTopN.md),
  [mkurtosisTopN](../funcs/c/../m/mkurtosisTopN.md),[tmsumTopN](../funcs/c/../t/tmsumTopN.md), [tmavgTopN](../funcs/c/../t/tmavgTopN.md), [tmstdTopN](../funcs/c/../t/tmstdTopN.md), [tmstdpTopN](../funcs/c/../t/tmstdpTopN.md), [tmvarTopN](../funcs/c/../t/tmvarTopN.md), [tmvarpTopN](../funcs/c/../t/tmvarpTopN.md), [tmskewTopN](../funcs/c/../t/tmskewTopN.md), [tmkurtosisTopN](../funcs/c/../t/tmkurtosisTopN.md), [tmbetaTopN](../funcs/c/../t/tmbetaTopN.md), [tmcorrTopN](../funcs/c/../t/tmcorrTopN.md), [tmcovarTopN](../funcs/c/../t/tmcovarTopN.md), [tmwsumTopN](../funcs/c/../t/tmwsumTopN.md)
* 高阶函数：[segmentby](../funcs/c/../ho_funcs/segmentby.md) (参数 *func* 暂支持 cumsum, cummax, cummin, cumcount,
  cumavg, cumstd, cumvar, cumstdp, cumvarp), [moving](../funcs/c/../ho_funcs/moving.md), [byColumn](../funcs/c/../ho_funcs/byColumn.md), [accumulate](../funcs/c/../ho_funcs/accumulate.md), [window](../funcs/c/../ho_funcs/window.md)
* 其他函数：[talibNull](../funcs/c/../t/talibNull.md), [dynamicGroupCumsum](../funcs/c/../d/dynamicGroupCumsum.md), [dynamicGroupCumcount](../funcs/c/../d/dynamicGroupCumcount.md), [topRange](../funcs/c/../t/topRange.md), [lowRange](../funcs/c/../l/lowRange.md), [trueRange](../funcs/c/../t/trueRange.md), [sumbars](../funcs/c/../s/sumbars.md)
* 特殊函数（仅支持在引擎内使用）：[stateIterate](../funcs/c/../s/stateIterate.md), [conditionalIterate](../funcs/c/conditionalIterate.md), [genericStateIterate](../funcs/c/../g/genericStateIterate.md), [genericTStateIterate](../funcs/c/../g/genericTStateIterate.md)

以下内置函数可以作为时序聚合引擎的有状态算子：

corr, covar, first, last, max, med, min, percentile, quantile, std, var, sum, sum2,
sum3, sum4, wavg, wsum, count, firstNot, ifirstNot, lastNot, ilastNot, imax, imin,
nunique, prod, sem, mode, searchK, beta, avg。

以下内置函数可以作为 window join 引擎的有状态算子：

sum, sum2, avg, std, var, corr, covar, wavg, wsum, beta, max, min, last, first, med,
percentile。

**自定义有状态算子**

用户还可以通过 @state 声明自定义函数，将其封装一个自定义的状态算子。在使用自定义状态函数时，需要注意以下事项：

1. 需在定义前添加声明 "@state"。状态函数只能包含赋值语句和 return 语句。

   自 2.00.9 版本起，支持使用 if-else
   条件语句，且条件只能是标量。

   自2.00.11 版本起，支持使用 for 循环（包含 break, continue
   语句），请注意不支持嵌套 for 循环，且循环次数须小于 100 次。
2. 状态引擎中可以使用无状态函数或者状态函数。但不允许在无状态函数中嵌套使用状态函数。
3. 若赋值语句的右值是一个多返回值的函数（内置函数或自定义函数），则需要将多个返回值同时赋予多个变量。例如：两个返回值的函数 linearTimeTrend
   应用于自定义状态函数中，正确写法为：

   ```
   @state
   def forcast2(S, N){
         linearregIntercept, linearregSlope = linearTimeTrend(S, N)
         return (N - 1) * linearregSlope + linearregIntercept
   }
   ```

自定义状态算子在使用上存在一些局限性，例如其运行效率低于内置状态算子，并且仅支持部分语句。为更方便用户开发自定义状态算子，DolphinDB
还提供了更灵活且易于维护的解决方案：

* 使用 DolphinDB Class 开发状态算子。更多信息，请参考使用 DolphinDB Class 来开发流计算状态算子 。

## 有状态算子应用示例

本节我们以涨幅为例介绍如何使用响应式状态引擎进行有状态计算。在股票市场中涨幅指最新成交价格与之前某一刻的历史成交价格的价差的比。本例中将涨幅定义为当前一条行情快照的最新价与上一条行情快照的最新价格的比。

**step1：创建发布流数据表**

```
share(table=streamTable(1:0, `securityID`datetime`lastPrice`openPrice, [SYMBOL,TIMESTAMP,DOUBLE,DOUBLE]), sharedName=`tick)
```

**step2：创建存储处理后数据的共享流数据表**

```
share(table=streamTable(10000:0, `securityID`datetime`factor, [SYMBOL, TIMESTAMP, DOUBLE]), sharedName=`resultTable)
```

**step3：自定义状态算子--涨幅因子**

```
@state
def priceChange(lastPrice){
    return lastPrice \ prev(lastPrice) - 1
}
```

**step4：**创建响应式状态引擎****

```
try{ dropStreamEngine("reactiveDemo") } catch(ex){ print(ex) }
createReactiveStateEngine(name="reactiveDemo",
metrics =<[datetime, priceChange(lastPrice)]>,
dummyTable=tick, outputTable=resultTable, keyColumn="securityID")
```

创建响应式状态引擎时指定
securityID 作为分组列，即计算每支股票各自的价格涨幅。 输入引擎的消息格式同表 tick，结果输出到内存表 resultTable
中。需要计算的指标定义在 *metrics*里。

**step5：订阅发布流数据表**

```
subscribeTable(tableName="tick", actionName="reactiveDemo",
handler=getStreamEngine(`reactiveDemo), msgAsTable=true, offset=-1)
```

**step6：模拟批量数据写入**

```
securityID = ["AA", "AA", "BB", "AA"]
dateTime = [2024.06.02 09:00:00.000, 2024.06.02 09:01:00.000, 2024.06.02 09:03:00.000, 2024.06.02 09:04:00.000]
lastPrice = [9.99, 1.58, 5.37, 9.82]
openPrice = [10.05, 1.50, 5.25, 9.70]
simulateData =  table(securityID, dateTime, lastPrice, openPrice)
tableInsert(tick, simulateData)
```

**step7：查询结果表数据**

```
res = select * from resultTable
```

返回结果
res：

![](images/stateful_operator_3.png)

**step8：取消订阅**

```
unsubscribeTable(tableName="tick", actionName="reactiveDemo")
```

**step9：删除响应式状态引擎**

```
dropStreamEngine(name="reactiveDemo")
```

**step10：删除发布流数据表和结果流数据表**

**注意**：删除发布流数据表前，必须先把其所有订阅取消掉。

```
dropStreamTable(tableName="tick")
dropStreamTable(tableName="resultTable")
```

