# alter

## 语法

```
alter table tableObj add columnName columnType;
alter table tableObj drop [column] columnName;
alter table tableObj rename [column] columnName to newColumnName;
```

## 详情

alter 语句用于向已有的表中添加、删除或重命名列。需要注意的是，TSDB 引擎仅支持 add 操作。

## 参数

* **tableObj** 可为任何形式的数据表，包括内存表、流数据表、分布式表。
* **colNames** 字符串标量，表示要添加的列的名称。
* **newColNames** 字符串标量，表示要修改的列的新名称。
* **colTypes** 表示数据类型的标量。

## 例子

```
if(existsDatabase("dfs://test")) dropDatabase("dfs://test")
create database "dfs://test" partitioned by VALUE(1..10), HASH([SYMBOL, 40]), engine='OLAP', atomic='TRANS', chunkGranularity='TABLE'

create table "dfs://test"."pt"(
        id INT,
        deviceId SYMBOL,
        date DATE[comment="time_col", compress="delta"],
        value DOUBLE,
        isFin BOOL
    )
partitioned by ID, deviceID

pt = loadTable("dfs://test", `pt)
alter table pt add location SYMBOL;
pt = loadTable("dfs://test", `pt)
pt.schema().colDefs

```

| name | typeString | typeInt | extra | comment |
| --- | --- | --- | --- | --- |
| id | INT | 4 |  |  |
| deviceId | SYMBOL | 17 |  |  |
| date | DATE | 6 |  | time\_col |
| value | DOUBLE | 16 |  |  |
| isFin | BOOL | 1 |  |  |
| location | SYMBOL | 17 |  |  |

```
alter table pt rename location to loc
pt = loadTable("dfs://test", `pt)
pt.schema().colDefs

```

| name | typeString | typeInt | extra | comment |
| --- | --- | --- | --- | --- |
| id | INT | 4 |  |  |
| deviceId | SYMBOL | 17 |  |  |
| date | DATE | 6 |  | time\_col |
| value | DOUBLE | 16 |  |  |
| isFin | BOOL | 1 |  |  |
| loc | SYMBOL | 17 |  |  |

```
alter table pt drop value
pt = loadTable("dfs://test", `pt)
pt.schema().colDefs

```

| name | typeString | typeInt | extra | comment |
| --- | --- | --- | --- | --- |
| id | INT | 4 |  |  |
| deviceId | SYMBOL | 17 |  |  |
| date | DATE | 6 |  | time\_col |
| isFin | BOOL | 1 |  |  |
| loc | SYMBOL | 17 |  |  |

**相关信息**

* [addColumn](../../funcs/a/addColumn.html "addColumn")
* [dropColumns!](../../funcs/d/dropColumns_.html "dropColumns!")
* [rename!](../../funcs/r/rename_.html "rename!")

