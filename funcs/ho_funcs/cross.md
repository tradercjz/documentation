# cross

## 语法

`cross(func, X, [Y])`

或

`X <operator>:C Y`

或

`func:C(X, [Y])`

## 参数

* **func** 是一个二元函数。
* **X** 和 **Y** 可以是数据对、向量或矩阵。X 和 Y 可以有不同的数据形式和长度或维度。
* **Y** 是一个可选参数。如果Y没有指定，将会执行cross(func, X,
  X)，其中func必须是对称二元函数，如 [corr](../c/corr.md) 函数。

## 详情

将 X 和 Y 中元素的两两组合作为参数来调用函数。如果 X 或 Y 是矩阵，以列为单位遍历。以下是
`cross` 高阶函数的伪代码：

```
for(i:0~(size(X)-1)){

for(j:0~(size(Y)-1)){

  result[i,j]=<function>(X[i], Y[j]);

}

}

return result;
```

假设 X 有 m 个元素或 m 列，Y 有 n 个元素或 n 列，如果 func(X[i], Y[j]) 是标量，将返回一个 m×n
矩阵，如果 func(X[i], Y[j]) 是向量，将返回一个长度为 m 的元组，每个元素是一个长度为 n 的元组。

*pcross* 是并行计算版本的 *cross* 高阶函数。

## 例子

基于以下的 x 和 y 值，两个向量执行 `cross`：

```
x=1 2;
y=3 5 7;
x+:C y;
```

返回：

| lable | 3 | 5 | 7 |
| --- | --- | --- | --- |
| 1 | 4 | 6 | 8 |
| 2 | 5 | 7 | 9 |

```
cross(mul, x, y);
```

得到：

| lable | 3 | 5 | 7 |
| --- | --- | --- | --- |
| 1 | 3 | 5 | 7 |
| 2 | 6 | 10 | 14 |

```
cross(pow, x, y);
```

得到：

| lable | 3 | 5 | 7 |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 2 | 8 | 32 | 128 |

矩阵 m：

```
m = 1..6$2:3;
m;
```

| clo1 | col2 | col3 |
| --- | --- | --- |
| 1 | 3 | 5 |
| 2 | 4 | 6 |

矩阵 n：

```
n=1..4$2:2;
n;
```

| clo1 | col2 |
| --- | --- |
| 1 | 3 |
| 2 | 4 |

对矩阵 m 和 n 执行 `cross`：

```
cross(**, m, n);
```

得到：

| clo1 | col2 |
| --- | --- |
| 5 | 11 |
| 11 | 25 |
| 17 | 39 |

一个向量和一个矩阵执行 `cross`，返回一个矩阵：

```
def topsum(x,n){return sum x[0:n]};
a=1..18$6:3;
a;
```

得到：

| clo1 | col2 | col3 |
| --- | --- | --- |
| 1 | 7 | 13 |
| 2 | 8 | 14 |
| 3 | 9 | 15 |
| 4 | 10 | 16 |
| 5 | 11 | 17 |
| 6 | 12 | 18 |

```
b=2 4;
a topsum :C b;
```

| 2 | 4 |
| --- | --- |
| 3 | 10 |
| 15 | 34 |
| 27 | 58 |

一个向量和一个矩阵执行 `cross`，返回一个元组：

```
x=1 2
y=1..6$2:3
cross(add, x, y);
```

返回：(([2,3],[4,5],[6,7]),([3,4],[5,6],[7,8]))

```
x=1 2
y=1..6$3:2
cross(add, x, y);
```

返回：(([2,3,4],[5,6,7]),([3,4,5],[6,7,8]))

