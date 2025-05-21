# remoteRun

## 语法

`remoteRun(conn, script, args)`

## 参数

**conn** 是远程数据库的连接句柄。

**script** 是要执行的脚本或函数名。

**args** 可选的可变长度参数。如果 *script* 是函数名，*args* 是函数的参数。

## 详情

将脚本或函数传输到远程数据库执行。

## 例子

第一种用法：在远程节点上执行脚本。

```
conn =  xdb("localhost",81);
remoteRun(conn, "x=rand(1.0,10000000); y=x pow 2; avg y");
```

输出返回：0.333254

第二种用法：

* 如果 functionName
  加了单引号，双引号或者反引号，那么表示在远程节点上调用函数。函数是定义在远程节点上，但是参数由本地节点传过去。

  ```
  h=xdb("localhost",80);
  x=remoteRun(h, "sum",1..100);
  x;
  ```

  输出返回：5050
* 如果 functionName
  没有加单引号，双引号或者反引号，那么表示调用的函数定义在本地节点上。参数也是由本地节点传过去。

  假设在本地节点，我们有一个表
  EarningsDates，该表有两列：股票代码和日期。表中3个股票中的每一个，都有2006年第三季度公布盈利的日期。在远程节点有一个表
  USPrices，节点的名字为 localhost，端口号为8081。它包含所有美国股票的每日股票价格。我们希望从远程节点获得在宣布收益后的一周内所有
  EarningsDates 表中股票的价格。 在远程节点，我们导入数据文件创建表 USPrices，然后将其共享为名叫 sharedUSPrices
  的表。

  ```
  USPrices = loadText("c:/DolphinDB/Data/USPrices.csv");
  share USPrices as USPrices;
  ```

  当我们创建到远程节点的连接时，远程节点将为此连接创建一个新的会话。此新会话与远程节点上的其他会话完全隔离。这对于开发来说很方便，因为开发人员不必担心名称冲突。
  然而，有时候我们也希望在同一节点上的多个会话之间共享数据。这时我们可以使用函数 [share](../../progr/statements/share.html) 来共享对象。目前只能在
  DolphinDB 中共享表。 在本地节点上，我们创建 EarningsDates
  表，然后用脚本将其传输到远程节点。在执行完毕后，结果被返回到本地节点。

  ```
  EarningsDates=table(`XOM`AAPL`IBM as TICKER, 2006.10.26 2006.10.19 2006.10.17 as date)
  def loadDailyPrice(data){
      dateDict = dict(data.TICKER, data.date)
      return select date, TICKER, PRC from objByName("sharedUSPrices") where dateDict[TICKER]<date<=dateDict[TICKER]+7
  }
  conn = xdb("localhost",8081)
  prices = conn.remoteRun(loadDailyPrice, EarningsDates);
  prices;
  ```

  输出返回：

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

相关函数：[remoteRunCompatible](remoteruncompatible.html)

