# tmkurtosisTopN

## 语法

`tmkurtosisTopN(T, X, S, window, top, [biased=true], [ascending=true],
[tiesMethod='latest'])`

参数说明和窗口计算规则请参考：[tmTopN](../themes/tmTopN.md)

## 参数

**biased** 是一个布尔值，表示是否是有偏估计。默认值为 true，表示有偏估计。

## 详情

在给定长度（以时间 *T* 衡量）的滑动窗口内，根据 *ascending* 指定的排序方式将 *X*
按照 *S* 进行稳定排序后，计算前 *top* 个元素的峰度。

## 返回值

DOUBLE 类型向量。

## 例子

```
T=2023.01.03+1..10
X = [2, 1, 4, 3, 4, 3, 1, 5, 8, 2]
S = [5, 8, 1, , 1, 1, 3, 2, 5 ,1]  //S 中包含的空值不参与排序，对应位置的 X 不参与计算
tmkurtosisTopN(T,X,S,6,4)
// output
[,,1.5,1.5,1.2798,1.628,2,2,1.8457,1.64]

T=2023.01.03 2023.01.07 2023.01.08 2023.01.10 2023.01.11 2023.01.12 2023.01.13 2023.01.14 2023.01.15 2023.01.16
X=8 3 1 2 5 2 5 4 2 6
S=1 5 2 3 1 1 2 4 5 3
t=table(T as time, X as val, S as id)
select tmkurtosisTopN(time,val,id,6,4) as topN from t
```

| topN |
| --- |
|  |
|  |
| 1.5 |
| 1.5 |
| 1.8457 |
| 2.1852 |
| 1.1522 |
| 1 |
| 1 |
| 2.1852 |

相关函数：[tmkurtosis](tmkurtosis.md)

