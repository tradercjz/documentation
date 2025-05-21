# distinct

添加在 select / exec 语句后，用于去除重复值并返回唯一值（distinct value）。支持在分布式查询中使用。

注：

* distinct 关键字和 distinct 函数不同，后者不保证返回结果的顺序，且默认将结果列的列名重命名为
  distinct\_colName。
* 暂不支持 distinct 与 group by, context by 或 pivot by 配合使用。

## 语法

```
select distinct col1, col2, ...
from table
```

## 例子

```
t = table(`a`a`b`b`a`a`a`b as sym, 1 3 1 4 5 2 1 3 as id, 1..8 as value)
select distinct id from t
```

| id |
| --- |
| 1 |
| 3 |
| 4 |
| 5 |
| 2 |

```
select distinct id, sym from t
```

| id | sym |
| --- | --- |
| 1 | a |
| 3 | a |
| 1 | b |
| 4 | b |
| 5 | a |
| 2 | a |
| 3 | b |

