# union/union all

用于合并两个或多个 select / exec 查询的结果集。union 会将重复的记录删去，union all 保留所有记录。支持在分布式查询中使用。

**注意**：

* union / union all 连接的 select / exec 语句必须查询相同数量的列，且对应列的类型必须能够相互转换；
* 第一个查询的列名和类型决定了结果集的列名和列类型。

## 例子

```
t1= table(1 2 3 3 as id, 7.8 4.6 5.1 0.1 as v1)
t2 = table(5 3 3 as id,  3.2 5.1 0.1 as v2);
select * from t1 union select * from t2
```

| id | v1 |
| --- | --- |
| 1 | 7.8 |
| 2 | 4.6 |
| 3 | 5.1 |
| 3 | 0.1 |
| 5 | 3.2 |

```
select * from t1 union all select * from t2
```

| id | v1 |
| --- | --- |
| 1 | 7.8 |
| 2 | 4.6 |
| 3 | 5.1 |
| 3 | 0.1 |
| 5 | 3.2 |
| 3 | 5.1 |
| 3 | 0.1 |

```
t3 = table(3 3 4 as id,  5.1 0.2 1.1 as v3);
(select * from t1 where id=3) union all (select * from t2 where id=3) union (select * from t3 where id=3)
```

| id | v1 |
| --- | --- |
| 3 | 5.1 |
| 3 | 0.1 |
| 3 | 0.2 |

Copyright

**©2025 浙江智臾科技有限公司 浙ICP备18048711号-3**
