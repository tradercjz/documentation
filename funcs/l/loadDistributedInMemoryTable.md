# loadDistributedInMemoryTable

## 语法

`loadDistributedInMemoryTable(tableName)`

## 参数

**tableName** 字符串标量，表示分布式共享内存表的名称。

## 详情

返回分布式共享内存表的句柄。该函数只能在数据节点/计算节点上执行。

## 例子

```
pt = createDistributedInMemoryTable(`dt, `time`id`value, `DATETIME`INT`LONG, HASH, [INT, 2],`id)
time = take(2021.08.20 00:00:00..2021.08.30 00:00:00, 40);
id = 0..39;
value = rand(100, 40);
tmp = table(time, id, value);

pt = loadDistributedInMemoryTable(`dt)
pt.append!(tmp);
select * from pt;
```

相关函数：[dropDistributedInMemoryTable](../d/dropDistributedInMemoryTable.md), [createDistributedInMemoryTable](../c/createDistributedInMemoryTable.md)

