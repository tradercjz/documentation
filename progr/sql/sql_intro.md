# SQL 语句

DolphinDB 中 SQL 语句的基本语法和用法

## DolphinDB 中的 SQL 语句

在以下内容中，您将了解到 SQL 语句在 DolphinDB
中访问、获取以及操作数据的使用方法。DolphinDB 的 SQL 格式与主流关系型数据库管理系统中的 SQL 语言十分相似，例如 MySQL, Oracle, SQL
Server 等。

## 语法

```
SELECT [top_clause] column_expressions
FROM table_name | table_expression
[WHERE filtering_conditions]
[grouping_clause [having_clause] | order_clause]
```

## 对 ANSI SQL 92 标准的支持

DolphinDB SQL 对 ANSI SQL 92 （下文简称 SQL-92）标准的支持历史如下：

* 支持 select, insert, update, delete
  语句分别用于查询、插入、更新、删除数据表中的记录。从 2.00.5 版本开始，DolphinDB 支持 create
  语句创建数据库（表），alter 语句为表增加列。从 2.00.10 版本开始，DolphinDB 的 SQL 关键字也可以采用全部大写的形式，例如
  SELECT, FROM, WHERE 等。
* 支持 where 条件。
* 支持分组 (group by) 和排序 (order by) 子句。
* 支持表连接：inner join, left join, left semijoin, full join。
* 从版本 2.00.10 开始，支持将 SQL 语句分成多行编写。但请注意以下2点：
  + 由 2 个单词组成的关键字（例如：order by, group by, context by,
    pivot by, union all, inner join, nulls first 等）不能在中间拆分换行。
  + 为字段或表指定别名时，若不使用关键字 as，则别名必须紧跟在原名称后面，不能换行。

## DolphinDB SQL 与 SQL 92 的区别

* 可在 SQL 查询中直接使用绝大部分函数。
* 其它区别如下表所示：

表 1. DolphinDB SQL与 SQL-92 的语法差异

| SQL-92 语法 | DolphinDB 语法 | 说明 |
| --- | --- | --- |
| N/A | `context by` | `context by` 是 DolphinDB 的独有的创新，它使得在处理各组内时间序列时非常方便。`context by`与`group by`相似，但是`group by`的结果为每一组返回一个标量值，而`context by`的结果为 每一组返回一个与组内记录数同样长度的向量。 |
| N/A | `pivot by` | `pivot by`将数据转换成二维视图。 |
| N/A | `cgroup by` |  |
| N/A | `map` | 将 SQL 语句在每个分区分别执行，然后将结果合并。 |
| N/A | `aj` | `asof`连接。它把左表中的每一条记录作为标准，并且检查右表中是否有匹配行。如果没有完全匹配的行，将会选择最近的行。如果有多个匹配行，将会选择最后一行。 |
| N/A | `wj`, `pwj` | 窗口连接和现行窗口连接。它们是`asof`连接的扩展。对于左表中的每一行，窗口连接把聚合函数应用到在滑动窗口中右表的行。如果右表中没有与窗口匹配的值，现行窗口连接会选择滑动窗口的前一个值，并对它使用聚合函数。 |

## SQL 方言兼容

自 2.00.10
版本开始，DolphinDB 实现了对 Oracle 和 MySQL 方言的兼容性。除了支持 SQL-92
语法外，还解决了因不同方言的扩展特性导致同名函数执行行为不一致的问题。通过会话（session）选择方言模式，便可在该会话中执行相应语言编写的脚本。目前有三种模式可选：DolphinDB,
Oracle 和 MySQL。

注：

* Oracle 和 MySQL 方言模式也能正确解析使用 DolphinDB 语言编写的脚本。
* 仅支持 Oracle 和 MySQL 的部分功能和函数，见下表：

| SQL 方言 | 支持功能 | 支持函数（无分大小写） |
| --- | --- | --- |
| Oracle | * 注释符：--、/\*\*/ * 字符串拼接符：|| | asciistr, concat, decode, instr, length, listagg, nvl, nvl2, rank, regexp\_like, replace, to\_char, to\_date, to\_number, trunc, wm\_concat 注： to\_char 只接收数值类型和 DATE, DATEHOUR, DATETIME 类型的参数。有关 Oracle SQL 函数的语法参考，请访问：[SQL Language Reference](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/Functions.html#GUID-D079EFD3-C683-441F-977E-2C9503089982) |
| MySQL |  | sysdate 注： 有关 MySQL 函数的语法参考，请访问：[MySQL :: MySQL 8.0 Reference Manual :: 12 Functions and Operators](https://dev.mysql.com/doc/refman/8.0/en/functions.html) |

