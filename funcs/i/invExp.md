# invExp

## 语法

`invExp(mean, X)`

## 参数

**mean** 是指数分布的均值。

**X** 是0到1之间的浮点型标量或向量。

## 详情

返回指数分布的累计密度函数的逆函数值。

## 例子

```
invExp(1, [0.05 0.15 0.25 0.35]);
// output
[0.051293, 0.162519, 0.287682, 0.430783]

invExp(1, [0.1, 0.3, 0.5, 0.7, 0.9]);
// output
[0.105361, 0.356675, 0.693147, 1.203973, 2.302585]
```

