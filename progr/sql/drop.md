# drop

drop 语句用于删除数据库或者数据表。建库建表语句请参考 [create](create.html)。

## 删除分布式数据库

### 语法

```
drop database [if exists] dbPath
```

### 参数

**dbPath** 数据库的路径。

### 例子

```
drop database if exists "dfs://test"
```

相关函数：[dropDatabase](../../funcs/d/dropDatabase.html), [existsDatabase](../../funcs/e/existsDatabase.html)

## 删除分布式表或维度表

### 语法

```
drop table [if exists] dbPath.tableName
```

### 参数

* **dbPath** 字符串，表示数据库的路径。
* **tableName** 字符串，分布式表和维度表的表名。

### 例子

```
drop table if exists "dfs://test"."pt"
```

相关函数：[dropTable](../../funcs/d/dropTable.html), [existsTable](../../funcs/e/existsTable.html)

## 删除 catalog 中的数据库

### 语法

```
drop table [if exists] catalog.schema
```

### 参数

**catalog.schema** 要删除数据库的结构为 catalog.schema 的字符串。若已设置当前的默认 catalog，则可忽略
catalog 前缀，直接传入 *schema。*

## 删除 catalog 中的数据表

### 语法

```
drop table [if exists] catalog.schema.tableName
```

### 参数

**catalog.schema.tableName**
要删除数据库的结构为“catalog.schema.tableName”的字符串。若已设置当前的默认 catalog，则可忽略 catalog
前缀，直接传入“*schema*.tableName”*。*

## 删除内存表

### 语法

```
drop table [if exists] tableName
```

### 参数

**tableName** 与内存表对象同名的字符串。

### 例子

```
drop table if exists "t"
```

相关函数：[undef](../../funcs/u/undef.html), [objs](../../funcs/o/objs.html)

