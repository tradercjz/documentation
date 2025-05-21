# anova

## 语法

`anova(X)`

## 参数

**X** 是一个矩阵或所有列均为数值的表。

## 详情

对 *X* 进行单因素方差分析（one-way ANOVA）。*X* 中的每一列都被视为一个单独的组。

返回的结果是一个字典，包含以下 key 值：

* pValue：p 值
* fValue：F 统计量
* ssBetween：组间平方和
* dfBetween：组间自由度
* ssWithin：组内平方和
* dfWithin：组内自由度

## 例子

```
a=300 287 301 400 211 399 412 312 390 412
b=240 259 302 311 210 402 390 298 347 380
c=210 230 213 210 220 208 290 300 201 201
m=matrix(a,b,c)
anova(m);

// output
pValue->0.000515
fValue->10.15459
ssBetween->70528.066667
dfBetween->2
ssWithin->93763.4
dfWithin->27
```

