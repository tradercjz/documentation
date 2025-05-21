# addMetrics

## 语法

`addMetrics(engine, newMetrics, newMetricsSchema,
[windowSize], [fill])`

别名：`extendMetrics`

## 参数

**engine** 是流数据引擎，即 [createTimeSeriesEngine](../c/createTimeSeriesEngine.html) 等函数返回的抽象表对象。请注意，暂不支持 [createAnomalyDetectionEngine](../c/createAnomalyDetectionEngine.html) 和 [createReactiveStateEngine](../c/createReactiveStateEngine.html) 引擎。

**newMetrics**
是元代码，表示流数据引擎增加的计算指标。可以是一个或多个表达式、系统内置或用户自定义函数，也可以是一个常量标量/向量。当指定为常量向量时，对应的输出列应该设置为数组向量类型。

**newMetricsSchema** 是表对象，指定新增的计算指标在输出表中的列名和数据类型。

**windowSize**
是一个正整数，表示新增指标的计算窗口长度。仅适用于时间序列引擎，且必须为已指定的窗口长度之一。若未指定，默认值为第一个已指定的窗口长度。

**fill** 可选参数，一个标量或向量，指定某个分组的某个窗口无数据时的处理方法。可取以下值：

* 'none': 不输出结果。
* 'null': 输出结果为 NULL。
* 'ffill': 输出上一个有数据的窗口的结果。
* '具体数值'：该值的数据类型需要和对应的 *metrics* 计算结果的类型保持一致。

*fill* 可以输入向量，长度与 *metrics* 元素个数保持一致，表示为每个 *metrics* 指定不同的 *fill*
方式。若为向量，向量中各项只能是 'null', 'ffill' 或一个数值，不能是 'none'。

## 详情

动态增加流数据引擎的计算指标。

## 例子

使用流数据时间序列引擎计算 sum(x) 指标。

```
share streamTable(10000:0,`time`id`x, [TIMESTAMP,SYMBOL,INT]) as t
output1 = table(10000:0, `time`sum_x, [TIMESTAMP,INT])
agg1 = createTimeSeriesEngine(name=`agg1, windowSize=100, step=50, metrics=<sum(x)>, dummyTable=t, outputTable=output1, timeColumn=`time)
subscribeTable(tableName="t", actionName="agg1", offset=0, handler=append!{agg1}, msgAsTable=true)
n=500
time=2019.01.01T00:00:00.000+(1..n)
id=take(`ABC`DEF, n)
x=1..n
insert into t values(time, id, x);
select * from output1;
```

| time | sum\_x |
| --- | --- |
| 2019.01.01T00:00:00.050 | 1,225 |
| 2019.01.01T00:00:00.100 | 4,950 |
| 2019.01.01T00:00:00.150 | 9,950 |
| 2019.01.01T00:00:00.200 | 14,950 |
| 2019.01.01T00:00:00.300 | 24,950 |
| 2019.01.01T00:00:00.350 | 29,950 |
| 2019.01.01T00:00:00.400 | 34,950 |
| 2019.01.01T00:00:00.450 | 39,950 |
| 2019.01.01T00:00:00.500 | 44,950 |

给时间序列引擎增加 avg(x) 指标，该指标在输出表中的名称为 avg\_x，数据类型为 DOUBLE。

```
newMetricsSchema= table(1:0, [`avg_x], [DOUBLE])
addMetrics(agg1, <avg(x)>, newMetricsSchema);
n=300
time=2019.01.01T00:00:00.500+(1..n)
id=take(`ABC`DEF, n)
x=500+1..n
insert into t values(time, id, x);
select * from output1;
```

| time | sum\_x | avg\_x |
| --- | --- | --- |
| 2019.01.01T00:00:00.050 | 1,225 |  |
| 2019.01.01T00:00:00.100 | 4,950 |  |
| 2019.01.01T00:00:00.150 | 9,950 |  |
| 2019.01.01T00:00:00.200 | 14,950 |  |
| 2019.01.01T00:00:00.250 | 19,950 |  |
| 2019.01.01T00:00:00.300 | 24,950 |  |
| 2019.01.01T00:00:00.350 | 29,950 |  |
| 2019.01.01T00:00:00.400 | 34,950 |  |
| 2019.01.01T00:00:00.450 | 39,950 |  |
| 2019.01.01T00:00:00.500 | 44,950 |  |
| 2019.01.01T00:00:00.550 | 49,950 | 525 |
| 2019.01.01T00:00:00.600 | 54,950 | 550 |
| 2019.01.01T00:00:00.650 | 59,950 | 599.5 |
| 2019.01.01T00:00:00.700 | 64,950 | 649.5 |
| 2019.01.01T00:00:00.750 | 69,950 | 699.5 |
| 2019.01.01T00:00:00.800 | 74,950 | 749.5 |

