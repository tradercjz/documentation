# mutualInfo

## 语法

`mutualInfo(X, Y)`

别名：`infoGain`

## 参数

**X** 是一个标量、向量或矩阵。

**Y** 是一个标量、向量或矩阵。

*X* 和 *Y* 支持 Integral 和 symbol 类型。

## 详情

计算 *X* 和 *Y* 的互信息。

DolphinDB 使用以下公式计算互信息：

![img](../../images/mutualinfo.png)

若 *X* 或 *Y* 是矩阵，计算每列的互信息，返回一个向量。

注： 该公式计算时使用自然对数，若需要 *base* 为2或者10，直接以结果除以 log 2 或 log
10 即可。

## 例子

```
a = [NULL,4,NULL,NULL,-82,97,NULL,56,5,-92]
b = [NULL,53,NULL,18,97,-4,-73,NULL,NULL,24]
mutualInfo(a, b)
// output
2.302585

// 计算表中两列数据的互信息
t=table(take(1..10,10000000) as id, rand(10,10000000) as x, rand(10,10000000) as y);
mutualInfo(t.x, t.y)
// output
0.000004

m1 = 1..12$3:4
m2 = 1..3
mutualInfo(m1, m2)
// output
[1.0986,1.0986,1.0986,1.0986]
```

如果 *X* 是矩阵，*Y* 可以是标量、向量或者是与 *X* 行数相同的矩阵。返回结果是与
*X* 列数相同的向量。

```
m1 = 1..12$3:4
m2 = 1..3
mutualInfo(m1, m2)
// output
[1.0986,1.0986,1.0986,1.0986]
```

