# withNullFill

## 语法

`withNullFill(func, x, y, fillValue)`

## 详情

* 如果 x 与 y 中相同位置的元素只有一个为NULL，使用 fillValue 替换 NULL 值参与计算。
* 如果 x 和 y 相同位置的元素均为 NULL，返回 NULL。

## 参数

* **func** 是一个DolphinDB内置函数，须为双目运算符，例如+, -, \*, /, , %, pow, and, or 等。
* **x** 与 **y** 是向量或矩阵。
* **fillValue** 是一个标量。

## 例子

```
x = 0 1 NULL NULL 2
y = 1 NULL 2 NULL 3;
add(x,y);
// output
[1,,,,5]

withNullFill(add, x, y, 0);
// output
[1,1,2,,5]

m=matrix(1..5, y);
m;
```

| col1 | col2 |
| --- | --- |
| 1 | 1 |
| 2 |  |
| 3 | 2 |
| 4 |  |
| 5 | 3 |

```
add(x, m);
```

| col1 | col2 |
| --- | --- |
| 1 | 1 |
| 3 |  |
|  |  |
|  |  |
| 7 | 5 |

```
withNullFill(add, x, m, 0);
```

| col1 | col2 |
| --- | --- |
| 1 | 1 |
| 3 | 1 |
| 3 | 2 |
| 4 |  |
| 7 | 5 |

