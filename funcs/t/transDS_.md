# transDS!

## 语法

`transDS!(ds, tranFunc)`

## 参数

**ds** 是数据源或数据源列表。

**tranFunc** 是一个函数。它的参数必须是一个表。

## 详情

将函数应用到数据源。

## 例子

下例将分布式表 trades1 的时间列从 TIMESTAMP 类型转换成 NANOTIMESTAMP 类型后插入到分布式表
trades2中。

```
db=database("dfs://stock1",VALUE,`A`B`C`D)
n=200000
trade_time=2018.01.02T06:12:03.458+1..n
sym=rand(`A`B`C`D,n)
qty=rand(100.0,n)
price=rand(100.0,n)
t=table(trade_time,sym,qty,price)
trades1=db.createPartitionedTable(t,`trades1,`sym).append!(t);

ds=sqlDS(<select * from trades1>);

def convertNanotimestamp(t){
   return select nanotimestamp(trade_time), sym, qty, price from t
}

ds.transDS!(convertNanotimestamp);

db=database("dfs://stock2",VALUE,`A`B`C`D)
t=table(1:0,`trade_time`sym`qty`price,[NANOTIMESTAMP,SYMBOL,DOUBLE,DOUBLE])
trades2=db.createPartitionedTable(t,`trades2,`sym);

mr(ds,append!{trades2},,,false);

exec count(*) from trades2;
// output
200000
```

