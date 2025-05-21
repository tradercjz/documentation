# sample

## 语法

`sample(partitionCol, size)`

## 参数

* **partitionCol** 是字符串，表示分区列。
* **size** 是0到1之间的小数或大于0的整数。

## 详情

sample只能在where语句中使用，随机抽取分区表中的分区。

假设数据库有N个分区，如果 0<size<1，随机抽取int(N\*size)个分区，如果size是正整数，随机抽取size个分区。

## 例子

```
n=1000000
ID=rand(50, n)
x=rand(1.0, n)
t=table(ID, x)
db=database("dfs://rangedb1", RANGE, 0 10 20 30 40 50)
pt = db.createPartitionedTable(t, `pt, `ID)
pt.append!(t)
pt=loadTable(db,`pt);
```

pt有5个分区。如果需要随机抽取两个分区，可以使用下面的语句：

```
x = select * from pt where sample(ID, 0.4);

x = select * from pt where sample(ID, 2);
```

