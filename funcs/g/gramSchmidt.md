# gramSchmidt

## 语法

`gramSchmidt(X, [normalize = false])`

## 参数

**X** 一个列满秩矩阵（每个列向量均线性无关），且不能包含空值。

**normalize** 可选参数，一个布尔值，表示是否输出标准正交矩阵，默认值为 false。

## 详情

将列满秩矩阵转换为一个列向量正交的矩阵。

返回值：DOUBLE 类型矩阵。

## 例子

```
x = matrix([2 3 5, 3 6 2, 8 3 6]);
gramSchmidt(x)

// output
col1    col2    col3
2.0000  1.2105  4.7932
3.0000  3.3157  -2.1968
5.0000  -2.4736 -0.5991

// 指定 normalize=true，则输出标准正交矩阵。
gramSchmidt(x, true)

// output
col1    col2    col3
0.3244      0.2808  0.9033
0.4867      0.7693  -0.414
0.8111      -0.5739 -0.1129

// 矩阵的列向量线性相关时，则会报错
x = matrix([1 4, 2 5, 3 6]);
gramSchmidt(x)

// output
vector set must be linearly independent
```

