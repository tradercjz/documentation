# objByName

## 语法

`objByName(name, [sharedVar])`

## 参数

**name** 是一个字符串，表示表名。

**sharedVar** 是一个布尔值。

## 详情

DolphinDB 在执行脚本之前先解析脚本。解析脚本的过程是检查变量是否在本地定义。如果没有在本地定义，则抛出异常。

假设我们在本地定义一个函数，然后在远程节点上执行。这个函数会查询共享表。但是，共享表在远程节点上而不在本地节点上。如果在函数的
SQL 语句中直接调用表名，系统将不能解析脚本。

为了解决这个问题，系统函数 `objByName` 在执行时会根据名称返回对象。

如果没有指定 *sharedVar* 参数，系统首先搜索会话中的局部变量，再搜索共享变量。如果 *sharedVar*
为true，表示只搜索共享变量。如果 *sharedVar* 为false，表示只搜索局部变量。

## 例子

假设在本地节点上有一个表 EarningsDates，它包含两列：Ticker 和 date。主机名为localhost 服务器的
8081 端口上的远程节点有一个表 USPrices。它包含所有美国股票的每日价格。我们想要从远程节点取得 EarningsDates
表中所有股票在公布收益后一周的价格。

在远程节点，导入数据文件创建表 USPrices，然后在所有节点间共享。

```
USPrices = loadText("c:/DolphinDB/Data/USPrices.csv")
share USPrices as sharedUSPrices;
```

在本地节点，创建表 EarningsDates，然后把表和脚本发送到远程节点。执行完成后，结果会发送回本地节点。

```
EarningsDates=table(`XOM`AAPL`IBM as TICKER, 2006.10.26 2006.10.19 2006.10.17 as date)
def loadDailyPrice(data){
   dateDict = dict(data.TICKER, data.date)
   return select date, TICKER, PRC from objByName("sharedUSPrices") where dateDict[TICKER]<date<=dateDict[TICKER]+7
}
conn = xdb("localhost",8081)
prices = conn(loadDailyPrice, EarningsDates);

prices;
```

| date | TICKER | PRC |
| --- | --- | --- |
| 2006.10.27 | XOM | 71.46 |
| 2006.10.30 | XOM | 70.84 |
| 2006.10.31 | XOM | 71.42 |
| 2006.11.01 | XOM | 71.06 |
| 2006.11.02 | XOM | 71.19 |
| 2006.10.18 | IBM | 89.82 |
| 2006.10.19 | IBM | 89.86 |
| 2006.10.20 | IBM | 90.48 |
| 2006.10.23 | IBM | 91.56 |
| 2006.10.24 | IBM | 91.49 |
| 2006.10.20 | AAPL | 79.95 |
| 2006.10.23 | AAPL | 81.46 |
| 2006.10.24 | AAPL | 81.05 |
| 2006.10.25 | AAPL | 81.68 |
| 2006.10.26 | AAPL | 82.19 |

