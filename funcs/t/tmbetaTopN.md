# tmbetaTopN

## 语法

`tmbetaTopN(T, X, Y, S, window, top, [ascending=true],
[tiesMethod='latest'])`

参数说明和窗口计算规则请参考：[tmTopN](../themes/tmTopN.md)

## 详情

在给定长度（以时间 *T* 衡量）的滑动窗口内，根据 *ascending* 指定的排序方式将 *X*
和 *Y* 按照 *S* 进行稳定排序后，取前 *top* 个元素，计算 *Y* 在 *X*
上的回归系数的最小二乘估计。

返回值：DOUBLE 类型向量。

## 例子

```
T=2023.01.03+1..7
X = [2, 1, 4, 3, 4, 3, 1]
Y=[1, 7, 8, 9, 0, 5, 8]
S = [5, 8, 1, , 1, 1, 3]  // S 中包含的空值不参与排序，对应位置的 X 和 Y不参与计算
tmbetaTopN(T,X,Y,S,6,4)
// output
[,-0.1666,0.1279,0.1279,-0.06,0.0853,-0.1871]

T=2023.01.03 2023.01.07 2023.01.08 2023.01.10 2023.01.11 2023.01.12
X=8 3 1 2 5 2
Y=1 7 8 9 0 5
S=1 5 2 3 1 1
t=table(T as time, X as val1, Y as val2, S as id)
select tmbetaTopN(time,val1,val2,id,4,3) as topN from t
```

| topN |
| --- |
|  |
|  |
| -2 |
| -0.5 |
| -0.3972 |
| -0.3442 |

相关函数：[tmbeta](tmbeta.md)

