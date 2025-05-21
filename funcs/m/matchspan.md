# matchSpan

## 语法

`matchSpan(textCol, span, slop)`

## 参数

**textCol** 待查询的列，即 PKEY 存储引擎中设置了文本索引的列。

**span** STRING 类型标量，用于指定待查询的短语。

**slop** 非负整数，表示用户输入的词距。匹配时，若短语前、后或短语中有不多于 *slop* 个其他词语，仍视作匹配成功。

## 详情

该函数用于 SQL 语句的 WHERE 子句，针对 PKEY 存储引擎中设置文本索引的列进行文本匹配，返回包含指定短语的行。

## 例子

```
// 构造数据
stringColumn = ["There are some apples and oranges.","Mike likes apples.","Alice likes oranges.","Mike gives Alice an apple.","Alice gives Mike an orange.","John likes peaches, so he does not give them to anyone.","Mike, can you give me some apples?","Alice, can you give me some oranges?","Mike traded an orange for an apple with Alice."]
t = table([1,1,1,2,2,2,3,3,3] as id1, [1,2,3,1,2,3,1,2,3] as id2, stringColumn as remark)
if(existsDatabase("dfs://textDB")) dropDatabase("dfs://textDB")
db = database(directory="dfs://textDB", partitionType=VALUE, partitionScheme=[1,2,3], engine="PKEY")
pt = createPartitionedTable(dbHandle=db, table=t, tableName="pt", partitionColumns="id1",primaryKey=`id1`id2,indexes={"remark":"textindex(parser=english, full=false, lowercase=true, stem=true)"})
pt.tableInsert(t)

// 匹配包含短语 mike apple 的行，且允许短语前后或内部有小于等于3个其他词汇（不包括停止词）
select * from pt where matchSpan(remark, "mike apple", 2)
```

| id1 | id2 | remark |
| --- | --- | --- |
| 1 | 2 | Mike likes apples. |
| 2 | 1 | Mike gives Alice an apple. |
| 3 | 3 | Mike traded an orange for an apple with Alice. |

