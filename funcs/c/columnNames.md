# columnNames

## 语法

`columnNames(X)`

## 参数

**X** 可以是矩阵或表。

## 详情

返回 *X* 的列名的向量。参见相关函数：[rowNames](../r/rowNames.md)。

## 例子

```
x=1..6$2:3;
x;
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 1 | 3 | 5 |
| 2 | 4 | 6 |

```
x.rename!(`a`b`c);
```

| a | b | c |
| --- | --- | --- |
| 1 | 3 | 5 |
| 2 | 4 | 6 |

```
x.columnNames();
// output
["a","b","c"]

t = table(1 2 3 as id, 4 5 6 as value, `IBM`MSFT`GOOG as name);
t;
```

| id | value | name |
| --- | --- | --- |
| 1 | 4 | IBM |
| 2 | 5 | MSFT |
| 3 | 6 | GOOG |

```
columnNames t;
// output
["id","value","name"]

t[t.columnNames().tail()];
// output
["IBM","MSFT","GOOG"]
// 获取表的最后一列，返回的结果是一个向量
```

