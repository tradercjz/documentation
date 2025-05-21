# getReactiveMetrics

## 语法

`getReactiveMetrics(name)`

### 参数

**name** 字符串，表示 narrowReactiveStateEngine 的名称。

### 详情

获取指定名称的 narrowReactiveStateEngine 的计算指标列。

返回一个表，第一列为 metricName，第二列为 metricCode。

### 例子

```
dummy = streamTable(1:0, ["securityID1","securityID2","securityID3","createTime","updateTime","upToDatePrice","qty","value"], [STRING,STRING,STRING,TIMESTAMP,TIMESTAMP,DOUBLE,DOUBLE,INT])
outputTable = streamTable(1:0,["securityID1","securityID2","securityID3","createTime","updateTime","metricNames","factorValue"], [STRING,STRING,STRING, TIMESTAMP,TIMESTAMP,STRING,DOUBLE])
factor = [<createTime>, <updateTime>,<cumsum(qty)>]
Narrowtest = createNarrowReactiveStateEngine(name="narrowtest1",metrics=factor,metricNames="factor1",dummyTable=dummy,outputTable=outputTable,keyColumn=["securityID1","securityID2","securityID3"])
getReactiveMetrics("narrowtest1")
```

| metricName | metricCode |
| --- | --- |
| factor1 | cumsum(qty) |

相关函数：[createNarrowReactiveStateEngine](../c/createnarrowreactivestateengine.html)，[addReactiveMetrics](../a/addreactivemetrics.html)

