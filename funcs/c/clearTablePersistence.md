# clearTablePersistence

## 语法

`clearTablePersistence(table)`

## 参数

**table** 是一个表。

## 详情

停止将流数据表持久化到磁盘，然后删除磁盘上表的内容，但仍然保留表的结构。

## 例子

```
colName=["time","x"]
colType=["timestamp","int"]
t = streamTable(100:0, colName, colType);
enableTableShareAndPersistence(table=t, tableName=`st, cacheSize=1200000)
go;
```

```
for(s in 0:200){
    n=10000
    time=2019.01.01T00:00:00.000+s*n+1..n
    x=rand(10.0, n)
    insert into st values(time, x)
}
clearTablePersistence(st);
```

相关函数：[enableTablePersistence](../e/enableTablePersistence.md), [disableTablePersistence](../d/disableTablePersistence.md)

