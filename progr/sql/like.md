# like/LIKE

like/LIKE 用于测试列中的值是否与指定模式匹配。其功能与 [like](../../funcs/l/like.md) 函数相同。

## 语法

`match_expression [NOT] LIKE pattern`

## 参数

* `match_expression` 是一个列名或包含列名的表达式。
* `pattern` 是要在 match\_expression
  中搜索的字符串（区分大小写）。包含以下通配符：

  + % 匹配零个或多个字符的任何字符串。
  + ? 匹配任何单个字符。

## 用法

* 如果 match\_expression 与 pattern 匹配，则 like 返回 true；否则，like 返回
  false。
* 如果指定了 not，则取和 like 相反的结果。like 通常和 where
  子句搭配使用，根据指定的字段模式过滤数据。例如：使用 like 来查找以 “A“ 开头、以 “b“ 结尾、或包含 “Ca“ 的数据。
* LIKE 支持内存表和分布式表。

## 例子

```
t= table(`a1`a2`a3`b1`b2`b3`c1`c2 as id, 7 4 NULL 1 8 NULL 12 NULL as val)
select * from t where id like "a%"
//等价于 select * from t where like(id, "a%")
```

输出返回：

| id | val |
| --- | --- |
| a1 | 7 |
| a2 | 4 |
| a3 |  |

```
select * from t where id not like "a%"
```

输出返回：

| id | val |
| --- | --- |
| b1 | 1 |
| b2 | 8 |
| b3 |  |
| c1 | 12 |
| c2 |  |

