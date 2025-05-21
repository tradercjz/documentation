# loadTableBySQL

## 语法

`loadTableBySQL(sql)`

## 参数

**sql** 是表示 SQL 查询的元代码。它可以用 WHERE 子句来过滤分区或记录行，也可以用 SELECT
语句选择包括计算列在内的列，但不能包含 TOP 子句、GROUP BY 子句、 ORDER BY 子句、CONTEXT BY 子句和 LIMIT 子句。

## 详情

把分区表中满足 SQL 查询的记录行加载到内存中。返回的是分区的内存表，其分区机制与分区表一致。

注： 该函数用于根据 *sql*
创建分区内存表，存在一些查询限制。因此，在大数据量查询场景下，使用该函数可能会出现内存占用多的情况。建议在这种情况下直接使用 SQL 语句进行查询。

## 例子

```
n=1000000
t=table(rand('A'..'Z',n) as sym, 2000.01.01+rand(365,n) as date, 10.0+rand(2.0,n) as price1, 100.0+rand(20.0,n) as price2, rand(10,n) as qty1, rand(100,n) as qty2)

db = database("dfs://tradeDB", VALUE, 'A'..'Z')
trades=db.createPartitionedTable(t,`trades,`sym).append!(t)

sample=select * from loadTableBySQL(<select * from trades where date between 2000.03.01 : 2000.05.01>)
sample=select * from loadTableBySQL(<select sym, date, price1, qty1 from trades where date between 2000.03.01 : 2000.05.01>)

dates = 2000.01.16 2000.02.14 2000.08.01
st = sql(<select sym, date, price1, qty1>, trades, expr(<date>, in, dates))
sample = select * from loadTableBySQL(st)

colNames =`sym`date`qty2`price2
st= sql(sqlCol(colNames), trades)
sample = select * from loadTableBySQL(st)
```

