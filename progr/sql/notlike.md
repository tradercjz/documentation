# notLike/NOTLIKE

NOTLIKE 是与 LIKE 相反的操作，用于确定特定字符串是否与指定模式不匹配。其功能与 [notLike](../../funcs/n/notlike.md) 函数、NOT LIKE 相同。notLike 支持内存表和分布式表。

## 语法

`match_expression notLike pattern`

## 参数

**match\_expression**任何有效的字符串类型的表达式。

**pattern** 要在 match\_expression 中搜索并且可以包含有效通配符的字符串（区分大小写）。有效通配符如下：

* % 匹配零个或多个字符的任何字符串。
* ? 匹配任何单个字符。

## 用法

* 如果 match\_expression 与 pattern 不匹配，则 notLike 返回 true；否则，notLike返回 false。
* notLike 通常和 where 子句搭配使用，根据指定的模式过滤数据。例如：使用 notLike 来查找不以 “A“ 开头、不以 “b“ 结尾、或不包含
  “Ca“ 的数据。

## 例子

```
t= table(`a1`a2`a3`b`b2`b3`ca1`ca2 as id, 7 4 NULL 1 8 NULL 12 NULL as val)
select * from t where id notLike "a%"
// 等价于 select * from t where id not like "a%"
```

| id | val |
| --- | --- |
| b | 1 |
| b2 | 8 |
| b3 |  |
| ca1 | 12 |
| ca2 |  |

查询 id 列中不以 “b” 结尾的记录

```
select * from t where id notLike "%b"
```

| id | val |
| --- | --- |
| a1 | 7 |
| a2 | 4 |
| a3 |  |
| b2 | 8 |
| b3 |  |
| ca1 | 12 |
| ca2 |  |

查询 id 列中不包含字符串 “a” 的记录

```
select * from t where id notLike "%a%"
```

| id | val |
| --- | --- |
| b | 1 |
| b2 | 8 |
| b3 |  |

