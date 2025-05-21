# addReactiveMetrics

## 语法

`addReactiveMetrics(name, metricNames, metrics)`

## 参数

**name** 字符串，表示需要增加指标的 narrowReactiveStateEngine 的名称。

**metricNames** 字符串标量或向量，表示 narrowReactiveStateEngine 增加的计算指标的名称。

**metrics** 以元代码的格式表示计算指标，支持输入元组，表示流数据引擎增加的计算指标。计算指标与 *metricNames*
指定的名称一一对应。

## 详情

动态增加 narrowReactiveStateEngine 的计算指标。更新后的计算指标在引擎后续注入的数据时生效。

## 例子

```
dummy = streamTable(1:0, ["securityID1","securityID2","securityID3","createTime","updateTime","upToDatePrice","qty","value"], [STRING,STRING,STRING,TIMESTAMP,TIMESTAMP,DOUBLE,DOUBLE,INT])
outputTable = streamTable(1:0,["securityID1","securityID2","securityID3","createTime","updateTime","metricNames","factorValue"], [STRING,STRING,STRING, TIMESTAMP,TIMESTAMP,STRING,DOUBLE])
factor = [<createTime>, <updateTime>,<cumsum(qty)>]
Narrowtest = createNarrowReactiveStateEngine(name="narrowtest1",metrics=factor,metricNames="factor1",dummyTable=dummy,outputTable=outputTable,keyColumn=["securityID1","securityID2","securityID3"])
num = 5
tmp = table(take("A" + lpad(string(1..4),4,"0"),num) as securityID1,take("CC.HH" + lpad(string(21..34),4,"0"),num) as securityID2,take("FFICE" + lpad(string(13..34),4,"0"),num) as securityID3, 2023.09.01 00:00:00+(1..num) as createTime, 2023.09.01 00:00:00+(1..num) as updateTime,100.0+(1..num) as upToDatePrice, 130.0+(1..num) as qty,take(1..3,num) as value)
Narrowtest.append!(tmp)

select * from outputTable
```

| securityID1 | securityID2 | securityID3 | createTime | updateTime | metricNames | factorValue |
| --- | --- | --- | --- | --- | --- | --- |
| A0001 | CC.HH0021 | FFICE0013 | 2023.09.01T00:00:01.000 | 2023.09.01T00:00:01.000 | factor1 | 131 |
| A0002 | CC.HH0022 | FFICE0014 | 2023.09.01T00:00:02.000 | 2023.09.01T00:00:02.000 | facto1 | 132 |
| A0003 | CC.HH0023 | FFICE0015 | 2023.09.01T00:00:03.000 | 2023.09.01T00:00:03.000 | facto1 | 133 |
| A0004 | CC.HH0024 | FFICE0016 | 2023.09.01T00:00:04.000 | 2023.09.01T00:00:04.000 | facto1 | 134 |
| A0001 | CC.HH0025 | FFICE0017 | 2023.09.01T00:00:05.000 | 2023.09.01T00:00:05.000 | facto1 | 135 |

```
metrics = [<cumavg(upToDatePrice)>]
addReactiveMetrics("narrowtest1", "factor2", metrics)

//新增计算指标后，再次向引擎注入数据，则会输出更新后的指标计算结果
tmp1 = table("A5" as securityID1,"CC.HH0033" as securityID2,"FFICE0034" as securityID3, 2023.09.01 00:00:11 as createTime, 2023.09.01 00:00:09 as updateTime,59 as upToDatePrice,100 as qty,13 as value)
Narrowtest.append!(tmp1)
select * from outputTable where securityID1="A5"
```

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| securityID1 | securityID2 | securityID3 | createTime | updateTime | metricNames | factorValue |
| A5 | CC.HH0033 | FFICE0034 | 2023.09.01T00:00:11.000 | 2023.09.01T00:00:09.000 | facto1 | 100 |
| A5 | CC.HH0033 | FFICE0034 | 2023.09.01T00:00:11.000 | 2023.09.01T00:00:09.000 | facto2 | 59 |

相关函数：[createNarrowReactiveStateEngine](../c/createnarrowreactivestateengine.html)，[getReactiveMetrics](../g/getreactivemetrics.html)

