# objs

## 语法

`objs([shared=false])`

## 参数

**shared** 布尔值，默认为 false。

* false：返回当前会话中所有变量的信息；
* true：返回当前会话中所有变量的信息以及所有会话共享的变量信息；

## 详情

用于获取内存中缓存的各变量的内存占用情况等信息。返回一个表，它具有以下几列：

* name: 变量名。
* type: 变量的数据类型。
* form: 变量的数据形式。
* rows:

  + 若 form 为向量/字典/集合，则返回所有元素（包含 NULL）的个数
  + 若 form 为矩阵/表，则返回它们的行数
* columns:

  + 若 form 为向量/字典/集合，则返回 1
  + 若 form 为矩阵/表，则返回它们的列数
* bytes: 变量占用的内存大小，单位为字节
* shared: 是否为共享变量
* extra: 分布式表的逻辑路径，格式为
  "dfs://dbName/tableName"
* owner：共享变量的创建者。只有设置 shared=true 时才会显示该字段。对于本地变量，此字段值为空。

注意，该函数不返回函数定义。我们应该用 defs 检查函数定义，或通过 [memSize](../m/memSize.md) 查看函数定义的内存占用。

## 例子

```
// 创建分布式数据库
if(existsDatabase("dfs://listdb")){
        dropDatabase("dfs://listdb")
}
n=1000000
ticker = rand(`MSFT`GOOG`FB`ORCL`IBM,n);
ticker[0..5]
x=rand(1.0, n)
t=table(ticker, x)
db=database(directory="dfs://listdb", partitionType=HASH, partitionScheme=[STRING, 5])
pt=db.createPartitionedTable(t, `pt, `ticker)
pt.append!(t)

// 共享内存表
time = take(2021.08.20 00:00:00..2021.08.30 00:00:00, 40);
id = 0..39;
value = rand(100, 40);
tmp = table(time, id, value);
share tmp as st

// 创建 set
s = set([1,2,3,4,5])

// 创建 dict
x=1 2 3
y=4.5 7.8 4.3
z=dict(x,y);

// 创建 matrix
m = matrix(1 2 3, 4 5 6)

// 创建 pair
p = 1:2
```

```
objs(true)
```

| name | type | form | rows | columns | bytes | shared | extra | owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| n | INT | SCALAR | 1 | 1 | 16 | false |  |  |
| ticker | SYMBOL | VECTOR | 1,000,000 | 1 | 4,000,000 | false |  |  |
| x | INT | VECTOR | 3 | 1 | 12 | false |  |  |
| t | BASIC | TABLE | 1,000,000 | 2 | 12,000,312 | false |  |  |
| db | HANDLE | SCALAR | 1 | 1 | 24 | false |  |  |
| pt | ALIAS | TABLE | 0 | 2 | 12,000,000 | false | dfs://listdb/pt |  |
| time | DATETIME | VECTOR | 40 | 1 | 160 | false |  |  |
| id | INT | VECTOR | 40 | 1 | 160 | false |  |  |
| value | INT | VECTOR | 40 | 1 | 160 | false |  |  |
| tmp | BASIC | TABLE | 40 | 3 | 832 | false |  |  |
| s | INT | SET | 5 | 1 | 28 | false |  |  |
| y | DOUBLE | VECTOR | 3 | 1 | 24 | false |  |  |
| z | DOUBLE | DICTIONARY | 3 | 1 | 199 | false |  |  |
| m | INT | MATRIX | 3 | 2 | 24 | false |  |  |
| p | INT | PAIR | 2 | 1 | 8 | false |  |  |
| st | BASIC | TABLE | 40 | 3 | 832 | true |  | admin |

