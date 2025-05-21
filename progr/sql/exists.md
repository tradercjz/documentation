# exists

和 where 子句搭配使用，通过子查询过滤外查询。

## 语法

```
where [not] exists(subquery)
```

subquery：select / exec 语句，其过滤条件中可以包含外查询的字段。

## 详情

* 若子查询涉及到外查询的字段，即相关子查询：

  + 先执行一遍外查询并缓存查询结果。
  + 然后循环将外查询的每一行结果作为子查询的条件进行查询：

    - 若子查询有返回结果，则 exists 子句返回 true，外查询的该行结果将作为最终结果输出；
    - 否则 exists 子句返回 false，改行结果不输出。
* 若子查询和外查询无关，即不相关子查询，则 exists 将根据下述规则进行计算：

  + 如果子查询结果集非空，输出所有外查询结果。
  + 如果子查询结果集为空，则外查询结果为空。 not exists 的计算逻辑和 exists 相反。

**注意**：暂不支持在分布式查询中使用。

## 例子

```
t1 = table(`a`b`c`a`e`f as sym, 3.1 2.9 3.0 2.8 3.2 2.9 as val)
t2 = table(`a`b`c as sym, 0 1 -1 as flag)
```

查询1：相关子查询

```
select * from t1 where exists(select * from t2 where t1.sym in t2.sym)
```

| sym | val |
| --- | --- |
| a | 3.1 |
| b | 2.9 |
| c | 3 |
| a | 2.8 |

```
select * from t1 where not exists(select * from t2 where t1.sym in t2.sym)
```

| sym | val |
| --- | --- |
| e | 3.2 |
| f | 2.9 |

查询2：不相关子查询

```
select * from t1 where exists(select * from t2 where flag >= 0)
```

| sym | val |
| --- | --- |
| a | 3.1 |
| b | 2.9 |
| c | 3 |
| a | 2.8 |
| e | 3.2 |
| f | 2.9 |

```
select * from t1 where not exists(select * from t2 where flag >= 0)
    //返回值为空
```

查询3：子查询无返回结果

```
select * from t1 where exists(select * from t2 where sym=`e)
    //返回值为空
select * from t1 where not exists(select * from t2 where sym=`e)
```

| sym | val |
| --- | --- |
| a | 3.1 |
| b | 2.9 |
| c | 3 |
| a | 2.8 |
| e | 3.2 |
| f | 2.9 |

