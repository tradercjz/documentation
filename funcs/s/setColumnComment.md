# setColumnComment

## 语法

`setColumnComment(table, columnComments)`

## 参数

**table** 是一个分布式表或 mvcc 表。

**columnComments** 是一个字典，其中 key 表示表中的列，value 表示各列的注释。

## 详情

给分布式表或 mvcc 表的列添加注释。通过 [schema](schema.md) 函数可以查看各列的注释。

## 例子

```
n=1000000
sym=rand(`A`B`C`D`E`F,n)
date=rand(2019.06.01..2019.06.10,n)
open=rand(100.0,n)
high=rand(200.0,n)
close=rand(200.0,n)
pre_close=rand(200.0,n)
change=rand(100.0,n)
vol=rand(10000,n)
amount=rand(100000.0,n)
t=table(sym,date,open,high,close,pre_close,change,vol,amount);

db1=database("",VALUE,2019.06.01..2019.06.10)
db2=database("",VALUE,`A`B`C`D`E`F)
db=database("dfs://db1",COMPO,[db1,db2])
pt=db.createPartitionedTable(t,`pt,`date`sym).append!(t);

setColumnComment(pt,{sym:"股票代码",date:"交易日期",open:"开盘价",high:"最高价",close:"收盘价",pre_close:"昨收价",change:"涨跌额",vol:"成交量（手）",amount:"成交额（千元）"})
schema(pt).colDefs;
```

| name | typeString | typeInt | comment |
| --- | --- | --- | --- |
| sym | SYMBOL | 17 | 股票代码 |
| date | DATE | 6 | 交易日期 |
| open | DOUBLE | 16 | 开盘价 |
| high | DOUBLE | 16 | 最高价 |
| close | DOUBLE | 16 | 收盘价 |
| pre\_close | DOUBLE | 16 | 昨收价 |
| change | DOUBLE | 16 | 涨跌额 |
| vol | INT | 4 | 成交量（手） |
| amount | DOUBLE | 16 | 成交额（千元） |

```
id=`XOM`GS`AAPL
x=102.1 33.4 73.6
mt = mvccTable(id, x);
setColumnComment(mt, {id:"标识符"})
schema(mt).colDefs
```

| name | typeString | typeInt | extra | comment |
| --- | --- | --- | --- | --- |
| id | STRING | 18 |  | 标识符 |
| x | DOUBLE | 16 |  |  |

