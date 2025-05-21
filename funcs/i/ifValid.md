# ifValid

## 语法

`ifValid(X,Y)`

## 参数

**X** 可以是标量、数据对、向量或矩阵。

**Y** 可以是标量、数据对、向量或矩阵。

*X* 和 *Y* 必须具有相同的数据类型。

## 详情

判断 *X* 是否非空。若为非空，则返回 *X* 的值，若为 NULL，则返回 *Y* 的值。

## 例子

```
x = take(1..5 join NULL 6,7)
y = 1..7
ifValid(x,y)
// output
[1,2,3,4,5,6,6]
x1 = int(take(1..5 join int(),6))$2:3
y1 = int(take(100,6))$2:3
ifValid(x1,y1)
```

| col1 | col2 | col3 |
| --- | --- | --- |
| 1 | 3 | 5 |
| 2 | 4 | 100 |

若 *X* 为向量，*Y* 为 n 行 m 列的矩阵，则 *X* 的长度为 n\*m

```
m=int(take(1..4 join NULL 8,6))
ifValid(m,y1)
// output
[1,2,3,4,100,8]
```

