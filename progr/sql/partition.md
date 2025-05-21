# partition

## 语法

`partition(partitionCol, keys)`

## 参数

* **partitionCol** 是字符串，表示分区列。对于组合分区，可以指定任意一个分区列。
* **keys** 可以是不含空值的标量/向量，表示需要选择的分区。不同分区方案对应的 keys 的选取规则如下：

| 分区方案 | keys |
| --- | --- |
| VALUE | 分区向量的一个元素 |
| RANGE | 每个分区的编号，从0开始 |
| HASH | 分区列的哈希余数 |
| LIST | 每个分区的编号，从0开始 |

注： *keys* 指定的分区需包含在分区表的分区范围内，否则会出现指定分区键超出范围的报错。

## 详情

用于选择分区表中的分区，以进行过滤。只能在 where 子句中使用。对于以哈希，列表或范围进行分区的分区表，通过此函数可以方便选取具体的分区。

## 例子

```
dbName="dfs://test_topic_partition"
if(existsDatabase(dbName)){
      dropDatabase(dbName)
}
db=database(dbName, LIST, ["A"+string(1..10), "A"+string(11..20), "A"+string(21..30)])
n=20
date=rand(2012.01.01..2012.01.10, n)
sym=rand("A"+string(1..30), n)
qty=rand(100, n)
t=table(date, sym, qty)
pt=db.createPartitionedTable(t, `pt, `sym).append!(t)
select * from pt where partition(sym, 0 1)
```

| date | sym | qty |
| --- | --- | --- |
| 2012.01.06 | A4 | 32 |
| 2012.01.03 | A10 | 34 |
| 2012.01.03 | A17 | 51 |
| 2012.01.04 | A14 | 47 |
| 2012.01.06 | A16 | 50 |
| 2012.01.04 | A15 | 56 |
| 2012.01.04 | A16 | 80 |
| 2012.01.02 | A11 | 69 |
| 2012.01.01 | A14 | 68 |

```
dbName="dfs://test_topic_partition"
if(existsDatabase(dbName)){
       dropDatabase(dbName)
}
db1=database("", HASH, [SYMBOL, 10])
db2=database("", LIST, ["A"+string(1..10), "B"+string(1..10), "C"+string(1..10)])
db=database(dbName, COMPO, [db1, db2])
n=20
id=symbol(string(rand(uuid(), n)))
sym=rand(["A"+string(1..10), "B"+string(1..10), "C"+string(1..10)].flatten(), n)
qty=rand(100, n)
t=table(id, sym, qty)
pt=db.createPartitionedTable(t, `pt, `id`sym).append!(t)
select * from pt where partition(id, 2 3), partition(sym, 1 2) order by id, sym, qty
```

| id | sym | vqty |
| --- | --- | --- |
| 19e8591f-8b7c-c611-bd3e-582d00a414430 | C6 | 69 |
| 2db9074a-0502-27ad-06d5-8d1bf3270245 | B4 | 2 |
| 73c1ae86-51c9-3e04-c1dd-6c4b62d8a129 | B9 | 65 |
| 99d78d5e-14bb-dc7e-7210-7bc5ad0cda5d | C10 | 11 |

