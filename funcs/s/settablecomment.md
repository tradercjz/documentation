# setTableComment

## 语法

`setTableComment(table, comment)`

## 参数

**table** 是一个分布式表。

**comment** 字符串标量，表示表注释。长度不可超过 4096 字节。

## 详情

给分布式表添加注释，表注释可通过函数 [schema](schema.html) 查看。

## 例子

```
// 创建分布式表
db = database(directory="dfs://testDB", partitionType=VALUE, partitionScheme=1..5)
schemaTB = table(1..5 as id, take(`A`B`C,5) as sym, rand(10.0,5) as price)
pt = db.createPartitionedTable(table=schemaTB, tableName="pt", partitionColumns="id")

// 设置表的注释
setTableComment(table=pt, comment="my first pt")

// 通过 schema 查看
schema(pt)["tableComment"]
// output：'my first pt'
```

