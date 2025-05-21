# matchPhraseInfix

## 语法

`matchPhraseInfix(textCol, suffix, phrase, prefix)`

## 参数

**textCol** 待查询的列，即 PKEY 存储引擎中设置了文本索引的列。

**suffix** STRING 类型标量，用于指定待查询的后缀。

**phrase** STRING 类型标量，用于指定待查询的短语。

**prefix** STRING 类型标量，用于指定待查询的前缀。

## 详情

该函数用于 SQL 语句的 WHERE 子句，针对 PKEY
存储引擎中设置文本索引的列进行文本匹配，若包含特定短语，且短语前是某一特定后缀的单词，短语后是某一特定前缀的单词，则该行匹配成功。返回所有匹配成功的行。

## 例子

```
// 构造数据
stringColumn = ["There are some apples and oranges.","Mike likes apples.","Alice likes oranges.","Mike gives Alice an apple.","Alice gives Mike an orange.","John likes peaches, so he does not give them to anyone.","Mike, can you give me some apples?","Alice, can you give me some oranges?","Mike traded an orange for an apple with Alice."]
t = table([1,1,1,2,2,2,3,3,3] as id1, [1,2,3,1,2,3,1,2,3] as id2, stringColumn as remark)
if(existsDatabase("dfs://textDB")) dropDatabase("dfs://textDB")
db = database(directory="dfs://textDB", partitionType=VALUE, partitionScheme=[1,2,3], engine="PKEY")
pt = createPartitionedTable(dbHandle=db, table=t, tableName="pt", partitionColumns="id1",primaryKey=`id1`id2,indexes={"remark":"textindex(parser=english, full=false, lowercase=true, stem=true)"})
pt.tableInsert(t)

// 匹配包含单词 give，且 give 前为 ke 后缀单词, 后为 al 前缀单词的行
select * from pt where matchPhraseInfix(remark,"ke","give","al")
```

| id1 | id2 | remark |
| --- | --- | --- |
| 2 | 1 | Mike gives Alice an apple. |

