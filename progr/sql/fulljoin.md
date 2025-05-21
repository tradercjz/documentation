# full join/full outer join

## 语法

```
fj(leftTable, rightTable, matchingCols, [rightMatchingCols])
```

## 参数

* **leftTable** 和 **rightTable** 是连接的表。
* **matchingCols** 是表示连接列的字符串标量或向量。
* **rightMatchingCols** 是表示右表连接列的字符串标量或向量。当 *leftTable* 和
  *rightTable* 至少有一个连接列不同时，必须指定
  *rightMatchingCols*。返回结果中的连接列与左表的连接列名称相同。

## 兼容 SQL 的语法

```

select column_name(s)
from leftTable full [outer] join rightTable
on leftTable.matchingCol=rightTable.rightMatchingCol
```

**注意**：

兼容 SQL 语法的 full join 不支持以下几点：

1. 如果有多个连接列，必须使用 and 连接。
2. 不能和 update 关键字一起使用。
3. 若 *leftTable* 不是分布式表，则其 *rightTable* 也不能是分布式表。

## 详情

完全连接除了返回等值连接的结果集之外，还会返回左表或右表中不匹配的行。

## 例子

```
t1= table(1 2 3 3 as id, 7.8 4.6 5.1 0.1 as value);
t1;
```

| id | value |
| --- | --- |
| 1 | 7.8 |
| 2 | 4.6 |
| 3 | 5.1 |
| 3 | 0.1 |

```
t2 = table(5 3 1 as id,  300 500 800 as qty);
t2;
```

| id | qty |
| --- | --- |
| 5 | 300 |
| 3 | 500 |
| 1 | 800 |

```
fj(t1, t2, `id);
```

| id | value | t2\_id | qty |
| --- | --- | --- | --- |
| 1 | 7.8 | 1 | 800 |
| 2 | 4.6 |  |  |
| 3 | 5.1 | 3 | 500 |
| 3 | 0.1 | 3 | 500 |
|  |  | 5 | 300 |

```
select * from fj(t1, t2, `id) where id=3;
//等价于 select * from t1 full join t2 on t1.id=t2.id where id=3
```

| id | value | t2\_id | qty |
| --- | --- | --- | --- |
| 3 | 5.1 | 3 | 500 |
| 3 | 0.1 | 3 | 500 |

