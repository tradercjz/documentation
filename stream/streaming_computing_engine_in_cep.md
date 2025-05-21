# 流计算引擎在 CEP 中的应用

基于 DolphinDB 的流数据框架，可在 CEP
引擎内使用和管理各种流数据计算引擎。这使得从事件流中筛选数据并进行复杂计算（如窗口聚合和序列计算等）变得便捷高效。

下例展示在 CEP 引擎中整合股票事件，并通过时序聚合引擎计算行情 K 线，计算结果将存储在 MainMonitor 的 streamMinuteBar\_1min
属性中。

```
class MarketData{
    market :: STRING
    code :: STRING
    price :: DOUBLE
    qty :: INT
    eventTime :: TIMESTAMP
    def MarketData(m,c,p,q){
        market = m
        code = c
        price = p
        qty = q
        eventTime = now()
  }
}

class MainMonitor{
    streamMinuteBar_1min :: ANY //行情K线计算结果
    tsAggrOHLC :: ANY //时间序列聚合引擎
    def MainMonitor(){
        colNames = ["time","symbol","open","max","min","close","volume","amount","ret","vwap"]
        colTypes = [TIMESTAMP, SYMBOL, DOUBLE, DOUBLE, DOUBLE, DOUBLE, INT, DOUBLE, DOUBLE, DOUBLE]
        streamMinuteBar_1min = table(10000:0,colNames, colTypes)
    }

    def updateMarketData(event)
    // 监听行情数据并创建时间序列聚合引擎，计算一分钟行情K线。
    def onload(){
        addEventListener(updateMarketData,'MarketData',,'all')
        colNames=["symbol","time","price","type","volume"]
        colTypes=[SYMBOL, TIMESTAMP, DOUBLE, STRING, INT]
        dummy = table(10000:0,colNames,colTypes)
        colNames = ["time","symbol","open","max","min","close","volume","amount","ret","vwap"]
        colTypes = [TIMESTAMP, SYMBOL, DOUBLE, DOUBLE, DOUBLE, DOUBLE, INT, DOUBLE, DOUBLE, DOUBLE]
        output = table(10000:0,colNames, colTypes)
        tsAggrOHLC = createTimeSeriesEngine(name="tsAggrOHLC", windowSize=60000, step=60000, metrics=<[first(price) as open ,max(price) as max,min(price) as min ,last(price) as close ,sum(volume) as volume ,wsum(volume, price) as amount ,(last(price)-first(price)/first(price)) as ret, (wsum(volume, price)/sum(volume)) as vwap]>, dummyTable=dummy, outputTable=streamMinuteBar_1min, timeColumn='time', useSystemTime=false, keyColumn="symbol", fill=`none)
    }

    def updateMarketData(event){
        tsAggrOHLC.append!(table(event.code as symbol, event.eventTime as time, event.price as price, event.market as type, event.qty as volume))
    }
}
dummy = table(array(STRING, 0) as eventType, array(BLOB, 0) as blobs)
engine = createCEPEngine(name='cep1', monitors=<MainMonitor()>, dummyTable=dummy, eventSchema=[MarketData])
```

Copyright

**©2025 浙江智臾科技有限公司 浙ICP备18048711号-3**
