# byColumn

## 语法

`byColumn(func, X, [Y])`

或

`func:V(X)`

或

`func:V(X, [Y])`

## 参数

* **func**
  一个单目函数，支持以部分应用的形式传入。该函数可以是向量函数（输入与输出为等长的向量），亦可为聚合函数。
* **X** 一个矩阵、表、元组、数组向量、列式元组。
* **Y** 矩阵、表、元组、数组向量、列式元组。

## 详情

*func* 为单目函数时，对 *X* 的每一列应用指定函数；*func* 为双目函数时，对 *X* 和 *Y* 的每列执行 func(Xi, Yi)
。

同时指定 X 和 Y 时，则对 X 和 Y 的每列执行 func(Xi, Yi) 。

支持在响应式状态引擎中使用 `byColumn` 函数。

**计算规则**：

* 如果 *X/Y* 是矩阵、表或元组，byColumn 对 X/Y 的每一列数据应用指定的函数。
* 如果 X/Y 是数组向量或列式元组：byColumn 首先将对象转置，然后对转置后的对象的每一行应用指定函数。

  + 当 *func* 是向量函数时，byColumn 会把 *func* 的计算结果转置后输出。
  + 当 *func* 是聚合函数时，输出结果是一个向量。特别地，当 *func* 是以下聚合函数时，由于 byColumn
    不对 X/Y 进行转置，从而提高了计算性能：sum, sum2, avg, min, max, count, imax, imin,
    imaxLast, iminLast, prod, std, stdp, var, varp, skew, kurtosis, any,
    all, corr, covar, wavg, wsum, beta, euclidean, dot, tanimoto

**返回值**：

* 当 *func* 是聚合函数时，

  + 如果 *X/Y* 是矩阵、数组向量或列式元组，则输出结果是一个向量。向量的长度与 *X/Y* 的列数相同。
  + 如果 *X/Y* 是元组，则输出结果是一个元组。
  + 如果 *X/Y* 是表，则输出结果是一个表。
* 当 *func* 是向量函数时，输出结果的形式、维度和 *X/Y* 的形式、维度相同。

## 计算规则

* 如果 *X/Y* 是矩阵、表或元组，byColumn 对 X/Y 的每一列数据应用指定的函数。
* 如果 X/Y 是数组向量或列式元组：byColumn 首先将对象转置，然后对转置后的对象的每一行应用指定函数。

  + 当 *func* 是向量函数时，byColumn 会把 *func* 的计算结果转置后输出。
  + 当 *func* 是聚合函数时，输出结果是一个向量，无需进行转置操作。特别地，当 *func*
    是以下聚合函数时，byColumn 进行了优化，不会对 *X*/*Y*
    进行上步的转置操作，从而提高了计算性能：sum, sum2, avg, min, max, count, imax, imin,
    imaxLast, iminLast, prod, std, stdp, var, varp, skew, kurtosis, any,
    all, corr, covar, wavg, wsum, beta, euclidean, dot, tanimoto。

## 例子

对于不支持矩阵运算的单目向量函数，通过 `byColumn` 进行按列计算，等效于 `each`。

```
def myvfunc(x): var(x).log()
m = matrix(1.1 2.3 2.1 3.5 4.2, 3.3 2.5 4.2 5.1 0, -1 3.3 2 1.7 2.3)
byColumn(myvfunc, m)
```

输出返回： [0.3974329364109,1.334211281249665,0.945072533299607]

传入多元函数时，需要把该函数的其他参数通过部分应用进行固定，然后传入 `func`。

```
byColumn(autocorr{,2},m)
```

返回：[-0.05,-0.28,-0.06]

输出返回：

```
col1 col2 col3
3.1  5.3  1
4.3  4.5  5.3
4.1  6.2  4
5.5  7.1  3.7
6.2  2    4.3
```

```
byColumn(add{1 2 3 4 5}, m)
```

输出返回：

```
col1 col2 col3
2.1  4.3  0
4.3  4.5  5.3
5.1  7.2  5
7.5  9.1  5.7
9.2  5    7.3
```

`func` 是一个自定义函数。

```
def my_func(x){
   return iif(x > 0, 1, -1)
}
m = matrix(3 -6 5 0, 2 -9 -4 5)
byColumn(my_func, m)
```

输出返回：

```
col1 col2
 1    1
-1   -1
 1    -1
-1    1
```

`func` 是一个嵌套函数。

```
m = matrix(1 5 3 , 7 5 2)
byColumn(accumulate{def (x, y):iif(x > 5, y-1, y+1), ,1}, m)
```

输出返回：

```
col1 col2
2    8
6    4
2    3
```

入参是矩阵：

```
m=matrix([1 3 4 2,1 2 2 1])
max:V(m)
[4,2]

cummax:V(m)

col1	col2
1	1
3	2
4	2
4	2

n=matrix([11 5 9 2,8 5 3 2])
corr:V(m,n)
[-0.09,-0.21]

```

入参是表：

```
qty1 = 2200 1900 2100 3200 6800 5400 1300 2500 8800
qty2 = 2100 1800  6800 5400 1300 2400 8500 4100 3200
t = table(qty1, qty2);
max:V(t)

qty1	qty2
8,800	8,500

cummax:V(t)

qty1	qty2
2,200	2,100
2,200	2,100
2,200	6,800
3,200	6,800
6,800	6,800
6,800	6,800
6,800	8,500
6,800	8,500
8,800	8,500

qty3 = 7800 5400 5300 2500 1800 2200 3900 3100 1200
qty4 = 3200 2800 6400 8300 2300 3800 2900 1600 2900
t1 = table(qty3, qty4);

corr:V(t,t1)

qty1	qty2
-0.7267	0.4088

```

入参是元组：

```
tp=[1 3 4 2,1 2 2 1]
sum:V(tp)
(10,6)

cummax:V(tp)
([1,3,4,4],[1,2,2,2])

tp1=[11 23 14 21,10 12 32 21]

corr:V(tp,tp1)
(0.25,0.37)
```

入参是数组向量：

```
a=array(INT[], 0, 10).append!([1 2 3, 4 5 4, 6 7 8, 1 9 10]);
sum:V(a)
[12,23,25]

cummax:V(a)
[[1,2,3],[4,5,4],[6,7,8],[6,9,10]]

b=array(DOUBLE[], 0, 10).append!([11.8 21.2 23.9, 83.3 90.2 78.2, 86.5 52 36.5, 10.1 12.4 16.8])
corr:V(a,b)

[0.95,-0.13,-0.46]
```

入参是列式元组：

```
ctp=[1 3 4 2,1 2 2 1]
ctp.setColumnarTuple!()
sum:V(ctp)
[2,5,6,3]

cummax:V(ctp)
([1,3,4,2],[1,3,4,2])

ctp1=[11 23 14 21,10 12 32 21]
ctp1.setColumnarTuple!()

corr:V(ctp,ctp1)
[,1,-1,]
```

**相关信息**

* [byRow](byRow.html "byRow")

