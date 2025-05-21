# tmstdpTopN

## 语法

`tmstdpTopN(T, X, S, window, top, [ascending=true],
[tiesMethod='latest'])`

参数说明和窗口计算规则请参考：[tmTopN](../themes/tmTopN.html)

## 详情

在给定长度（以时间 *T* 衡量）的滑动窗口内，根据 *ascending* 指定的排序方式将 *X*
按照 *S* 进行稳定排序后，计算前 *top* 个元素的总体标准差。

## 返回值

DOUBLE 类型向量。

## 例子

```
T=2023.01.03+1..7
X = [2, 1, 4, 3, 4, 3, 1]
S = [5, 8, 1, , 1, 1, 3]  //S 中包含的空值不参与排序，对应位置的 X 不参与计算
tmstdpTopN(T,X,S,6,4)
// output
[0,0.5,1.2472,1.2472,1.299,0.8291,1.2247]

T=2023.01.03 2023.01.07 2023.01.08 2023.01.10 2023.01.11 2023.01.12
X=8 3 1 2 5 2
S=1 5 2 3 1 1
t=table(T as time, X as val, S as id)
select tmstdpTopN(time,val,id,4,3) as topN from t
```

| topN |
| --- |
| 0 |
| 0 |
| 1 |
| 0.8164 |
| 1.6996 |
| 1.4142 |

相关函数：[tmstdp](tmstdp.html)

