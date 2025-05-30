# shape

## 语法

`shape(X)`

## 参数

**X** 可以是标量、向量、矩阵或表。

## 详情

以数据对的形式返回标量、向量或矩阵的维度。

## 例子

标量的维度总是 1:1

```
shape 1;
// output
1:1

s;
```

向量的维度总是向量长度:1

```
shape 1 5 3 7 8;
// output
5:1
```

矩阵的维度

```
m=(5 3 1 4 9 10)$3:2;
m;
```

| #0 | #1 |
| --- | --- |
| 5 | 4 |
| 3 | 9 |
| 1 | 10 |

```
shape m;

// output
3 :2
```

表的维度

```
t=table(1 2 3 as x, 4 5 6 as y);
t;
```

| x | y |
| --- | --- |
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |

```
shape t;
// output
3 :2
```

