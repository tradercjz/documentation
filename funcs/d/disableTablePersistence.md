# disableTablePersistence

## 语法

`disableTablePersistence(table)`

## 参数

**table** 是一个表对象。

## 详情

停止把表持久化到磁盘，后续表更新的内容将不会持久化到磁盘上。

```
colName=["time","x"]
colType=["timestamp","int"]
t = streamTable(100:0, colName, colType);
share t as st
enableTablePersistence(table=st, cacheSize=1200000)

for(s in 0:200){
   n=10000
   time=2019.01.01T00:00:00.000+s*n+1..n
   x=rand(10.0, n)
   insert into st values(time, x)
}
disableTablePersistence(st);
```

相关命令：[enableTablePersistence](../e/enableTablePersistence.md), [clearTablePersistence](../c/clearTablePersistence.md)

