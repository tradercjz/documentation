# with

`with` 语句又称为子查询重构语句，其将子查询的结果保存在一个临时表变量中。

通过 `with` 语句编写 SQL 脚本，有以下优势：

* 将复杂的 SQL 脚本改写为 `with` 语句，既增强了代码的可读性，也减轻了脚本的编写负担。
* 使用临时表存储每个子查询的结果，只做一次查询，后续 SQL 语句可反复使用该临时表数据，提升了查询性能。
* 子查询结果保存到临时表中，当语句执行完后即被释放，降低了变量定义的空间开销。

注：支持在分布式查询中使用。

## 语法

```
    with table_name_1[(colNames..)] as (select_statement_1),
    table_name_2[(colNames..)] as (select_statement_2),
    ...
    table_name_n[(colNames..)] as (select_statement_n)
    final_select_statement
```

注：

* `with` 后的子查询语句不能以";"结尾。
* 可以写多条子查询，每条子查询间使用逗号（","）分隔。最后一个子查询语句后不加逗号。
* 支持在 *table\_name* 后指定参数，用于对 as 后的结果列进行重命名。
* 不支持在自定义函数中使用 `with as` 语法。

## 参数

* **table\_name** 临时表名称。
* **colNames..** 用于重命名 `as` 返回结果列。注意 *colNames*
  是一个变量而不是字符串。*colNames* 的数量需要和 `as` 返回结果的列数一致。
* **select\_statement**
  `select` 语句或者 `exec` 语句。

## 例子

```
t1 = table(1 3 4 5 8 as id, 2 2.5 2.4 2.2 2.9 as val)
t2 = table(1 2 4 6 8 as id, `a`a`b`d`c as sym)

with tmp as (select * from t1 inner join t2 on t1.id=t2.id) select count(*) from tmp
3
```

