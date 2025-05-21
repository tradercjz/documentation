# 集群内跨节点订阅

本节介绍集群内跨节点订阅流处理结果的交互方式。对于集群内跨节点订阅，发布端与订阅端在一个集群的不同节点，在订阅时需要指定发布端的节点名称。

下面为以逐笔成交数据为例介绍订阅流数据结果订阅及写入数据库的流程。

1. 发布端创建一个共享的流数据表 *tglobal*。

   ```
   name = `ChannelNo`ApplSeqNum`MDStreamID`BidApplSeqNum`OfferApplSeqNum`SecurityID`SecurityIDSource`TradePrice`TradeQty`ExecType`TradeTime`LocalTime`SeqNo`DataStatus`TradeMoney`TradeBSFlag`BizIndex`OrderKind`Market
   type = [INT,LONG,SYMBOL,LONG,LONG,SYMBOL,SYMBOL,DOUBLE,INT,SYMBOL,TIMESTAMP,TIME,LONG,INT,DOUBLE,SYMBOL,LONG,SYMBOL,SYMBOL]
   share streamTable(100:0, name, type) as tglobal
   ```
2. 订阅端创建一个分布式数据表，用于存储订阅到的数据。

   ```
   if(existsDatabase("dfs://tradeDB"))
       dropDatabase("dfs://tradeDB")
   db1 = database(, VALUE, 2020.01.01..2021.01.01)
   db2 = database(, HASH, [SYMBOL, 50])
   db = database("dfs://tradeDB", COMPO, [db1, db2], , "TSDB")
   name = `ChannelNo`ApplSeqNum`MDStreamID`BidApplSeqNum`OfferApplSeqNum`SecurityID`SecurityIDSource`TradePrice`TradeQty`ExecType`TradeTime`LocalTime`SeqNo`DataStatus`TradeMoney`TradeBSFlag`BizIndex`OrderKind`Market
   type = [INT,LONG,SYMBOL,LONG,LONG,SYMBOL,SYMBOL,DOUBLE,INT,SYMBOL,TIMESTAMP,TIME,LONG,INT,DOUBLE,SYMBOL,LONG,SYMBOL,SYMBOL]
   t = db.createPartitionedTable(table=table(1:0, name, type), tableName="tradeTB", partitionColumns=`TradeTime`SecurityID, sortColumns=[`SecurityID, `TradeTime])
   ```
3. 创建表 *tglobal* 的本地订阅，server 参数需设置为发布端节点名，在本例中为 dnode1； *handler*
   设置为需要写入的表 *trades*，*batchSize* 和 *throttle*
   应根据需求合理设置，具体参数含义见[subscribeTable](../funcs/s/subscribeTable.md)。

   ```
   trade = loadTable("dfs://tradeDB", "tradeTB")
   subscribeTable(server="dnode1", tableName="tglobal", actionName="insertDB", offset=0, handler=trade, msgAsTable=true, batchSize=100000, throttle=60)
   ```
4. 向发布端流数据表 *tglobal* 写入模拟数据。

   ```
   for(i in 1..100){
       insertData = [rand(100,1),long(i),string(i),long(i),long(i),string(i),string(i),rand(1.0,1),rand(100,1),string(i),timestamp('2021.01.04T09:30:02.000'),time('09:30:02.000'),long(i),rand(100,1),rand(1.0,1),string(i),long(i),string(i),string(i)]
       insert into tglobal values(insertData)
   }
   ```
5. 查看写入接收端库表的数据。

   ```
   select * from loadTable("dfs://tradeDB","tradeTB") limit 5

   // output
   ChannelNo	ApplSeqNum	MDStreamID	BidApplSeqNum	OfferApplSeqNum	SecurityID	SecurityIDSource	TradePrice	TradeQty	ExecType	TradeTime	LocalTime	SeqNo	DataStatus	TradeMoney	TradeBSFlag	BizIndex	OrderKind	Market
   60	43	43	43	43	43	43	0.7538	56	43	2021.01.04T09:30:02.000	09:30:02.000	43	92	0.6234	43	43	43	43
   56	59	59	59	59	59	59	0.1549	48	59	2021.01.04T09:30:02.000	09:30:02.000	59	94	0.428	59	59	59	59
   60	92	92	92	92	92	92	0.198	13	92	2021.01.04T09:30:02.000	09:30:02.000	92	87	0.2109	92	92	92	92
   57	41	41	41	41	41	41	0.0822	30	41	2021.01.04T09:30:02.000	09:30:02.000	41	32	0.2611	41	41	41	41
   7	61	61	61	61	61	61	0.7593	81	61	2021.01.04T09:30:02.000	09:30:02.000	61	15	0.7564	61	61	61	61
   ```
6. 当流数据订阅结束时，可以取消订阅并取消对流数据表的定义，取消流数据表定义需在对该表的订阅全部取消后进行。

   ```
   //取消订阅
   unsubscribeTable(tableName="tglobal", actionName="insertDB")
   //取消定义流数据表
   undef(`tglobal, SHARED)
   ```

Copyright

**©2025 浙江智臾科技有限公司 浙ICP备18048711号-3**
