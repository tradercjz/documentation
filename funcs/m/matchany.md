# matchAny

## 语法

`matchAny(textCol, terms)`

## 参数

**textCol** 待查询的列，即 PKEY 存储引擎中设置了文本索引的列。

**terms** STRING 类型标量，用于指定待查询的词。若需查询多个词，可将它们用空格分隔写入该字符串中。

## 详情

该函数用于 SQL 语句的 WHERE 子句，针对 PKEY 存储引擎中设置文本索引的列进行文本匹配，返回符合任一指定匹配词的行。

## 例子

```
// 构造数据
stringColumn = ["There are some apples and oranges.","Mike likes apples.","Alice likes oranges.","Mike gives Alice an apple.","Alice gives Mike an orange.","John likes peaches, so he does not give them to anyone.","Mike, can you give me some apples?","Alice, can you give me some oranges?","Mike traded an orange for an apple with Alice."]
t = table([1,1,1,2,2,2,3,3,3] as id1, [1,2,3,1,2,3,1,2,3] as id2, stringColumn as remark)
if(existsDatabase("dfs://textDB")) dropDatabase("dfs://textDB")
db = database(directory="dfs://textDB", partitionType=VALUE, partitionScheme=[1,2,3], engine="PKEY")
pt = createPartitionedTable(dbHandle=db, table=t, tableName="pt", partitionColumns="id1",primaryKey=`id1`id2,indexes={"remark":"textindex(parser=english, full=false, lowercase=true, stem=true)"})
pt.tableInsert(t)

// 匹配包含 apple 或 orange 的行
select * from pt where matchAny(textCol=remark,terms="apple orange")
```

| id1 | id2 | remark |
| --- | --- | --- |
| 1 | 1 | There are some apples and oranges. |
| 1 | 2 | Mike likes apples. |
| 1 | 3 | Alice likes oranges. |
| 2 | 1 | Mike gives Alice an apple. |
| 2 | 2 | Alice gives Mike an orange. |
| 3 | 1 | Mike, can you give me some apples? |
| 3 | 2 | Alice, can you give me some oranges? |
| 3 | 3 | Mike traded an orange for an apple with Alice. |

