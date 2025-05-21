# sqlDelete

## 语法

`sqlDelete(table, [where], [from])`

## 参数

**table** 可以是内存表，亦可为分布式表。

**where** 是元代码，表示 where 条件。

**from** 是元代码，表示 from 子句。

## 详情

动态生成 SQL delete 语句的元代码。若需执行生成的元代码，请配合使用 [eval](../e/eval.md) 函数。

## 例子

例1. 删除内存表记录

```
t1=table(`A`B`C as symbol, 10 20 30 as x)
sqlDelete(t1, <symbol=`C>).eval()
t1;
```

| symbol | x |
| --- | --- |
| A | 10 |
| B | 20 |

例2. 删除分区表记录

```
if(existsDatabase("dfs://db1")){
    dropDatabase("dfs://db1")
}

n=1000000
t=table(take(`A`B`C`D,n) as symbol, rand(10.0, n) as value)
db = database("dfs://db1", VALUE, `A`B`C`D)
Trades = db.createPartitionedTable(t, "Trades", "symbol")
Trades.append!(t)
select count(*) from Trades;

// output: 1000000

Trades=loadTable("dfs://db1", "Trades")
sqlDelete(Trades, <symbol=`A>).eval()
select count(*) from Trades;

// output: 750000
```

例3. 结合表连接删除记录

```
t1 = table(1..5 as id, [1,2,2,1,1] as flag)
t2 = table(3..7 as id, [100,200,100,150,100] as profit)
sqlDelete(table=t2, where=<flag=1>, from=<ej(t2,t1,`id)>).eval()
t2
```

| id | profit |
| --- | --- |
| 3 | 100 |
| 6 | 150 |
| 7 | 100 |

